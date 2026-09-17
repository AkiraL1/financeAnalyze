import json

from catalog.registry import load_catalog
from desk.analyst import fill_report_with_llm
from desk.pipeline import build_briefing


class FakeClient:
    def complete(self, messages: list[dict[str, str]]) -> str:
        assert messages[0]["role"] == "system"
        payload = json.loads(messages[1]["content"])
        assert payload["instrument"]["code"] == "GC"
        return json.dumps(
            {
                "background": ["背景测试"],
                "focus": ["焦点测试"],
                "specs": ["待交易所官网核验"],
                "process": ["过程测试"],
                "conclusion": ["证据不足"],
                "risks": ["待办测试"],
            },
            ensure_ascii=False,
        )


class BoomClient:
    def complete(self, messages: list[dict[str, str]]) -> str:
        raise RuntimeError("boom")


def test_fill_report_with_fake_client():
    catalog = load_catalog()
    instrument = catalog.get("GC")
    mode = catalog.sector(instrument.sector)
    report = fill_report_with_llm(instrument, mode, None, FakeClient())
    by_key = {section["key"]: section["body"] for section in report}
    assert by_key["background"] == ["背景测试"]
    assert by_key["specs"] == ["待交易所官网核验"]


def test_build_briefing_uses_minimax_client():
    briefing = build_briefing(
        "GC",
        include_oracle=False,
        include_llm=True,
        llm_client=FakeClient(),
    )
    assert briefing.analyst == "minimax"
    background = next(section for section in briefing.report if section["key"] == "background")
    assert background["body"] == ["背景测试"]
    assert any("MiniMax" in note for note in briefing.notes)


def test_build_briefing_falls_back_when_llm_fails():
    briefing = build_briefing(
        "GC",
        include_oracle=False,
        include_llm=True,
        llm_client=BoomClient(),
    )
    assert briefing.analyst == "template"
    assert any("回退模板" in note for note in briefing.notes)


def test_build_briefing_missing_key(monkeypatch):
    monkeypatch.setattr("desk.pipeline.default_client", lambda: None)
    briefing = build_briefing("GC", include_oracle=False, include_llm=True)
    assert briefing.analyst == "template"
    assert any("MINIMAX_API_KEY" in note for note in briefing.notes)
