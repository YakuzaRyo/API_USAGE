## Why

多个 LLM 厂商（OpenAI、Anthropic、Google、DeepSeek 等）的 API 用量数据分散在各平台，用户需要一个统一的服务端来配置厂商凭证、通过内置 HTTP caller 定时拉取用量数据并持久化，最终通过 REST API 暴露给前端 Dashboard 消费。与前端 Change `llm-usage-monitor-frontend`（已归档）配合构成完整平台。

## What Changes

- 新增 FastAPI 后端服务，采用异步 SQLAlchemy (aiosqlite) + SQLite 数据持久化
- 新增厂商配置管理 API，支持名称、API Key、Base URL、用量 API 路径、追踪模型列表、轮询间隔的 CRUD
- 新增内置 HTTP caller，根据厂商配置调用对应 LLM 用量 API，解析响应并写入 UsageRecord 表
- 新增 APScheduler 调度引擎，按各厂商配置的 interval 定时触发采集
- 新增用量统计 API（总量、趋势、模型分布），支持按厂商筛选
- 取消脚本上传/执行机制 — 用量采集完全由后端内置 HTTP caller 驱动

## Capabilities

### New Capabilities

- `provider-management`: 厂商配置 CRUD — 名称、API Key（加密存储）、Base URL、用量 API 路径、追踪模型列表（JSON）、轮询间隔（≥10s 或手动），连接测试 endpoint
- `usage-collection`: 内置 HTTP caller — 根据 Provider 配置构造请求（Bearer token），调用厂商用量 API，解析 JSON 响应提取 Token/费用/余额，写入 UsageRecord；支持手动触发 `POST /api/providers/{id}/collect`
- `usage-scheduling`: 定时调度 — 基于 APScheduler，读取各 Provider 的 interval_seconds，按间隔自动执行采集任务，interval=0 表示手动模式不自动调度
- `usage-stats-api`: 聚合统计接口 — `/api/stats/summary`（Token 总量、费用、活跃厂商数）、`/api/stats/trends`（按日趋势）、`/api/stats/distribution`（按模型分布），均支持 `?provider_id=` 筛选

### Modified Capabilities

无。这是全新项目。

## Impact

- 新建 `backend/` 目录，FastAPI 应用入口 `main.py`
- 依赖：FastAPI, uvicorn, SQLAlchemy (async), aiosqlite, APScheduler, httpx, pydantic
- 数据库：SQLite at `backend/data/app.db`，WAL 模式
- API 路由挂载于 `/api` 前缀，CORS 允许 `localhost:5173`
- 前端对接接口：`/api/providers`、`/api/stats/*`
