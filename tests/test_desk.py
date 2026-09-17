from catalog.models import Product
from catalog.registry import load_catalog
from desk.pipeline import build_briefing
from oracle.gateway import OracleGateway


def test_build_briefing_without_oracle():
    briefing = build_briefing("GC", include_oracle=False)
    assert briefing.product.code == "GC"
    assert briefing.oracle is None
    keys = [section["key"] for section in briefing.report]
    assert keys[0] == "background"
    assert keys[2] == "specs"
    assert any("不生成" in note for note in briefing.notes)
    assert "分析模式参考" in briefing.knowledge_disclaimer
    assert all(section["key"] != "cases" for section in briefing.report)


def test_build_briefing_with_fake_oracle():
    catalog = load_catalog()

    def fetchers_for(product: Product):
        return {
            "fear_greed": lambda: {"score": 22, "rating": "Extreme Fear"},
            "cftc": lambda: [{"mm_long": 10, "mm_short": 40, "market_name": "GOLD"}],
        }

    briefing = build_briefing(
        "GC",
        include_oracle=True,
        catalog=catalog,
        gateway=OracleGateway(fetchers_for=fetchers_for),
    )
    assert briefing.oracle is not None
    assert "fear_greed" in briefing.oracle.results
    assert any("Extreme Fear" in note for note in briefing.notes)
    process = next(section for section in briefing.report if section["key"] == "process")
    assert any("Managed Money" in line for line in process["body"])
