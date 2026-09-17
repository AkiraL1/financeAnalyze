# MODULE_GUIDE — 期货交易品种分析项目模块总览

> 本文件是整个项目的**模块边界与职责定义**。任何对模块结构、职责或对外接口的修改，必须同步更新本文件。
> 与 `.cursor/rules/futures-workflow.mdc` §5「信息验证规范」保持完全一致；任何修改必须两边同步。

---

## 1. 项目定位

- **项目名称**：个人期货交易品种分析（Personal Futures Products Analysis Workspace）
- **使用对象**：单一用户（Owner）
- **主市场**：境外（CME Group / CBOT / NYMEX / COMEX / ICE）+ 境内（SHFE / DCE / CZCE / INE / GFEX）
- **覆盖范围**：跨品种期货合约——农产品、能源、金属、股指、利率、外汇、加密衍生品
- **不涉及**：实盘交易执行、券商对接、自动交易系统
- **文档语言**：中文为主，关键合约规格 / 规则 / 数据保留英文原文与中文严谨翻译

---

## 2. 模块结构

项目采用两层结构：**基础层（profile）** + **领域层（modules）**。

```
Futures/
├── MODULE_GUIDE.md                     # 本文件：模块总览（必须最先阅读）
├── README.md                           # 项目使用说明
├── .gitignore
│
├── .cursor/
│   └── rules/
│       └── futures-workflow.mdc        # 项目级硬性规则（必须最先阅读）
│
├── profile/                            # 【基础层】交易档案，跨模块共享的事实来源
│   ├── README.md
│   └── TEMPLATE.md                     # 交易档案模板（待用户填写）
│
└── modules/                            # 【领域层】按品种大类划分的分析模块
    ├── agricultural/                   # 农产品
    ├── energy/                         # 能源
    ├── metals/                         # 金属
    ├── equity-index/                   # 股指
    ├── interest-rate/                  # 利率
    ├── fx/                             # 外汇
    └── crypto/                         # 加密衍生品
```

每个 `modules/<品种>/` 下标准子结构：

```
modules/<品种>/
├── README.md                  # 模块入口：职责边界、品种清单、术语表
├── notes/                     # 合约规格速查、规则要点、季节性规律、研报索引
└── cases/                     # 具体合约分析（按合约代码 / 主题组织）
```

---

## 3. 模块职责定义

### 3.1 `profile/` — 交易档案（基础层）

| 项目 | 内容 |
| --- | --- |
| **职责** | 集中存放与交易相关的**稳定事实**（资金规模、账户类型、风险承受、品种偏好、持仓约束、税务身份等），供各品种模块引用，避免事实重复描述 |
| **写入方** | 用户本人填写 `TEMPLATE.md`；或由 AI 协助整理后由用户确认 |
| **读取方** | 所有 `modules/*` 中的具体合约分析文档（引用式读取，不复制） |
| **公开接口** | `profile/README.md`、`profile/TEMPLATE.md`（用户填写的实例命名为 `trading-profile.md`，**默认不入仓**） |
| **禁止** | 在该目录下存放具体合约分析、实盘持仓、交易记录、券商凭证 |

### 3.2 `modules/agricultural/` — 农产品

| 项目 | 内容 |
| --- | --- |
| **职责** | CBOT 玉米（ZC）、大豆（ZS）、豆粕（ZM）、豆油（ZL）、小麦（ZW）、ICE 棉花、ICE 糖、ICE 咖啡、ICE 可可、ICE 橙汁、DCE 豆一 / 豆二 / 棕榈 / 鸡蛋 / 生猪 / 玉米 / 玉米淀粉 / 豆粕 / 豆油、CZCE 白糖 / 棉花 / 苹果 / 红枣 / 花生 / 菜油 / 菜粕 / 菜籽 |
| **典型场景** | USDA WASDE 月报、播种 / 生长 / 收割季节性、北半球 / 南半球主产国天气、CBOT ↔ DCE 跨市套利、油籽压榨利润（crush margin） |
| **公开接口** | `agricultural/README.md`、`agricultural/notes/`、`agricultural/cases/` |

