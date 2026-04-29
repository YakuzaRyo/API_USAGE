## Context

后端已有完整的日志基础设施：`logging_config.py` 配置了 JSON 格式文件日志（按天/大小 rotate）+ 控制台输出，`main.py` 在 lifespan 启动时调用 `setup_logging()`。所有 logger 使用 `"backend.*"` 命名空间。

当前实际产生日志的代码只有 `services/collector.py` 中两处 `logger.error()`（仅异常时）。`routers/providers.py`、`routers/stats.py`、`services/scheduler.py` 完全无日志。

## Goals / Non-Goals

**Goals:**
- 为每个 API 端点和关键服务操作添加结构化日志
- 覆盖 CRUD 事件、API 测试、定时任务、采集成功/失败
- 使用现有 `logging.getLogger("backend.<module>")` 模式，零配置变更

**Non-Goals:**
- 不添加请求/响应体全文 logging（避免泄露 API Key）
- 不引入分布式追踪或 OpenTelemetry
- 不修改日志基础配置（轮转、格式、级别）
- 不添加数据库持久化的审计日志
- 不添加 FastAPI middleware 自动请求日志（uvicorn.access 已存在）

## Decisions

### 1. Logger 命名约定

沿用现有模式：`logging.getLogger("backend.<module>")`

| 文件 | Logger name |
|------|-------------|
| `routers/providers.py` | `backend.routers.providers` |
| `routers/stats.py` | `backend.routers.stats` |
| `services/scheduler.py` | `backend.services.scheduler` |
| `services/collector.py` | `backend.services.collector`（已存在） |

### 2. 日志级别策略

| 级别 | 使用场景 |
|------|---------|
| `info` | 正常操作完成：创建/更新/删除厂商、采集成功、定时任务注册、测试 API |
| `warning` | 非致命问题：厂商未找到（404）、采集返回空数据 |
| `error` | 异常和失败：采集异常、API 调用失败（collector 已有此用法） |

### 3. 日志内容策略

每条日志包含：
- 操作描述（动词 + 对象，如 `Provider created id=3`）
- 关键标识字段（`provider_id`, `name` 等）
- 不记录明文 API Key（仅记录 provider_id 或 name 即可定位）
- 不记录完整请求/响应体

```python
# providers.py
logger = logging.getLogger("backend.routers.providers")
logger.info("Provider created | provider_id=%s name=%s", provider.id, provider.name)
logger.info("Provider deleted | provider_id=%s", provider_id)
logger.warning("Provider not found | provider_id=%s", provider_id)

# scheduler.py
logger.info("Job registered | provider_id=%s interval=%s", provider_id, interval_seconds)
logger.info("Job removed | provider_id=%s", provider_id)

# collector.py (补充)
logger.info("Collection succeeded | provider_id=%s record_count=%s", provider.id, record_count)
logger.info("Balance collection succeeded | provider_id=%s balance=%s", provider.id, balance)
```

### 4. 格式化方式

使用 `%s` 占位符而非 f-string，让 logging 框架延迟执行字符串格式化，避免不需要的日志级别也产生格式化开销。

## Risks / Trade-offs

- **日志量增长**：正常操作每次请求产生 1-2 行日志，10MB/day 轮转策略已足够覆盖中等负载。低风险。
- **敏感信息泄露**：设计已明确不记录 API Key 明文，仅记录 provider_id 和 name。需在 code review 中验证。
- **性能影响**：日志写入为同步 I/O（Python logging 默认），但对本项目的请求量级无影响。若未来高并发可切换 `QueueHandler`。

## Open Questions

- 无。
