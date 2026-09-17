from __future__ import annotations

import json
import re
from typing import Any

from catalog.models import AnalysisMode, Instrument
from catalog.template import REPORT_SECTIONS
from desk.llm import ChatClient
from oracle.models import OracleSnapshot

_SYSTEM = """你是期货分析台的分析员。分析模式参考 AkiraL1/Futures：
用六段结构输出，只依据用户提供的交易数据信号与透镜问题。
铁规则：
1. 只使用用户给出的价格、持仓、曲线、预测市场等交易数据，不要编造数字。
2. 不要填写合约乘数、Tick、保证金、涨跌停、交割规则；规格段只写“待交易所官网核验”。
3. 不要把研报观点或新闻当证据。
4. 没有信号时明确写“证据不足”，不要给交易指令。
5. 只输出 JSON，不要 Markdown。"""


def _oracle_context(oracle: OracleSnapshot | None) -> dict[str, Any]:
    if oracle is None:
        return {"results": {}, "errors": {}}
    return {"results": oracle.results, "errors": oracle.errors}


def _parse_json(text: str) -> dict[str, Any]:
    stripped = text.strip()
    fenced = re.search(r"```(?:json)?\s*(\{.*\})\s*```", stripped, re.S)
    blob = fenced.group(1) if fenced else stripped
    start = blob.find("{")
    end = blob.rfind("}")
    if start < 0 or end <= start:
        raise ValueError("no JSON object")
    data = json.loads(blob[start : end + 1])
    if not isinstance(data, dict):
        raise ValueError("JSON root must be object")
    return data


def _as_lines(value: Any) -> list[str]:
    if isinstance(value, list):
        return [str(item).strip() for item in value if str(item).strip()]
    if isinstance(value, str) and value.strip():
        return [value.strip()]
    return []


def fill_report_with_llm(
    instrument: Instrument,
    mode: AnalysisMode,
    oracle: OracleSnapshot | None,
    client: ChatClient,
) -> list[dict[str, object]]:
    user = {
        "instrument": {
            "code": instrument.code,
            "name": instrument.name,
            "exchange": instrument.exchange,
        },
        "mode": {
            "id": mode.id,
            "label": mode.label,
            "summary": mode.summary,
            "questions": mode.questions,
            "calendars": mode.calendars,
            "lenses": mode.lenses,
        },
        "oracle": _oracle_context(oracle),
        "output_keys": [key for key, _title in REPORT_SECTIONS],
        "output_schema": {
            key: ["该段若干短句，不要编造未给出的数字"]
            for key, _title in REPORT_SECTIONS
        },
    }
    raw = client.complete(
        [
            {"role": "system", "content": _SYSTEM},
            {
                "role": "user",
                "content": json.dumps(user, ensure_ascii=False),
            },
        ]
    )
    parsed = _parse_json(raw)
    report = []
    for key, title in REPORT_SECTIONS:
        body = _as_lines(parsed.get(key))
        if not body:
            body = ["模型未给出该段，保持空缺。"]
        report.append({"key": key, "title": title, "body": body})
    return report
