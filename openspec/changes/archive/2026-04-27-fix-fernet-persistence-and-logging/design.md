## Context

两个基础设施缺陷修复。

## Decisions

### D1: Fernet 密钥持久化策略

存储位置：`data/.fernet_key`（与 `data/app.db` 同目录）。

启动流程：
1. 检查 `settings.SECRET_KEY`，非空则使用
2. 检查 `data/.fernet_key`，存在则读取
3. 以上都不存在 → 生成新密钥 → 写入 `data/.fernet_key`

### D2: 日志配置

移植 workflow_develop 的 `logging_config.py`，支持：
- TimedRotatingFileHandler：按天切分 + 10MB 大小分块
- 双输出：JSON 文件 + 控制台
- 30 天保留
- uvicorn/sqlalchemy 日志静默
