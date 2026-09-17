from __future__ import annotations

import json
import urllib.error
import urllib.request
from dataclasses import dataclass
from typing import Protocol

from finance_analyze.settings import MiniMaxSettings, minimax_settings


class ChatClient(Protocol):
    def complete(self, messages: list[dict[str, str]]) -> str: ...


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


@dataclass
class MiniMaxClient:
    settings: MiniMaxSettings
    timeout_seconds: int = 120

    def complete(self, messages: list[dict[str, str]]) -> str:
        payload = json.dumps(
            {
                "model": self.settings.model,
                "messages": messages,
                "temperature": 0.2,
                "max_completion_tokens": 4096,
                "thinking": {"type": "disabled"},
            }
        ).encode("utf-8")
        request = urllib.request.Request(
            f"{self.settings.base_url}/chat/completions",
            data=payload,
            headers={
                "Authorization": f"Bearer {self.settings.api_key}",
                "Content-Type": "application/json",
            },
            method="POST",
        )
        try:
            with urllib.request.urlopen(request, timeout=self.timeout_seconds) as response:
                body = json.loads(response.read().decode("utf-8"))
        except urllib.error.HTTPError as exc:
            detail = exc.read().decode("utf-8", errors="replace")[:400]
            raise RuntimeError(f"MiniMax HTTP {exc.code}: {detail}") from exc
        choices = body.get("choices")
        if not isinstance(choices, list) or not choices:
            raise RuntimeError("MiniMax response missing choices")
        message = choices[0].get("message") if isinstance(choices[0], dict) else None
        if not isinstance(message, dict):
            raise RuntimeError("MiniMax response missing message")
        content = _message_text(message)
        if not content.strip():
            raise RuntimeError("MiniMax response missing content")
        return content


def default_client() -> MiniMaxClient | None:
    settings = minimax_settings()
    if settings is None:
        return None
    return MiniMaxClient(settings)


def llm_status() -> dict[str, object]:
    settings = minimax_settings()
    if settings is None:
        return {"configured": False, "provider": "minimax"}
    return {
        "configured": True,
        "provider": "minimax",
        "model": settings.model,
        "base_url": settings.base_url,
    }
