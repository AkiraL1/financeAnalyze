# Futures — 个人期货品种分析项目

> **项目定位**：单一用户的期货合约品种（基本面 / 技术面 / 政策面）分析知识库
> **主市场**：境外（CME Group / CBOT / NYMEX / COMEX / ICE 等）+ 国内（SHFE / DCE / CZCE / INE / GFEX）
> **文档语言**：中文为主，关键合约规格 / 规则 / 数据保留英文原文与中文严谨翻译
> **不涉及**：实盘交易执行、券商对接、自动交易系统

---

## 0. 阅读顺序（首次进入项目必读）

1. [`MODULE_GUIDE.md`](MODULE_GUIDE.md) — 项目模块总览、职责边界、信息验证规范
2. [`.cursor/rules/futures-workflow.mdc`](.cursor/rules/futures-workflow.mdc) — 项目级硬性规则（强制）
3. [`profile/TEMPLATE.md`](profile/TEMPLATE.md) — 交易档案模板（先填这份）
4. 各品种模块的 `README.md`（按需进入）

---

## 1. 目录结构

```
Futures/
├── MODULE_GUIDE.md                     # 模块总览（最先阅读）
├── README.md                           # 本文件
├── .gitignore
│
├── .cursor/
│   └── rules/
│       └── futures-workflow.mdc        # 项目级硬性规则
│
├── profile/                            # 【基础层】交易档案
│   ├── README.md
│   └── TEMPLATE.md                     # 资金、风险偏好、品种偏好模板
│
└── modules/                            # 【领域层】按品种大类划分
    ├── agricultural/                   # 农产品
    ├── energy/                         # 能源
    ├── metals/                         # 金属
    ├── equity-index/                   # 股指
    ├── interest-rate/                  # 利率
    ├── fx/                             # 外汇
    └── crypto/                         # 加密衍生品
```

每个 `modules/<品种>/` 标准子结构：

```
modules/<品种>/
├── README.md                  # 模块入口：品种清单、关键交易所、术语表
├── notes/                     # 合约规格速查、规则要点、季节性规律、研报索引
└── cases/                     # 具体合约分析（按合约代码 / 主题组织）
```

---

## 2. ego-browser 交叉验证速查

