## 1. Fernet 密钥持久化

- [x] 1.1 `backend/services/crypto.py`：生成密钥后写入 `data/.fernet_key`，启动时优先从文件读取

## 2. 日志系统

- [x] 2.1 `backend/logging_config.py`：新建，移植 workflow_develop 的 TimedRotatingFileHandler + JSON + 分块
- [x] 2.2 `backend/pyproject.toml`：加 `python-json-logger` 依赖
- [x] 2.3 `backend/main.py`：lifespan 中调用 `setup_logging()`

## 3. 验证

- [x] 3.1 重启后端后 GET /api/providers 不再报 InvalidToken
- [x] 3.2 `logs/app.log` 正常生成，JSON 格式正确
