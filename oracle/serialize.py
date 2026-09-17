from dataclasses import asdict, is_dataclass
from typing import Any


def to_jsonable(value: Any) -> Any:
    if value is None or isinstance(value, (str, int, float, bool)):
        return value
    if isinstance(value, dict):
        return {str(key): to_jsonable(item) for key, item in value.items()}
    if isinstance(value, (list, tuple)):
        return [to_jsonable(item) for item in value]
    if is_dataclass(value) and not isinstance(value, type):
        payload = asdict(value)
        payload.pop("raw", None)
        payload.pop("metadata", None)
        return to_jsonable(payload)
    return str(value)
