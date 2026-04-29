## 1. Router 层 — providers

- [x] 1.1 在 `routers/providers.py` 添加 `import logging` 和 `logger = logging.getLogger("backend.routers.providers")`
- [x] 1.2 `create_provider`: 创建成功后 logger.info（provider_id, name）
- [x] 1.3 `update_provider`: 更新成功后 logger.info（provider_id）；404 时 logger.warning
- [x] 1.4 `delete_provider`: 软删除成功后 logger.info（provider_id）；404 时 logger.warning
- [x] 1.5 `test_api`: logger.info（base_url, api_path，不记录 API Key）
- [x] 1.6 `trigger_collect`: 触发时 logger.info，采集结果 logger.info/error

## 2. Router 层 — stats

- [x] 2.1 在 `routers/stats.py` 添加 `import logging` 和 `logger = logging.getLogger("backend.routers.stats")`
- [x] 2.2 `get_summary`: logger.info（provider_id filter if any）
- [x] 2.3 `get_trends` / `get_distribution`: logger.info（provider_id filter if any）

## 3. Service 层 — collector

- [x] 3.1 补充 `collect_usage` 成功路径：logger.info 记录 provider_id、record_count、balance

## 4. Service 层 — scheduler

- [x] 4.1 在 `services/scheduler.py` 添加 `import logging` 和 `logger = logging.getLogger("backend.services.scheduler")`
- [x] 4.2 `register_job`: logger.info（provider_id, interval_seconds）
- [x] 4.3 `remove_job`: logger.info（provider_id）
- [x] 4.4 `reschedule_job`: logger.info（provider_id, new_interval）

## 5. 验证

- [x] 5.1 启动后端，确认控制台有 `backend.*` 日志输出
- [x] 5.2 执行创建/测试/采集操作后检查 `logs/app.log` 包含 JSON 格式日志
- [x] 5.3 确认日志中无 API Key 明文泄露
