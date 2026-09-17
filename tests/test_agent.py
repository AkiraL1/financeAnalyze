from catalog.models import Product
from catalog.registry import load_catalog
from desk.agent.browser import host_allowed, html_snapshot, snapshot_url
from desk.agent.run import fill_report_with_agent
from desk.agent.turn import AgentTurn, ToolCall
from desk.pipeline import build_briefing
from oracle.gateway import OracleGateway


def test_html_snapshot_extracts_refs():
    markup = "<html><title>GC</title><h1>Gold</h1><p>Official specs</p></html>"
    text = html_snapshot(markup, "https://www.cmegroup.com/gold")
    assert "url=https://www.cmegroup.com/gold" in text
    assert "[ref=1" in text
    assert "Gold" in text


def test_browser_blocks_non_allowlisted_hosts():
    assert host_allowed("https://www.cmegroup.com/markets")
    assert not host_allowed("http://www.cmegroup.com/markets")
    blocked = snapshot_url("https://example.com/")
    assert blocked["engine"] == "blocked"


class ScriptedClient:
    def __init__(self, turns: list[AgentTurn]) -> None:
        self.turns = list(turns)

    def complete_turn(self, messages, tools=None) -> AgentTurn:
        assert tools
        return self.turns.pop(0)

    def complete(self, messages) -> str:
        return "{}"


def _call(name: str, arguments: dict, call_id: str = "c1") -> AgentTurn:
    return AgentTurn(content="", tool_calls=[ToolCall(id=call_id, name=name, arguments=arguments)])


def test_agent_loop_plans_fetches_and_submits():
    catalog = load_catalog()
    instrument = catalog.get("GC")
    mode = catalog.sector(instrument.sector)

    def fetchers_for(product: Product):
        return {"fear_greed": lambda: {"score": 22, "rating": "Extreme Fear"}}

    client = ScriptedClient(
        [
            _call("plan_tasks", {"titles": ["拉信号", "写报告"]}, "1"),
            _call("get_oracle", {}, "2"),
            _call("ego_browser", {"url": "https://example.com/", "intent": "skip"}, "3"),
            _call(
                "submit_report",
                {
                    "background": ["背景来自循环"],
                    "focus": ["焦点来自循环"],
                    "specs": ["待交易所官网核验"],
                    "process": ["Fear & Greed 已读"],
                    "conclusion": ["证据不足"],
                    "risks": ["待办"],
                },
                "4",
            ),
        ]
    )
    result = fill_report_with_agent(
        instrument,
        mode,
        None,
        client,
        gateway=OracleGateway(fetchers_for=fetchers_for),
    )
    by_key = {section["key"]: section["body"] for section in result.report}
    assert by_key["background"] == ["背景来自循环"]
    assert by_key["specs"] == ["待交易所官网核验"]
    assert result.oracle is not None
    assert "fear_greed" in result.oracle.results
    assert result.tool_names == ["plan_tasks", "get_oracle", "ego_browser", "submit_report"]
    assert any(item.get("tool") == "ego_browser" and "白名单" in item.get("result", "") for item in result.trace)


def test_pipeline_uses_agent_when_complete_turn_exists():
    client = ScriptedClient(
        [
            _call(
                "submit_report",
                {
                    "background": ["循环背景"],
                    "focus": ["循环焦点"],
                    "specs": ["待交易所官网核验"],
                    "process": ["循环过程"],
                    "conclusion": ["证据不足"],
                    "risks": ["循环风险"],
                },
            )
        ]
    )
    briefing = build_briefing("GC", include_oracle=False, include_llm=True, llm_client=client)
    assert briefing.analyst == "minimax"
    assert briefing.trace
    assert any("任务循环" in note for note in briefing.notes)
    background = next(section for section in briefing.report if section["key"] == "background")
    assert background["body"] == ["循环背景"]


def test_wrap_up_submits_after_budget():
    catalog = load_catalog()
    instrument = catalog.get("GC")
    mode = catalog.sector(instrument.sector)
    client = ScriptedClient(
        [
            _call("plan_tasks", {"titles": ["写报告"]}, "1"),
            _call(
                "submit_report",
                {
                    "background": ["收尾背景"],
                    "focus": ["收尾焦点"],
                    "specs": ["待交易所官网核验"],
                    "process": ["收尾过程"],
                    "conclusion": ["证据不足"],
                    "risks": ["收尾风险"],
                },
                "2",
            ),
        ]
    )
    result = fill_report_with_agent(instrument, mode, None, client, max_turns=1)
    background = next(section for section in result.report if section["key"] == "background")
    assert background["body"] == ["收尾背景"]
    assert "submit_report" in result.tool_names


def test_health_marks_agent():
    from fastapi.testclient import TestClient

    from apps.api.main import app

    body = TestClient(app).get("/health").json()
    assert body["llm"]["agent"] is True
