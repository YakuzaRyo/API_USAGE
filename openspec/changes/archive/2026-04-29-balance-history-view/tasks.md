## 1. 后端 — 余额快照存储

- [x] 1.1 `models.py`: CollectionLog 添加 `balance: Mapped[float | None]` 字段
- [x] 1.2 `collector.py`: 采集余额成功时写入 `CollectionLog(balance=...)`
- [x] 1.3 运行或手动执行一次采集，验证 `CollectionLog` 表中出现 balance 记录

## 2. 后端 — 余额历史 API

- [x] 2.1 `routers/stats.py`: 新增 `GET /balance-history` 端点，查询 `CollectionLog where balance IS NOT NULL`，支持 `provider_id`、`days`、`start`/`end` 参数
- [x] 2.2 返回格式 `[{date, provider_name, balance, currency_symbol}, ...]`，按 `created_at` 升序
- [x] 2.3 `main.py`: 确认 stats router 已挂载，无需额外路由注册

## 3. 前端 — PillModeSelector 组件

- [x] 3.1 创建 `frontend/src/components/PillModeSelector.vue`，props: `modelValue`, `options`；emit: `update:modelValue`
- [x] 3.2 实现胶囊按钮样式（border-radius: 20px, scale transiton, 选中/未选中态）
- [x] 3.3 实现打字效果：`watch(modelValue)` → `clearInterval` → `setInterval(50ms)`，当前和上一次切换用的 interval 要清理
- [x] 3.4 实现响应式：`>768px` absolute 右上角，`≤768px` static 文档流
- [x] 3.5 组件 `onUnmounted` 清理 interval

## 4. 前端 — BalanceView 余额视图

- [x] 4.1 创建 `frontend/src/views/BalanceView.vue`，接收 `providerId` prop（可选，为以后扩展用）
- [x] 4.2 在 `api/index.ts` 添加 `BalancePoint` 类型和 `fetchBalanceHistory()` API 调用
- [x] 4.3 在 `stores/usage.ts` 添加 `balanceHistory` state + `fetchBalanceHistory()` action
- [x] 4.4 渲染 ECharts 多折线图：每个厂商一条线，不同颜色，图例在底部，`selectedMode: true`
- [x] 4.5 实现 Tooltip：显示余额值、较上次变化量/百分比、消耗速率（CNY/小时）
- [x] 4.6 实现日期筛选：两个 `<input type="date">`，默认起始 30 天前，变更后重新 fetch
- [x] 4.7 首次加载时默认展示最近 30 天

## 5. 前端 — DashboardView 集成

- [x] 5.1 `DashboardView.vue`: 包裹 `position: relative` 容器，添加 `<PillModeSelector>` 铆钉右上角
- [x] 5.2 两个选项：`{ label: '用量看板', value: 'dashboard', description: 'Token 消耗趋势与模型使用分布' }` 和 `{ label: '余额变化', value: 'balance', description: '各厂商余额消耗速率，点击图例筛选' }`
- [x] 5.3 `mode === 'dashboard'` 渲染现有内容，`mode === 'balance'` 渲染 `<BalanceView>`
- [x] 5.4 移除原有的 `<select>` 下拉和 `selectedProviderId` 相关逻辑
- [x] 5.5 验证 Pill 切换时图表数据正常加载、打字效果流畅、图例点击筛选正常工作
