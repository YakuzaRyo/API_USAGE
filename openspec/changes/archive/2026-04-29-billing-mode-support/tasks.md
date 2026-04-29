## 1. 后端 — 数据模型

- [x] 1.1 `models.py`: Provider 加 `billing_mode`、`monthly_fee`、`sub_start_date` 字段
- [x] 1.2 `routers/providers.py`: ProviderCreate/ProviderUpdate 适配新字段

## 2. 后端 — API

- [x] 2.1 `routers/stats.py`: 修复 `active_providers` 为 `COUNT(Provider WHERE deleted=false)`
- [x] 2.2 `routers/stats.py`: 新增 `GET /billing-summary` 端点，返回各厂商 mode + amount

## 3. 前端 — API & Store

- [x] 3.1 `api/index.ts`: 新增 `BillingItem` 类型 + `fetchBillingSummary()` 函数
- [x] 3.2 `stores/usage.ts`: 新增 `billingSummary` state + `fetchBillingSummary()` action

## 4. 前端 — ProviderWizard Step 3

- [x] 4.1 Step 3 顶部新增 billing_mode 切换（Pill 或 radio）
- [x] 4.2 API 模式区块：Balance API Path + Balance JSONPath（v-if）
- [x] 4.3 Token Plan 模式区块：月费金额 + 订阅起始日期（v-else）
- [x] 4.4 货币符号、轮询间隔（两种模式共用）

## 5. 前端 — 卡片 & 看板

- [x] 5.1 `ProviderView.vue`: 卡片展示 billing_mode tag + 对应金额信息
- [x] 5.2 `DashboardView.vue`: 费用卡片改为前端聚合 billingSummary 的 amount 总和
