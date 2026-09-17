# financeAnalyze — 金融分析台

- **分析模式**参考 [AkiraL1/Futures](https://github.com/AkiraL1/Futures)：六段报告、品种透镜、规格必须核验。**不把该仓库当作知识库摘录。**
- **市场信号**来自 [AkiraL1/digital-oracle](https://github.com/AkiraL1/digital-oracle)。

本台**不生成**未核验的合约乘数、保证金、涨跌停。

详见 [MODULE_GUIDE.md](MODULE_GUIDE.md)。

## 安装

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -e ".[dev]"
```

## CLI

```powershell
python -m finance_analyze.main catalog
python -m finance_analyze.main desk --code GC
python -m finance_analyze.main desk --code CL --oracle
```

## 分析台

```powershell
uvicorn apps.api.main:app --reload
```

http://127.0.0.1:8000/

实时 Yahoo 价格：`pip install -e ".[oracle]"`。

## 测试

```powershell
pytest
```
