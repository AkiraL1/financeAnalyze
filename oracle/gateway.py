from collections.abc import Callable
from concurrent.futures import ThreadPoolExecutor, TimeoutError as FuturesTimeout
from dataclasses import dataclass

from oracle.models import OracleSnapshot
from oracle.serialize import to_jsonable

Fetcher = Callable[[], object]


@dataclass
class OracleGateway:
    fetchers_for: Callable[[object], dict[str, Fetcher]]
    timeout_seconds: float = 25.0

    def snapshot(self, product: object) -> OracleSnapshot:
        fetchers = self.fetchers_for(product)
        if not fetchers:
            return OracleSnapshot()
        results: dict[str, object] = {}
        errors: dict[str, str] = {}
        workers = min(8, max(1, len(fetchers)))
        with ThreadPoolExecutor(max_workers=workers) as pool:
            futures = {key: pool.submit(fn) for key, fn in fetchers.items()}
            for key, future in futures.items():
                try:
                    results[key] = to_jsonable(future.result(timeout=self.timeout_seconds))
                except FuturesTimeout:
                    errors[key] = "timeout"
                except Exception as exc:  # noqa: BLE001 - partial failure is expected
                    errors[key] = f"{type(exc).__name__}: {exc}"
        return OracleSnapshot(results=results, errors=errors)
