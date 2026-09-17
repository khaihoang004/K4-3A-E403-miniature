import json
import logging
import re
from pathlib import Path
from typing import List, Optional

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field

from dotenv import load_dotenv
from codebase.provider.gemini_provider import GeminiProvider

load_dotenv()

app = FastAPI(title="Flashcard Generator API", version="1.0.0")
logger = logging.getLogger(__name__)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

gemini = GeminiProvider(fallback_models=["gemini-3.1-flash-lite"])


class GenerateRequest(BaseModel):
    content: str = Field(..., description="Nội dung bài học, bao gồm thông tin trang/slide.")


class Source(BaseModel):
    page: int = Field(..., ge=1, description="Số trang/slide chứa thông tin nguồn.")
    text: str = Field(..., min_length=1, description="Đoạn văn bản nguồn được sử dụng.")


class Flashcard(BaseModel):
    question: str = Field(..., min_length=1)
    answer: str = Field(..., min_length=1)
    source: Source


class GenerateResponse(BaseModel):
    success: bool
    data: List[Flashcard]
    warning: Optional[str] = None
    message: Optional[str] = None


SYSTEM_PROMPT_PATH = Path(__file__).resolve().parent / "artifact" / "system_prompt.md"


def load_system_prompt() -> str:
    if not SYSTEM_PROMPT_PATH.exists():
        raise RuntimeError(f"System prompt not found: {SYSTEM_PROMPT_PATH}")
    return SYSTEM_PROMPT_PATH.read_text(encoding="utf-8")


SYSTEM_PROMPT = load_system_prompt()


def clean_json_response(raw_text: str) -> str:
    text = raw_text.strip()
    text = re.sub(r"^```(?:json)?\s*", "", text, flags=re.IGNORECASE)
    text = re.sub(r"\s*```$", "", text)
    return text.strip()


def parse_flashcards(raw_text: str) -> list[Flashcard]:
    try:
        data = json.loads(clean_json_response(raw_text))
    except json.JSONDecodeError as exc:
        logger.error("Invalid JSON from Gemini: %s", raw_text[:1000])
        raise HTTPException(status_code=502, detail="AI trả về dữ liệu không đúng định dạng JSON.") from exc

    if not isinstance(data, list):
        raise HTTPException(status_code=502, detail="AI không trả về danh sách flashcard.")

    flashcards = []

    for index, item in enumerate(data):
        if not isinstance(item, dict):
            raise HTTPException(status_code=502, detail=f"Flashcard thứ {index + 1} không phải object hợp lệ.")

        try:
            flashcards.append(Flashcard.model_validate(item))
        except Exception as exc:
            logger.error("Invalid flashcard %s: %s", index + 1, item)
            raise HTTPException(
                status_code=502,
                detail=f"Flashcard thứ {index + 1} không đúng schema.",
            ) from exc

    return flashcards


@app.post("/api/generate_flashcards", response_model=GenerateResponse)
def generate_flashcards(req: GenerateRequest):
    if not req.content.strip():
        return GenerateResponse(
            success=False,
            data=[],
            message="Bài học này chưa có dữ liệu slide để trích xuất thẻ. Vui lòng chọn bài học khác.",
        )

    messages = [
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": f"VĂN BẢN BÀI HỌC:\n\n{req.content}"},
    ]

    try:
        response = gemini.complete(messages=messages, temperature=0.2)
        raw_text = response.text or ""

        if not raw_text.strip():
            raise HTTPException(status_code=502, detail="AI không trả về nội dung.")

        flashcards = parse_flashcards(raw_text)

        if not flashcards:
            return GenerateResponse(
                success=False,
                data=[],
                message="AI không tìm thấy đủ nội dung phù hợp để tạo flashcard.",
            )

        warning_msg = None

        if len(flashcards) < 5:
            warning_msg = f"Bài học ngắn, AI chỉ tạo được {len(flashcards)} flashcard."
        elif len(flashcards) > 10:
            warning_msg = f"AI đã tạo {len(flashcards)} flashcard, vượt số lượng khuyến nghị."

        return GenerateResponse(success=True, data=flashcards, warning=warning_msg)

    except HTTPException:
        raise
    except Exception as exc:
        logger.exception("Unexpected error while generating flashcards")
        raise HTTPException(
            status_code=500,
            detail=f"{type(exc).__name__}: {exc}",
        ) from exc