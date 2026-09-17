import json
import logging
import re
import uuid
from datetime import datetime
from pathlib import Path

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field

from dotenv import load_dotenv
from codebase.provider.gemini_provider import GeminiProvider
from codebase.agent_tools import ToolRegistry, load_tool_schemas

load_dotenv()

app = FastAPI(title="VLearn Flashcard API", version="1.0.0")
logger = logging.getLogger(__name__)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

gemini = GeminiProvider(fallback_models=["gemini-3.1-flash-lite"])

BASE_DIR = Path(__file__).resolve().parent.parent
PROMPT_FILE = BASE_DIR / "codebase" / "artifact" / "system_prompt.md"
TOOLS_FILE = BASE_DIR / "codebase" / "artifact" / "tools.yaml"
DATA_DIR = BASE_DIR / "data"

PUBLISHED_FILE = DATA_DIR / "published_decks.json"
PERSONAL_FILE = DATA_DIR / "personal_decks.json"
LOG_FILE = DATA_DIR / "learning_logs.json"
REPORT_FILE = DATA_DIR / "reports.json"
agent_tools = ToolRegistry(BASE_DIR)


class Source(BaseModel):
    page: int = Field(..., ge=1)
    text: str = Field(..., min_length=1)


class Flashcard(BaseModel):
    id: str | None = None
    question: str = Field(..., min_length=1)
    answer: str = Field(..., min_length=1)
    source: Source


class GenerateRequest(BaseModel):
    content: str
    lesson_id: str = "demo-lesson"
    focus: list[str] = []


class GenerateResponse(BaseModel):
    success: bool
    data: list[Flashcard]
    warning: str | None = None
    message: str | None = None


class AgentRequest(BaseModel):
    query: str = Field(..., min_length=1)
    history: list[dict[str, str]] = []
    confirmed: bool = False


class AgentResponse(BaseModel):
    success: bool
    message: str | None = None
    tool_calls: list[dict] = []
    pending_confirmation: list[dict] = []


class PublishRequest(BaseModel):
    lesson_id: str
    title: str = "Flashcard Deck"
    flashcards: list[Flashcard] = Field(..., min_length=1)


class ReviewRequest(BaseModel):
    student_id: str
    result: str


class ReportRequest(BaseModel):
    student_id: str
    type: str
    description: str = ""


class CloneRequest(BaseModel):
    student_id: str


class PersonalCardUpdate(BaseModel):
    question: str = Field(..., min_length=1)
    answer: str = Field(..., min_length=1)


class PersonalCardCreate(BaseModel):
    student_id: str
    deck_id: str
    question: str = Field(..., min_length=1)
    answer: str = Field(..., min_length=1)

def read_json(path: Path, default):
    if not path.exists():
        return default

    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, OSError):
        return default


def write_json(path: Path, data):
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(data, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )


def load_system_prompt():
    if not PROMPT_FILE.exists():
        raise RuntimeError(f"System prompt not found: {PROMPT_FILE}")

    return PROMPT_FILE.read_text(encoding="utf-8")


def clean_json_response(text: str):
    text = text.strip()
    text = re.sub(r"^```(?:json)?\s*", "", text, flags=re.IGNORECASE)
    text = re.sub(r"\s*```$", "", text)
    return text.strip()


def parse_flashcards(text: str):
    try:
        data = json.loads(clean_json_response(text))
    except json.JSONDecodeError as exc:
        raise HTTPException(
            status_code=502,
            detail="AI trả về dữ liệu không đúng định dạng JSON.",
        ) from exc

    if not isinstance(data, list):
        raise HTTPException(
            status_code=502,
            detail="AI không trả về danh sách flashcard.",
        )

    cards = []

    for index, item in enumerate(data):
        try:
            card = Flashcard.model_validate(item)
            card.id = f"fc-{uuid.uuid4().hex[:8]}"
            cards.append(card)
        except Exception as exc:
            raise HTTPException(
                status_code=502,
                detail=f"Flashcard #{index + 1} không đúng schema.",
            ) from exc

    return cards


@app.get("/api/health")
def health():
    return {"status": "ok"}


