from catalog.registry import load_catalog
from catalog.template import REPORT_SECTIONS


def test_registry_modes_and_instruments():
    catalog = load_catalog()
    ids = {mode.id for mode in catalog.sectors}
    assert {"agricultural", "energy", "metals", "crypto"} <= ids
    gold = catalog.get("GC", sector="metals")
    assert gold is not None
    assert gold.exchange == "COMEX"
    assert catalog.get("USDA") is None
    assert len(REPORT_SECTIONS) == 6
    metals = catalog.sector("metals")
    assert metals is not None
    assert metals.questions
