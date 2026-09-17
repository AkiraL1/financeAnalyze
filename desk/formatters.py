from dataclasses import asdict

from desk.models import DeskBriefing


def format_briefing(briefing: DeskBriefing) -> str:
    product = briefing.product
    lines = [
        f"# {product.code}  {product.name}",
        f"交易所：{product.exchange}    模式：{briefing.sector.label}    分析员：{briefing.analyst}",
        "",
        briefing.knowledge_disclaimer,
        "",
    ]
    for section in briefing.report:
        lines.append(f"## {section['title']}")
        for line in section["body"]:
            lines.append(f"- {line}")
        lines.append("")
    lines.append("## 备注")
    lines.extend(f"- {note}" for note in briefing.notes)
    if briefing.oracle is not None:
        lines.append("")
        lines.append("## digital-oracle")
        if briefing.oracle.results:
            lines.append("成功：" + ", ".join(sorted(briefing.oracle.results)))
        if briefing.oracle.errors:
            lines.append("失败：" + ", ".join(sorted(briefing.oracle.errors)))
    return "\n".join(lines) + "\n"


def briefing_payload(briefing: DeskBriefing) -> dict:
    oracle = None
    if briefing.oracle is not None:
        oracle = {
            "results": briefing.oracle.results,
            "errors": briefing.oracle.errors,
        }
    return {
        "product": asdict(briefing.product),
        "sector": {
            "id": briefing.sector.id,
            "title": briefing.sector.title,
            "label": briefing.sector.label,
            "summary": briefing.sector.summary,
            "questions": briefing.sector.questions,
            "calendars": briefing.sector.calendars,
        },
        "report": briefing.report,
        "oracle": oracle,
        "notes": briefing.notes,
        "knowledge_disclaimer": briefing.knowledge_disclaimer,
        "analyst": briefing.analyst,
    }
