from __future__ import annotations

import json
import urllib.error
import urllib.request
from typing import Any, Protocol

from desk.agent.turn import AgentTurn, ToolCall
from finance_analyze.settings import MiniMaxSettings, minimax_settings


class ChatClient(Protocol):
    def complete(self, messages: list[dict[str, Any]]) -> str: ...


def _message_text(message: dict) -> str:
    content = message.get("content")
    if isinstance(content, str) and content.strip():
        return content
    parts: list[str] = []
    if isinstance(content, list):
        for item in content:
            if isinstance(item, str) and item.strip():
                parts.append(item)
            elif isinstance(item, dict):
                text = item.get("text") or item.get("content")
                if isinstance(text, str) and text.strip():
                    parts.append(text)
    if parts:
        return "\n".join(parts)
    reasoning = message.get("reasoning_content")
    if isinstance(reasoning, str):
        return reasoning
    return ""


def _parse_arguments(raw: object) -> dict[str, Any]:
    if isinstance(raw, dict):
        return raw
    if isinstance(raw, str) and raw.strip():
        try:
            parsed = json.loads(raw)
        except json.JSONDecodeError:
            return {"_raw": raw}
        return parsed if isinstance(parsed, dict) else {"_raw": parsed}
    return {}


def parse_tool_calls(message: dict) -> list[ToolCall]:
    raw = message.get("tool_calls")
    if not isinstance(raw, list):
        return []
    calls: list[ToolCall] = []
    for item in raw:
        if not isinstance(item, dict):
            continue
        fn = item.get("function") if isinstance(item.get("function"), dict) else {}
        name = fn.get("name") or item.get("name")
        if not isinstance(name, str) or not name:
            continue
        calls.append(
            ToolCall(
                id=str(item.get("id") or f"call_{len(calls) + 1}"),
                name=name,
                arguments=_parse_arguments(fn.get("arguments") or item.get("arguments")),
            )
        )
    return calls


class MiniMaxClient:
    def __init__(self, settings: MiniMaxSettings, timeout_seconds: int = 120) -> None:
        self.settings = settings
        self.timeout_seconds = timeout_seconds

    def _post(self, messages: list[dict[str, Any]], tools: list[dict[str, Any]] | None) -> dict:
        payload: dict[str, Any] = {
            "model": self.settings.model,
            "messages": messages,
            "temperature": 0.2,
            "max_completion_tokens": 4096,
            "thinking": {"type": "disabled"},
        }
        if tools:
            payload["tools"] = tools
            payload["tool_choice"] = "auto"
        request = urllib.request.Request(
            f"{self.settings.base_url}/chat/completions",
            data=json.dumps(payload).encode("utf-8"),
            headers={
                "Authorization": f"Bearer {self.settings.api_key}",
                "Content-Type": "application/json",
            },
            method="POST",
        )
        try:
            with urllib.request.urlopen(request, timeout=self.timeout_seconds) as response:
                return json.loads(response.read().decode("utf-8"))
        except urllib.error.HTTPError as exc:
            detail = exc.read().decode("utf-8", errors="replace")[:400]
            raise RuntimeError(f"MiniMax HTTP {exc.code}: {detail}") from exc

    def complete_turn(
        self,
        messages: list[dict[str, Any]],
        tools: list[dict[str, Any]] | None = None,
    ) -> AgentTurn:
        body = self._post(messages, tools)
        choices = body.get("choices")
        if not isinstance(choices, list) or not choices:
            raise RuntimeError("MiniMax response missing choices")
        message = choices[0].get("message") if isinstance(choices[0], dict) else None
        if not isinstance(message, dict):
            raise RuntimeError("MiniMax response missing message")
        return AgentTurn(
            content=_message_text(message),
            tool_calls=parse_tool_calls(message),
            raw_message=message,
        )

    def complete(self, messages: list[dict[str, Any]]) -> str:
        turn = self.complete_turn(messages)
        if not turn.content.strip():
            raise RuntimeError("MiniMax response missing content")
        return turn.content


def default_client() -> MiniMaxClient | None:
    settings = minimax_settings()
    if settings is None:
        return None
    return MiniMaxClient(settings)


def llm_status() -> dict[str, object]:
    settings = minimax_settings()
    if settings is None:
        return {"configured": False, "provider": "minimax", "agent": True}
    return {
        "configured": True,
        "provider": "minimax",
        "model": settings.model,
        "base_url": settings.base_url,
        "agent": True,
    }
