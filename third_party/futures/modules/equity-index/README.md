# `modules/equity-index/` — 股指

> **职责**：覆盖境外 + 境内股指期货。
> **关键交易所**：CME（E-mini 系列）、ICE、Eurex、SGX、HKEX、CFFEX（中金所）

---

## 1. 品种清单

### 1.1 境外（CME / ICE / Eurex / SGX / HKEX）

| 代码 | 名称 | 交易所 | 备注 |
| --- | --- | --- | --- |
| ES | E-mini S&P 500 | CME | 全球最大股指期货 |
| NQ | E-mini Nasdaq-100 | CME | 科技股 |
| YM | E-mini Dow ($5) | CBOT | 道指 |
| RTY | E-mini Russell 2000 | CME | 小盘股 |
| SP | S&P 500 标准合约 | CME | 已基本被 ES 取代 |
| NKD | Nikkei 225 USD | CME | 日经 225 美元计价 |
| NIY | Nikkei 225 JPY | CME | 日经 225 日元计价 |
| HSI | Hang Seng Index Futures | HKEX | 恒生指数（HKEX 主场） |
| HSCEI | H-share Index Futures | HKEX | 恒生中国企业指数 |
| CN | SGX CNX Nifty | SGX | 印度 Nifty 50 |
| TW | SGX MSCI Taiwan | SGX | MSCI 台湾 |
| Z | Mini-DAX | Eurex |  |
| FDAX | DAX Futures | Eurex |  |
| FESX | Euro Stoxx 50 | Eurex |  |
| FGBL | Euro-Bund | Eurex | （实为利率） |
| Z | FTSE 100 | ICE |  |

### 1.2 境内（中金所 CFFEX）

| 简称 | 名称 | 交易所 | 备注 |
| --- | --- | --- | --- |
| IF | 沪深 300 股指期货 | CFFEX |  |
| IH | 上证 50 股指期货 | CFFEX |  |
| IC | 中证 500 股指期货 | CFFEX |  |
| IM | 中证 1000 股指期货 | CFFEX |  |
| TS | 2 年期国债期货 | CFFEX |  |
| TF | 5 年期国债期货 | CFFEX |  |
| T | 10 年期国债期货 | CFFEX |  |
| TL | 30 年期国债期货 | CFFEX | 2023 上市 |

---

## 2. 关键数据源

| 缩写 | 全称 | 用途 |
| --- | --- | --- |
| FOMC | Federal Open Market Committee | 美联储议息会议 |
| ECB | European Central Bank | 欧央行决议 |
| BOJ | Bank of Japan | 日银决议 |
| PBoC | People's Bank of China | 央行决议 |
| BLS | Bureau of Labor Statistics | 非农、CPI、PPI |
| BEA | Bureau of Economic Analysis | GDP、PCE |
| CBOE | Chicago Board Options Exchange | VIX 波动率指数 |
| MOVE | ICE BofA MOVE Index | 美债隐含波动率 |

---

## 3. 关键概念

### 3.1 Fair Value Gap（理论价差）

股指期货与现货指数之间的"合理价差"，由利率 + 股息决定：

```
Fair Value = Futures Price - Index Price
           ≈ Index × [r × (T / 365) - d × (t / 365)]
```

- `r` = 无风险利率
- `d` = 标的指数的远期股息率
- `T` = 到合约到期天数
- `t` = 距上次除息日天数

ES 等合约的 fair value 由 CME 实时公布。

### 3.2 展期收益（Roll Yield）

- **Contango（远月升水）**：空头获得正 roll yield；多头支付 roll yield
- **Backwardation（远月贴水）**：多头获得正 roll yield；空头支付

### 3.3 季月 vs 连续月

- 季月合约（3 / 6 / 9 / 12）：流动性最好
- 连续月合约：策略用途，CME 提供连续合约代码

---

## 4. 跨时区套利

- **ES（美东盘） ↔ NKD（日盘开盘前）**：美国科技 vs 日本蓝筹
- **HSI ↔ ES**：跨时区 beta 调整
- **A50（SGX）↔ IF（CFFEX）**：A 股开盘前预判

---

## 5. 模块文档模板

参考 [`MODULE_GUIDE.md` §4.1](../../MODULE_GUIDE.md#41-文档模板合约分析通用)。

`cases/<合约代码>/` 推荐章节：

1. `01-事实.md` — 当前指数估值、宏观环境、市场情绪（VIX）
2. `02-合约规格.md` — 合约乘数、Tick、保证金、最后交易日
3. `03-季节性.md` — 月度效应、年末效应
4. `04-政策.md` — FOMC、ECB、BOJ、PBoC 决议与点阵图
5. `05-股息.md` — 除息日、fair value gap
6. `06-分析.md` — 综合观点

---

## 6. 修改记录

| 日期 | 变更 | 备注 |
| --- | --- | --- |
| 2026-09-13 | 初始化 `modules/equity-index/` README.md | 项目首次创建 |