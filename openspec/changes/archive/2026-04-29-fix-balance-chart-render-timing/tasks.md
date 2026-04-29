## 1. Fix chart render timing

- [x] 1.1 Add `nextTick` to the import from `vue` in `BalanceView.vue`
- [x] 1.2 Add `await nextTick()` before `renderChart()` in `loadData()`

## 2. Fix end date filter — inclusive of full day

- [x] 2.1 In `routers/stats.py` `get_balance_history`, change end filter from `<= datetime.fromisoformat(end)` to `< datetime.fromisoformat(end) + timedelta(days=1)`

## 3. Verification

- [ ] 3.1 Navigate to Dashboard, switch to "余额变化" — verify chart renders with balance data
- [ ] 3.2 Change date range — verify chart updates with filtered data