@app.get("/api/lesson-content/{lesson_id}")
def get_lesson_content(lesson_id: str):
    lesson_files = {
        "day01": BASE_DIR / "data" / "d1-slide-hackathon.json",
        "day02": BASE_DIR / "data" / "d2-slide-hackathon.json",
    }
    lesson_file = lesson_files.get(lesson_id.lower())
    if not lesson_file:
        raise HTTPException(status_code=404, detail="Không tìm thấy bài học.")

    slides = read_json(lesson_file, [])
    if not slides:
        raise HTTPException(status_code=404, detail="Bài học chưa có nội dung.")

    content_parts = []
    concepts = []
    for slide in slides:
        page = slide.get("page")
        content = str(slide.get("content", "")).strip()
        if page and content:
            content_parts.append(f"[Trang {page}]\n\n{content}")
        concepts.extend(slide.get("concepts", []))

    return {
        "success": True,
        "lesson_id": lesson_id.lower(),
        "title": slides[0].get("title", lesson_id),
        "content": "\n\n".join(content_parts),
        "focus": list(dict.fromkeys(concepts)),
        "slide_count": len(slides),
    }


@app.post("/api/agent", response_model=AgentResponse)
def run_agent(req: AgentRequest):
    try:
        tools = load_tool_schemas(TOOLS_FILE)
        messages = [{"role": "system", "content": load_system_prompt()}]
        messages.extend(req.history)
        messages.append({"role": "user", "content": req.query})
        trace = []
        pending = []

        for _ in range(4):
            response = gemini.complete(messages=messages, tools=tools, temperature=0.1)
            if not response.tool_calls:
                return AgentResponse(
                    success=True,
                    message=response.text or "Đã xử lý yêu cầu.",
                    tool_calls=trace,
                    pending_confirmation=pending,
                )

            tool_results = []
            messages.append({
                "role": "assistant",
                "content": "",
                "tool_calls": [
                    {
                        "name": call.name,
                        "args": call.args,
                        "thought_signature": call.thought_signature,
                    }
                    for call in response.tool_calls
                ],
            })
            for call in response.tool_calls:
                result = agent_tools.execute(call.name, call.args, confirmed=req.confirmed)
                trace.append({"id": call.id, "name": call.name, "args": call.args, "result": result})
                if result.get("pending_confirmation"):
                    pending.append({"name": call.name, "args": call.args})
                tool_results.append({"tool_call_id": call.id, "name": call.name, "result": result})

            if pending:
                return AgentResponse(
                    success=True,
                    message="Cần xác nhận trước khi thực hiện thao tác ghi.",
                    tool_calls=trace,
                    pending_confirmation=pending,
                )

            for tool_result in tool_results:
                messages.append({
                    "role": "tool",
                    "name": tool_result["name"],
                    "tool_call_id": tool_result["tool_call_id"],
                    "content": json.dumps(tool_result["result"], ensure_ascii=False),
                })

        raise HTTPException(status_code=502, detail="Agent vượt quá số vòng gọi tool cho phép.")
    except HTTPException:
        raise
    except Exception as exc:
        logger.exception("Agent execution failed")
        if "GEMINI_API_KEY" in str(exc) or "API key" in str(exc):
            raise HTTPException(status_code=503, detail=str(exc)) from exc
        raise HTTPException(status_code=500, detail=f"{type(exc).__name__}: {exc}") from exc


@app.post("/api/generate_flashcards", response_model=GenerateResponse)
def generate_flashcards(req: GenerateRequest):
    if not req.content.strip():
        return GenerateResponse(
            success=False,
            data=[],
            message="Bài học này chưa có dữ liệu slide để trích xuất thẻ.",
        )

    prompt = load_system_prompt()

    focus_text = (
        "\nTRỌNG TÂM:\n" + "\n".join(f"- {x}" for x in req.focus)
        if req.focus
        else ""
    )

    messages = [
        {"role": "system", "content": prompt},
        {
            "role": "user",
            "content": (
                f"BÀI HỌC: {req.lesson_id}\n"
                f"{focus_text}\n\n"
                f"VĂN BẢN BÀI HỌC:\n{req.content}"
            ),
        },
    ]

    try:
        response = gemini.complete(
            messages=messages,
            temperature=0.2,
        )

        if not response.text:
            raise HTTPException(
                status_code=502,
                detail="AI không trả về nội dung.",
            )

        cards = parse_flashcards(response.text)

        warning = None

        if len(cards) < 5:
            warning = (
                f"Bài học ngắn, AI chỉ tạo được {len(cards)} "
                "flashcard chắc chắn. Hãy tạo thêm thẻ thủ công."
            )
        elif len(cards) > 10:
            warning = (
                f"AI tạo {len(cards)} flashcard, "
                "vượt số lượng khuyến nghị."
            )

        return GenerateResponse(
            success=True,
            data=cards,
            warning=warning,
        )

    except HTTPException:
        raise
    except Exception as exc:
        logger.exception("Generate flashcards failed")
        if "GEMINI_API_KEY" in str(exc) or "API key" in str(exc):
            raise HTTPException(status_code=503, detail=str(exc)) from exc
        raise HTTPException(
            status_code=500,
            detail=f"{type(exc).__name__}: {exc}",
        ) from exc


