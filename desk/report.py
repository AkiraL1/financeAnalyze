from catalog.models import AnalysisMode, Instrument
from catalog.template import MODE_SOURCE, REPORT_SECTIONS
from oracle.models import OracleSnapshot


def _price_line(oracle: OracleSnapshot | None) -> str | None:
    if oracle is None:
        return None
    history = oracle.results.get("price")
    if not isinstance(history, dict):
        return None
    bars = history.get("bars")
    if not isinstance(bars, list) or not bars:
        return None
    last = bars[-1]
    if not isinstance(last, dict):
        return None
    close = last.get("close")
    date = last.get("date")
    if close is None:
        return None
    return f"最新价格样本 {close}（{date or '无日期'}，digital-oracle 价格源，非合约规格）。"


def _cot_line(oracle: OracleSnapshot | None) -> str | None:
    if oracle is None:
        return None
    payload = oracle.results.get("cftc")
    if not isinstance(payload, list) or not payload:
        return None
    first = payload[0]
    if not isinstance(first, dict):
        return None
    long_pos = first.get("mm_long")
    short_pos = first.get("mm_short")
    if isinstance(long_pos, int) and isinstance(short_pos, int):
        net = long_pos - short_pos
        side = "净多" if net > 0 else "净空"
        return f"CFTC Managed Money {side} {net} 张（{first.get('market_name', '')}）。"
    return None


def compose_report(
    instrument: Instrument,
    mode: AnalysisMode,
    oracle: OracleSnapshot | None,
) -> list[dict[str, object]]:
    waiting = "尚未拉取 digital-oracle 信号。"
    price = _price_line(oracle)
    cot = _cot_line(oracle)
    sections: dict[str, list[str]] = {key: [] for key, _title in REPORT_SECTIONS}
    sections["background"] = [
        f"{instrument.code} {instrument.name} @ {instrument.exchange}",
        f"分析透镜：{mode.label} — {mode.summary}",
        MODE_SOURCE,
    ]
    if price:
        sections["background"].append(price)
    sections["focus"] = list(mode.questions)
    sections["specs"] = [
        "按 Futures 分析纪律：合约乘数 / Tick / 保证金 / 交割规则必须核验交易所官网。",
        "本台不摘录 Futures 仓库文档，也不凭记忆填写规格数字。",
    ]
    sections["process"] = [
        f"基本面：{cot or waiting}",
        f"技术面：{price or waiting}",
        "政策面：利率路径、预测市场、监管事件用 oracle 对照，不引用研报观点当证据。",
        "跨市场：同一透镜下对照相关合约（如黄金 vs 实际利率，原油 vs 库存）。",
    ]
    if oracle and oracle.errors:
        sections["process"].append("部分信号失败：" + ", ".join(sorted(oracle.errors)))
    if oracle is None:
        sections["conclusion"] = ["信号未拉取，不给出方向性结论。"]
    else:
        sections["conclusion"] = [
            "结论只来自已成功的交易数据信号，启发式见备注；不是投资建议。",
        ]
    sections["risks"] = [
        "规格未核验。",
        *list(mode.calendars),
        "单一信号不足以下结论，至少交叉三个独立维度。",
    ]
    return [
        {"key": key, "title": title, "body": sections[key]}
        for key, title in REPORT_SECTIONS
    ]
