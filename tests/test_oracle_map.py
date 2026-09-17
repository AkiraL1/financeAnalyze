from catalog.models import Product
from catalog.oracle_map import resolve_route


def test_resolve_gold_and_alias():
    gold = resolve_route("GC")
    assert gold.yahoo == "GC=F"
    assert gold.cftc == "GOLD"
    assert resolve_route("AU").yahoo == "GC=F"


def test_resolve_unknown_uses_sector_extras():
    product = Product("RB", "螺纹钢", "SHFE", "metals")
    route = resolve_route("RB", product)
    assert "fear_greed" in route.extras
