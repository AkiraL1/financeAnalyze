from catalog.models import Catalog, Instrument
from catalog.registry import load_catalog
from catalog.template import MODE_SOURCE
from desk.analyst import fill_report_with_llm
from desk.llm import ChatClient, default_client
from desk.models import DeskBriefing
from desk.notes import compose_notes
from desk.report import compose_report
from oracle.gateway import OracleGateway
from oracle.live import live_gateway


def build_briefing(
    code: str,
    *,
    include_oracle: bool = False,
    include_llm: bool | None = None,
    sector: str | None = None,
    catalog: Catalog | None = None,
    gateway: OracleGateway | None = None,
    llm_client: ChatClient | None = None,
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
    report = compose_report(instrument, mode, oracle)
    notes = compose_notes(instrument, oracle)
    analyst = "template"
    client = llm_client if llm_client is not None else default_client()
    use_llm = include_llm if include_llm is not None else client is not None
    if use_llm:
        if client is None:
            notes.append("未配置 MINIMAX_API_KEY，回退模板填充。")
        else:
            try:
                report = fill_report_with_llm(instrument, mode, oracle, client)
                analyst = "minimax"
                notes.append("分析正文由 MiniMax 按 Futures 六段模式生成。")
            except Exception as exc:  # noqa: BLE001 - fall back to template
                notes.append(f"MiniMax 调用失败，回退模板：{type(exc).__name__}")
    return DeskBriefing(
        product=instrument,
        sector=mode,
        report=report,
        oracle=oracle,
        notes=notes,
        knowledge_disclaimer=MODE_SOURCE,
        analyst=analyst,
    )
