# 模块指南

本仓库是金融分析台。品种知识来自 [AkiraL1/Futures](https://github.com/AkiraL1/Futures)，市场价格信号来自 [AkiraL1/digital-oracle](https://github.com/AkiraL1/digital-oracle)。修改前先定目标模块。

## `catalog`

读取 Futures 知识库，不计算行情。

| 文件 | 职责 |
|------|------|
| `models.py` | `Product`、`SectorInfo`、`CaseDoc`、`Catalog` |
| `parse.py` | 从模块 README 表格解析品种 |
| `loader.py` | 扫描 `third_party/futures/modules` |
| `oracle_map.py` | 品种代码 → digital-oracle 查询路由 |

公开接口：`load_catalog(root=...)`、`resolve_route(code)`。

## `oracle`

digital-oracle 适配层。不写品种知识。

| 文件 | 职责 |
|------|------|
| `models.py` | `OracleSnapshot` |
| `gateway.py` | 并行拉取、部分失败容忍 |
| `serialize.py` | provider 结果转 JSON |
| `live.py` | 按路由组装真实 provider |

公开接口：`OracleGateway.snapshot(product)`、`build_live_fetchers(product)`。

## `desk`

把知识库与市场信号合成一份分析台简报。不编造合约规格。

| 文件 | 职责 |
|------|------|
| `models.py` | `DeskBriefing` |
| `notes.py` | 启发式备注（明确标注未核验） |
| `pipeline.py` | `build_briefing(code, include_oracle=...)` |
| `formatters.py` | CLI 纯文本 |

公开接口：`build_briefing`。

## `finance_analyze`

| 文件 | 职责 |
|------|------|
| `paths.py` | 仓库根、Futures 根、oracle 包路径 |
| `main.py` | `catalog` / `desk` 子命令 |

## `apps.api` / `apps.web`

FastAPI 分析台与静态页。路由只编排 `catalog` 与 `desk`，不写指标公式。
