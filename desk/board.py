from datetime import datetime, timezone

from catalog.loader import load_catalog
from catalog.models import Catalog, Product
from catalog.oracle_map import resolve_route
from desk.watchlist import FOCUS, SECTOR_LABELS


def _now() -> str:
    return datetime.now(timezone.utc).astimezone().strftime("%Y-%m-%d %H:%M:%S")


def _product_row(product: Product, case_count: int) -> dict:
    route = resolve_route(product.code, product)
    signals = [name for name, flag in (
        ("价格", route.yahoo),
        ("COT", route.cftc),
        ("预测市场", route.polymarket),
        ("加密", route.coingecko),
    ) if flag]
    signals.extend(route.extras)
    return {
        "code": product.code,
        "name": product.name,
        "exchange": product.exchange,
        "sector": product.sector,
        "sector_label": SECTOR_LABELS.get(product.sector, product.sector),
        "note": product.note,
        "signals": signals,
        "yahoo": route.yahoo,
        "cftc": route.cftc,
        "case_count": case_count,
    }


def build_overview(catalog: Catalog | None = None) -> dict:
    loaded = catalog or load_catalog()
    sectors = []
    for sector in loaded.sectors:
        sectors.append(
            {
                "id": sector.id,
                "title": sector.title,
                "label": SECTOR_LABELS.get(sector.id, sector.id),
                "summary": sector.summary,
                "product_count": len(sector.products),
                "case_count": len(sector.cases),
            }
        )
    rows = []
    for code, sector_id in FOCUS:
        product = loaded.get(code, sector=sector_id)
        if product is None:
            continue
        sector = loaded.sector(sector_id)
        rows.append(_product_row(product, len(sector.cases) if sector else 0))
    return {
        "generated_at": _now(),
        "disclaimer": "关注列表是工作台默认观察池，不是持仓；不展示未核验的盈亏。",
        "kpis": [
            {"label": "关注品种", "value": str(len(rows)), "sub": "默认观察池"},
            {"label": "知识模块", "value": str(len(sectors)), "sub": "AkiraL1/Futures"},
            {"label": "已索引品种", "value": str(len(loaded.products)), "sub": "代码/简称表"},
            {"label": "研究案例", "value": str(sum(item["case_count"] for item in sectors)), "sub": "modules/*/cases"},
        ],
        "sectors": sectors,
        "tape": rows,
        "cases": [
            {
                "sector": case.sector,
                "title": case.title,
                "relpath": case.relpath,
                "excerpt": case.excerpt,
            }
            for sector in loaded.sectors
            for case in sector.cases
        ],
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
