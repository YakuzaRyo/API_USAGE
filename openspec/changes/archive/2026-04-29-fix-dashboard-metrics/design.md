## Context

当前用量看板有 3 个数据正确性问题：(1) API 计费模式用 `initial_balance - last_balance` 计算消耗，充值导致公式失效；(2) 余额变化图表的 5 个 time pill 只有 2 个有数据；(3) 折线头尾用 `null` 填充导致悬空。改动横跨后端 `stats.py` 和前端 `BalanceView.vue`，无 API 变更、无 DB 变更。

## Goals / Non-Goals

**Goals:**
- API 计费模式下费用随消耗单调递增，不受充值影响
- 余额变化图表 3 个 pill 均能产出有意义的聚合折线
- 折线从 y=0 出发、经过所有聚合点、回到 y=0
- Y 轴下限=0，上限自动缩放
- 窗口右端向上取整到 bucket 边界，X 轴上限始终对齐 bucket

**Non-Goals:**
- 不修改 token_plan 计费模式
- 不改动 CollectionLog 表结构
- 不新增 API 端点

## Decisions

### 1. API 计费：增量累加

**选择**: 对每个 provider，查询其所有带 balance 的 CollectionLog（按时间升序），遍历相邻两条 — 当 `prev > curr` 时累加 `prev - curr`，当 `prev < curr` 时跳过（视为充值）。

**替代方案**: 维护一张充值记录表。未采用——当前无充值记录，且累加逻辑完全等价，无需额外 schema。
 
### 2. Pill 预设与 Bucket 缩放

**选择**: 3 个 pill，bucket 时长在 1h～24h 之间线性缩放：

| Pill | Window | Bucket (ms) | 约数据点数 |
|------|--------|-------------|-----------|
| 当天 | 1d | 3,600,000 (1h) | ~24 |
| 7天 | 7d | ~20,738,000 (~5.76h) | ~29 |
| 30天 | 30d | 86,400,000 (24h) | ~30 |

计算式：`bucket = 1h + (24h - 1h) × (window_days - 1) / (30 - 1)`

### 3. 折线起止：每 series 独立锚定相邻 bucket

**选择**: 每条折线从自身第一个数据 bucket 的前一个 bucket 处（y=0）起飞，经过所有聚合点后，在最后一个数据 bucket 的后一个 bucket 处（y=0）降落。不使用窗口边界。

```
   y=0 ●────────────────●───●───●────────────────●
       ↑                ↑       ↑                ↑
   firstBucket       第一个   最后一个       lastBucket
   - bMs             数据点   数据点          + bMs
```

**实现**: 对每个 series，取 `pts[0].time - bMs` 和 `pts[last].time + bMs` 作为起止 0 点。X 轴范围取所有 series 起止点的 min/max。

### 4. Y 轴：min=0, max 自动

**选择**: `yAxis.min = 0`，不设置 `max`。ECharts 根据数据范围自动计算上限。

### 5. 滑动窗口与 X 轴范围

**选择**: 每个 pill 的窗口右端为当前时间，左端 = 右端 - window。X 轴范围由实际数据的起止 bucket 决定：min = 所有 series 中最小的 `firstBucket - bMs`，max = 所有 series 中最大的 `lastBucket + bMs`。不使用窗口边界作为 X 轴范围。

## Risks / Trade-offs

- **首尾 0 值在 bucket 粒度较粗时可能导致折线"骤降"到 0**：如果 30 天窗口只有 1 个数据点，折线会从 0 陡升再陡降。这实际反映了数据稀疏的真实情况，可接受。
- **增量累加需要读取全部 CollectionLog**：对于历史悠久的 provider 可能产生大量记录。当前数据规模在数百条量级，无性能风险；若未来增长，可考虑按月预聚合。
