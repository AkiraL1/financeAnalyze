from catalog.loader import load_catalog
from catalog.models import Catalog
from desk.board import build_overview
from desk.formatters import format_briefing
from desk.pipeline import build_briefing
from desk.watchlist import FOCUS, SECTOR_LABELS


def build_review(catalog: Catalog | None = None, *, include_oracle: bool = False) -> dict:
    loaded = catalog or load_catalog()
    overview = build_overview(loaded)
    briefs = []
    for code, sector_id in FOCUS:
        try:
            briefing = build_briefing(
                code,
                include_oracle=include_oracle,
                sector=sector_id,
                catalog=loaded,
            )
        except KeyError:
            continue
        briefs.append(
            {
                "code": briefing.product.code,
                "name": briefing.product.name,
                "sector": briefing.product.sector,
                "sector_label": SECTOR_LABELS.get(briefing.product.sector, briefing.product.sector),
                "notes": briefing.notes,
                "markdown": format_briefing(briefing),
            }
        )
    attribution = [
        {
            "label": item["label"],
            "value": item["product_count"],
        }
        for item in overview["sectors"]
    ]
    markdown_parts = [
        f"# {overview['generated_at']} 每日简报",
        "",
        overview["disclaimer"],
        "",
    ]
    for item in briefs:
        markdown_parts.append(item["markdown"])
        markdown_parts.append("")
    return {
        "generated_at": overview["generated_at"],
        "disclaimer": overview["disclaimer"],
        "kpis": overview["kpis"],
        "attribution": attribution,
        "briefs": briefs,
        "markdown": "\n".join(markdown_parts),
    }