### 3.3 `modules/energy/` — 能源

| 项目 | 内容 |
| --- | --- |
| **职责** | NYMEX WTI 原油（CL）、Henry Hub 天然气（NG）、RBOB 汽油（RB）、取暖油（HO）、ICE Brent（CO）、ICE Gasoil、SHFE 原油（SC）、INE 低硫燃料油、上期所燃料油、动力煤 |
| **典型场景** | EIA 周度库存、OPEC+ 月度决议、地缘风险溢价、Brent ↔ WTI 价差（Brent-WTI spread）、原油月差结构（contango / backwardation）、炼厂裂解价差（crack spread） |
| **公开接口** | `energy/README.md`、`energy/notes/`、`energy/cases/` |

### 3.4 `modules/metals/` — 金属

| 项目 | 内容 |
| --- | --- |
| **职责** | COMEX 黄金（GC）、白银（SI）、铜（HG）、铝（AL）、LME 镍 / 锌 / 铅 / 锡、SHFE 铜 / 铝 / 锌 / 镍 / 锡 / 螺纹钢 / 热卷 / 不锈钢 / 铁合金 / 黄金 / 白银、DCE 铁矿石 / 焦煤 / 焦炭 / 硅铁 / 锰硅、GFEX 工业硅 / 多晶硅 / 碳酸锂 |
| **典型场景** | 美元指数与实际利率、矿山供给中断、LME ↔ SHFE / COMEX 跨市套利、库存周期、CFTC COT 持仓报告 |
| **公开接口** | `metals/README.md`、`metals/notes/`、`metals/cases/` |

### 3.5 `modules/equity-index/` — 股指

| 项目 | 内容 |
| --- | --- |
| **职责** | CME E-mini S&P 500（ES）、E-mini Nasdaq-100（NQ）、E-mini Dow（YM）、E-mini Russell 2000（RTY）、CME Nikkei 225（NKD）、CME Hang Seng（HSI）、SGX Nifty、SGX 沪深 300（CN）、ICE FTSE 100、ICE Euro Stoxx 50、Eurex DAX、国内 IF / IH / IC / IM |
| **典型场景** | VIX 波动率、股息分红调整（ES fair value gap）、宏观流动性事件、跨时区套利、季月合约 vs 连续月合约、展期收益（roll yield） |
| **公开接口** | `equity-index/README.md`、`equity-index/notes/`、`equity-index/cases/` |

### 3.6 `modules/interest-rate/` — 利率

| 项目 | 内容 |
| --- | --- |
| **职责** | CBOT 30 年长债（ZB）、10 年中债（ZN）、5 年（ZF）、2 年（ZT）、30 天联邦基金（ZQ，已转 SOFR）、SOFR 期货、CME 利率期权、ICE Gilt、Eurex Bund / Bobl / Schatz、国内 T / TF / T |
| **典型场景** | Fed / ECB / PBoC 议息会议、收益率曲线形态（normal / flat / inverted）、duration / DV01 / 凸性（convexity）测算、抵押贷款利差（MOVE 指数） |
| **公开接口** | `interest-rate/README.md`、`interest-rate/notes/`、`interest-rate/cases/` |

### 3.7 `modules/fx/` — 外汇

| 项目 | 内容 |
| --- | --- |
| **职责** | CME 欧元（6E）、日元（6J）、英镑（6B）、瑞郎（6S）、加元（6C）、澳元（6A）、纽元（6N）、墨西哥比索（6M）、南非兰特（6Z）、人民币（CNH / CNY 期货）、ICE 美元指数（DXY 期货） |
| **典型场景** | 利差交易、套息交易（carry trade）、央行政策分化、跨境资金流、避险情绪（risk-on / risk-off） |
| **公开接口** | `fx/README.md`、`fx/notes/`、`fx/cases/` |

### 3.8 `modules/crypto/` — 加密衍生品（可选）

