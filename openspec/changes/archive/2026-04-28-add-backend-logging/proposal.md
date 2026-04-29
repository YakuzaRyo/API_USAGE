## Why

后端日志基础设施（`logging_config.py` + `main.py` 调用 `setup_logging()`）已就位，但路由层和调度层完全没有日志调用。当前仅 `collector.py` 在异常时写了两条 error 日志，所有 CRUD 操作、API 测试、定时任务调度均无声运行，排障时无法追踪请求轨迹。

## What Changes

- 在 `routers/providers.py` 的每个端点添加 `logger.info()` / `logger.warning()` 调用，记录厂商创建、更新、删除、API 测试、手动采集事件
- 在 `routers/stats.py` 的查询端点添加简要日志
- 在 `services/scheduler.py` 添加定时任务注册、移除、重新调度的日志
- 补充 `services/collector.py` 采集成功时的 info 日志（当前仅记录异常）
- 所有日志使用 `logging.getLogger("backend.<module>")` 命名空间，与现有日志配置兼容

## Capabilities

### New Capabilities
- `backend-logging`: Structured operational logging for backend routers and services, covering CRUD events, scheduled jobs, and API test requests

### Modified Capabilities
<!-- 无现有能力被修改 -->

## Impact

- [routers/providers.py](backend/routers/providers.py) — 添加 ~10 处 logger 调用
- [routers/stats.py](backend/routers/stats.py) — 添加 ~3 处 logger 调用
- [services/scheduler.py](backend/services/scheduler.py) — 添加 ~5 处 logger 调用
- [services/collector.py](backend/services/collector.py) — 补充成功路径的 info 日志
- 无新增依赖（使用 Python 标准库 `logging`）
- 日志写入路径 `logs/app.log`，与现有 `logging_config.py` 一致
