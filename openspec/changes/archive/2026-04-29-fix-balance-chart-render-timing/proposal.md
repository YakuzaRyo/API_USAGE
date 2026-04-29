## Why

The balance history chart in `BalanceView.vue` never renders because `renderChart()` executes before Vue's DOM has flushed. On initial mount, the chart container div is in a `v-else` branch that hasn't been rendered yet, so `chartRef.value` is `undefined` and the function returns early. The user sees "暂无余额历史数据" even though the API returns valid data.

## What Changes

- Add `await nextTick()` before `renderChart()` in `loadData()` to ensure the DOM has updated before accessing `chartRef`

## Capabilities

### New Capabilities

None.

### Modified Capabilities

None — this is a one-line timing fix in an existing view.

## Impact

- **Frontend**: `BalanceView.vue` — add `nextTick` import, one `await nextTick()` call
- No API changes, no backend changes
