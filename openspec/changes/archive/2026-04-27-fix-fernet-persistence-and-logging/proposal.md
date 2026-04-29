## Why

Fernet 密钥未持久化导致服务器重启后无法解密已有的 API Key（InvalidToken），Provider 列表接口直接 500。后端无日志系统，排查问题困难。

## What Changes

- Fernet 密钥持久化：自动生成后写入 `data/.fernet_key`，启动时优先读取
- 移植 workflow_develop 的日志系统：JSON 格式 + 按天/大小分块 + 30 天保留

## Capabilities

无新 capability，缺陷修复 + 基础设施。

## Impact

- `backend/services/crypto.py` — 密钥持久化逻辑
- `backend/logging_config.py` — 新建，日志配置
- `backend/pyproject.toml` — 加 `python-json-logger`
- `backend/main.py` — lifespan 调用 `setup_logging()`
