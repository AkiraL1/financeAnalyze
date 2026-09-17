from catalog.models import Catalog
from catalog.registry import load_catalog
from desk.board import build_overview
from desk.formatters import format_briefing
from desk.pipeline import build_briefing


def build_review(catalog: Catalog | None = None, *, include_oracle: bool = False) -> dict:
    loaded = catalog or load_catalog()
    overview = build_overview(loaded)
    briefs = []
    for instrument in loaded.products:
        briefing = build_briefing(
            instrument.code,
            include_oracle=include_oracle,
            include_llm=False,
            sector=instrument.sector,
            catalog=loaded,
        )
        briefs.append(
            {
                "code": briefing.product.code,
                "name": briefing.product.name,
                "sector": briefing.product.sector,
                "sector_label": briefing.sector.label,
                "notes": briefing.notes,
                "markdown": format_briefing(briefing),
            }
        )
    return {
        "generated_at": overview["generated_at"],
        "disclaimer": overview["disclaimer"],
        "kpis": overview["kpis"],
        "attribution": [
            {"label": item["label"], "value": item["product_count"]}
            for item in overview["sectors"]
        ],
        "briefs": briefs,
        "markdown": "\n".join(
            [f"# {overview['generated_at']} 每日简报", "", overview["disclaimer"], ""]
            + [item["markdown"] + "\n" for item in briefs]
        ),
    }
