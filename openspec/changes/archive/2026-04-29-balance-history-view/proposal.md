## Why

当前 Dashboard 仅展示 Token 消耗趋势和模型分布，余额虽然在统计卡中显示了一个瞬时值，但用户无法看到余额随时间的变化曲线。每次采集到的余额快照被直接覆盖丢弃，无法追溯消耗速率和历史上限。用户需要一个独立的余额历史视图来监控资金消耗节奏。

## What Changes

- 后端 `CollectionLog` 新增 `balance` 字段，每次采集余额时同时写入快照
- 新增 `GET /api/stats/balance-history` API，返回按厂商分组的余额时序数据，支持日期范围筛选
- 新增 `PillModeSelector` 组件：胶囊形二选一切换器，锚定在卡面右上角，含 scale 过渡 + 打字效果描述
- `DashboardView` 集成 Pill Mode Selector，在「用量看板」和「余额变化」之间切换
- 余额变化页面：各厂商独立折线图，图例点击 toggle 显示/隐藏（ECharts 原生），默认 30 天，支持日期筛选
- 移除 Dashboard 中原来的 `<select>` 厂商下拉筛选，替代为图例交互

## Capabilities

### New Capabilities
- `pill-mode-selector`: Capsule-shaped dual-option toggle component with scale transition and typewriter description effect
- `balance-history`: Balance tracking view with per-provider line charts, legend-based filtering, and date range selector

### Modified Capabilities
<!-- 无现有能力被修改 -->

## Impact

- [models.py](backend/models.py) — `CollectionLog` 加 `balance Float` 字段
- [collector.py](backend/services/collector.py) — 采集余额时写入 `CollectionLog(balance=...)`
- [routers/stats.py](backend/routers/stats.py) — 新增 `/balance-history` 端点
- [DashboardView.vue](frontend/src/views/DashboardView.vue) — 集成 Pill Mode Selector，条件渲染两种视图
- 新建 [PillModeSelector.vue](frontend/src/components/PillModeSelector.vue)
- 新建 [BalanceView.vue](frontend/src/views/BalanceView.vue)
- [usage.ts](frontend/src/stores/usage.ts) — 新增 `fetchBalanceHistory()`
- [api/index.ts](frontend/src/api/index.ts) — 新增 `BalancePoint` 类型 + `fetchBalanceHistory` API
