from catalog.models import Product

_SKIP_CODES = {"代码", "简称", "类别", "缩写", "缩写 / 来源"}


def parse_product_tables(text: str, sector: str) -> list[Product]:
    products: list[Product] = []
    seen: set[str] = set()
    for raw in text.splitlines():
        line = raw.strip()
        if not line.startswith("|"):
            continue
        cells = [cell.strip() for cell in line.strip("|").split("|")]
        if len(cells) < 3:
            continue
        code, name, exchange = cells[0], cells[1], cells[2]
        if not code or code in _SKIP_CODES:
            continue
        if set(code.replace(":", "")) <= {"-"}:
            continue
        key = code.upper()
        if key in seen:
            continue
        seen.add(key)
        note = cells[3] if len(cells) > 3 else ""
        products.append(
            Product(
                code=code,
                name=name,
                exchange=exchange,
                sector=sector,
                note=note,
            )
        )
    return products


def first_heading(text: str) -> str:
    for line in text.splitlines():
        stripped = line.strip()
        if stripped.startswith("# "):
            return stripped[2:].strip()
    return ""


def first_blockquote(text: str) -> str:
    for line in text.splitlines():
        stripped = line.strip()
        if stripped.startswith(">"):
            return stripped.lstrip("> ").strip()
    return ""


def bullets_under_headings(text: str, keywords: tuple[str, ...], limit: int = 8) -> list[str]:
    collect = False
    found: list[str] = []
    for line in text.splitlines():
        stripped = line.strip()
        if stripped.startswith("#"):
            heading = stripped.lstrip("# ").strip()
            collect = any(key in heading for key in keywords)
            continue
        if collect and stripped.startswith("- "):
            found.append(stripped[2:].strip())
            if len(found) >= limit:
                break
    return found
