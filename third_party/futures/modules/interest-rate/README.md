# `modules/interest-rate/` — 利率

> **职责**：覆盖境外 + 境内利率期货（含国债期货）。
> **关键交易所**：CBOT（ZB/ZN/ZF/ZT/ZQ）、CME（SOFR、Eurodollar）、ICE（欧洲国债）、SGX、CFFEX（国债）

---

## 1. 品种清单

### 1.1 境外（CBOT / CME / ICE / Eurex）

| 代码 | 名称 | 交易所 | 备注 |
| --- | --- | --- | --- |
| ZB | 30-Year T-Bond | CBOT |  |
| ZN | 10-Year T-Note | CBOT |  |
| ZF | 5-Year T-Note | CBOT |  |
| ZT | 2-Year T-Note | CBOT |  |
| ZQ | 30-Day Fed Funds | CBOT | ⚠️ 已转 SOFR |
| SR | 1-Month SOFR | CME | 取代 Eurodollar |
| SR3 | 3-Month SOFR | CME |  |
| FGBL | Euro-Bund | Eurex | 德国 10 年 |
| FGBM | Euro-Bobl | Eurex | 德国 5 年 |
| FBTP | Euro-BTP | Eurex | 意大利 10 年 |
| FOAT | Euro-OAT | Eurex | 法国 10 年 |
| FGBX | Euro-Buxl | Eurex | 德国 30 年 |
| G | Long Gilt | ICE | 英国 10 年 |
| JGB | JGB Futures | OSE / SGX | 日本 10 年国债 |
| N | 10-Year Canadian Government Bond | MX | 加拿大 10 年 |

### 1.2 境内（中金所 CFFEX）

| 简称 | 名称 | 交易所 | 备注 |
| --- | --- | --- | --- |
| TS | 2 年期国债期货 | CFFEX |  |
| TF | 5 年期国债期货 | CFFEX |  |
| T | 10 年期国债期货 | CFFEX |  |
| TL | 30 年期国债期货 | CFFEX |  |

---

## 2. 关键概念

### 2.1 Duration（久期）

- 衡量债券价格对利率变化的敏感度
- **Modified Duration** ≈ -(%ΔP / ΔY)，单位：年
- 国债期货价格 ≈ 100 - (CTD yield - 6%) × duration_factor（简化）

### 2.2 DV01 / BPV（Dollar Value of 1 bp）

- 利率变动 1 个基点（0.01%）对应的美元价格变化
- 计算：DV01 ≈ Modified Duration × Price × 0.0001
- 套保时常用 DV01 中性

### 2.3 收益率曲线形态

- **Normal（向上倾斜）**：长期 > 短期，扩张期常见
- **Flat（平坦）**：长短期接近，政策拐点附近
- **Inverted（倒挂）**：短期 > 长期，衰退预警信号

### 2.4 CTD（Cheapest-to-Deliver）

- 国债期货可交割债券中，对空头而言最便宜的一只
- CTD 切换会改变期货与债券的基差关系
- 转换因子（Conversion Factor）决定名义价格调整

### 2.5 抵押贷款利差（MOVE Index）

- ICE BofA MOVE Index：美债隐含波动率（类 VIX 对国债）
- 数值高 → 国债市场预期大幅波动

---

## 3. 关键数据源 / 报告

- **FOMC 议息会议**：每年 8 次，决议 + 点阵图（SEP）+ 鲍威尔新闻发布会
- **ECB Governing Council**：每年约 8 次
- **BOJ Policy Board**：每年 8 次
- **PBoC Monetary Policy Committee**：每月 LPR + 季度货币政策报告
- **美国财政部季度再融资公告（Quarterly Refunding）**：影响国债供给预期

---

## 4. 套保 / 套利

- **DV01 中性套保**：现货债券 vs 期货
- **曲线交易（curve trade）**：买近卖远 / 卖近买远
- **跨交易所套利**：CBOT ZN ↔ Eurex FGBL（10 年美债 vs 10 年德债）
- **CME SOFR ↔ OIS / Fed Funds**：政策利率路径定价

---

## 5. 模块文档模板

参考 [`MODULE_GUIDE.md` §4.1](../../MODULE_GUIDE.md#41-文档模板合约分析通用)。

`cases/<合约代码>/` 推荐章节：

1. `01-事实.md` — 当前收益率曲线、央行政策、MOVE 指数
2. `02-合约规格.md` — CTD 篮子、转换因子、交割方式、最后交易日
3. `03-久期.md` — CTD 久期、DV01、应计利息
4. `04-政策.md` — 央行决议、点阵图、SEP
5. `05-曲线.md` — 跨期限套利
6. `06-分析.md` — 综合观点

---

## 6. 修改记录

| 日期 | 变更 | 备注 |
| --- | --- | --- |
| 2026-09-13 | 初始化 `modules/interest-rate/` README.md | 项目首次创建 |