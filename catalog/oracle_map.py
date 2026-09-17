from dataclasses import dataclass

from catalog.models import Product


@dataclass(frozen=True)
class OracleRoute:
    yahoo: str | None = None
    cftc: str | None = None
    polymarket: str | None = None
    coingecko: str | None = None
    extras: tuple[str, ...] = ()


_ROUTES: dict[str, OracleRoute] = {
    "GC": OracleRoute("GC=F", "GOLD", "gold", extras=("fear_greed", "treasury")),
    "SI": OracleRoute("SI=F", "SILVER", "silver", extras=("fear_greed",)),
    "HG": OracleRoute("HG=F", "COPPER", "copper", extras=("fear_greed",)),
    "CL": OracleRoute("CL=F", "CRUDE OIL", "oil", extras=("fear_greed",)),
    "BRN": OracleRoute("BZ=F", "CRUDE OIL", "oil", extras=("fear_greed",)),
    "NG": OracleRoute("NG=F", "NATURAL GAS", extras=("fear_greed",)),
    "ZC": OracleRoute("ZC=F", "CORN", "corn"),
    "ZS": OracleRoute("ZS=F", "SOYBEANS", "soy"),
    "ZW": OracleRoute("ZW=F", "WHEAT", "wheat"),
    "CT": OracleRoute(None, "COTTON", "cotton"),
    "SB": OracleRoute(None, "SUGAR", "sugar"),
    "KC": OracleRoute(None, "COFFEE", "coffee"),
    "CC": OracleRoute(None, "COCOA", "cocoa"),
    "ES": OracleRoute("ES=F", "S&P 500", "recession", extras=("fear_greed", "treasury")),
    "NQ": OracleRoute("NQ=F", None, "nasdaq", extras=("fear_greed",)),
    "ZN": OracleRoute("ZN=F", None, "fed", extras=("treasury", "fedwatch")),
    "ZB": OracleRoute("ZB=F", None, extras=("treasury",)),
    "DX": OracleRoute("DX-Y.NYB", None, extras=("treasury", "fear_greed")),
    "6E": OracleRoute("EURUSD=X", None, extras=("treasury",)),
    "6J": OracleRoute("USDJPY=X", None, extras=("treasury",)),
    "BTC": OracleRoute("BTC-USD", None, "bitcoin", "bitcoin", extras=("fear_greed",)),
    "ETH": OracleRoute("ETH-USD", None, "ethereum", "ethereum", extras=("fear_greed",)),
}

_ALIASES: dict[str, str] = {
    "AU": "GC",
    "AG": "SI",
    "CU": "HG",
    "SC": "CL",
    "FU": "CL",
    "IF": "ES",
    "IH": "ES",
    "T": "ZN",
    "TF": "ZN",
    "MBT": "BTC",
    "MET": "ETH",
}


def canonical_code(code: str) -> str:
    key = code.strip().upper()
    return _ALIASES.get(key, key)


def resolve_route(code: str, product: Product | None = None) -> OracleRoute:
    key = canonical_code(code)
    if key in _ROUTES:
        return _ROUTES[key]
    extras: tuple[str, ...] = ("fear_greed",)
    sector = product.sector if product else ""
    if sector in {"interest-rate", "fx", "equity-index"}:
        extras = ("fear_greed", "treasury")
    return OracleRoute(extras=extras, polymarket=product.name if product else key)
