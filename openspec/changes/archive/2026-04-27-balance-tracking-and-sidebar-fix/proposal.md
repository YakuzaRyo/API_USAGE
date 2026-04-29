## Why

当前 Provider 用量和余额共用同一个 API 路径，但主流 LLM 厂商的用量查询和余额查询通常是两个独立 endpoint，无法分别配置导致余额数据采集失败或不准确。Dashboard 也只展示 Token 费用估算，缺少余额可视化。侧边栏在页面滚动时消失，影响导航体验。

## What Changes

- **后端**: Provider 模型新增 `balance_api_path` 和 `last_balance` 字段，用量查询和余额查询路径分离
- **后端**: Collector 支持双路径采集 — 先调用 usage_api_path 获取 Token/费用写入 UsageRecord，再调用 balance_api_path 获取余额缓存到 Provider
- **后端**: Stats API 的 summary/trends 增加 `total_balance` 字段
- **前端**: Provider 配置表单新增 `balance_api_path` 输入框
- **前端**: Dashboard 统计卡牌从 3 张扩展为 4 张，新增"当前余额"卡牌
- **前端**: 侧边栏 fix — `position: sticky; top: 0; height: 100vh` + 主内容区 `overflow-y: auto`

## Capabilities

### New Capabilities

- `balance-api-separation`: Provider 用量/余额查询路径分离，支持分别配置 `usage_api_path` 和 `balance_api_path`，Collector 双路径采集，余额缓存到 Provider.last_balance
- `balance-dashboard-display`: Dashboard 新增余额统计卡牌（显示各厂商 last_balance 汇总），Stats API 返回 total_balance

### Modified Capabilities

无。基于已归档 Change 的增量改动。

## Impact

后端:
- `backend/models.py` — Provider 加 `balance_api_path`, `last_balance`
- `backend/routers/providers.py` — Pydantic schema 加对应字段
- `backend/services/collector.py` — 双路径采集逻辑
- `backend/routers/stats.py` — summary/trends 加 `total_balance`

前端:
- `frontend/src/App.vue` — Sidebar sticky + main overflow
- `frontend/src/api/index.ts` — Provider/UsageSummary 类型加 balance 字段
- `frontend/src/stores/usage.ts` — UsageSummary 加 `total_balance`
- `frontend/src/views/ProviderView.vue` — 表单加 balance_api_path
- `frontend/src/views/DashboardView.vue` — 加余额卡牌
