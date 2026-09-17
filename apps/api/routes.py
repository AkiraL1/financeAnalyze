from dataclasses import asdict

from fastapi import APIRouter, HTTPException, Query

from catalog.registry import load_catalog
from desk.formatters import briefing_payload
from desk.llm import llm_status
from desk.pipeline import build_briefing

router = APIRouter()


@router.get("/health")
def health() -> dict:
    return {"ok": True, "service": "financeAnalyze", "llm": llm_status()}


@router.get("/api/sectors")
def sectors() -> dict:
    catalog = load_catalog()
    return {
        "sectors": [
            {
                "id": mode.id,
                "title": mode.title,
                "label": mode.label,
                "summary": mode.summary,
                "product_count": len(mode.products),
                "questions": mode.questions,
            }
            for mode in catalog.sectors
        ]
    }


@router.get("/api/products")
def products(sector: str | None = None) -> dict:
    catalog = load_catalog()
    items = [
        asdict(item)
        for item in catalog.products
        if not sector or item.sector == sector
    ]
    items.sort(key=lambda row: (row["sector"], row["code"]))
    return {"products": items}


@router.get("/api/desk/{code}")
def desk(
    code: str,
    oracle: bool = Query(default=False),
    llm: bool = Query(default=True),
    sector: str | None = Query(default=None),
) -> dict:
    try:
        briefing = build_briefing(
            code,
            include_oracle=oracle,
            include_llm=llm,
            sector=sector,
        )
    except KeyError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc
    return briefing_payload(briefing)
