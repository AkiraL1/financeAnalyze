from dataclasses import dataclass, field


@dataclass(frozen=True)
class Product:
    code: str
    name: str
    exchange: str
    sector: str
    note: str = ""


@dataclass(frozen=True)
class CaseDoc:
    sector: str
    relpath: str
    title: str
    excerpt: str


@dataclass
class SectorInfo:
    id: str
    title: str
    summary: str
    products: list[Product] = field(default_factory=list)
    bullets: list[str] = field(default_factory=list)
    cases: list[CaseDoc] = field(default_factory=list)


@dataclass
class Catalog:
    sectors: list[SectorInfo]
    products: list[Product]

    def get(self, code: str, sector: str | None = None) -> Product | None:
        key = code.strip().upper()
        matches = [item for item in self.products if item.code.upper() == key]
        if sector:
            matches = [item for item in matches if item.sector == sector]
        return matches[0] if matches else None

    def sector(self, sector_id: str) -> SectorInfo | None:
        for item in self.sectors:
            if item.id == sector_id:
                return item
        return None
