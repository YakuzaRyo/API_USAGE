## Why

用量看板有 Token 消耗、费用、活跃厂商、当前余额四张统计卡，但缺少"余额消耗总量"——即从首次采集以来总共消耗了多少余额。这是用户最关心的财务指标之一。

## What Changes

- 后端 `/api/stats/summary` 新增 `balance_consumed` 字段，计算方式：每个厂商首次采集余额合计 - 当前余额合计
- 前端 Dashboard 统计卡区新增第 5 张「余额消耗」卡

## Capabilities

### New Capabilities
- `balance-consumed-stat`: Balance consumed total in dashboard stats cards

## Impact

- [stats.py](backend/routers/stats.py) — summary 接口新增 `balance_consumed` 计算
- [api/index.ts](frontend/src/api/index.ts) — `UsageSummary` 新增字段
- [DashboardView.vue](frontend/src/views/DashboardView.vue) — 新增第 5 张 stat card
