from __future__ import annotations

from typing import Any


def _fn(name: str, description: str, properties: dict[str, Any], required: list[str]) -> dict[str, Any]:
    return {
        "type": "function",
        "function": {
            "name": name,
            "description": description,
            "parameters": {
                "type": "object",
                "properties": properties,
                "required": required,
            },
        },
    }


MAIN_TOOLS = [
    _fn(
        "plan_tasks",
        "把本次分析拆成可执行任务清单，覆盖数据拉取、透镜与六段报告。",
        {"titles": {"type": "array", "items": {"type": "string"}}},
        ["titles"],
    ),
    _fn(
        "update_task",
        "更新任务状态：pending / in_progress / done / blocked。",
        {
            "id": {"type": "string"},
            "status": {"type": "string"},
        },
        ["id", "status"],
    ),
    _fn("list_tasks", "查看当前任务板。", {}, []),
    _fn(
        "get_oracle",
        "拉取 digital-oracle 交易数据（价格/COT/曲线等），不要编造数字。",
        {},
        [],
    ),
    _fn(
        "ego_browser",
        "打开白名单交易所/监管页面并返回语义快照（优先 ego-browser，否则 HTTP 快照）。",
        {
            "url": {"type": "string"},
            "intent": {"type": "string"},
        },
        ["url"],
    ),
    _fn(
        "run_task",
        "把一个独立子任务交给子分析员循环执行，只返回结论摘要。",
        {
            "title": {"type": "string"},
            "prompt": {"type": "string"},
        },
        ["title", "prompt"],
    ),
    _fn(
        "submit_report",
        "提交六段报告并结束循环。每段为字符串数组。specs 无官网证据时写待核验。",
        {
            "background": {"type": "array", "items": {"type": "string"}},
            "focus": {"type": "array", "items": {"type": "string"}},
            "specs": {"type": "array", "items": {"type": "string"}},
            "process": {"type": "array", "items": {"type": "string"}},
            "conclusion": {"type": "array", "items": {"type": "string"}},
            "risks": {"type": "array", "items": {"type": "string"}},
        },
        ["background", "focus", "specs", "process", "conclusion", "risks"],
    ),
]

CHILD_TOOLS = [
    _fn("get_oracle", "拉取 digital-oracle 交易数据。", {}, []),
    _fn(
        "ego_browser",
        "打开白名单页面并返回语义快照。",
        {"url": {"type": "string"}, "intent": {"type": "string"}},
        ["url"],
    ),
    _fn(
        "finish_task",
        "提交子任务结论摘要，结束子循环。",
        {"summary": {"type": "array", "items": {"type": "string"}}},
        ["summary"],
    ),
]
