# `modules/crypto/` — 加密衍生品

> **职责**：覆盖 CME 加密货币期货 / 期权，以及与现货 / 永续合约的套利机会。
> **关键交易所**：CME（BTC、ETH 期货 / 期权 / 微型），Coibase / Binance / OKX 等（现货 / 永续）

---

## 1. 品种清单

### 1.1 境外（CME）

| 代码 | 名称 | 交易所 | 备注 |
| --- | --- | --- | --- |
| BTC | Bitcoin Futures | CME | 5 BTC / 张 |
| ETH | Ether Futures | CME | 50 ETH / 张 |
| MBT | Micro Bitcoin Futures | CME | 0.1 BTC / 张 |
| MET | Micro Ether Futures | CME | 0.1 ETH / 张 |
| BTF | Bitcoin Friday Futures | CME | 短期合约 |
| BTC options | Bitcoin Options | CME |  |
| ETH options | Ether Options | CME |  |
| BTQ | Micro Bitcoin Options | CME |  |

### 1.2 现货 / 永续（境外 - 仅作价差参考）

| 类别 | 交易所 | 用途 |
| --- | --- | --- |
| 现货 BTC / ETH | Coinbase / Kraken / Binance | CME 期货 vs 现货价差 |
| 永续合约（perpetual） | Binance / OKX / Bybit | CME 期货 vs 永续合约价差 |
| 现货 ETF | BlackRock IBIT / Fidelity FBTC / Grayscale GBTC | 资金流指标 |

---

## 2. 关键概念

### 2.1 现货 ETF 与期货关系

- 美国现货 BTC ETF 自 2024 年 1 月获批以来，资金流是核心驱动
- 现货 ETF 净流入 → 现货需求上升 → 期货跟随上涨
- "Cash-and-carry" 套利：买现货 ETF + 卖 CME 期货（contango 时）

### 2.2 永续合约（Perpetual Futures）

- 无到期日，通过 funding rate（资金费率）锚定现货
- 资金费率由 long / short 失衡决定
- CME 季度合约 vs 永续：基差套利 + funding carry

### 2.3 CME vs 永续合约基差

- 季度合约临近到期时，CME ↔ 现货 / 永续的价差收敛
- 8 月 / 9 月 / 12 月 / 3 月季月合约

### 2.4 监管环境

- **CFTC**：监管 CME 期货；永续合约（离岸）非 CFTC 监管
- **SEC**：监管现货 ETF、监管 ICO / 代币是否构成证券
- **MiCA**（EU）：欧盟加密资产市场监管框架
- **境内**：境内交易所禁止运营加密资产现货 / 期货；CME 是合规跨境通道

---

## 3. 关键数据源

| 缩写 / 来源 | 用途 |
| --- | --- |
| CME Group | 期货合约规格、持仓 |
| CFTC COT | 周度持仓报告 |
| Farside Investors | 现货 ETF 净流入 |
| Glassnode | 链上指标（活跃地址、矿工流出） |
| Coinglass | 永续合约 funding rate、爆仓数据 |
| Bitcoin Treasuries | 公司持有 BTC 数量 |

---

## 4. 套利 / 策略

- **Cash-and-carry**：买现货（ETF 或链上）+ 卖 CME 期货
- **季度合约 roll**：在季月到期前做展期
- **CME ↔ 永续合约价差**：funding rate 高时，CME 多 + 永续空
- **BTC ↔ ETH ratio**：β / 风险偏好切换
- **现货 ETF 流入跟随**：日内动量

---

## 5. ⚠️ 关键风险

- **监管风险极高**：SEC 政策、ETF 审批、MiCA、各国禁令变化频繁
- **24/7 市场**：永续合约全天候交易，需注意风控
- **交易所风险**：离岸交易所破产 / 挤兑风险（FTX、Alameda 等历史案例）
- **网络风险**：链上拥堵、矿池算力
- **合约规格风险**：CME 已多次调整合约乘数与 Tick，**核验日期必须附**

---

## 6. 模块文档模板

参考 [`MODULE_GUIDE.md` §4.1](../../MODULE_GUIDE.md#41-文档模板合约分析通用)。

`cases/<合约代码>/` 推荐章节：

1. `01-事实.md` — 当前现货 / 期货价、funding rate、ETF 资金流
2. `02-合约规格.md` — 合约乘数、Tick、保证金、最后交易日（**必核验**）
3. `03-季节性.md` — 减半周期、宏观周期
4. `04-政策.md` — SEC / CFTC 决议、ETF 审批
5. `05-套利.md` — Cash-and-carry、CME ↔ 永续
6. `06-分析.md` — 综合观点

---

## 7. 修改记录

| 日期 | 变更 | 备注 |
| --- | --- | --- |
| 2026-09-13 | 初始化 `modules/crypto/` README.md | 项目首次创建 |