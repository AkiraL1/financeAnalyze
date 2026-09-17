from datetime import datetime, timezone

from catalog.models import Catalog, Instrument
from catalog.oracle_map import resolve_route
from catalog.registry import load_catalog
from catalog.template import REPORT_SECTIONS


def _now() -> str:
    return datetime.now(timezone.utc).astimezone().strftime("%Y-%m-%d %H:%M:%S")


def _row(instrument: Instrument, label: str) -> dict:
    route = resolve_route(instrument.code, instrument)
    signals = [name for name, flag in (
        ("价格", route.yahoo),
        ("COT", route.cftc),
        ("预测市场", route.polymarket),
        ("加密", route.coingecko),
    ) if flag]
    signals.extend(route.extras)
    return {
        "code": instrument.code,
        "name": instrument.name,
        "exchange": instrument.exchange,
        "sector": instrument.sector,
        "sector_label": label,
        "note": instrument.note,
        "signals": signals,
        "yahoo": route.yahoo,
        "cftc": route.cftc,
    }


def build_overview(catalog: Catalog | None = None) -> dict:
    loaded = catalog or load_catalog()
    labels = {mode.id: mode.label for mode in loaded.sectors}
    sectors = [
        {
            "id": mode.id,
            "title": mode.title,
            "label": mode.label,
            "summary": mode.summary,
            "questions": mode.questions,
            "calendars": mode.calendars,
            "product_count": len(mode.products),
        }
        for mode in loaded.sectors
    ]
    rows = [_row(item, labels.get(item.sector, item.sector)) for item in loaded.products]
    return {
        "generated_at": _now(),
        "disclaimer": "观察池用于套用分析模式，不是持仓；规格不在本台填写。",
        "kpis": [
            {"label": "观察品种", "value": str(len(rows)), "sub": "工作台维护"},
            {"label": "分析模式", "value": str(len(sectors)), "sub": "Futures 透镜"},
            {"label": "报告章节", "value": str(len(REPORT_SECTIONS)), "sub": "固定结构"},
            {"label": "信号源", "value": "oracle", "sub": "digital-oracle"},
        ],
        "sectors": sectors,
        "tape": rows,
        "template": [{"key": key, "title": title} for key, title in REPORT_SECTIONS],
    }


def build_board(catalog: Catalog | None = None) -> dict:
    overview = build_overview(catalog)
    return {
        "generated_at": overview["generated_at"],
        "disclaimer": overview["disclaimer"],
        "kpis": overview["kpis"],
        "rows": overview["tape"],
        "sectors": overview["sectors"],
    }
