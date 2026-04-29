## 1. Data transformation layer

- [x] 1.1 Implement `computeConsumption(balanceHistory, granularityMs, startDate, endDate)` — sort by date, compute adjacent diff, bucket by epoch floor, sum per bucket, return `[Date, number][]` per provider
- [x] 1.2 Add preset definitions `{ label, bucketMs, defaultDays }` for 5分钟/1小时/7天/30天
- [x] 1.3 Wire computed consumption into the chart data pipeline, replacing raw balance data

## 2. Chart rendering

- [x] 2.1 Replace `xAxis: { type: 'category' }` with `xAxis: { type: 'time' }` and convert data to `[Date, number]` tuples
- [x] 2.2 Change series style to `smooth: 0.3`, `showSymbol: false`, `areaStyle: { opacity: 0.08 }`, `lineStyle: { width: 2 }`
- [x] 2.3 Update Y axis to show consumption amount with currency label "消耗 (CNY)"
- [x] 2.4 Update tooltip `valueFormatter` to show "¥X.XX" with bucket time label

## 3. Header bar layout

- [x] 3.1 Move preset pills and date picker into a `.balance-header` bar fixed at the top of the chart card
- [x] 3.2 Style pills left-aligned, date picker right-aligned within the bar, bar visually attached to the card below
- [x] 3.3 Selected pill uses `--color-primary` background with white text; unselected pills use outline style
- [x] 3.4 Date picker inputs inherit the selected preset's default range; changing dates overrides range but preserves granularity

## 4. Interaction wiring

- [x] 4.1 Clicking a preset pill updates granularity, resets date picker to preset's default range, and reloads data
- [x] 4.2 Changing date picker values reloads data with current granularity and custom date range
- [x] 4.3 Track active preset; when a custom date range is set, no preset pill appears active (deselect all)

## 5. Empty state and edge cases

- [x] 5.1 Show "暂无消耗数据" when consumption data is empty after transformation
- [x] 5.2 Handle single-provider and multi-provider scenarios (multiple series on same chart)
- [x] 5.3 Handle balance refills (increase) — skip those intervals, show note if significant refills detected

## 6. Cleanup

- [x] 6.1 Remove old manual date parsing/sorting code (the `split(/[/\s]/)` and hardcoded year 2026 logic)
- [x] 6.2 Remove old category-axis label generation code
- [x] 6.3 Ensure `nextTick()` call from previous fix remains in place
