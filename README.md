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

- 看板：http://127.0.0.1:8000/
- OpenAPI：http://127.0.0.1:8000/docs

## 测试

```powershell
pytest
```
