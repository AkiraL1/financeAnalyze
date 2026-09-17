# 模块指南

本仓库是金融分析台。[AkiraL1/Futures](https://github.com/AkiraL1/Futures) **只提供分析模式**（六段报告、品种透镜、核验纪律），不在运行时当知识库读取。[AkiraL1/digital-oracle](https://github.com/AkiraL1/digital-oracle) 提供市场价格信号。分析正文默认由 MiniMax（`MiniMax-M3`）按六段 JSON 填写。

## `catalog`

分析模式注册表与观察品种（工作台自己维护）。不解析 Futures README / cases。

| 文件 | 职责 |
|------|------|
| `models.py` | `Instrument`、`AnalysisMode`、`Catalog` |
| `template.py` | 六段报告结构 |
| `registry.py` | 七种透镜 + 观察池 |
| `oracle_map.py` | 品种代码 → digital-oracle 路由 |

公开接口：`load_catalog()`、`resolve_route(code)`、`REPORT_SECTIONS`。

## `oracle`

digital-oracle 适配层。不写分析模式。

| 文件 | 职责 |
|------|------|
| `models.py` | `OracleSnapshot` |
| `gateway.py` | 并行拉取、部分失败容忍 |
| `serialize.py` | provider 结果转 JSON |
| `live.py` | 按路由组装真实 provider |
| `intel.py` | 资讯用的宏观信号抓取 |

公开接口：`OracleGateway.snapshot(product)`、`build_live_fetchers(product)`、`intel_gateway()`。

## `desk`

按 Futures 模式填报告：MiniMax 先 `plan_tasks` 拆解，再循环调用 `get_oracle` / `ego_browser` / `run_task`，最后 `submit_report`。无密钥或循环失败回退模板。不编造合约规格。每日简报不调用模型。

| 文件 | 职责 |
|------|------|
| `report.py` | 六段模板填充 |
| `analyst.py` | 无工具客户端时的六段 JSON 回退 |
| `llm.py` | MiniMax Chat Completions（含 tool_calls） |
| `agent/` | 任务板、循环、白名单浏览器快照 |
| `pipeline.py` | `build_briefing` |
| `board.py` | 总览 / 观察池 |
| `intel.py` | 模式焦点 + oracle 资讯 |
| `review.py` | 每日简报（模板，不调 LLM） |
| `notes.py` / `formatters.py` | 备注与文本 |

公开接口：`build_briefing(..., include_llm=)`、`llm_status()`、`fill_report_with_agent()`。

### `desk.agent`

参考公开的 Agent 循环（模型 → 工具 → 结果 → 再决策），不是复制任何闭源实现。

| 文件 | 职责 |
|------|------|
| `loop.py` | `run_loop` / `supports_tools` |
| `tasks.py` | 任务拆解板 |
| `browser.py` | `ego_browser` CLI 或 HTTP 语义快照（域名白名单） |
| `schemas.py` | MiniMax function tools |
| `session.py` | 工具执行与子任务循环 |
| `run.py` | 协调员入口 `fill_report_with_agent` |

## `finance_analyze`

启动配置与 CLI。`.env` 只在本机读取，不入库。

| 文件 | 职责 |
|------|------|
| `settings.py` | `MINIMAX_API_KEY` / `MINIMAX_BASE_URL` / `MINIMAX_MODEL` |
| `main.py` | `catalog` / `desk --llm` CLI |
| `paths.py` | 仓库根路径 |

公开接口：`minimax_settings()`。

## `apps.api` / `apps.web`

工作台：总览、关注品种、品种诊断（MiniMax 开关）、市场资讯、每日简报、分析模式、报告模板。
`GET /health` 返回 MiniMax 是否已配置（不含密钥）。
`GET /api/desk/{code}?llm=true` 默认启用模型分析。
