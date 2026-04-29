## Context

后端使用 FastAPI + 异步 SQLAlchemy + SQLite，架构模式沿用 workflow_develop 的 backend。单服务架构，无独立的 script-backend 层。通过内置 httpx caller 直接调用 LLM 厂商 API，用 APScheduler 管理定时采集任务。

## Goals / Non-Goals

**Goals:**
- Provider CRUD API with encrypted API key storage
- Built-in HTTP caller that fetches usage data from LLM provider APIs
- APScheduler-driven periodic collection per provider interval
- Stats API: summary (total tokens/cost/active providers), trends (daily), distribution (by model)
- Connection test endpoint per provider

**Non-Goals:**
- 不存储明文 API Key（使用 Fernet 对称加密）
- 不支持用户自定义脚本（HTTP caller 内置，响应解析通过 provider 配置的 mapping 驱动）
- 不处理 LLM 厂商 API 的 rate limit（由 interval 下限 10s 保证，不内置重试逻辑）

## Decisions

### D1: 数据模型

```
Provider
├─ id: int (PK)
├─ name: str
├─ api_key: str          ← Fernet 加密存储
├─ base_url: str
├─ usage_api_path: str   ← 如 /v1/usage
├─ models: JSON          ← ["gpt-4", "gpt-3.5-turbo"]
├─ interval_seconds: int ← 0=手动, ≥10=自动
├─ created_at: datetime

UsageRecord
├─ id: int (PK)
├─ provider_id: int (FK → Provider)
├─ model: str            ← 模型名
├─ tokens_used: int
├─ cost: float
├─ balance: float
├─ recorded_at: datetime ← 采集时间

CollectionLog
├─ id: int (PK)
├─ provider_id: int (FK → Provider)
├─ status: str           ← ok / error
├─ record_count: int
├─ error_message: str?
├─ created_at: datetime
```

Provider 与 UsageRecord 之间不设 cascade delete — 删除 Provider 时保留历史用量数据（将 provider_id 置 NULL 或软删除）。

### D2: 项目结构

```
backend/
├── main.py              ← FastAPI app, CORS, lifespan (DB init + scheduler start)
├── config.py            ← settings (DB path, secret key for Fernet)
├── database.py          ← async engine, session factory, get_db dependency
├── models.py            ← Provider, UsageRecord, CollectionLog
├── routers/
│   ├── providers.py     ← CRUD + test + collect
│   └── stats.py         ← summary, trends, distribution
├── services/
│   ├── crypto.py        ← Fernet encrypt/decrypt
│   ├── collector.py     ← HTTP caller: build request → fetch → parse → write DB
│   └── scheduler.py     ← APScheduler setup, job management
└── data/                ← SQLite DB location (gitignored)
```

### D3: HTTP Caller 响应解析策略

不同厂商返回的 JSON 结构不同。Provider 表增加 `response_mapping` JSON 字段，定义提取路径：

```json
{
  "total_tokens": "data.total_usage",
  "cost": "data.total_cost",
  "balance": "data.remaining_balance"
}
```

Caller 用简单的点号路径（`data.total_usage`）从响应 JSON 中取值。若 mapping 未配置则尝试常见路径自动检测。首次实现覆盖 OpenAI `/v1/usage` 和 Anthropic 格式，后续通过 mapping 扩展。

### D4: APScheduler 集成

- 使用 `AsyncIOScheduler`，在 FastAPI lifespan 中启动
- 每个 interval_seconds > 0 的 Provider 注册一个 `IntervalTrigger` job
- Provider 更新/删除时重建对应的 job
- 采集函数为 async，内部使用 httpx.AsyncClient
- scheduler 不持久化 job 状态（重启后从 Provider 表重新注册）

### D5: API Key 加密

使用 `cryptography.fernet.Fernet` 对称加密。密钥存储在 `backend/.env` 或由 config.py 的 `SECRET_KEY` 生成。API Key 在写入 DB 前加密，读取时解密。对外 API 响应中始终脱敏（仅显示后 4 位）。

### D6: API 路由设计

| Method | Path | Purpose |
|--------|------|---------|
| GET | `/api/providers` | 列表（api_key 脱敏） |
| POST | `/api/providers` | 创建（api_key 加密入库） |
| PUT | `/api/providers/{id}` | 更新 |
| DELETE | `/api/providers/{id}` | 删除（软删除，保留用量数据） |
| POST | `/api/providers/{id}/test` | 连接测试（用 httpx 试调 usage API） |
| POST | `/api/providers/{id}/collect` | 手动触发采集 |
| GET | `/api/stats/summary` | 总量（?provider_id= 可选） |
| GET | `/api/stats/trends` | 日趋势（?provider_id= 可选） |
| GET | `/api/stats/distribution` | 模型分布（?provider_id= 可选） |

### D7: 统计查询策略

- `summary`: `SELECT SUM(tokens_used), SUM(cost), COUNT(DISTINCT provider_id) FROM usage_records WHERE recorded_at > date('now', '-7 days')`
- `trends`: `SELECT DATE(recorded_at) as date, SUM(tokens_used), SUM(cost) FROM usage_records GROUP BY date ORDER BY date`
- `distribution`: `SELECT model, SUM(tokens_used) FROM usage_records GROUP BY model ORDER BY SUM(tokens_used) DESC`

所有查询支持 `?provider_id=` 过滤。

## Risks / Trade-offs

- **Fernet 密钥丢失 → API Key 无法解密** → `.env.example` 文档化密钥生成方式；首次启动自动生成并打印警告
- **不同厂商 API 响应格式差异大** → mapping 配置是 fallback，主流厂商（OpenAI/Anthropic/Google/DeepSeek）内置解析器优先
- **SQLite 并发写入瓶颈** → 单进程 async SQLite 足够；WAL 模式；采集间隔 ≥10s 避免高频写入
- **APScheduler 不持久化** → 重启后从 Provider 表重建，无状态丢失
