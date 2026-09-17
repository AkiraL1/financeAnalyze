from __future__ import annotations

import argparse

from catalog.registry import load_catalog
from desk.formatters import format_briefing
from desk.pipeline import build_briefing


def _cmd_catalog() -> int:
    catalog = load_catalog()
    for mode in catalog.sectors:
        print(f"[{mode.id}] {mode.label}  ({len(mode.products)} 个观察品种)")
        for product in mode.products:
            print(f"  {product.code:8} {product.name}  ({product.exchange})")
    return 0


def _cmd_desk(code: str, oracle: bool, sector: str | None) -> int:
    try:
        briefing = build_briefing(code, include_oracle=oracle, sector=sector)
    except KeyError as exc:
        print(f"未找到品种：{exc}")
        return 1
    print(format_briefing(briefing), end="")
    return 0


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="finance-analyze")
    sub = parser.add_subparsers(dest="cmd", required=True)
    sub.add_parser("catalog", help="列出分析模式与观察品种")
    desk = sub.add_parser("desk", help="按 Futures 模式生成简报")
    desk.add_argument("--code", required=True, help="品种代码，如 GC / CL / ES")
    desk.add_argument("--sector", help="分析模式 id，如 energy / metals")
    desk.add_argument("--oracle", action="store_true", help="拉取 digital-oracle 信号")
    args = parser.parse_args(argv)
    if args.cmd == "catalog":
        return _cmd_catalog()
    return _cmd_desk(args.code, args.oracle, args.sector)


if __name__ == "__main__":
    raise SystemExit(main())
