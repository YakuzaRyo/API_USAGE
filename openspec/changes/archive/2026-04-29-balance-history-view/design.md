## Context

Dashboard 当前只有 Token 趋势和模型分布两个图表。余额数据仅以一行的瞬时数字展示在统计卡中，每次采集后旧值被覆盖。用户需要查看余额随时间的变化曲线、对比各厂商消耗速率、快速筛选关注厂商。

项目已有 ECharts、Vue 3 Composition API、Pinia、以及全局 CSS 变量（`--color-primary: #FF6B35`）。

## Goals / Non-Goals

**Goals:**
- 后端存储每次采集的余额快照，提供带日期筛选的余额历史 API
- 实现 PillModeSelector 组件（完全按设计文档规范）
- Dashboard 用 Pill 切换「用量看板」和「余额变化」两种模式
- 余额视图：每个厂商一条折线，图表图例点击 toggle，默认 30 天，日期筛选
- 移除 Dashboard 中原有的 `<select>` 下拉，用图例交互替代

**Non-Goals:**
- 不改变 Token 趋势图和模型分布图的现有行为
- 不引入新的图表库（继续用 ECharts）
- 不改变路由结构（Pill 切换是组件内条件渲染，不是新路由）

## Decisions

### 1. 余额快照存储

`CollectionLog` 加 `balance Float nullable` 字段。每次采集余额时同步写入。

```python
# collector.py — balance section
if balance is not None:
    provider.last_balance = float(balance)
    db.add(CollectionLog(
        provider_id=provider.id, status="ok", record_count=1,
        balance=float(balance)  # 新增
    ))
```

选择 `CollectionLog` 而非 `UsageRecord` 的理由：
- CollectionLog 每次采集产生一条，天然就是时序
- UsageRecord 按模型拆分（多行/次），余额是总体的不适合拆
- CollectionLog 已有 `created_at`，直接就是时间轴

### 2. 余额历史 API

```
GET /api/stats/balance-history?provider_id=&days=30&start=&end=

返回:
[
  { "date": "2026-04-01T10:00:00", "provider_name": "OpenAI", "balance": 100.0 },
  ...
]
```

查询 `CollectionLog` where `balance IS NOT NULL`，按 `created_at` 排序，支持 `provider_id` 和日期范围过滤。每行是一个采集快照。

### 3. PillModeSelector 组件

严格遵循 `Pill-Mode-Selector 组件设计.md` 规范：

- **Props**: `modelValue: string`, `options: [{ label, value, description }]`
- **Emits**: `update:modelValue`
- **动画**: scale(1.05)/scale(0.95) + 50ms/字打字效果 + all 0.15s ease
- **定位**: absolute 铆钉右上角，`top: var(--space-md); right: var(--space-md)`
- **样式**: `border-radius: 20px`, 选中背景 `var(--color-surface)` + `box-shadow: var(--shadow-sm)`, 未选中透明 + opacity 0.55
- **响应式**: ≤768px 时 `position: static` 退回文档流

### 4. Dashboard 集成

DashboardView.vue 变为条件渲染：

```
<template>
  <div class="dashboard-card" style="position: relative;">
    <!-- 右上角 Pill 切换：只有两个选项 -->
    <PillModeSelector v-model="mode" :options="pillOptions" />

    <!-- 共用的统计卡：Pill 在右上角，统计卡在下方 -->
    <div v-if="mode === 'dashboard'">
      <!-- 现有：stats cards + trend chart + dist chart -->
    </div>
    <div v-else>
      <BalanceView />
    </div>
  </div>
</template>
```

Dashboard 包装为 `position: relative` 容器，作为 Pill 的铆钉宿主。

### 5. 余额折线图 — ECharts 配置

```typescript
// 多条折线，一个 series 对应一个厂商
series: providers.map(p => ({
  name: p.name,
  type: 'line',
  data: p.balanceHistory,  // [ [date, balance], ... ]
  smooth: true,
  symbol: 'circle',
  symbolSize: 6,
}))

// 图例交互 — 原生 toggle
legend: {
  type: 'scroll',
  selectedMode: true,     // 点击 toggle 显示/隐藏
  inactiveColor: '#ccc',   // 隐藏后变灰
  bottom: 0,
}

// Tooltip 显示消耗速率
tooltip: {
  trigger: 'axis',
  formatter: (params) => {
    // 当前值 + 较上次变化 + 消耗速率
  }
}
```

日期筛选：两个 `<input type="date">` 分别设置起始和结束，默认起始 30 天前。

### 6. 移除旧 `<select>` 下拉

DashboardView 中的 `<select>` 和 `usageStore.selectedProviderId` 被 Pill + 图例替代：
- Pill 切换「用量看板 / 余额变化」
- 图例切换厂商显示/隐藏
- `selectedProviderId` 相关逻辑移除

## Risks / Trade-offs

- **历史数据缺失**：已有的 CollectionLog 没有 balance 值。只有从部署后新采集的数据才有余额快照。→ 无历史数据时图表显示「暂无余额数据」。
- **CollectionLog 表膨胀**：原本每次采集 2 条 log（usage + balance），加 balance 字段不增加行数，无额外存储压力。
- **Pill 打字效果在快速切换时可能残留旧文字** → `clearInterval` 在 `watch` 和 `onUnmounted` 中执行，已规约。

## Open Questions

- 无。Explore 阶段已充分讨论。
