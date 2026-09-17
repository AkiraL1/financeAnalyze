from catalog.parse import first_heading, parse_product_tables


def test_parse_product_tables():
    text = """
# metals

| 代码 | 名称 | 交易所 | 备注 |
| --- | --- | --- | --- |
| GC | Gold / 黄金 | COMEX |  |
| SI | Silver / 白银 | COMEX |  |
"""
    products = parse_product_tables(text, "metals")
    assert [item.code for item in products] == ["GC", "SI"]
    assert products[0].exchange == "COMEX"
    assert first_heading(text) == "metals"
