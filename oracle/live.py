from catalog.models import Product
from catalog.oracle_map import resolve_route
from finance_analyze.paths import ensure_oracle_on_path
from oracle.gateway import Fetcher, OracleGateway


def build_live_fetchers(product: Product) -> dict[str, Fetcher]:
    ensure_oracle_on_path()
    from digital_oracle import (
        CMEFedWatchProvider,
        CftcCotProvider,
        CftcCotQuery,
        CoinGeckoProvider,
        FearGreedProvider,
        PolymarketEventQuery,
        PolymarketProvider,
        PriceHistoryQuery,
        USTreasuryProvider,
        YahooPriceProvider,
    )

    route = resolve_route(product.code, product)
    fetchers: dict[str, Fetcher] = {}

    if "fear_greed" in route.extras:
        fetchers["fear_greed"] = FearGreedProvider().get_index

    if "treasury" in route.extras:
        fetchers["treasury"] = USTreasuryProvider().latest_yield_curve

    if "fedwatch" in route.extras:
        fetchers["fedwatch"] = CMEFedWatchProvider().get_probabilities

    if route.yahoo:
        symbol = route.yahoo

        def _price(sym: str = symbol) -> object:
            return YahooPriceProvider().get_history(
                PriceHistoryQuery(symbol=sym, interval="d", limit=80)
            )

        fetchers["price"] = _price

    if route.cftc:
        name = route.cftc

        def _cot(commodity: str = name) -> object:
            reports = CftcCotProvider().list_reports(
                CftcCotQuery(commodity_name=commodity, limit=4)
            )
            return reports[:2]

        fetchers["cftc"] = _cot

    if route.polymarket:
        query = route.polymarket

        def _poly(text: str = query) -> object:
            events = PolymarketProvider().list_events(
                PolymarketEventQuery(title_contains=text, limit=5)
            )
            return events[:5]

        fetchers["polymarket"] = _poly

    if route.coingecko:
        coin_id = route.coingecko

        def _coin(cid: str = coin_id) -> object:
            from digital_oracle import CoinGeckoPriceQuery

            return CoinGeckoProvider().get_prices(CoinGeckoPriceQuery(coin_ids=(cid,)))

        fetchers["coingecko"] = _coin

    return fetchers


def live_gateway() -> OracleGateway:
    return OracleGateway(fetchers_for=build_live_fetchers)