> 任何合约规格 / 规则 / 数据 / 报告引用，**必须**通过 `ego-browser` 核验后写入。
> 详细规则见 [`MODULE_GUIDE.md` §5](MODULE_GUIDE.md#5-信息验证规范强制) 与 [`.cursor/rules/futures-workflow.mdc` §4](.cursor/rules/futures-workflow.mdc)。

### 2.1 调用骨架

```bash
ego-browser nodejs <<'EOF'
const task = await useOrCreateTaskSpace('verify ZC corn contract specs')
cliLog('task space id: ' + task.id)

await openOrReuseTab(
  'https://www.cmegroup.com/markets/agriculture/grains-and-oilseeds/corn.contractSpecs.html',
  { wait: true }
)

cliLog(await snapshotText())
EOF
```

### 2.2 关键约束

- ✅ `cliLog(value)` 是 heredoc 内**唯一**输出机制
- ✅ 跨轮次复用：`useOrCreateTaskSpace(nameOrId)` + `task.id`
- ✅ 完成时**独立** heredoc 关闭：`completeTaskSpace(name, { keep: false })`
- ❌ 不要把 heredoc（Node.js）与 `js(...)`（浏览器）混着写
- ❌ 不要把 `@N` ref 当 `document.querySelector` 选择器用
- ⚠️ `wait` / `timeout` 是**秒**；`XxxMs` 才是毫秒

---

## 3. 重点术语对照速查（持续扩展）

| 中文 | English Term | 备注 |
|---|---|---|
| 合约单位 / 合约乘数 | Contract Size / Contract Unit | 每张合约代表的标的数量 |
| 最小变动价位 | Tick Size | 最小报价单位 |
| 最小变动值 | Tick Value | 每跳最小变动对应的金额 |
| 涨跌停板 | Daily Price Limit | 单日最大波动幅度 |
| 持仓限额 | Position Limit | 单账户最大持仓 |
| 初始保证金 | Initial Margin | 开仓所需保证金 |
| 维持保证金 | Maintenance Margin | 持仓期间最低保证金 |
| 变动保证金 | Variation Margin | 每日盯市追加的保证金 |
| 第一通知日 | First Notice Day (FND) | 卖方可发出交割通知的第一天 |
| 最后通知日 | Last Notice Day (LND) | 卖方可发出交割通知的最后一天 |
| 最后交易日 | Last Trade Day (LTD) | 合约可交易的最后一天 |
| 实物交割 | Physical Delivery | 以标的物交收 |
| 现金交割 | Cash Settlement | 以现金结算差价 |
| 持仓量 | Open Interest | 未平仓合约总数 |
| 结算价 | Settlement Price | 每日收盘结算价 |
| 期货升水 | Contango | 远月价格高于近月 |
| 期货贴水 | Backwardation | 远月价格低于近月 |
| 基差 | Basis | 现货价格 − 期货价格 |
| 多头 / 多仓 | Long Position | 买入头寸 |
| 空头 / 空仓 | Short Position | 卖出头寸 |
| 套保 | Hedging | 风险对冲 |
| 投机 | Speculation | 承担风险博取收益 |
| 套利 | Arbitrage | 跨市场 / 跨期 / 跨品种 |
| 交易者持仓报告 | Commitment of Traders (COT) | CFTC 周度报告 |
| 分类持仓报告 | Disaggregated COT | COT 细分类版本 |
| 理论价 | Fair Value | 期货相对现货的理论价格 |
| 理论价差 | Fair Value Gap | 期货与现货指数之间的理论差 |

完整术语表随 `notes/glossary.md`（建议建于根目录或 `modules/README.md`）动态扩展。

---

## 4. 关键交易所速查

### 境外

| 代码 | 名称 | 覆盖品种 |
|---|---|---|
| CME | Chicago Mercantile Exchange | 利率、外汇、股指、农产品部分 |
| CBOT | Chicago Board of Trade | 农产品（玉米、小麦、大豆、豆粕、豆油等）、利率 |
| NYMEX | New York Mercantile Exchange | 能源（WTI、Henry Hub NG、RBOB、HO）、金属部分 |
| COMEX | Commodities Exchange | 金属（GC 黄金、SI 白银、HG 铜） |
| ICE | Intercontinental Exchange | 软商品（糖、棉、咖啡、可可、橙汁）、Brent、外汇 GLOBEX 部分 |

### 境内

| 代码 | 名称 | 覆盖品种 |
|---|---|---|
| SHFE | 上海期货交易所 | 铜、铝、锌、镍、锡、螺纹钢、热卷、黄金、白银、原油（SC）等 |
| DCE | 大连商品交易所 | 豆一、豆二、豆粕、豆油、棕榈油、玉米、玉米淀粉、鸡蛋、生猪、铁矿石、焦煤、焦炭、聚乙烯、聚丙烯、PVC 等 |
| CZCE | 郑州商品交易所 | 白糖、棉花、棉纱、苹果、红枣、花生、菜籽、菜油、菜粕、PTA、甲醇、尿素、玻璃、纯碱、硅铁、锰硅等 |
| INE | 上海国际能源交易中心 | 原油（SC）、低硫燃料油、国际铜、20 号胶、集运指数（欧线）等 |
| GFEX | 广州期货交易所 | 工业硅、多晶硅、碳酸锂、铂、钯等 |

---

## 5. 关键监管 / 数据源速查

| 缩写 | 全称 | 用途 |
|---|---|---|
| CFTC | Commodity Futures Trading Commission | 美国期货监管；COT 周度持仓报告 |
| SEC | U.S. Securities and Exchange Commission | 美国证券监管 |
| CSRC | China Securities Regulatory Commission | 中国证监会 |
| USDA | U.S. Department of Agriculture | 农产品 WASDE 报告、作物进度报告 |
| EIA | U.S. Energy Information Administration | 原油 / 天然气周度库存 |
| OPEC | Organization of the Petroleum Exporting Countries | 原油产量决议 |
| BLS | U.S. Bureau of Labor Statistics | 非农就业、CPI、PPI |
| Fed | Federal Reserve | 联邦基金利率决议、议息会议纪要 |
| ECB | European Central Bank | 欧元区利率决议 |
| PBoC | People's Bank of China | 中国央行利率决议 |

---

## 6. 修改记录

| 日期 | 变更 | 备注 |
|---|---|---|
| 2026-09-13 | 项目初始化：建立 `profile/` + 7 个品种模块 + 信息验证规范 | 由 Owner 明确要求；从 `law/` 项目规范迁移而来 |