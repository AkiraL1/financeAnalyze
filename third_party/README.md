# 第三方来源

本分析台**不复制**两库的业务逻辑，运行时读取 / 调用：

| 目录 | 上游 | 用途 |
|------|------|------|
| `third_party/futures/` | https://github.com/AkiraL1/Futures | 品种知识库：模块 README、cases、profile 模板 |
| `third_party/digital-oracle/` | https://github.com/AkiraL1/digital-oracle | 市场价格 / 预测市场 / COT 等 provider |

更新方式：重新 clone 对应仓库到上述目录（不要带嵌套 `.git`）。
