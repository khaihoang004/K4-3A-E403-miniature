from __future__ import annotations

import json
import logging
import os
import time
import uuid
from typing import Any

from codebase.provider.base import ModelResponse, ToolCall

logger = logging.getLogger(__name__)


def _to_gemini_declarations(tools: list[dict[str, Any]] | None) -> list[dict[str, Any]]:
    declarations: list[dict[str, Any]] = []
    for item in tools or []:
        function = item.get("function", item)
        declarations.append({
            "name": function["name"],
            "description": function.get("description", ""),
            "parameters": function.get("parameters", {"type": "object", "properties": {}}),
        })
    return declarations


def _to_gemini_contents(messages: list[dict[str, str]]) -> tuple[str | None, list[dict[str, Any]]]:
    system_parts: list[str] = []
    contents: list[dict[str, Any]] = []
    
    for msg in messages:
        role = msg.get("role")
        content = msg.get("content", "")
        tool_call_id = msg.get("tool_call_id", "")
        name = msg.get("name", "tool_call")
        
        if role == "system":
            system_parts.append(content)
        elif role == "assistant":
            parts: list[dict[str, Any]] = []
            if content:
                parts.append({"text": content})
            for tool_call in msg.get("tool_calls", []):
                function_call = {
                    "name": tool_call["name"],
                    "args": tool_call.get("args", {}),
                }
                if tool_call.get("thought_signature") is not None:
                    function_call["thought_signature"] = tool_call["thought_signature"]
                parts.append({
                    "functionCall": function_call,
                })
            if parts:
                contents.append({"role": "model", "parts": parts})
        elif role == "user":
            contents.append({"role": "user", "parts": [{"text": content}]})
        elif role == "tool":
            try:
                parsed_content = json.loads(content)
            except json.JSONDecodeError:
                parsed_content = {"result": content}
            
            function_response_payload: dict[str, Any] = {
                "name": name,
                "response": parsed_content
            }
            
            if tool_call_id:
                function_response_payload["id"] = tool_call_id
                
            contents.append({
                "role": "user",
                "parts": [{
                    "functionResponse": function_response_payload
                }]
            })
            
    return ("\n\n".join(system_parts) if system_parts else None), contents


def _part_text(part: Any) -> str | None:
    if hasattr(part, "text"):
        return getattr(part, "text")
    if isinstance(part, dict):
        return part.get("text")
    return None


def _part_function_call(part: Any) -> Any | None:
    if hasattr(part, "function_call"):
        return getattr(part, "function_call")
    if isinstance(part, dict):
        return part.get("function_call")
    return None


def _function_call_name(call: Any) -> str | None:
    if hasattr(call, "name"):
        return getattr(call, "name")
    if isinstance(call, dict):
        return call.get("name")
    return None


def _function_call_args(call: Any) -> dict[str, Any]:
    if hasattr(call, "args"):
        return dict(getattr(call, "args") or {})
    if isinstance(call, dict):
        return dict(call.get("args") or {})
    return {}


def _function_call_id(call: Any) -> str | None:
    """Helper mới để lấy ID thật từ Gemini nếu có."""
    if hasattr(call, "id"):
        return getattr(call, "id")
    if isinstance(call, dict):
        return call.get("id")
    return None


def _part_thought_signature(part: Any) -> Any | None:
    if hasattr(part, "thought_signature"):
        return getattr(part, "thought_signature")
    if isinstance(part, dict):
        return part.get("thought_signature")
    return None


