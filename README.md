# financeAnalyze — 金融分析台

把两个仓库接到同一张台上：

- **品种知识**：[AkiraL1/Futures](https://github.com/AkiraL1/Futures)（农产品 / 能源 / 金属 / 股指 / 利率 / 外汇 / 加密）
- **市场价格信号**：[AkiraL1/digital-oracle](https://github.com/AkiraL1/digital-oracle)（价格、CFTC COT、美债曲线、Fear & Greed、Polymarket 等）

本台**不生成**未核验的合约乘数、保证金、涨跌停。规格以 Futures 知识库和交易所官网为准。

详见 [MODULE_GUIDE.md](MODULE_GUIDE.md)。

## 安装

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -e ".[dev]"
```

Linux / macOS：

```bash
python -m venv .venv
source .venv/bin/activate
pip install -e ".[dev]"
```

## CLI

```powershell
python -m finance_analyze.main catalog
python -m finance_analyze.main desk --code GC
python -m finance_analyze.main desk --code CL --oracle
```

`--oracle` 会访问 digital-oracle 的公开数据源（无需 API Key，需要网络）。

## 分析台

```powershell
uvicorn apps.api.main:app --reload
```

看板在 http://127.0.0.1:8000/ ，界面按个人理财工作台的信息架构组织：

- 工作台总览
- 关注品种（默认观察池，**不是**实盘持仓）
- 品种诊断
- 市场资讯
- 每日简报（可复制 / 下载 Markdown）
- 标的研究
- 研究摘录

实时 Yahoo 价格需要可选依赖 `yfinance`（`pip install -e ".[oracle]"`）。其它 digital-oracle 信号仍可在「市场资讯 → 抓取」或诊断页勾选后拉取。

## 测试

```powershell
pytest
```
