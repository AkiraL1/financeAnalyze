from dataclasses import asdict

from fastapi import APIRouter, HTTPException, Query

from catalog.loader import load_catalog
from desk.formatters import briefing_payload
from desk.pipeline import build_briefing

router = APIRouter()


@router.get("/health")
def health() -> dict:
    return {"ok": True, "service": "financeAnalyze"}


@router.get("/api/sectors")
def sectors() -> dict:
    catalog = load_catalog()
    return {
        "sectors": [
            {
                "id": sector.id,
                "title": sector.title,
                "summary": sector.summary,
                "product_count": len(sector.products),
                "case_count": len(sector.cases),
            }
            for sector in catalog.sectors
        ]
    }


@router.get("/api/products")
def products(sector: str | None = None) -> dict:
    catalog = load_catalog()
    items = []
    for product in catalog.products:
        if sector and product.sector != sector:
            continue
        items.append(asdict(product))
    items.sort(key=lambda row: (row["sector"], row["code"]))
    return {"products": items}


@router.get("/api/desk/{code}")
def desk(
    code: str,
    oracle: bool = Query(default=False),
    sector: str | None = Query(default=None),
) -> dict:
    try:
        briefing = build_briefing(code, include_oracle=oracle, sector=sector)
    except KeyError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc
    return briefing_payload(briefing)