| 项目 | 内容 |
| --- | --- |
| **职责** | CME Bitcoin Futures（BTC）、CME Ether Futures（ETH）、CME Micro Bitcoin / Micro Ether |
| **典型场景** | 现货 ETF 资金流、CME ↔ 现货 / 永续合约价差、监管政策（SEC ETF 决议、CFTC 监管范围）、基差套利 |
| **公开接口** | `crypto/README.md`、`crypto/notes/`、`crypto/cases/` |
| **注意** | 加密衍生品监管框架变化频繁，本模块所有规格 / 规则引用**必须**附核验日期 |

---

## 4. 跨模块约定

### 4.1 文档模板（合约分析通用）

`modules/<品种>/cases/<合约>.md` 推荐结构：

1. **背景事实** — 通过引用 `profile/` 提供事实（资金、风险偏好），避免重复
2. **分析焦点** — 列出待解决的品种问题（季节性 / 政策 / 套利 / 套保）
3. **合约规格与适用规则** — 具体条款 + 链接/出处 + 中英双语 + 核验日期
4. **分析过程** — 基本面 + 技术面 + 政策面 + 季节性 + 跨市 / 跨期
5. **结论与建议** — 明确方向（多 / 空 / 观望）、风险敞口、对冲方案
6. **风险与待办** — 不确定项、后续动作、报告日历、限仓 / 保证金监控

### 4.2 引用规范

- 合约规格引用格式：`《合约名称》, <交易所代码>, <字段>:<值>`，如 `CBOT Corn Futures (ZC), Contract Size: 5,000 bushels`
- 交易所规则引用格式：`《Rulebook Name>, <Exchange>, <Chapter>`，如 `CBOT Rulebook, Chapter 7 - Delivery`
- 监管公告引用格式：`《<机构> <公告类型>》, <编号>, <日期>`，如 `CFTC Commitment of Traders Report, 2026-09-09`
- 跨模块引用使用相对路径：`参见 [交易档案 §3 资金与仓位](../profile/trading-profile.md#3-资金与仓位)`

### 4.3 隐私与本地原则

- 所有事实只保存在**本地仓库**
- 提交时检查是否包含敏感信息（完整账户号、完整持仓、券商凭证等）
- 交易档案实例（`trading-profile.md`）默认加入 `.gitignore`，仅保留模板（`TEMPLATE.md`）提交

### 4.4 文件大小约束

- 新建文件 ≤ 300 行；推荐 ≤ 200 行
- 超大文件应按章节拆分为子文件（如 `cases/CBOT_ZC/01-事实.md`、`02-合约规格.md`、`03-季节性.md`）

---

## 5. 信息验证规范（强制）

> ⚠️ **本节是项目级硬性约束，所有 AI 协作与人类协作均必须遵守**。违反本节即视为产出不可信。

### 5.1 核心原则

- **期货市场信息必须严谨交叉验证** — 任何合约规格、规则、报告数据、历史价格、持仓量、保证金比例、涨跌停板，**不得仅凭模型记忆直接写入文档**
- **默认信息源优先级**：
  1. **官方一手源**：交易所官网公告（CME Group / CBOT / NYMEX / COMEX / ICE / DCE / SHFE / CZCE / INE / GFEX 等）
  2. **监管机构**：CFTC、SEC、CSRC、国务院期货监督管理办公室
  3. **清算所与结算机构**：CME Clearing、SHCH 等
  4. **权威数据提供商**：Bloomberg、Reuters、Wind、Choice、同花顺
  5. **交易所公开行情与公告栏公告**
  6. **券商研报、行业媒体**（仅作为线索，需核验）
- **模型先验 = 假设而非结论** — 模型"记得"的合约规格、规则编号、保证金比例，必须在写入文档前用官方源验证一次

### 5.2 强制工具：ego-browser

