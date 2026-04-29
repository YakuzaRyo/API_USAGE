## Context

`BalanceView.vue` template uses `v-if`/`v-else` to switch between an empty-state message and the chart container:

```html
<div v-if="!balanceLoading && balanceHistory.length === 0">暂无数据...</div>
<div v-else ref="chartRef">...</div>
```

On mount, `balanceHistory` is `[]` and `balanceLoading` is `false`, so the `v-if` branch renders. `onMounted` calls `loadData()` which awaits the API call, then calls `renderChart()` synchronously. At that point, Vue has scheduled but not yet flushed the DOM update that would switch to the `v-else` branch — so `chartRef.value` is `undefined`.

## Goals / Non-Goals

**Goals:** Ensure `renderChart()` runs after the DOM contains the chart container.

**Non-Goals:** Restructuring the template, changing the data flow.

## Decisions

**Decision: `await nextTick()` before `renderChart()`**

Vue's `nextTick()` returns a promise that resolves after the next DOM flush cycle. Adding `await nextTick()` guarantees `chartRef.value` references a live DOM element.

## Risks / Trade-offs

- Zero risk — `nextTick()` is a standard Vue API with no side effects.
- Adds one microtick of latency before chart render, imperceptible to users.
