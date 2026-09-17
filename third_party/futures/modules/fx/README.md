# `modules/fx/` — 外汇

> **职责**：覆盖主要货币对外汇期货，包括 CME 标准合约、ICE 美元指数等。
> **关键交易所**：CME（CME FX）、ICE Futures U.S.、SGX

---

## 1. 品种清单

### 1.1 境外（CME / ICE）

| 代码 | 名称 | 交易所 | 备注 |
| --- | --- | --- | --- |
| 6E | Euro FX Futures | CME |  |
| 6B | British Pound | CME |  |
| 6J | Japanese Yen | CME |  |
| 6A | Australian Dollar | CME |  |
| 6C | Canadian Dollar | CME |  |
| 6S | Swiss Franc | CME |  |
| 6N | New Zealand Dollar | CME |  |
| 6M | Mexican Peso | CME |  |
| 6Z | South African Rand | CME |  |
| DX | U.S. Dollar Index | ICE | 美元指数期货 |
| DXP | ICE US Dollar Index | ICE |  |

### 1.2 微型 / 迷你

| 代码 | 名称 | 交易所 | 备注 |
| --- | --- | --- | --- |
| M6E | E-mini Euro FX | CME | 0.6 倍 6E |
| M6A | E-mini Australian Dollar | CME |  |
| M6B | E-mini British Pound | CME |  |
| M6J | E-mini Japanese Yen | CME |  |

### 1.3 境内（境外交易所 + 境内 OTC）

- 境内尚无标准场内人民币外汇期货（CFETS 等尚未推出人民币期货合约）
- 常用人民币风险管理工具：境内外汇衍生品（远期 / 掉期 / 期权）+ 境外 CNH 期货

---

## 2. 关键概念

### 2.1 利差交易（Carry Trade）

- 借入低息货币（如 JPY、CHF），买入高息货币（如 AUD、BRL）
- 赚取利差，但承担汇率波动风险
- 反向操作：卖出高息货币买入低息货币（short carry）

### 2.2 套息 / 利差

- **Covered Interest Rate Parity** ≈ 无风险平价
- 远期升水 / 贴水反映利差

### 2.3 避险情绪（Risk-On / Risk-Off）

- **Risk-On**：偏好高息（澳元、新西兰元）、新兴市场货币、风险资产
- **Risk-Off**：偏好低息（日元、瑞郎）、美元、黄金、美债

### 2.4 美元周期

- **强美元**：美元指数走强 → 新兴市场资本外流 → 商品货币（澳元、加元）承压
- **弱美元**：反之

---

## 3. 关键数据源

- **美联储（Fed）**：议息会议、FOMC Statement、SEP
- **欧央行（ECB）**：利率决议、APP / PEPP
- **日银（BOJ）**：YCC / 收益率曲线控制（已退出，2024 起）
- **英央行（BoE）**：Bank Rate 决议
- **中国央行（PBoC）**：LPR、MLF、存款准备金率
- **瑞士央行（SNB）**：政策利率
- **加拿大央行（BoC）**：Overnight Rate
- **澳洲央行（RBA）**：Cash Rate
- **新西兰央行（RBNZ）**：OCR
- **BLS**：非农、CPI、PPI
- **ISM**：ISM PMI

---

## 4. 跨货币套利

- **EUR / USD ↔ GBP / USD**：欧美利差
- **AUD / JPY**：典型套息组合
- **EUR / JPY ↔ EUR / USD + USD / JPY**：三角套利
- **DX（美元指数）↔ 一篮子货币反向加权**：DX 本身由 EUR 57.6% + JPY 13.6% + GBP 11.9% + CAD 9.1% + SEK 4.2% + CHF 3.6% 加权

---

## 5. 模块文档模板

参考 [`MODULE_GUIDE.md` §4.1](../../MODULE_GUIDE.md#41-文档模板合约分析通用)。

`cases/<货币对>/` 推荐章节：

1. `01-事实.md` — 当前利差、汇率水平、技术形态
2. `02-合约规格.md` — 合约乘数、Tick、最后交易日
3. `03-利差.md` — 利差、carry、远期点
4. `04-政策.md` — 央行决议、利率路径
5. `05-避险.md` — risk-on / risk-off 状态
6. `06-分析.md` — 综合观点

---

## 6. 修改记录

| 日期 | 变更 | 备注 |
| --- | --- | --- |
| 2026-09-13 | 初始化 `modules/fx/` README.md | 项目首次创建 |