- **必须使用** `ego-browser` 技能进行网页交叉验证
- **不适用 ego-browser 的例外**：纯本地文档整理 / 引用既有文档内容
- **触发场景**（任一即必须使用）：
  - 引用某合约**具体规格**（代码、合约乘数、最小变动价位、保证金、交割方式、交割品级）
  - 引用某**交易所规则编号、年份、章节**（如 CBOT Rulebook 章节）
  - 引用某**监管公告**（CFTC 持仓报告 COT、SHFE 风险控制公告、CSRC 监管通知）
  - 引用某**历史价格数据、持仓量、成交量**（必须有数据源 URL + 核验日期）
  - 引用某**保证金比例、涨跌停板、限仓规则**
  - 引用某**宏观经济数据**（USDA 报告、OPEC 决议、EIA 库存、BLS 非农、CPI 等）
  - 用户提出"帮我查一下 …" / "这个条款现在还生效吗" 等明确检索需求
- **使用流程**：
  1. **观察**：`snapshotText()` 获取可访问性树
  2. **执行**：必要时 `click` / `fillInput` / `cdp`
  3. **再次观察**：每次操作后重新 `snapshotText()` 或 `captureScreenshot()` 确认
  4. **记录**：将验证过的关键事实连同**官方源 URL** 写入文档
- **heredoc 调用方式**：

  ```bash
  ego-browser nodejs <<'EOF'
  const task = await useOrCreateTaskSpace('verify ZC corn contract specs')
  await openOrReuseTab('https://www.cmegroup.com/markets/agriculture/grains-and-oilseeds/corn.contractSpecs.html', { wait: true })
  cliLog(await snapshotText())
  EOF
  ```

### 5.3 文档中的强制标注

在 `cases/`、`notes/` 或任何分析文档中引用合约规格 / 规则 / 数据时，**必须同时**：

1. 给出**精确引用**（如 `ZC contract size 5,000 bushels`）
2. 给出**官方源 URL**（CME Group / Exchange / USDA / CFTC / SHFE 等）
3. 标注**最后核验日期**（如 `🗓 最后核验：2026-09-13 via CME Group Website`）
4. 标注**核验方式**（如 `✅ ego-browser 核验` / `🟡 仅引用既有文档，未重新核验`）

**反例**（禁止出现）：

> ❌ "玉米期货合约乘数是 5000 蒲式耳，最小变动 0.25 美分。"（无章节、无 URL、无核验日期）

**正例**（必须照此写）：

> ✅ "CBOT Corn Futures (ZC), Contract Size: **5,000 bushels**, Tick Size: **1/4 cent per bushel ($12.50)**（来源：<https://www.cmegroup.com/markets/agriculture/grains-and-oilseeds/corn.contractSpecs.html>）。🗓 最后核验：2026-09-13 via ego-browser + CME Group Website。"

### 5.4 时效性管理

- 合约规格可能修订 → 引用时**附核验日期**
- 保证金比例、涨跌停板随行情调整 → 引用时**写明生效日期**
- USDA、EIA、OPEC 等月报 / 年报数据 → 必须标注**报告期**
- 监管政策（SEC ETF 决议、CSRC 限仓调整）变化频繁 → **必须重新核验**
- 用户在建仓 / 平仓 / 交割 / 合规等关键事项上做决定前 → **必须重新核验**一次当前规则

### 5.5 已知不可验证情形

若 ego-browser 无法访问目标源（如登录墙、付费墙、地区限制），AI 应：

1. **不**继续凭记忆编造
2. **明确告知用户**："该项信息源当前无法验证，建议人工核对 [官方源链接]"
3. 在文档中标注 `🟠 无法自动核验 — 待人工确认`

### 5.6 与项目级 Cursor 规则的关系

本节与 `.cursor/rules/futures-workflow.mdc` 中的"信息验证规范"段落**保持一致并互相引用**。两边任一处修改，必须同步另一边。

### 5.7 中英双语要求（强制）

> 本节是对 §5.3「文档中的强制标注」的补充，专门规定**语言呈现方式**。

#### 5.7.1 适用范围

本要求适用于 `modules/<品种>/cases/`、`modules/<品种>/notes/`、`profile/` 下任何分析文档中**出现以下内容**的场合：

