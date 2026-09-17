# 模块指南

本仓库是金融分析台。[AkiraL1/Futures](https://github.com/AkiraL1/Futures) **只提供分析模式**（六段报告、品种透镜、核验纪律），不在运行时当知识库读取。[AkiraL1/digital-oracle](https://github.com/AkiraL1/digital-oracle) 提供市场价格信号。

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

按 Futures 模式填报告，用 oracle 填数据。不编造合约规格，不摘录 Futures 文档。

| 文件 | 职责 |
|------|------|
| `report.py` | 六段报告填充 |
| `pipeline.py` | `build_briefing` |
| `board.py` | 总览 / 观察池 |
| `intel.py` | 模式焦点 + oracle 资讯 |
| `review.py` | 每日简报 |
| `notes.py` / `formatters.py` | 备注与文本 |

## `apps.api` / `apps.web`

工作台：总览、关注品种、品种诊断、市场资讯、每日简报、分析模式、报告模板。
