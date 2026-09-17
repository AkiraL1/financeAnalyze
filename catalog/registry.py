from catalog.models import AnalysisMode, Catalog, Instrument

_MODES: tuple[tuple[str, str, str, str, tuple[str, ...], tuple[str, ...]], ...] = (
    (
        "agricultural",
        "农产品",
        "农产品透镜",
        "供需、天气、压榨利润与跨市价差。",
        ("主产区天气是否定价？", "压榨/替代利润是否驱动油籽？", "CBOT 与国内盘是否分裂？"),
        ("USDA WASDE 月报窗口", "生长季天气炒作", "出口销售周报"),
    ),
    (
        "energy",
        "能源",
        "能源透镜",
        "库存、产量、裂解价差与地缘溢价。",
        ("库存相对五年均值？", "曲线 contango 还是 backwardation？", "裂解价差是否支持炼厂开工？"),
        ("EIA / API 周期库存", "OPEC+ 会议", "冬夏天然气季节"),
    ),
    (
        "metals",
        "金属",
        "金属透镜",
        "实际利率、美元、库存与工业需求。",
        ("实际利率是否压制黄金？", "铜是否在为全球工业定价？", "内外盘价差有没有窗口？"),
        ("CFTC COT 周报", "交易所库存", "美元与实际利率"),
    ),
    (
        "equity-index",
        "股指",
        "股指透镜",
        "风险偏好、利率路径与波动率。",
        ("VIX / 情绪是否极端？", "利率预期是否主导估值？", "风格是进攻还是防守？"),
        ("FOMC / 非农 / CPI", "季月展期", "波动率事件"),
    ),
    (
        "interest-rate",
        "利率",
        "利率透镜",
        "曲线形态、政策利率与久期。",
        ("曲线是倒挂、平坦还是陡峭？", "市场定价的降息/加息路径？", "波动率是否抬升？"),
        ("FOMC / 点阵图", "国债供给", "SOFR 路径"),
    ),
    (
        "fx",
        "外汇",
        "外汇透镜",
        "利差、美元周期与避险。",
        ("利差是否支撑套息？", "当前是 risk-on 还是 risk-off？", "美元周期处在哪一段？"),
        ("主要央行议息", "非农 / CPI", "避险流动"),
    ),
    (
        "crypto",
        "加密",
        "加密透镜",
        "基差、资金费率与风险偏好。",
        ("期货/现货基差是否极端？", "情绪是否拥挤？", "监管事件有没有被定价？"),
        ("CME 持仓", "资金费率", "ETF 资金流线索"),
    ),
)

_INSTRUMENTS = (
    Instrument("ZC", "Corn / 玉米", "CBOT", "agricultural"),
    Instrument("ZS", "Soybean / 大豆", "CBOT", "agricultural"),
    Instrument("ZW", "Wheat / 小麦", "CBOT", "agricultural"),
    Instrument("CL", "WTI Crude Oil / WTI 原油", "NYMEX", "energy"),
    Instrument("NG", "Henry Hub Natural Gas / 天然气", "NYMEX", "energy"),
    Instrument("BRN", "Brent Crude Oil / 布伦特原油", "ICE", "energy"),
    Instrument("GC", "Gold / 黄金", "COMEX", "metals"),
    Instrument("SI", "Silver / 白银", "COMEX", "metals"),
    Instrument("HG", "Copper / 铜", "COMEX", "metals"),
    Instrument("ES", "E-mini S&P 500", "CME", "equity-index"),
    Instrument("NQ", "E-mini Nasdaq-100", "CME", "equity-index"),
    Instrument("ZN", "10-Year T-Note", "CBOT", "interest-rate"),
    Instrument("ZB", "30-Year T-Bond", "CBOT", "interest-rate"),
    Instrument("6E", "Euro FX Futures", "CME", "fx"),
    Instrument("DX", "U.S. Dollar Index", "ICE", "fx"),
    Instrument("BTC", "Bitcoin Futures", "CME", "crypto"),
    Instrument("ETH", "Ether Futures", "CME", "crypto"),
)


def load_catalog() -> Catalog:
    grouped: dict[str, list[Instrument]] = {item[0]: [] for item in _MODES}
    for instrument in _INSTRUMENTS:
        grouped.setdefault(instrument.sector, []).append(instrument)
    modes = []
    for mode_id, label, title, summary, questions, calendars in _MODES:
        modes.append(
            AnalysisMode(
                id=mode_id,
                label=label,
                title=title,
                summary=summary,
                questions=list(questions),
                calendars=list(calendars),
                lenses=["基本面", "技术面", "政策面", "跨市场对照"],
                products=grouped.get(mode_id, []),
            )
        )
    return Catalog(sectors=modes, products=list(_INSTRUMENTS))
