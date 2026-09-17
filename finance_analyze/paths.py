from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
FUTURES_ROOT = ROOT / "third_party" / "futures"
ORACLE_ROOT = ROOT / "third_party" / "digital-oracle"
WEB_ROOT = ROOT / "apps" / "web"


def ensure_oracle_on_path() -> None:
    import sys

    path = str(ORACLE_ROOT)
    if path not in sys.path:
        sys.path.insert(0, path)
