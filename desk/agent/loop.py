from __future__ import annotations

from collections.abc import Callable
from typing import Any, Protocol

from desk.agent.turn import AgentTurn, LoopResult, ToolCall


class ToolClient(Protocol):
    def complete_turn(
        self,
        messages: list[dict[str, Any]],
        tools: list[dict[str, Any]] | None = None,
    ) -> AgentTurn: ...


def supports_tools(client: object) -> bool:
    return hasattr(client, "complete_turn")


def run_loop(
    client: ToolClient,
    messages: list[dict[str, Any]],
    tools: list[dict[str, Any]],
    execute: Callable[[ToolCall], str],
    *,
    max_turns: int = 8,
    should_stop: Callable[[], bool] | None = None,
) -> LoopResult:
    """Model → tools → results until no tool calls, max_turns, or should_stop."""
    names: list[str] = []
    trace: list[dict[str, Any]] = []
    last_text = ""
    for turn_index in range(1, max_turns + 1):
        turn = client.complete_turn(messages, tools=tools)
        last_text = turn.content or last_text
        if not turn.tool_calls:
            trace.append({"turn": turn_index, "tools": [], "final": True})
            return LoopResult(last_text, turn_index, names, trace, done=True)
        messages.append(turn.assistant_message())
        batch: list[str] = []
        for call in turn.tool_calls:
            names.append(call.name)
            result = execute(call)
            batch.append(call.name)
            messages.append(
                {
                    "role": "tool",
                    "tool_call_id": call.id,
                    "content": result[:8000],
                }
            )
            trace.append(
                {
                    "turn": turn_index,
                    "tool": call.name,
                    "args": _short_args(call.arguments),
                    "result": result[:400],
                }
            )
            if should_stop and should_stop():
                return LoopResult(last_text, turn_index, names, trace, done=True)
        last_text = last_text or "called: " + ", ".join(batch)
    return LoopResult(last_text, max_turns, names, trace, done=False)


def _short_args(arguments: dict[str, Any]) -> dict[str, Any]:
    out: dict[str, Any] = {}
    for key, value in arguments.items():
        text = str(value)
        out[key] = text if len(text) <= 120 else text[:117] + "..."
    return out
