from dataclasses import asdict

from desk.models import DeskBriefing


def format_briefing(briefing: DeskBriefing) -> str:
    product = briefing.product
    lines = [
        f"# {product.code}  {product.name}",
        f"交易所：{product.exchange}    模块：{product.sector}",
        "",
        briefing.knowledge_disclaimer,
        "",
        "## 知识库",
        briefing.sector.summary or briefing.sector.title,
    ]
    if product.note:
        lines.append(f"备注：{product.note}")
    if briefing.sector.bullets:
        lines.append("要点：")
        lines.extend(f"- {item}" for item in briefing.sector.bullets)
    if briefing.cases:
        lines.append("案例：")
        for case in briefing.cases:
            lines.append(f"- {case.title} ({case.relpath})")
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
            "summary": briefing.sector.summary,
            "bullets": briefing.sector.bullets,
        },
        "cases": [asdict(case) for case in briefing.cases],
        "oracle": oracle,
        "notes": briefing.notes,
        "knowledge_disclaimer": briefing.knowledge_disclaimer,
    }
