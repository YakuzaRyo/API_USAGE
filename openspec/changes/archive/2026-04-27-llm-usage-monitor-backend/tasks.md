## 1. 项目骨架

- [x] 1.1 创建 `backend/pyproject.toml`：依赖 FastAPI, uvicorn, sqlalchemy (asyncio), aiosqlite, apscheduler, httpx, cryptography, pydantic
- [x] 1.2 创建 `backend/config.py`：Settings 类（DB 路径 `./data/app.db`、Fernet SECRET_KEY、CORS origins）
- [x] 1.3 创建 `backend/database.py`：async SQLAlchemy engine (aiosqlite, WAL 模式), session factory, `get_db` async generator
- [x] 1.4 创建 `backend/models.py`：Provider（api_key 加密存储、models 为 JSON、response_mapping 为 JSON nullable）、UsageRecord（provider_id FK、model、tokens_used、cost、balance、recorded_at）、CollectionLog（provider_id FK、status、record_count、error_message、created_at）
- [x] 1.5 创建 `backend/main.py`：FastAPI app, CORSMiddleware (allow localhost:5173), lifespan（DB init + scheduler 启动/关闭）, include routers under `/api`

## 2. 加密与工具服务

- [x] 2.1 创建 `backend/services/crypto.py`：Fernet 初始化（从 config SECRET_KEY 或自动生成），`encrypt(s: str) -> str`、`decrypt(s: str) -> str`、`mask_key(s: str) -> str`（`...后4位`）

## 3. 厂商管理 API

- [x] 3.1 创建 `backend/routers/providers.py`：Pydantic schemas（ProviderCreate, ProviderUpdate, ProviderResponse with masked key），`GET /api/providers` 列表
- [x] 3.2 实现 `POST /api/providers`：校验必填字段，encrypt api_key，写入 DB，返回 ProviderResponse
- [x] 3.3 实现 `PUT /api/providers/{id}`：查找 → 更新字段（若 api_key 变更则 re-encrypt），404 处理
- [x] 3.4 实现 `DELETE /api/providers/{id}`：软删除（设置 deleted 标记但保留 UsageRecord），404 处理
- [x] 3.5 实现 `POST /api/providers/{id}/test`：decrypt api_key，httpx GET `{base_url}{usage_api_path}` with Bearer auth，返回 ok/error

## 4. 用量采集

- [x] 4.1 创建 `backend/services/collector.py`：`collect_usage(provider, db)` — decrypt api_key → httpx GET usage API → 解析 JSON → dot-path extract（`data.total_usage`）→ 按 provider.models 拆分 UsageRecord → 写入 DB → 创建 CollectionLog
- [x] 4.2 实现响应解析：支持 `response_mapping` dot-path 提取，回退到内置解析器（OpenAI `/v1/usage` 格式、Anthropic 格式）
- [x] 4.3 实现 `POST /api/providers/{id}/collect` endpoint：调用 collector.collect_usage，返回 record_count 或 error

## 5. 定时调度

- [x] 5.1 创建 `backend/services/scheduler.py`：`init_scheduler()` 在 lifespan 中创建 AsyncIOScheduler，`register_job(provider_id, interval)` / `remove_job(provider_id)` / `reschedule_job(provider_id, new_interval)`
- [x] 5.2 lifespan 启动时查询所有 interval_seconds > 0 的 Provider，注册对应 interval job（IntervalTrigger）
- [x] 5.3 集成到 Provider router：create 时若 interval > 0 则 register_job；update 时若 interval 变更则 reschedule_job；delete 时 remove_job
- [x] 5.4 interval_seconds 校验：拒接 1-9 的值（仅允许 0 或 >= 10）

## 6. 统计 API

- [x] 6.1 创建 `backend/routers/stats.py`：`GET /api/stats/summary` — 最近 7 天 SUM(tokens_used), SUM(cost), COUNT(DISTINCT provider_id)，支持 `?provider_id=` 筛选
- [x] 6.2 `GET /api/stats/trends` — GROUP BY DATE(recorded_at) 按日聚合 tokens + cost，支持 `?provider_id=` 筛选，返回 `[{date, tokens, cost, provider_name}]`
- [x] 6.3 `GET /api/stats/distribution` — GROUP BY model 聚合 tokens，按 tokens DESC 排序，支持 `?provider_id=` 筛选

## 7. 验证

- [x] 7.1 `uv run python -m uvicorn main:app --port 8000` 启动成功
- [x] 7.2 Provider CRUD 全流程 curl 测试通过（create → list → update → test → delete）
- [x] 7.3 Stats API 返回正确聚合数据
- [ ] 7.4 前端 `frontend/` 代理到后端，Dashboard 和 Provider 页数据正常展示
