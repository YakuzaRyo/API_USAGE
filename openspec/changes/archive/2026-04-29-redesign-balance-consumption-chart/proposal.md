## Why

The current balance page plots raw balance values as a dense category-axis line chart. Each 10-second collection cycle produces a data point, but balance only changes ~18% of the time. The result is 133 points of which 110 are redundant, all crammed into a single hour with unreadable overlapping labels. The chart's purpose is unclear — it shows balance level rather than what users actually want to see: how fast money is being spent.

## What Changes

- **Data transformation**: Convert raw balance time series into consumption-per-time-bucket on the frontend (adjacent diff → sum by bucket)
- **Chart type**: Smooth curve (`smooth: true`) replacing noisy step-like line with circle symbols
- **Time axis**: Replace fragile category-axis with manual date parsing by ECharts `type: 'time'` for automatic label spacing and formatting
- **Preset pills**: Four preset granularity buttons — 5分钟 / 1小时 / 7天 / 30天 — placed in the card's top-left area
- **Date picker**: Relocated to the card's top-right area, outside the chart canvas
- **Layout**: Controls sit in a header bar above the chart card, not inside it
- **Y-axis semantics**: Now shows consumption amount (¥) per bucket rather than absolute balance

## Capabilities

### New Capabilities

- `balance-consumption-chart`: Smooth time-series curve displaying per-bucket consumption derived from balance history, with preset granularity pills and a date range picker in a header bar above the card.

### Modified Capabilities

None — this replaces the balance section of the DashboardView, not an existing spec.

## Impact

- **Frontend**: `BalanceView.vue` (major rework of data transform, chart options, template layout)
- **Frontend**: `DashboardView.vue` (minor — move controls out of card)
- **No API changes**, no backend changes, no dependency changes
