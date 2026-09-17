from catalog.models import Catalog
from desk.watchlist import SECTOR_LABELS
from oracle.models import OracleSnapshot


def _case_items(catalog: Catalog) -> list[dict]:
    items: list[dict] = []
    for sector in catalog.sectors:
        label = SECTOR_LABELS.get(sector.id, sector.id)
        for case in sector.cases:
            items.append(
                {
                    "source": "Futures cases",
                    "kind": "research",
                    "title": case.title,
                    "body": case.excerpt,
                    "related": label,
                    "path": case.relpath,
                }
            )
        for bullet in sector.bullets[:4]:
            items.append(
                {
                    "source": "模块日历",
                    "kind": "calendar",
                    "title": f"{label} · 季节性 / 报告窗口",
                    "body": bullet,
                    "related": label,
                    "path": f"modules/{sector.id}/README.md",
                }
            )
    return items


def _oracle_items(snapshot: OracleSnapshot) -> list[dict]:
    items: list[dict] = []
    fear = snapshot.results.get("fear_greed")
    if isinstance(fear, dict):
        items.append(
            {
                "source": "CNN Fear & Greed",
                "kind": "oracle",
                "title": f"情绪 {fear.get('rating', '')}  ·  {fear.get('score', '')}",
                "body": "数字来自 digital-oracle FearGreedProvider，不是交易指令。",
                "related": "宏观",
                "path": "",
            }
        )
    events = snapshot.results.get("polymarket")
    if isinstance(events, list):
        for event in events[:8]:
            if not isinstance(event, dict):
                continue
            title = event.get("title") or event.get("slug") or "Polymarket"
            items.append(
                {
                    "source": "Polymarket",
                    "kind": "oracle",
                    "title": str(title),
                    "body": str(event.get("description") or event.get("slug") or ""),
                    "related": "预测市场",
                    "path": "",
                }
            )
    for key, message in snapshot.errors.items():
        items.append(
            {
                "source": "oracle error",
                "kind": "error",
                "title": f"{key} 拉取失败",
                "body": message,
                "related": "信号",
                "path": "",
            }
        )
    return items


def build_intel(catalog: Catalog, snapshot: OracleSnapshot | None = None) -> dict:
    items = _case_items(catalog)
    if snapshot is not None:
        items = _oracle_items(snapshot) + items
    return {
        "live": snapshot is not None,
        "count": len(items),
        "items": items,
    }
