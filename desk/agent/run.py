from __future__ import annotations

import json
from dataclasses import dataclass
from typing import Any

from catalog.models import AnalysisMode, Instrument
from catalog.template import PROCESS_LENSES, REPORT_SECTIONS
from desk.agent.loop import ToolClient, run_loop
from desk.agent.schemas import MAIN_TOOLS
from desk.agent.session import AnalysisSession
from desk.agent.turn import LoopResult
from desk.analyst import _as_lines, _parse_json, fill_report_with_llm
from oracle.gateway import OracleGateway
from oracle.models import OracleSnapshot

_SYSTEM = """你是期货分析台的协调员，不是知识库摘录器。
工作方式（必须遵守）：
1. 先 plan_tasks 拆解：拉数、透镜、核验、写六段。
2. 循环调用工具。需要行情用 get_oracle；需要官网原文用 ego_browser。
3. 独立透镜可 run_task 委派子循环，只回收摘要。
4. 证据够用或网页失败时立刻 submit_report，不要把轮次耗在反复打开同一站点。
不要输出 Markdown。
铁规则：
- 只使用工具返回的数字，禁止编造。
- 合约乘数/Tick/保证金/涨跌停：无官网快照就写“待交易所官网核验”。
- 没有信号就写“证据不足”，不要给交易指令。
- 新闻研报不是证据。"""


@dataclass
class AgentReport:
    report: list[dict[str, object]]
    oracle: OracleSnapshot | None
    trace: list[dict[str, Any]]
    tool_names: list[str]
    turns: int


def fill_report_with_agent(
    instrument: Instrument,
    mode: AnalysisMode,
    oracle: OracleSnapshot | None,
    client: ToolClient,
    *,
    gateway: OracleGateway | None = None,
    max_turns: int = 10,
) -> AgentReport:
    session = AnalysisSession(
        instrument=instrument,
        mode=mode,
        client=client,
        oracle=oracle,
        gateway=gateway,
    )
    user = {
        "instrument": {
            "code": instrument.code,
            "name": instrument.name,
            "exchange": instrument.exchange,
        },
        "mode": {
            "id": mode.id,
            "label": mode.label,
            "questions": mode.questions,
            "calendars": mode.calendars,
            "lenses": mode.lenses or list(PROCESS_LENSES),
        },
        "oracle_prefetched": bool(oracle and (oracle.results or oracle.errors)),
        "output_keys": [key for key, _title in REPORT_SECTIONS],
    }
    messages: list[dict[str, Any]] = [
        {"role": "system", "content": _SYSTEM},
        {"role": "user", "content": json.dumps(user, ensure_ascii=False)},
    ]
    loop = run_loop(
        client,
        messages,
        MAIN_TOOLS,
        session.execute,
        max_turns=max_turns,
        should_stop=lambda: session.submitted,
    )
    if not session.submitted:
        loop = _wrap_up(client, messages, session, loop)
    if session.report:
        sections = _to_sections(session.report)
    else:
        parsed = _from_text(loop.content)
        if any(parsed.values()):
            sections = _to_sections(parsed)
        else:
            sections = fill_report_with_llm(
                instrument, mode, session.oracle, _JsonOnly(client)
            )
    return AgentReport(
        report=sections,
        oracle=session.oracle,
        trace=loop.trace,
        tool_names=loop.tool_names,
        turns=loop.turns,
    )


class _JsonOnly:
    def __init__(self, client: object) -> None:
        self._client = client

    def complete(self, messages: list[dict[str, Any]]) -> str:
        return self._client.complete(messages)


def _wrap_up(client, messages, session, loop) -> LoopResult:
    messages.append(
        {
            "role": "user",
            "content": "停止打开网页。根据已有工具结果立即 submit_report；缺数据写证据不足或待交易所官网核验。",
        }
    )
    try:
        extra = run_loop(
            client,
            messages,
            MAIN_TOOLS,
            session.execute,
            max_turns=2,
            should_stop=lambda: session.submitted,
        )
    except Exception:
        return loop
    return LoopResult(
        extra.content or loop.content,
        loop.turns + extra.turns,
        loop.tool_names + extra.tool_names,
        loop.trace + extra.trace,
        extra.done or loop.done,
    )


def _from_text(text: str) -> dict[str, list[str]]:
    try:
        parsed = _parse_json(text)
    except (ValueError, json.JSONDecodeError):
        return {}
    return {key: _as_lines(parsed.get(key)) for key, _title in REPORT_SECTIONS}


def _to_sections(report: dict[str, list[str]]) -> list[dict[str, object]]:
    sections = []
    for key, title in REPORT_SECTIONS:
        body = [line for line in report.get(key, []) if line]
        if not body:
            body = ["模型未给出该段，保持空缺。"]
        sections.append({"key": key, "title": title, "body": body})
    return sections
