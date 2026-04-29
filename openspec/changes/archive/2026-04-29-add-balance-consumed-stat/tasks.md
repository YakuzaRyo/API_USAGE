## 1. 后端

- [x] 1.1 `stats.py`: summary 接口新增 `balance_consumed` 计算（首次余额合计 - 当前余额合计）
- [x] 1.2 返回 JSON 中新增 `balance_consumed` 字段

## 2. 前端

- [x] 2.1 `api/index.ts`: `UsageSummary` 类型新增 `balance_consumed: number`
- [x] 2.2 `DashboardView.vue`: 统计卡区新增第 5 张卡「余额消耗」
