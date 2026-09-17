from catalog.models import Catalog
from oracle.models import OracleSnapshot


def _mode_items(catalog: Catalog) -> list[dict]:
    items: list[dict] = []
    for mode in catalog.sectors:
        for question in mode.questions:
            items.append(
                {
                    "source": f"{mode.label}透镜",
                    "kind": "focus",
                    "title": question,
                    "body": mode.summary,
                    "related": mode.label,
                    "path": "",
                }
            )
        for calendar in mode.calendars:
            items.append(
                {
                    "source": "分析日历",
                    "kind": "calendar",
                    "title": f"{mode.label} · {calendar}",
                    "body": "这是分析模式里的时间窗口，不是从 Futures 仓库摘录的研报。",
                    "related": mode.label,
                    "path": "",
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
                "body": "digital-oracle 交易数据信号，不是观点。",
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
    items = _mode_items(catalog)
    if snapshot is not None:
        items = _oracle_items(snapshot) + items
    return {"live": snapshot is not None, "count": len(items), "items": items}
