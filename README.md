# financeAnalyze — 金融分析台

- **分析模式**参考 [AkiraL1/Futures](https://github.com/AkiraL1/Futures)：六段报告、品种透镜、规格必须核验。**不把该仓库当作知识库摘录。**
- **分析正文**默认由 MiniMax（`MiniMax-M3`，中国区 `https://api.minimaxi.com/v1`）生成；失败回退模板。
- **市场信号**来自 [AkiraL1/digital-oracle](https://github.com/AkiraL1/digital-oracle)。

本台**不生成**未核验的合约乘数、保证金、涨跌停。

详见 [MODULE_GUIDE.md](MODULE_GUIDE.md)。

## 安装

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -e ".[dev]"
Copy-Item .env.example .env
```

在 `.env` 填写 `MINIMAX_API_KEY`（Token Plan，`sk-cp-` 前缀）。**不要把 `.env` 提交到 Git。**

## CLI

```powershell
python -m finance_analyze.main catalog
python -m finance_analyze.main desk --code GC
python -m finance_analyze.main desk --code CL --oracle
python -m finance_analyze.main desk --code GC --no-llm
```

未加 `--no-llm` 且已配置密钥时，desk 会调用 MiniMax。

## 分析台

```powershell
uvicorn apps.api.main:app --reload
```

http://127.0.0.1:8000/

实时 Yahoo 价格：`pip install -e ".[oracle]"`。

品种诊断页默认勾选「MiniMax 分析」。每日简报只用模板，不调用模型。

## 测试

```powershell
pytest
```