class GeminiProvider:
    """Google Gemini API provider with normalized tool_calls and built-in Fallback/Cooldown."""

    def __init__(
        self,
        *,
        api_key_env: str = "GEMINI_API_KEY",
        default_model: str = "gemini-3.5-flash-lite",
        fallback_models: list[str] | None = None,
        cooldown_seconds: int = 60,
    ) -> None:
        self.api_key_env = api_key_env
        self.default_model = default_model
        
        # Cấu hình Fallback
        self.fallback_models = fallback_models or []
        self.cooldown_seconds = cooldown_seconds
        self._cooldowns: dict[str, float] = {}

    def _is_rate_limit_error(self, exc: Exception) -> bool:
        """Kiểm tra xem exception có phải là lỗi hết quota/rate limit không."""
        error_str = str(exc).lower()
        if "429" in error_str or "quota" in error_str or "exhausted" in error_str:
            return True
        if hasattr(exc, "code") and getattr(exc, "code") == 429:
            return True
        return False

    def complete(
        self,
        messages: list[dict[str, str]],
        tools: list[dict[str, Any]] | None = None,
        *,
        model: str | None = None,
        temperature: float = 0.0,
        tool_choice: Any | None = None,
    ) -> ModelResponse:
        
        try:
            from google import genai
            from google.genai import types
        except ImportError as exc:
            raise RuntimeError("Install live provider dependency first: pip install google-genai") from exc

        api_key = os.getenv(self.api_key_env)
        if not api_key:
            raise RuntimeError(f"Missing API key env var: {self.api_key_env}")

        system_instruction, contents = _to_gemini_contents(messages)
        declarations = _to_gemini_declarations(tools)
        
        config_kwargs: dict[str, Any] = {"temperature": temperature}
        if system_instruction:
            config_kwargs["system_instruction"] = system_instruction
        if declarations:
            config_kwargs["tools"] = [types.Tool(function_declarations=declarations)]
            if tool_choice in {"required", "any"}:
                config_kwargs["tool_config"] = types.ToolConfig(
                    function_calling_config=types.FunctionCallingConfig(mode="ANY")
                )
            elif tool_choice in {"none", "disabled"}:
                config_kwargs["tool_config"] = types.ToolConfig(
                    function_calling_config=types.FunctionCallingConfig(mode="NONE")
                )

        client = genai.Client(api_key=api_key)

        target_model = model or self.default_model
        models_to_try = [target_model]
        for m in self.fallback_models:
            if m not in models_to_try:
                models_to_try.append(m)

        last_exception = None

        for current_model in models_to_try:
            if self._cooldowns.get(current_model, 0) > time.time():
                continue

            try:
                resp = client.models.generate_content(
                    model=current_model,
                    contents=contents,
                    config=types.GenerateContentConfig(**config_kwargs),
                )

                text_parts: list[str] = []
                calls: list[ToolCall] = []

                def append_call(function_call: Any, part: Any = None) -> None:
                    name = _function_call_name(function_call)
                    if name:
                        call_id = _function_call_id(function_call) or f"call_{uuid.uuid4().hex[:8]}"
                        calls.append(ToolCall(
                            id=call_id, 
                            name=name,
                            args=_function_call_args(function_call),
                            thought_signature=_part_thought_signature(part),
                        ))

                for candidate in getattr(resp, "candidates", []) or []:
                    content = getattr(candidate, "content", None)
                    for part in getattr(content, "parts", []) or []:
                        text = _part_text(part)
                        if text:
                            text_parts.append(text)
                        function_call = _part_function_call(part)
                        if function_call:
                            append_call(function_call, part)

                for function_call in getattr(resp, "function_calls", []) or []:
                    append_call(function_call)

                deduped_calls: list[ToolCall] = []
                seen: set[tuple[str, str]] = set()
                for call in calls:
                    key = (call.name, json.dumps(call.args, ensure_ascii=False, sort_keys=True))
                    if key not in seen:
                        seen.add(key)
                        deduped_calls.append(call)

                return ModelResponse(
                    text="\n".join(part for part in text_parts if part) or None, 
                    tool_calls=deduped_calls, 
                    raw=resp,
                    model=current_model
                )

            except Exception as exc:
                if "API_KEY_INVALID" in str(exc) or "API key not valid" in str(exc):
                    raise RuntimeError(
                        "GEMINI_API_KEY không hợp lệ. Hãy cập nhật key Google Gemini hợp lệ trong file .env."
                    ) from exc
                if self._is_rate_limit_error(exc):
                    self._cooldowns[current_model] = time.time() + self.cooldown_seconds
                    logger.warning(
                        f"[Gemini Fallback] Model '{current_model}' Rate Limit/Quota. "
                        f"Cooldown {self.cooldown_seconds}s. Trying next..."
                    )
                    last_exception = exc
                    continue
                else:
                    raise exc

        if last_exception:
            raise RuntimeError(
                f"Tất cả model khả dụng ({', '.join(models_to_try)}) đều báo lỗi hoặc Rate Limit."
            ) from last_exception
            
        raise RuntimeError("Tất cả models đang trong thời gian Cooldown, vui lòng thử lại sau.")