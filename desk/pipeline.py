from catalog.models import Catalog, Instrument
from catalog.registry import load_catalog
from catalog.template import MODE_SOURCE
from desk.models import DeskBriefing
from desk.notes import compose_notes
from desk.report import compose_report
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
    instrument = loaded.get(code, sector=sector)
    if instrument is None:
        raise KeyError(f"unknown instrument: {code}")
    mode = loaded.sector(instrument.sector)
    if mode is None:
        raise KeyError(f"unknown analysis mode: {instrument.sector}")
    oracle = None
    if include_oracle:
        oracle = (gateway or live_gateway()).snapshot(instrument)
    return DeskBriefing(
        product=instrument,
        sector=mode,
        report=compose_report(instrument, mode, oracle),
        oracle=oracle,
        notes=compose_notes(instrument, oracle),
        knowledge_disclaimer=MODE_SOURCE,
    )