- 合约规格字段（英文原称）+ 中文严谨翻译
- 交易所规则条款（英文原文）+ 中文严谨翻译
- 监管 / 数据报告标题（英文原称）+ 中文严谨翻译
- 官方术语（initial margin / first notice day 等）+ 中文严谨翻译
- 程序步骤、时限、字段名（英文原文）+ 中文严谨翻译
- 交易所 / 监管机构名称（英文原称 + 中文通用译名）

#### 5.7.2 双语呈现格式（强制）

**A. 合约规格 / 字段**

格式：

```
英文原文：<Contract Size: 5,000 bushels; Tick Size: 1/4 cent per bushel ($12.50)>
中文严谨翻译：合约单位：5,000 蒲式耳；最小变动价位：每蒲式耳 1/4 美分（$12.50）
```

**反例**（禁止）：

> ❌ "玉米期货合约乘数是 5000 蒲式耳，最小变动 0.25 美分。"

**正例**（必须照此写）：

> ✅ "Contract Size: **5,000 bushels**; Tick Size: **1/4 cent per bushel ($12.50)**"
> 中文严谨翻译：合约单位：**5,000 蒲式耳 / bushels**；最小变动价位：每蒲式耳 **1/4 美分 / cent（$12.50）**。

**B. 监管公告 / 政策**

格式：

```
英文原文：<CFTC Commitment of Traders Report (COT), as of September 9, 2026>
中文严谨翻译：CFTC 交易者持仓报告（Commitment of Traders Report, COT），截至 2026 年 9 月 9 日
```

**C. 交易所术语**

格式：

```
英文原称：<Initial Margin>
中文严谨翻译：初始保证金（Initial Margin）
首次出现后可在同文档内缩写为：Initial Margin / 初始保证金
```

**D. 程序 / 时限 / 字段名**

格式：

```
英文原文：submit delivery application through CME ClearPort
中文严谨翻译：通过 CME ClearPort（CME 清算门户系统）提交交割申请
```

#### 5.7.3 重点术语保留英文的规则

下列术语**首次出现时**必须采用 `中文译名 / English Term` 格式并**附中文释义括注**；后续出现可仅用中文译名：

- contract size（合约单位 / 合约乘数）、tick size（最小变动价位）、daily price limit（涨跌停板）、position limit（持仓限额）
- initial margin（初始保证金）、maintenance margin（维持保证金）、variation margin（变动保证金）
- physical delivery（实物交割）、cash settlement（现金交割）、first notice day（第一通知日，FND）、last trade day（最后交易日，LTD）、last notice day（最后通知日，LND）
- open interest（持仓量）、volume（成交量）、settlement price（结算价）
- contango（期货升水）、backwardation（期货贴水）、basis（基差）
- long position（多头 / 多仓）、short position（空头 / 空仓）、hedging（套保）、speculation（投机）、arbitrage（套利）
- Commitment of Traders（交易者持仓报告，COT）、disaggregated COT（分类持仓报告）
- fair value（理论价）、fair value gap（理论价差）
- crack spread（裂解价差）、crush margin（压榨利润）

完整清单随 `notes/` 积累动态扩展。

#### 5.7.4 翻译质量要求

- **严谨优先**：期货语境下中文翻译必须符合对应交易所惯例；歧义处保留英文原文
- **不增不减**：不得省略原文中 "must"、"shall"、"may" 等情态动词的关键含义
- **不创造**：不得凭模型记忆补全未在原文中出现的内容
- **核验过的原文优先**：凡 ego-browser 已核验过的合约规格 / 规则原文，应**优先采用核验版**而非凭记忆复述

#### 5.7.5 已知例外

- **纯本地整理 / 流程性清单**（如 `priority-checklist.md`）：可不强制双语，但首次出现英文专有名词仍需括注
- **代码 / 配置文件 / 命令**：不属于本要求范围
- **表格中已脱敏的数据字段**（如 "Account: XXX-XXXX"）：不强制双语

#### 5.7.6 与项目级 Cursor 规则的关系

