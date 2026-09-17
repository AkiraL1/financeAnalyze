from __future__ import annotations

import os
from dataclasses import dataclass
from pathlib import Path

from finance_analyze.paths import ROOT


def load_dotenv(path: Path | None = None) -> None:
    env_path = path or (ROOT / ".env")
    if not env_path.is_file():
        return
    for raw in env_path.read_text(encoding="utf-8").splitlines():
        line = raw.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, _, value = line.partition("=")
        os.environ.setdefault(key.strip(), value.strip().strip('"').strip("'"))


load_dotenv()


@dataclass(frozen=True)
class MiniMaxSettings:
    api_key: str
    base_url: str
    model: str


def minimax_settings() -> MiniMaxSettings | None:
    key = os.environ.get("MINIMAX_API_KEY", "").strip()
    if not key:
        return None
    return MiniMaxSettings(
        api_key=key,
        base_url=os.environ.get("MINIMAX_BASE_URL", "https://api.minimaxi.com/v1").rstrip("/"),
        model=os.environ.get("MINIMAX_MODEL", "MiniMax-M3"),
    )
