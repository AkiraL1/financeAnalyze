from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


@dataclass(frozen=True)
class ToolCall:
    id: str
    name: str
    arguments: dict[str, Any]

    def openai(self) -> dict[str, Any]:
        import json

        return {
            "id": self.id,
            "type": "function",
            "function": {
                "name": self.name,
                "arguments": json.dumps(self.arguments, ensure_ascii=False),
            },
        }


@dataclass
class AgentTurn:
    content: str
    tool_calls: list[ToolCall] = field(default_factory=list)
    raw_message: dict[str, Any] = field(default_factory=dict)

    def assistant_message(self) -> dict[str, Any]:
        message: dict[str, Any] = {
            "role": "assistant",
            "content": self.content or None,
        }
        if self.tool_calls:
            message["tool_calls"] = [call.openai() for call in self.tool_calls]
        return message


@dataclass
class LoopResult:
    content: str
    turns: int
    tool_names: list[str]
    trace: list[dict[str, Any]]
    done: bool = False
