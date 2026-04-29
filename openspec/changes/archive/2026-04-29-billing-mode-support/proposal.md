## Why

1. **活跃厂商数为 0**：当前 `active_providers` 统计 `UsageRecord` 中有记录的厂商，刚注册未采集的不计入。应改为统计所有未删除的 Provider。
2. **缺少计费模式**：很多厂商使用 Token Plan（按月固定扣费），和按量计费（API 查询余额）是两种不同的计费模型。当前系统只支持 API 模式，无法处理月费制的厂商。

## What Changes

- **后端**：`Provider` 新增 `billing_mode`（'api'|'token_plan'）、`monthly_fee`、`sub_start_date` 字段；新增 `GET /api/stats/billing-summary` 返回各厂商费用明细；修复 `active_providers` 统计
- **前端**：ProviderWizard Step 3 新增计费方式选择 + 显隐规则；厂商卡片展示模式 tag 和对应信息；费用 stat card 改为前端聚合

## Capabilities

### New Capabilities
- `billing-mode`: Dual billing model support (API query vs Token Plan monthly fee), with per-provider cost aggregation API
- `active-providers-fix`: Fix active providers count to use all non-deleted providers instead of UsageRecord DISTINCT

### Modified Capabilities
- `vendor-config-wizard`: Step 3 新增 billing_mode 切换 + monthly_fee + sub_start_date 字段，以及 API/TokenPlan 字段显隐规则
- `balance-consumed-stat`: 费用卡片从后端单字段改为前端聚合 billing-summary 结果

## Impact

- [models.py](backend/models.py) — Provider 加 3 字段
- [routers/stats.py](backend/routers/stats.py) — 修复 active_providers + 新增 billing-summary 端点
- [routers/providers.py](backend/routers/providers.py) — ProviderCreate/ProviderUpdate 模式适配
- [ProviderWizard.vue](frontend/src/components/ProviderWizard.vue) — Step 3 重构
- [ProviderView.vue](frontend/src/views/ProviderView.vue) — 卡片展示模式 tag
- [DashboardView.vue](frontend/src/views/DashboardView.vue) — 费用卡片聚合
- [api/index.ts](frontend/src/api/index.ts) — 新类型 + API 函数
- [stores/usage.ts](frontend/src/stores/usage.ts) — billing summary 状态
