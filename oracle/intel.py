from finance_analyze.paths import ensure_oracle_on_path
from oracle.gateway import Fetcher, OracleGateway


def build_intel_fetchers(_product: object | None = None) -> dict[str, Fetcher]:
    ensure_oracle_on_path()
    from digital_oracle import (
        FearGreedProvider,
        PolymarketEventQuery,
        PolymarketProvider,
        USTreasuryProvider,
    )

    def _events() -> object:
        return PolymarketProvider().list_events(
            PolymarketEventQuery(limit=8, active=True)
        )[:8]

    return {
        "fear_greed": FearGreedProvider().get_index,
        "treasury": USTreasuryProvider().latest_yield_curve,
        "polymarket": _events,
    }


def intel_gateway() -> OracleGateway:
    return OracleGateway(fetchers_for=build_intel_fetchers)
