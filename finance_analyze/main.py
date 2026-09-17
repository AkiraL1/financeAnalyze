from __future__ import annotations

import argparse

from catalog.loader import load_catalog
from desk.formatters import format_briefing
from desk.pipeline import build_briefing


def _cmd_catalog() -> int:
    catalog = load_catalog()
    for sector in catalog.sectors:
        print(f"[{sector.id}] {sector.title}  ({len(sector.products)} 个品种)")
        for product in sector.products[:8]:
            print(f"  {product.code:12} {product.name}  ({product.exchange})")
        extra = len(sector.products) - 8
        if extra > 0:
            print(f"  … 另有 {extra} 个品种")
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
    sub.add_parser("catalog", help="列出 Futures 知识库品种")
    desk = sub.add_parser("desk", help="生成分析台简报")
    desk.add_argument("--code", required=True, help="品种代码，如 GC / CL / ES")
    desk.add_argument("--sector", help="模块 id，用于消歧义，如 energy / metals")
    desk.add_argument("--oracle", action="store_true", help="拉取 digital-oracle 信号")
    args = parser.parse_args(argv)
    if args.cmd == "catalog":
        return _cmd_catalog()
    return _cmd_desk(args.code, args.oracle, args.sector)


if __name__ == "__main__":
    raise SystemExit(main())
