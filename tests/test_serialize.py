from oracle.serialize import to_jsonable


def test_to_jsonable_dataclass_and_nested():
    from dataclasses import dataclass

    @dataclass
    class Point:
        tenor: str
        value: float
        raw: dict

    payload = to_jsonable({"points": (Point("10Y", 4.1, {"skip": True}),)})
    assert payload["points"][0]["tenor"] == "10Y"
    assert "raw" not in payload["points"][0]
