from dataclasses import dataclass, field

from catalog.models import AnalysisMode, Instrument
from oracle.models import OracleSnapshot


@dataclass
class DeskBriefing:
    product: Instrument
    sector: AnalysisMode
    report: list[dict[str, object]]
    oracle: OracleSnapshot | None
    notes: list[str]
    knowledge_disclaimer: str
    analyst: str = "template"
    trace: list[dict[str, object]] = field(default_factory=list)