@app.post("/api/publish_flashcards")
def publish_flashcards(req: PublishRequest):
    cards = []

    for card in req.flashcards:
        card.id = card.id or f"fc-{uuid.uuid4().hex[:8]}"
        cards.append(card.model_dump())

    deck = {
        "deck_id": f"deck-{uuid.uuid4().hex[:8]}",
        "lesson_id": req.lesson_id,
        "title": req.title,
        "status": "published",
        "created_at": datetime.now().isoformat(),
        "flashcards": cards,
    }

    decks = read_json(PUBLISHED_FILE, [])
    decks.append(deck)
    write_json(PUBLISHED_FILE, decks)

    return {
        "success": True,
        "message": f"Đã phát hành {len(cards)} flashcard.",
        "deck": deck,
    }


@app.get("/api/decks")
def get_public_decks():
    decks = read_json(PUBLISHED_FILE, [])
    return {
        "success": True,
        "data": [d for d in decks if d.get("status") == "published"],
    }


@app.get("/api/decks/{deck_id}")
def get_public_deck(deck_id: str):
    decks = read_json(PUBLISHED_FILE, [])

    for deck in decks:
        if deck["deck_id"] == deck_id and deck["status"] == "published":
            return {"success": True, "data": deck}

    raise HTTPException(
        status_code=404,
        detail="Không tìm thấy bộ flashcard.",
    )


@app.post("/api/flashcards/{flashcard_id}/review")
def review_flashcard(flashcard_id: str, req: ReviewRequest):
    if req.result not in {"remembered", "not_remembered"}:
        raise HTTPException(
            status_code=400,
            detail="Result phải là remembered hoặc not_remembered.",
        )

    logs = read_json(LOG_FILE, [])

    logs.append({
        "log_id": f"log-{uuid.uuid4().hex[:8]}",
        "flashcard_id": flashcard_id,
        "student_id": req.student_id,
        "result": req.result,
        "created_at": datetime.now().isoformat(),
    })

    write_json(LOG_FILE, logs)

    return {
        "success": True,
        "message": "Đã lưu kết quả học tập.",
    }


@app.get("/api/students/{student_id}/progress")
def get_progress(student_id: str):
    logs = read_json(LOG_FILE, [])

    student_logs = [
        x for x in logs
        if x.get("student_id") == student_id
    ]

    total = len(student_logs)
    remembered = sum(
        x["result"] == "remembered"
        for x in student_logs
    )
    not_remembered = sum(
        x["result"] == "not_remembered"
        for x in student_logs
    )

    return {
        "student_id": student_id,
        "total_reviews": total,
        "remembered": remembered,
        "not_remembered": not_remembered,
        "remember_rate": (
            round(remembered / total * 100, 2)
            if total else 0
        ),
    }


@app.post("/api/flashcards/{flashcard_id}/report")
def report_flashcard(flashcard_id: str, req: ReportRequest):
    reports = read_json(REPORT_FILE, [])

    report = {
        "report_id": f"report-{uuid.uuid4().hex[:8]}",
        "flashcard_id": flashcard_id,
        "student_id": req.student_id,
        "type": req.type,
        "description": req.description,
        "status": "open",
        "created_at": datetime.now().isoformat(),
    }

    reports.append(report)
    write_json(REPORT_FILE, reports)

    return {
        "success": True,
        "message": "Đã gửi báo cáo lỗi cho giảng viên.",
        "data": report,
    }

@app.get("/api/reports")
def get_reports():
    reports = read_json(REPORT_FILE, [])

    return {
        "success": True,
        "data": reports,
    }


