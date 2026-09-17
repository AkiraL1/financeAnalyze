from dataclasses import dataclass

from catalog.models import CaseDoc, Product, SectorInfo
from oracle.models import OracleSnapshot


@dataclass
class DeskBriefing:
    product: Product
    sector: SectorInfo
    cases: list[CaseDoc]
    oracle: OracleSnapshot | None
    notes: list[str]
    knowledge_disclaimer: str
