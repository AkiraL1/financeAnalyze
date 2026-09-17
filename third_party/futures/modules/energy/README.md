# `modules/energy/` — 能源

> **职责**：覆盖原油、天然气、成品油、燃料油、动力煤等能源期货。
> **关键交易所**：NYMEX、ICE Futures、SHFE、INE

---

## 1. 品种清单

### 1.1 境外（NYMEX / ICE / CME）

| 代码 | 名称 | 交易所 | 备注 |
| --- | --- | --- | --- |
| CL | WTI Crude Oil / WTI 原油 | NYMEX | 全球基准原油之一 |
| BRN | Brent Crude Oil / 布伦特原油 | ICE | 全球基准原油之一 |
| NG | Henry Hub Natural Gas / 天然气 | NYMEX | 美国基准天然气 |
| HH | Henry Hub Financial Natural Gas | NYMEX | 财务天然气（末日货） |
| RB | RBOB Gasoline / 汽油 | NYMEX |  |
| HO | Heating Oil / 取暖油 | NYMEX |  |
| CL | Micro WTI Crude Oil | NYMEX | 微型 WTI |
| QM | E-mini Crude Oil | NYMEX | 迷你原油 |
| QG | E-mini Natural Gas | NYMEX | 迷你天然气 |
| G | Gasoil / 柴油 | ICE | 欧洲基准柴油 |
| T | Gas Oil Crack | ICE | 裂解价差 |

### 1.2 境内（SHFE / INE）

| 简称 | 名称 | 交易所 | 备注 |
| --- | --- | --- | --- |
| SC | 原油（中质含硫原油） | INE | 人民币计价 |
| LU | 低硫燃料油 | INE |  |
| FU | 燃料油 | SHFE |  |
| BC | 国际铜 | INE |  |
| NR | 20 号胶 | INE |  |
| EC | 集运指数（欧线） | INE |  |
| TC | 动力煤 | ZCE | ⚠️ 已暂停交易（核验日期见 notes/） |

---

## 2. 关键数据源

| 缩写 | 全称 | 用途 |
| --- | --- | --- |
| EIA | U.S. Energy Information Administration | 原油 / 天然气周度库存、月报、STEO |
| OPEC | Organization of the Petroleum Exporting Countries | OPEC+ 月度决议 |
| IEA | International Energy Agency | 月度石油市场报告（OMR） |
| Baker Hughes | Baker Hughes Co. | 美国活跃钻机数（每周五） |
| API | American Petroleum Institute | 周度原油库存（周三晚） |
| 中国统计局 | 国家统计局 | 国内原油产量、加工量 |
| 中国海关 | 海关总署 | 原油 / 燃料油进出口 |

---

## 3. 关键报告日历

- **EIA 周度库存（Petroleum Status Report）**：每周三 22:30（冬令时）/ 23:30（夏令时），北京时间
- **API 周度库存**：每周三 04:30 北京时间
- **Baker Hughes 钻机数**：每周五 01:00 北京时间
- **OPEC+ 月报**：每月 12–14 日左右
- **OPEC+ 部长级会议**：每月 / 每两月一次
- **EIA STEO（短期能源展望）**：每月 8–12 日左右

---

## 4. 跨市 / 跨期套利主要机会

- **Brent ↔ WTI 价差（Brent-WTI spread）**：受原油品质、运费、库欣库存驱动
- **WTI 月差结构（calendar spread）**：contango / backwardation 反映供需
- **天然气跨月（NG calendar）**：冬夏温差、库存 vs 5 年均值
- **RBOB ↔ HO ↔ WTI 裂解价差（crack spread）**：炼厂利润率
- **INE SC ↔ NYMEX CL / ICE BRN**：内外盘价差（汇率、运费、原油品质差异）
- **低硫燃油 LU ↔ 新加坡纸货 / MOPS**：亚洲现货基准

---

## 5. 模块文档模板

参考 [`MODULE_GUIDE.md` §4.1](../../MODULE_GUIDE.md#41-文档模板合约分析通用)。

`cases/<合约代码>/` 推荐章节：

1. `01-事实.md` — 当前库存、产量、需求、钻机数
2. `02-合约规格.md` — 合约乘数、Tick、保证金、品质、交割方式
3. `03-季节性.md` — 历史月差结构、库存周期
4. `04-政策.md` — OPEC+ 决议、出口禁令、关税、制裁
5. `05-地缘.md` — 中东、东欧、委内瑞拉等关键地缘事件
6. `06-分析.md` — 综合观点

---

## 6. 修改记录

| 日期 | 变更 | 备注 |
| --- | --- | --- |
| 2026-09-13 | 初始化 `modules/energy/` README.md | 项目首次创建 |