@app.put("/api/reports/{report_id}")
def update_report(report_id: str, status: str):
    allowed = {"open", "in_review", "resolved"}

    if status not in allowed:
        raise HTTPException(
            status_code=400,
            detail="Status không hợp lệ.",
        )

    reports = read_json(REPORT_FILE, [])

    for report in reports:
        if report["report_id"] == report_id:
            report["status"] = status
            report["updated_at"] = datetime.now().isoformat()

            write_json(REPORT_FILE, reports)

            return {
                "success": True,
                "data": report,
            }

    raise HTTPException(
        status_code=404,
        detail="Không tìm thấy report.",
    )

@app.post("/api/decks/{deck_id}/clone")
def clone_deck(deck_id: str, req: CloneRequest):
    decks = read_json(PUBLISHED_FILE, [])

    original = next(
        (
            deck for deck in decks
            if deck["deck_id"] == deck_id
            and deck["status"] == "published"
        ),
        None,
    )

    if not original:
        raise HTTPException(
            status_code=404,
            detail="Không tìm thấy bộ flashcard.",
        )

    personal_deck = {
        "deck_id": f"personal-{uuid.uuid4().hex[:8]}",
        "source_deck_id": deck_id,
        "student_id": req.student_id,
        "title": original["title"] + " - Bản cá nhân",
        "status": "personal",
        "created_at": datetime.now().isoformat(),
        "flashcards": [],
    }

    for card in original["flashcards"]:
        personal_deck["flashcards"].append({
            **card,
            "id": f"personal-fc-{uuid.uuid4().hex[:8]}",
            "source_flashcard_id": card["id"],
        })

    personal_decks = read_json(PERSONAL_FILE, [])
    personal_decks.append(personal_deck)
    write_json(PERSONAL_FILE, personal_decks)

    return {
        "success": True,
        "message": "Đã tạo bản sao cá nhân.",
        "data": personal_deck,
    }


@app.get("/api/students/{student_id}/personal-decks")
def get_personal_decks(student_id: str):
    decks = read_json(PERSONAL_FILE, [])

    return {
        "success": True,
        "data": [
            d for d in decks
            if d.get("student_id") == student_id
        ],
    }


@app.put("/api/personal-flashcards/{flashcard_id}")
def update_personal_flashcard(
    flashcard_id: str,
    req: PersonalCardUpdate,
):
    decks = read_json(PERSONAL_FILE, [])

    for deck in decks:
        for card in deck["flashcards"]:
            if card["id"] == flashcard_id:
                card["question"] = req.question
                card["answer"] = req.answer

                write_json(PERSONAL_FILE, decks)

                return {
                    "success": True,
                    "message": "Đã cập nhật flashcard cá nhân.",
                    "data": card,
                }

    raise HTTPException(
        status_code=404,
        detail="Không tìm thấy flashcard cá nhân.",
    )

@app.post("/api/personal-flashcards")
def create_personal_flashcard(req: PersonalCardCreate):
    decks = read_json(PERSONAL_FILE, [])

    for deck in decks:
        if (
            deck["deck_id"] == req.deck_id
            and deck["student_id"] == req.student_id
        ):
            card = {
                "id": f"personal-fc-{uuid.uuid4().hex[:8]}",
                "question": req.question,
                "answer": req.answer,
                "source": {
                    "page": 1,
                    "text": "Thẻ cá nhân do sinh viên tạo."
                },
                "source_flashcard_id": None,
            }

            deck["flashcards"].append(card)

            write_json(PERSONAL_FILE, decks)

            return {
                "success": True,
                "data": card,
            }

    raise HTTPException(
        status_code=404,
        detail="Không tìm thấy personal deck.",
    )

@app.delete("/api/personal-flashcards/{flashcard_id}")
def delete_personal_flashcard(flashcard_id: str):
    decks = read_json(PERSONAL_FILE, [])

    for deck in decks:
        for index, card in enumerate(deck["flashcards"]):
            if card["id"] == flashcard_id:
                deck["flashcards"].pop(index)

                write_json(PERSONAL_FILE, decks)

                return {
                    "success": True,
                    "message": "Đã xóa flashcard cá nhân.",
                }

    raise HTTPException(
        status_code=404,
        detail="Không tìm thấy flashcard cá nhân.",
    )