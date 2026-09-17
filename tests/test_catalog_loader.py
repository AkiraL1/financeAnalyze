from pathlib import Path

from catalog.loader import load_catalog


def test_load_fixture_catalog(tmp_path: Path):
    sector = tmp_path / "modules" / "energy"
    sector.mkdir(parents=True)
    (sector / "README.md").write_text(
        """# energy — 能源

> 覆盖原油

| 代码 | 名称 | 交易所 | 备注 |
| --- | --- | --- | --- |
| CL | WTI Crude Oil / WTI 原油 | NYMEX | 全球基准 |
""",
        encoding="utf-8",
    )
    catalog = load_catalog(tmp_path)
    product = catalog.get("cl")
    assert product is not None
    assert product.name.startswith("WTI")
    assert catalog.sector("energy") is not None


def test_load_vendored_futures_catalog():
    catalog = load_catalog()
    assert catalog.get("GC") is not None
    assert catalog.get("CL") is not None
    ids = {sector.id for sector in catalog.sectors}
    assert {"agricultural", "energy", "metals", "crypto"} <= ids
    energy_rb = catalog.get("RB", sector="energy")
    metals_rb = catalog.get("RB", sector="metals")
    assert energy_rb is not None and metals_rb is not None
    assert energy_rb.name != metals_rb.name
