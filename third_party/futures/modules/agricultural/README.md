# `modules/agricultural/` — 农产品

> **职责**：覆盖境外 + 境内农产品期货合约的基本面、技术面、政策面分析。
> **关键交易所**：CBOT、ICE Futures US（软商品）、DCE、CZCE

---

## 1. 品种清单

### 1.1 境外（CME Group / ICE）

| 代码 | 名称 | 交易所 | 备注 |
| --- | --- | --- | --- |
| ZC | Corn / 玉米 | CBOT | 主力合约：3、5、7、9、12 月 |
| ZS | Soybean / 大豆 | CBOT | 主力合约：1、3、5、7、8、9、11 月 |
| ZM | Soybean Meal / 豆粕 | CBOT |  |
| ZL | Soybean Oil / 豆油 | CBOT |  |
| ZW | Wheat / 小麦（冬麦） | CBOT | KC 冬麦代码 KE（硬红冬麦） |
| KE | KC HRW Wheat | CBOT | 硬红冬麦 |
| MWE | Spring Wheat | CBOT | 春麦（2026 上市） |
| ZO | Oats / 燕麦 | CBOT |  |
| ZR | Rough Rice / 稻谷 | CBOT |  |
| CC | Cocoa / 可可 | ICE |  |
| CT | Cotton No. 2 / 棉花 | ICE |  |
| KC | Coffee "C" / 咖啡 | ICE |  |
| SB | Sugar No. 11 / 白糖 | ICE |  |
| OJ | FCOJ / 冷冻浓缩橙汁 | ICE |  |
| DA | Milk Class III / 三级奶 | CME |  |
| DC | Cheese / 切达干酪 | CME |  |

### 1.2 境内（SHFE / DCE / CZCE / INE / GFEX）

| 简称 | 名称 | 交易所 | 备注 |
| --- | --- | --- | --- |
| a | 豆一（黄大豆一号） | DCE | 非转基因食用大豆 |
| b | 豆二（黄大豆二号） | DCE | 进口转基因榨油大豆 |
| m | 豆粕 | DCE |  |
| y | 豆油 | DCE |  |
| p | 棕榈油 | DCE |  |
| c | 玉米 | DCE |  |
| cs | 玉米淀粉 | DCE |  |
| jd | 鸡蛋 | DCE |  |
| lh | 生猪 | DCE |  |
| jr | 粳米 | DCE |  |
| bb | 胶合板 | DCE |  |
| fb | 纤维板 | DCE |  |
| yd | 豆二期权 | DCE |  |
| CF | 棉花（一号棉） | CZE |  |
| SR | 白糖 | CZE |  |
| CF | 棉纱 | CZE |  |
| AP | 苹果 | CZE |  |
| CJ | 红枣 | CZE |  |
| PK | 花生 | CZE |  |
| OI | 菜油 | CZE |  |
| RM | 菜粕 | CZE |  |
| RS | 菜籽 | CZE |  |
| WH | 强麦 | CZE |  |
| PM | 普麦 | CZE |  |
| RI | 早籼稻 | CZE |  |
| LR | 晚籼稻 | CZE |  |
| RR | 粳稻 | CZE |  |

---

## 2. 关键数据源

| 缩写 | 全称 | 用途 |
| --- | --- | --- |
| USDA | U.S. Department of Agriculture | WASDE 月度供需报告 |
| USDA NASS | National Agricultural Statistics Service | 作物进度、播种面积、单产 |
| USDA FAS | Foreign Agricultural Service | 全球供需、出口销售 |
| CFTC | Commodity Futures Trading Commission | COT 周度持仓 |
| CONAB | Companhia Nacional de Abastecimento (Brazil) | 巴西作物供需 |
| IGC | International Grains Council | 国际谷物理事会月报 |
| AMIS | Agricultural Market Information System | 全球农产品市场信息系统 |
| 中国农业农村部 | 农业农村部市场预警专家委员会 | 中国农产品供需平衡表（CASDE） |

---

## 3. 季节性日历

- **北半球春播**：4–5 月（玉米、大豆、冬小麦）
- **北半球生长关键期**：6–8 月（天气炒作高峰）
- **北半球秋收**：9–11 月
- **南半球（巴西、阿根廷）春播**：10–12 月；秋收 3–5 月
- **USDA WASDE 报告**：每月 8–12 日左右
- **USDA Crop Progress**：每年 4 月–11 月，每周一
- **USDA Export Sales**：每周四

---

## 4. 跨市 / 跨期套利主要机会

- **CBOT ↔ DCE 大豆**：关税、配额、汇率
- **CBOT 豆油 ↔ DCE 棕榈油**：替代品价差
- **CBOT 玉米 ↔ DCE 玉米**：配额与替代品
- **ICE 棉花 ↔ CZCE 棉花**：进口配额、滑准税
- **ICE 白糖 ↔ CZCE 白糖**：进口关税、配额

---

## 5. 模块文档模板

参考 [`MODULE_GUIDE.md` §4.1](../../MODULE_GUIDE.md#41-文档模板合约分析通用) 通用结构。

`cases/<合约代码>/` 推荐章节：

1. `01-事实.md` — 当前供需基本面（USDA / CONAB / CASDE 最新数据 + 核验日期）
2. `02-合约规格.md` — 合约乘数、最小变动价位、保证金、交割规则（**双镜像核验**）
3. `03-季节性.md` — 历史季节性图、关键时间窗口
4. `04-政策.md` — 关税、配额、生物燃料政策、补贴
5. `05-套利.md` — 跨期 / 跨市 / 跨品种价差
6. `06-分析.md` — 综合观点、关键驱动、风险

---

## 6. 修改记录

| 日期 | 变更 | 备注 |
| --- | --- | --- |
| 2026-09-13 | 初始化 `modules/agricultural/` README.md | 项目首次创建 |
| 2026-09-13 | 新增 `cases/el-nino-2026/01-分析.md` — 中国农产品期货综合分析 + 厄尔尼诺周期研究报告（NOAA RONI 1950-2026 完整 919 季节数据 + Polymarket 交叉验证） | 由 Owner 委托存档 |