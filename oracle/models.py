from dataclasses import dataclass, field


@dataclass
class OracleSnapshot:
    results: dict[str, object] = field(default_factory=dict)
    errors: dict[str, str] = field(default_factory=dict)

    @property
    def ok(self) -> bool:
        return not self.errors
