from catalog.loader import load_catalog
from catalog.models import Catalog
from desk.models import DeskBriefing
from desk.notes import compose_notes
from oracle.gateway import OracleGateway
from oracle.live import live_gateway


def build_briefing(
    code: str,
    *,
    include_oracle: bool = False,
    sector: str | None = None,
    catalog: Catalog | None = None,
    gateway: OracleGateway | None = None,
) -> DeskBriefing:
    loaded = catalog or load_catalog()
    product = loaded.get(code, sector=sector)
    if product is None:
        raise KeyError(f"unknown futures product: {code}")
    sector = loaded.sector(product.sector)
    if sector is None:
        raise KeyError(f"unknown sector: {product.sector}")
    oracle = None
    if include_oracle:
        oracle = (gateway or live_gateway()).snapshot(product)
    return DeskBriefing(
        product=product,
        sector=sector,
        cases=sector.cases,
        oracle=oracle,
        notes=compose_notes(product, oracle),
        knowledge_disclaimer=(
            "品种清单、季节性与案例摘录来自 AkiraL1/Futures；"
            "市场信号来自 AkiraL1/digital-oracle。"
        ),
    )
