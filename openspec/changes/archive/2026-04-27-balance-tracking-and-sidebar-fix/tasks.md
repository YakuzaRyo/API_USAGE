## 1. 后端 — 数据模型

- [x] 1.1 `backend/models.py`：Provider 加 `balance_api_path`（String, nullable）和 `last_balance`（Float, nullable）
- [x] 1.2 `backend/routers/providers.py`：ProviderCreate/Update/Response schema 加 `balance_api_path` 和 `last_balance` 字段

## 2. 后端 — 采集逻辑

- [x] 2.1 `backend/services/collector.py`：分离采集逻辑 — 先调 `usage_api_path` 写 UsageRecord，再调 `balance_api_path`（如有）更新 Provider.last_balance；两个 CollectionLog 独立记录

## 3. 后端 — 统计 API

- [x] 3.1 `backend/routers/stats.py`：summary 加 `total_balance`（SUM of Provider.last_balance），trends 加 `balance` 字段

## 4. 前端 — Sidebar 修复

- [x] 4.1 `frontend/src/App.vue`：sidebar `position: sticky; top: 0; height: 100vh`，main-content `overflow-y: auto; height: 100vh`；style.css `#app` 加 `height: 100vh`

## 5. 前端 — 余额展示

- [x] 5.1 `frontend/src/api/index.ts`：Provider 接口加 `balance_api_path`、`last_balance`；UsageSummary 加 `total_balance`
- [x] 5.2 `frontend/src/views/ProviderView.vue`：表单加 "余额 API 路径" 输入框（可选）
- [x] 5.3 `frontend/src/views/DashboardView.vue`：stats-cards 从 3 列改 4 列，新增 "当前余额" 卡牌
- [x] 5.4 `frontend/src/stores/usage.ts`：UsageSummary 类型同步 total_balance（无需修改，类型自动推断）

## 6. 验证

- [x] 6.1 后端 Provider CRUD 通过 balance_api_path 字段的创建/更新/查询
- [x] 6.2 前端 `npm run build` TypeScript 通过
- [ ] 6.3 Sidebar 滚动时固定在左侧，主内容区独立滚动（需启动前端手动验证）
