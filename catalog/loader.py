from pathlib import Path

from catalog.models import CaseDoc, Catalog, Product, SectorInfo
from catalog.parse import (
    bullets_under_headings,
    first_blockquote,
    first_heading,
    parse_product_tables,
)
from finance_analyze.paths import FUTURES_ROOT

_HEADING_KEYS = ("季节性", "报告日历", "关键报告", "套利", "跨市")


def _read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def _excerpt(text: str, lines: int = 24) -> str:
    body = [line.rstrip() for line in text.splitlines() if line.strip()]
    return "\n".join(body[:lines])


def _load_cases(modules_root: Path, sector_id: str) -> list[CaseDoc]:
    cases_dir = modules_root / sector_id / "cases"
    if not cases_dir.is_dir():
        return []
    docs: list[CaseDoc] = []
    for path in sorted(cases_dir.rglob("*.md")):
        text = _read(path)
        rel = path.relative_to(modules_root.parent)
        docs.append(
            CaseDoc(
                sector=sector_id,
                relpath=str(rel).replace("\\", "/"),
                title=first_heading(text) or path.stem,
                excerpt=_excerpt(text),
            )
        )
    return docs


def load_catalog(root: Path | None = None) -> Catalog:
    futures_root = root or FUTURES_ROOT
    modules_root = futures_root / "modules"
    if not modules_root.is_dir():
        raise FileNotFoundError(f"Futures modules not found: {modules_root}")

    sectors: list[SectorInfo] = []
    products: list[Product] = []
    for sector_dir in sorted(path for path in modules_root.iterdir() if path.is_dir()):
        readme = sector_dir / "README.md"
        if not readme.exists():
            continue
        text = _read(readme)
        sector_id = sector_dir.name
        parsed = parse_product_tables(text, sector_id)
        products.extend(parsed)
        sectors.append(
            SectorInfo(
                id=sector_id,
                title=first_heading(text) or sector_id,
                summary=first_blockquote(text),
                products=parsed,
                bullets=bullets_under_headings(text, _HEADING_KEYS),
                cases=_load_cases(modules_root, sector_id),
            )
        )
    return Catalog(sectors=sectors, products=products)