本子节与 `.cursor/rules/futures-workflow.mdc` §6「中英双语要求」**保持完全一致并互相引用**。两边任一处修改，必须同步另一边。

---

### 5.8 ego-browser 任务空间管理（强制）

> 本节是对 §5.2「强制工具：ego-browser」的**配套流程规则**。规则来源：[ego-browser SKILL.md「Task spaces」节](../../.cursor/skills/ego-browser/SKILL.md)。

#### 5.8.1 核心原则

- **每个 ego-browser task space 都必须被显式关闭**，**不得**让任务空间随会话遗留
- 一次"用户目标"对应一个 task space；同一目标的所有 heredoc 轮次复用同一 task space
- 当目标已完成（无论是成功、失败还是放弃），**立即**在最后一个 heredoc 中调用 `completeTaskSpace(name, { keep })` 关闭
- 默认 `{ keep: false }`；仅在**用户明确要求保留页面** / **需要用户在该页面手动操作**（如登录 Bloomberg Terminal） / **结果无法以 URL / 文件 / 摘要形式交付** 时才使用 `{ keep: true }`

#### 5.8.2 使用流程（强制 7 步）

| 步骤 | 调用 | 说明 |
| --- | --- | --- |
| 1 | `useOrCreateTaskSpace('<短名>')` | 命名应反映任务意图，例：`verify ZC corn contract specs` |
| 2 | `cliLog('task space id: ' + task.id)` | 把 `task.id` 用于后续轮次复用，**避免名称冲突** |
| 3 | `openOrReuseTab(url, { wait: true })` | 同一目标后续页面切换复用同一 tab |
| 4 | `snapshotText()` / `js()` / `cdp()` 等 | 观察 → 操作 → 再次观察（按 SKILL.md "Recommended workflow"） |
| 5 | **每个 heredoc 开头**：`useOrCreateTaskSpace(nameOrId)` | 跨轮次保留同一 task space |
| 6 | **目标完成时**：`completeTaskSpace(nameOrId, { keep: false })` | 关闭 task space；保留结果以 `cliLog` 输出 |
| 7 | 关闭时若结果 `{ done: false, skipped: ... }` | 立即重试或向用户报告，**不得**假装完成 |

#### 5.8.3 触发关闭的具体场景

- ✅ **应关闭**：核验全部完成并写入文档 / 数据已核验并写入 notes / 检索失败并标注"无法自动核验" / 用户明示放弃任务
- 🟢 **可保留 `{ keep: true }`**：用户明确说"保留这个页面" / 用户需要在该页面手动操作（例：登录 Bloomberg Terminal、点击 WSC 协议）
- ❌ **不应保留**：仅因"访问过" / "创建了文档" / "用了一次截图" 就保留页面

#### 5.8.4 跨轮次复用的硬性规则

- 同一用户目标的**所有后续 heredoc** 必须在开头调用：

  ```js
  const task = await useOrCreateTaskSpace('<目标短名>')
  ```

  **不得**为同一目标创建新 task space
- 仅在以下情况才创建**新** task space：
  - 用户开始**新目标**（与旧目标无关）
  - 用户明确要求开新空间
  - 原 task space 不可用且用户已确认
- 创建新 task space 时必须**说明原因**

#### 5.8.5 与项目级 Cursor 规则的关系

本子节与 `.cursor/rules/futures-workflow.mdc` §4.6「ego-browser 任务空间管理」**保持完全一致并互相引用**。两边任一处修改，必须同步另一边。

---

## 6. 变更记录

| 日期 | 变更 | 备注 |
| --- | --- | --- |
| 2026-09-13 | 项目初始化：建立 `profile/` + 7 个品种模块（agricultural / energy / metals / equity-index / interest-rate / fx / crypto） + `futures-workflow.mdc` + `MODULE_GUIDE.md §5` 双镜像规范；同步建立 `.gitignore` 与 README；由 `law/.cursor/rules/legal-workflow.mdc` 迁移而来 | 由 Owner 明确要求 |

> 任何模块结构、职责或公开接口变更，必须同步更新本节。