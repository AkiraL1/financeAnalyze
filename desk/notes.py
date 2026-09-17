from catalog.models import Product
from oracle.models import OracleSnapshot

_DISCLAIMER = (
    "本台不生成合约乘数、Tick、保证金、涨跌停等规格数字。"
    "规格以 Futures 知识库与交易所官网核验为准。"
)


def _rating(snapshot: OracleSnapshot) -> str | None:
    payload = snapshot.results.get("fear_greed")
    if isinstance(payload, dict):
        rating = payload.get("rating")
        if isinstance(rating, str):
            return rating
    return None


def _spread(snapshot: OracleSnapshot, long_tenor: str, short_tenor: str) -> float | None:
    payload = snapshot.results.get("treasury")
    if not isinstance(payload, dict):
        return None
    points = payload.get("points")
    if not isinstance(points, list):
        return None
    yields: dict[str, float] = {}
    for point in points:
        if not isinstance(point, dict):
            continue
        tenor = point.get("tenor")
        value = point.get("value")
        if isinstance(tenor, str) and isinstance(value, (int, float)):
            yields[tenor.upper()] = float(value)
    if long_tenor in yields and short_tenor in yields:
        return yields[long_tenor] - yields[short_tenor]
    return None


def _mm_net(snapshot: OracleSnapshot) -> int | None:
    payload = snapshot.results.get("cftc")
    if not isinstance(payload, list) or not payload:
        return None
    first = payload[0]
    if not isinstance(first, dict):
        return None
    if "mm_net" in first and isinstance(first["mm_net"], int):
        return first["mm_net"]
    long_pos = first.get("mm_long")
    short_pos = first.get("mm_short")
    if isinstance(long_pos, int) and isinstance(short_pos, int):
        return long_pos - short_pos
    return None


def compose_notes(product: Product, oracle: OracleSnapshot | None) -> list[str]:
    notes = [
        f"{product.code} {product.name} @ {product.exchange}，知识模块 `{product.sector}`。",
        _DISCLAIMER,
    ]
    if oracle is None:
        notes.append("未拉取 digital-oracle 信号。可用 --oracle 或看台上的「刷新市场信号」。")
        return notes
    if oracle.errors:
        failed = ", ".join(sorted(oracle.errors))
        notes.append(f"部分信号失败（容忍）：{failed}")
    rating = _rating(oracle)
    if rating:
        notes.append(f"启发式：CNN Fear & Greed 当前为 {rating}（情绪指标，不是交易指令）。")
    spread = _spread(oracle, "10Y", "2Y")
    if spread is not None:
        shape = "倒挂" if spread < 0 else "正斜率"
        notes.append(f"启发式：美债 10Y-2Y 利差约 {spread:.2f}bp/百分点量级，曲线{shape}。")
    net = _mm_net(oracle)
    if net is not None:
        side = "净多" if net > 0 else "净空"
        notes.append(f"启发式：CFTC Managed Money 最新报告{side}（{net} 张，smart money 方向参考）。")
    if "price" in oracle.results:
        notes.append("价格路径来自 digital-oracle Yahoo/Stooq 兼容 provider，用于技术面对照，不替代合约规格。")
    if "polymarket" in oracle.results:
        notes.append("预测市场价格仅作事件概率对照，需与品种基本面分开标注时间窗口。")
    return notes
