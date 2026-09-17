# `modules/metals/` — 金属

> **职责**：覆盖贵金属、工业金属、黑色金属期货，以及锂 / 硅 / 多晶硅等新能源金属期货。
> **关键交易所**：COMEX、NYMEX、LME、SHFE、DCE、GFEX

---

## 1. 品种清单

### 1.1 贵金属（COMEX / SHFE）

| 代码 | 名称 | 交易所 | 备注 |
| --- | --- | --- | --- |
| GC | Gold / 黄金 | COMEX |  |
| SI | Silver / 白银 | COMEX |  |
| PL | Platinum / 铂 | NYMEX |  |
| PA | Palladium / 钯 | NYMEX |  |
| AU | 黄金 | SHFE |  |
| AG | 白白银 | SHFE |  |

### 1.2 工业金属（COMEX / LME / SHFE）

| 代码 | 名称 | 交易所 | 备注 |
| --- | --- | --- | --- |
| HG | Copper / 铜 | COMEX |  |
| ALI | Aluminum / 铝 | COMEX | 微型铝（2024+） |
| LME Copper | LME 3M Copper | LME | 3M、cash、contango |
| LME Aluminium | LME 3M Aluminium | LME |  |
| LME Nickel | LME 3M Nickel | LME | ⚠️ 2022 伦镍事件影响仍需关注 |
| LME Zinc / Lead / Tin | LME 锌 / 铅 / 锡 | LME |  |
| CU | 铜 | SHFE |  |
| AL | 铝 | SHFE |  |
| ZN | 锌 | SHFE |  |
| NI | 镍 | SHFE |  |
| SN | 锡 | SHFE |  |
| PB | 铅 | SHFE |  |

### 1.3 黑色金属（SHFE / DCE）

| 代码 | 名称 | 交易所 | 备注 |
| --- | --- | --- | --- |
| RB | 螺纹钢 | SHFE |  |
| HC | 热卷 | SHFE |  |
| SS | 不锈钢 | SHFE |  |
| FU | 燃料油（虽属能源，但 SHFE 黑色产业链常对比） | SHFE |  |
| I | 铁矿石 | DCE |  |
| J | 焦炭 | DCE |  |
| JM | 焦煤 | DCE |  |
| SF | 硅铁 | DCE |  |
| SM | 锰硅 | DCE |  |

### 1.4 新能源金属（GFEX）

| 代码 | 名称 | 交易所 | 备注 |
| --- | --- | --- | --- |
| SI | 工业硅 | GFEX |  |
| PS | 多晶硅 | GFEX |  |
| LC | 碳酸锂 | GFEX |  |
| PT | 铂 | GFEX |  |
| PD | 钯 | GFEX |  |

---

## 2. 关键数据源

| 缩写 | 全称 | 用途 |
| --- | --- | --- |
| LME | London Metal Exchange | LME 库存、3M 价、cash/3M 升贴水 |
| SHFE | 上海期货交易所 | SHFE 库存 |
| COMEX | Commodity Exchange | COMEX 库存 |
| USGS | U.S. Geological Survey | 矿产产量 |
| World Bureau of Metal Statistics (WBMS) | 全球金属统计局 | 供需平衡 |
| CFTC | Commodity Futures Trading Commission | COT 持仓报告 |
| 中国海关 | 海关总署 | 铜、铁矿石等进出口 |
| 中国钢铁工业协会 | 中钢协 | 粗钢产量、铁矿石进口 |

---

## 3. 跨市 / 跨期套利主要机会

- **LME Copper ↔ SHFE CU**：含税价差、汇率、运费
- **LME ↔ COMEX 铜**：套利窗口常关闭
- **COMEX Gold ↔ SHFE AU**：汇率 + 国内升贴水
- **DCE I（铁矿石）↔ SGX TSI 铁矿石**：人民币 / 美元价差
- **DCE J / JM ↔ 现货价格**：焦炭 / 焦煤基差

---

## 4. 关键宏观驱动

- **美元指数（DXY）**：与贵金属负相关
- **实际利率（TIPS yield）**：黄金的核心驱动
- **全球工业生产 / PMI**：铜为代表
- **新能源汽车销量**：锂 / 镍 / 钴
- **中国房地产 + 基建**：螺纹钢 / 铜 / 铝
- **全球碳中和 / 能源转型**：工业硅 / 多晶硅 / 锂

---

## 5. 模块文档模板

参考 [`MODULE_GUIDE.md` §4.1](../../MODULE_GUIDE.md#41-文档模板合约分析通用)。

`cases/<合约代码>/` 推荐章节：

1. `01-事实.md` — 当前库存、产量、需求、宏观驱动
2. `02-合约规格.md` — 合约乘数、Tick、保证金、交割品级
3. `03-季节性.md` — 历史库存周期、季节性需求
4. `04-跨市.md` — LME ↔ SHFE / COMEX 价差、库存搬移
5. `05-政策.md` — 出口管制、关税、环保限产
6. `06-分析.md` — 综合观点

---

## 6. 修改记录

| 日期 | 变更 | 备注 |
| --- | --- | --- |
| 2026-09-13 | 初始化 `modules/metals/` README.md | 项目首次创建 |