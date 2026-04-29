## Context

`BalanceView.vue` currently renders a category-axis line chart from raw balance data. Each collection cycle (~10s) produces a point; 82% are consecutive duplicates. The chart uses manually-parsed date strings (hardcoded year 2026) as category labels, producing unreadable overlapping text at high density. Controls (date pickers) live inside the chart card alongside a shared PillModeSelector for dashboard/balance mode switching.

## Goals / Non-Goals

**Goals:**
- Show consumption rate (¥ per time bucket), not absolute balance level
- Smooth curve with time-aware X axis
- Frontend-only transformation — no API changes
- Preset granularity pills (5min / 1h / 7d / 30d) outside the chart card
- Date picker outside the chart card, right-aligned

**Non-Goals:**
- Backend aggregation endpoint (future optimization, not needed now)
- Real-time updates (data already refreshes on mount and date change)
- Multi-provider balance comparison (keep existing per-provider series)

## Decisions

### Decision 1: Client-side data transformation pipeline

```
GET /api/stats/balance-history  (raw balance points, ordered by time)
       │
       ▼
  Group by provider_name
       │
       ▼
  Sort by date ascending
       │
       ▼
  Compute adjacent diffs:  balance[i-1] - balance[i] = consumption
  (positive = money spent, negative or zero = skip)
       │
       ▼
  Bucket by granularity (floor date to bucket start)
       │
       ▼
  Sum consumption per bucket → [timestamp, ¥] pairs
       │
       ▼
  ECharts time-series
```

**Why not backend aggregation?**
Avoids API changes. The raw data is already available; deduplication + bucketing in JS is simple and fast for the expected data volume (<1000 points).

### Decision 2: ECharts time axis (`xAxis: { type: 'time' }`)

Replaces the current category axis with manual date parsing. Benefits:
- ECharts handles label spacing, formatting, and timezone automatically
- Tooltip shows precise timestamps natively
- Data format: `[Date object, number]` tuples instead of `["label string", number]`

**Why not keep category axis?**
Category axis requires manual label dedup/spacing logic and breaks when data density varies.

### Decision 3: Preset pills replace free-form date inputs

```
[5分钟] [1小时] [7天] [30天]        [日期范围选择器]
```

Each pill sets both the granularity (bucket size) and the default date range:
- 5分钟 → 5min buckets, last 5 minutes
- 1小时 → 1min buckets, last hour (to avoid too few buckets)
- 7天 → 1h buckets, last 7 days
- 30天 → 1d buckets, last 30 days

The date picker overrides the preset's date range but keeps the granularity.

**Why pills instead of a dropdown?**
Immediate one-click access to common views; matches the existing PillModeSelector pattern already used in DashboardView. Each pill encodes both granularity AND time range, reducing cognitive load.

### Decision 4: Layout — header bar + chart card

```
┌──────────────────────────────────────────────────┐
│  用量看板 / 余额变化   ← 复用 PillModeSelector     │
├──────────────────────────────────────────────────┤
│  [5分钟] [1小时] [7天] [30天]        [日期选择器]  │  ← 新 header bar
├──────────────────────────────────────────────────┤
│  card                                             │
│    消耗曲线                                       │
│    ...                                            │
└──────────────────────────────────────────────────┘
```

The existing PillModeSelector (用量看板/余额变化) stays at the top. A new header bar with preset pills + date picker appears only in balance mode. The chart card fills the remaining space.

### Decision 5: Curve style

```js
series: [{
  type: 'line',
  smooth: 0.3,       // gentle curve, not overly wavy
  showSymbol: false,  // no dots at data points (clean curve)
  lineStyle: { width: 2 },
  areaStyle: { opacity: 0.08 },  // subtle fill below curve
}]
```

`smooth: 0.3` (not boolean) gives a controlled curve — visible trend without distorting the actual data shape. `showSymbol: false` removes the dot-per-point visual noise. Light area fill adds depth without clutter.

## Risks / Trade-offs

- **[Risk] Fewer than 2 data points after bucketing** → Mitigation: If a series has <2 points, show the "暂无数据" message with the selected preset name
- **[Risk] DST or timezone edge cases with time bucketing** → Mitigation: Use UTC epoch math for bucketing (`Math.floor(timestamp / bucketMs) * bucketMs`), display in local time via ECharts
- **[Trade-off] Preset pills hide "custom range" discoverability** → Acceptable: the date picker is visible next to the pills; users can override the range at any time
