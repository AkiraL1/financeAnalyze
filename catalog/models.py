from dataclasses import dataclass, field


@dataclass(frozen=True)
class Instrument:
    code: str
    name: str
    exchange: str
    sector: str
    note: str = ""


@dataclass
class AnalysisMode:
    id: str
    label: str
    title: str
    summary: str
    questions: list[str] = field(default_factory=list)
    calendars: list[str] = field(default_factory=list)
    lenses: list[str] = field(default_factory=list)
    products: list[Instrument] = field(default_factory=list)

    @property
    def bullets(self) -> list[str]:
        return list(self.calendars)


@dataclass
class Catalog:
    sectors: list[AnalysisMode]
    products: list[Instrument]

    def get(self, code: str, sector: str | None = None) -> Instrument | None:
        key = code.strip().upper()
        matches = [item for item in self.products if item.code.upper() == key]
        if sector:
            matches = [item for item in matches if item.sector == sector]
        return matches[0] if matches else None

    def sector(self, sector_id: str) -> AnalysisMode | None:
        for item in self.sectors:
            if item.id == sector_id:
                return item
        return None


Product = Instrument
SectorInfo = AnalysisMode
