from __future__ import annotations

import json
from dataclasses import dataclass, field
from typing import Any

from catalog.models import AnalysisMode, Instrument
from catalog.template import REPORT_SECTIONS
from desk.agent.browser import snapshot_url
from desk.agent.loop import ToolClient, run_loop
from desk.agent.schemas import CHILD_TOOLS
from desk.agent.tasks import TaskBoard
from desk.agent.turn import ToolCall
from oracle.gateway import OracleGateway
from oracle.live import live_gateway
from oracle.models import OracleSnapshot

_CHILD_SYSTEM = """你是子分析员。只处理用户给出的子任务。
可调用 get_oracle / ego_browser。完成后必须 finish_task。
不要编造数字，不要填写未核验合约规格。"""


@dataclass
class AnalysisSession:
    instrument: Instrument
    mode: AnalysisMode
    client: ToolClient
    oracle: OracleSnapshot | None = None
    gateway: OracleGateway | None = None
    board: TaskBoard = field(default_factory=TaskBoard)
    report: dict[str, list[str]] = field(default_factory=dict)
    submitted: bool = False
    child_summary: list[str] = field(default_factory=list)
    depth: int = 0
    max_child_turns: int = 3

    def execute(self, call: ToolCall) -> str:
        handler = {
            "plan_tasks": self._plan,
            "update_task": self._update,
            "list_tasks": self._list,
            "get_oracle": self._oracle,
            "ego_browser": self._browse,
            "run_task": self._child,
            "submit_report": self._submit,
            "finish_task": self._finish,
        }.get(call.name)
        if handler is None:
            return json.dumps({"error": f"unknown tool: {call.name}"}, ensure_ascii=False)
        try:
            return handler(call.arguments)
        except Exception as exc:  # noqa: BLE001 - tool errors go back to the model
            return json.dumps({"error": type(exc).__name__, "detail": str(exc)[:240]}, ensure_ascii=False)

    def _plan(self, arguments: dict[str, Any]) -> str:
        titles = arguments.get("titles") or []
        if not isinstance(titles, list):
            return json.dumps({"error": "titles must be array"}, ensure_ascii=False)
        items = self.board.plan([str(item) for item in titles])
        return json.dumps({"tasks": [{"id": i.id, "title": i.title} for i in items]}, ensure_ascii=False)

    def _update(self, arguments: dict[str, Any]) -> str:
        item = self.board.update(str(arguments.get("id", "")), str(arguments.get("status", "")))
        if item is None:
            return json.dumps({"error": "unknown task or status"}, ensure_ascii=False)
        return json.dumps({"id": item.id, "status": item.status}, ensure_ascii=False)

    def _list(self, arguments: dict[str, Any]) -> str:
        return json.dumps({"tasks": self.board.as_lines()}, ensure_ascii=False)

    def _oracle(self, arguments: dict[str, Any]) -> str:
        if self.oracle is None or (not self.oracle.results and not self.oracle.errors):
            gateway = self.gateway or live_gateway()
            self.oracle = gateway.snapshot(self.instrument)
            self.gateway = gateway
        payload = {
            "results": _compact(self.oracle.results),
            "errors": self.oracle.errors,
        }
        return json.dumps(payload, ensure_ascii=False, default=str)[:6000]

    def _browse(self, arguments: dict[str, Any]) -> str:
        url = str(arguments.get("url", "")).strip()
        intent = str(arguments.get("intent", "")).strip()
        result = snapshot_url(url)
        result["intent"] = intent
        return json.dumps(result, ensure_ascii=False)

    def _child(self, arguments: dict[str, Any]) -> str:
        if self.depth >= 1:
            return json.dumps({"error": "子任务不能再拆子任务"}, ensure_ascii=False)
        title = str(arguments.get("title", "")).strip() or "subtask"
        prompt = str(arguments.get("prompt", "")).strip()
        child = AnalysisSession(
            instrument=self.instrument,
            mode=self.mode,
            client=self.client,
            oracle=self.oracle,
            gateway=self.gateway,
            depth=self.depth + 1,
        )
        messages = [
            {"role": "system", "content": _CHILD_SYSTEM},
            {
                "role": "user",
                "content": json.dumps(
                    {"title": title, "prompt": prompt, "instrument": self.instrument.code},
                    ensure_ascii=False,
                ),
            },
        ]
        run_loop(
            self.client,
            messages,
            CHILD_TOOLS,
            child.execute,
            max_turns=self.max_child_turns,
            should_stop=lambda: child.submitted,
        )
        self.oracle = child.oracle or self.oracle
        summary = child.child_summary or [messages[-1].get("content", "子任务无摘要")[:400]]
        return json.dumps({"title": title, "summary": summary}, ensure_ascii=False)

    def _submit(self, arguments: dict[str, Any]) -> str:
        for key, _title in REPORT_SECTIONS:
            value = arguments.get(key)
            lines = [str(item).strip() for item in value] if isinstance(value, list) else []
            self.report[key] = [item for item in lines if item]
        self.submitted = True
        return json.dumps({"ok": True, "sections": list(self.report)}, ensure_ascii=False)

    def _finish(self, arguments: dict[str, Any]) -> str:
        value = arguments.get("summary")
        lines = [str(item).strip() for item in value] if isinstance(value, list) else []
        self.child_summary = [item for item in lines if item]
        self.submitted = True
        return json.dumps({"ok": True}, ensure_ascii=False)


def _compact(results: dict[str, object]) -> dict[str, object]:
    packed: dict[str, object] = {}
    for key, value in results.items():
        if key == "price" and isinstance(value, dict):
            bars = value.get("bars")
            if isinstance(bars, list) and len(bars) > 8:
                packed[key] = {**value, "bars": bars[-8:]}
                continue
        packed[key] = value
    return packed
