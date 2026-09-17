from __future__ import annotations

import json
import uuid
from datetime import datetime
from pathlib import Path
from typing import Any, Callable

from pydantic import BaseModel, Field, ValidationError


class Source(BaseModel):
    page: int = Field(..., ge=1)
    text: str = Field(..., min_length=1)


class Flashcard(BaseModel):
    question: str = Field(..., min_length=1)
    answer: str = Field(..., min_length=1)
    source: Source


def read_json(path: Path, default: Any) -> Any:
    if not path.exists():
        return default
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, OSError):
        return default


def write_json(path: Path, data: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")


WRITE_TOOLS = {
    "create_lesson",
    "update_lesson",
    "delete_lesson",
    "create_flashcard",
    "update_flashcard",
    "delete_flashcard",
    "publish_flashcard_deck",
}


class ToolError(Exception):
    def __init__(self, code: str, message: str):
        self.code = code
        self.message = message
        super().__init__(message)


class ToolRegistry:
    def __init__(self, base_dir: Path):
        self.base_dir = base_dir
        self.data_dir = base_dir / "data"
        self.lessons_file = self.data_dir / "lessons.json"
        self.drafts_file = self.data_dir / "flashcard_drafts.json"
        self.published_file = self.data_dir / "published_decks.json"
        self.handlers: dict[str, Callable[[dict[str, Any]], dict[str, Any]]] = {
            "list_lessons": self.list_lessons,
            "get_lesson": self.get_lesson,
            "create_lesson": self.create_lesson,
            "update_lesson": self.update_lesson,
            "delete_lesson": self.delete_lesson,
            "list_flashcards": self.list_flashcards,
            "create_flashcard": self.create_flashcard,
            "update_flashcard": self.update_flashcard,
            "delete_flashcard": self.delete_flashcard,
            "publish_flashcard_deck": self.publish_flashcard_deck,
        }

    def execute(self, name: str, args: dict[str, Any], confirmed: bool = False) -> dict[str, Any]:
        if name not in self.handlers:
            return {"success": False, "error": {"code": "unknown_tool", "message": name}}
        if name in WRITE_TOOLS and not confirmed:
            return {
                "success": False,
                "pending_confirmation": True,
                "tool": name,
                "args": args,
                "message": "Xác nhận thao tác ghi trước khi thực hiện.",
            }
        try:
            return self.handlers[name](args)
        except ToolError as exc:
            return {"success": False, "error": {"code": exc.code, "message": exc.message}}
        except (ValidationError, TypeError, ValueError) as exc:
            return {"success": False, "error": {"code": "invalid_input", "message": str(exc)}}

    def list_lessons(self, args: dict[str, Any]) -> dict[str, Any]:
        lessons = self._load_lessons()
        query = str(args.get("query", "")).strip().lower()
        if query:
            lessons = [x for x in lessons if query in f"{x.get('lesson_id', '')} {x.get('title', '')}".lower()]
        return {"success": True, "data": lessons}

    def get_lesson(self, args: dict[str, Any]) -> dict[str, Any]:
        lesson = self._find_lesson(args.get("lesson_id"))
        return {"success": True, "data": lesson}

    def create_lesson(self, args: dict[str, Any]) -> dict[str, Any]:
        lesson_id = str(args.get("lesson_id", "")).strip()
        title = str(args.get("title", "")).strip()
        content = args.get("content")
        if not lesson_id or not title or not isinstance(content, list) or not content:
            raise ToolError("invalid_input", "lesson_id, title và content không được trống.")
        lessons = self._load_lessons()
        if any(x.get("lesson_id") == lesson_id for x in lessons):
            raise ToolError("already_exists", "Lesson ID đã tồn tại.")
        pages = self._validate_content(content)
        lesson = {"lesson_id": lesson_id, "title": title, "content": pages, "created_at": datetime.now().isoformat()}
        lessons.append(lesson)
        write_json(self.lessons_file, lessons)
        return {"success": True, "data": lesson}

    def update_lesson(self, args: dict[str, Any]) -> dict[str, Any]:
        lesson = self._find_lesson(args.get("lesson_id"))
        if "title" in args:
            lesson["title"] = str(args["title"]).strip()
        if "content" in args:
            lesson["content"] = self._validate_content(args["content"])
        if not lesson.get("title"):
            raise ToolError("invalid_input", "title không được trống.")
        lesson["updated_at"] = datetime.now().isoformat()
        lessons = read_json(self.lessons_file, [])
        write_json(self.lessons_file, [lesson if x.get("lesson_id") == lesson["lesson_id"] else x for x in lessons])
        return {"success": True, "data": lesson}

    def delete_lesson(self, args: dict[str, Any]) -> dict[str, Any]:
        lesson = self._find_lesson(args.get("lesson_id"))
        lessons = read_json(self.lessons_file, [])
        write_json(self.lessons_file, [x for x in lessons if x.get("lesson_id") != lesson["lesson_id"]])
        return {"success": True, "deleted_id": lesson["lesson_id"]}

    def list_flashcards(self, args: dict[str, Any]) -> dict[str, Any]:
        cards = read_json(self.drafts_file, [])
        lesson_id = args.get("lesson_id")
        if lesson_id:
            cards = [x for x in cards if x.get("lesson_id") == lesson_id]
        return {"success": True, "data": cards}

    def create_flashcard(self, args: dict[str, Any]) -> dict[str, Any]:
        lesson = self._find_lesson(args.get("lesson_id"))
        card = self._validate_card(args)
        self._validate_grounding(lesson, card)
        card_record = {"flashcard_id": f"fc-{uuid.uuid4().hex[:8]}", "lesson_id": lesson["lesson_id"], **card}
        cards = read_json(self.drafts_file, [])
        cards.append(card_record)
        write_json(self.drafts_file, cards)
        return {"success": True, "data": card_record}

    def update_flashcard(self, args: dict[str, Any]) -> dict[str, Any]:
        cards = read_json(self.drafts_file, [])
        card = next((x for x in cards if x.get("flashcard_id") == args.get("flashcard_id")), None)
        if not card:
            raise ToolError("not_found", "Không tìm thấy flashcard nháp.")
        for field in ("question", "answer", "source"):
            if field in args:
                card[field] = args[field]
        card.update(self._validate_card(card))
        self._validate_grounding(self._find_lesson(card["lesson_id"]), card)
        write_json(self.drafts_file, cards)
        return {"success": True, "data": card}

    def delete_flashcard(self, args: dict[str, Any]) -> dict[str, Any]:
        cards = read_json(self.drafts_file, [])
        if not any(x.get("flashcard_id") == args.get("flashcard_id") for x in cards):
            raise ToolError("not_found", "Không tìm thấy flashcard nháp.")
        write_json(self.drafts_file, [x for x in cards if x.get("flashcard_id") != args.get("flashcard_id")])
        return {"success": True, "deleted_id": args["flashcard_id"]}

    def publish_flashcard_deck(self, args: dict[str, Any]) -> dict[str, Any]:
        lesson = self._find_lesson(args.get("lesson_id"))
        drafts = [x for x in read_json(self.drafts_file, []) if x.get("lesson_id") == lesson["lesson_id"]]
        if not drafts:
            raise ToolError("invalid_state", "Lesson chưa có flashcard nháp để phát hành.")
        deck = {
            "deck_id": f"deck-{uuid.uuid4().hex[:8]}",
            "lesson_id": lesson["lesson_id"],
            "title": str(args.get("title") or lesson["title"]),
            "status": "published",
            "created_at": datetime.now().isoformat(),
            "flashcards": [self._public_card(x) for x in drafts],
        }
        decks = read_json(self.published_file, [])
        decks.append(deck)
        write_json(self.published_file, decks)
        return {"success": True, "data": deck}

    def _find_lesson(self, lesson_id: Any) -> dict[str, Any]:
        lessons = self._load_lessons()
        lesson = next((x for x in lessons if x.get("lesson_id") == lesson_id), None)
        if not lesson:
            raise ToolError("not_found", "Không tìm thấy lesson.")
        return lesson

    def _load_lessons(self) -> list[dict[str, Any]]:
        lessons = read_json(self.lessons_file, [])
        if lessons:
            return lessons

        slide_files = {
            "day01": self.base_dir / "data" / "d1-slide-hackathon.json",
            "day02": self.base_dir / "data" / "d2-slide-hackathon.json",
        }
        catalog = []
        for lesson_id, path in slide_files.items():
            slides = read_json(path, [])
            if not slides:
                continue
            catalog.append({
                "lesson_id": lesson_id,
                "title": slides[0].get("title", lesson_id),
                "content": [
                    {"page": slide["page"], "text": slide["content"]}
                    for slide in slides
                    if slide.get("page") and str(slide.get("content", "")).strip()
                ],
                "source": "slide_pack",
            })
        return catalog

    @staticmethod
    def _validate_content(content: Any) -> list[dict[str, Any]]:
        if not isinstance(content, list) or not content:
            raise ToolError("invalid_input", "content phải là danh sách trang.")
        pages = []
        for page in content:
            if not isinstance(page, dict) or not isinstance(page.get("page"), int) or page["page"] < 1 or not str(page.get("text", "")).strip():
                raise ToolError("invalid_input", "Mỗi content item cần page >= 1 và text.")
            pages.append({"page": page["page"], "text": page["text"]})
        return pages

    @staticmethod
    def _validate_card(card: dict[str, Any]) -> dict[str, Any]:
        try:
            validated = Flashcard(question=card["question"], answer=card["answer"], source=Source(**card["source"]))
        except (KeyError, ValidationError, TypeError) as exc:
            raise ToolError("invalid_input", f"Flashcard không hợp lệ: {exc}") from exc
        return validated.model_dump(exclude={"id"})

    @staticmethod
    def _validate_grounding(lesson: dict[str, Any], card: dict[str, Any]) -> None:
        source = card["source"]
        page = next((item for item in lesson["content"] if item["page"] == source["page"]), None)
        if not page or source["text"].strip() not in page["text"]:
            raise ToolError("ungrounded_source", "Source phải trích nguyên văn từ đúng trang của lesson.")

    @staticmethod
    def _public_card(card: dict[str, Any]) -> dict[str, Any]:
        return {"id": card["flashcard_id"], "question": card["question"], "answer": card["answer"], "source": card["source"]}


def load_tool_schemas(path: Path) -> list[dict[str, Any]]:
    return json.loads(path.read_text(encoding="utf-8"))
