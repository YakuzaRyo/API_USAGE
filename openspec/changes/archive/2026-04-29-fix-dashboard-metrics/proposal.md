## Why

用量看板中存在三个相互关联的数据正确性问题：API 计费模式在余额充值后费用计算失效（公式假设余额只减不增）；余额变化图表的 time-pill 预设不合理（5 个 pill 中只有 1h/24h 有图表产出）；折线图没有从 y=0 起止、头尾悬空。这三个问题导致看板数据不可信，需要从后端计算逻辑、前端 pill 配置和图表渲染三个层面一次性修复。

## What Changes

- **API 计费模式费用计算**：从"余额头尾差"改为"逐段累加余额下降量"，充值导致的余额上升自动跳过，费用只增不减
- **余额变化 Time Pill 重构**：从 5 个预设（5分钟/1小时/24小时/7天/30天）精简为 3 个（当天/7天/30天），bucket 时长在 1h~24h 之间等比例缩放
- **折线渲染规则**：所有聚合数据点从 y=0 连接、闭合回 y=0，形成有头有尾的连续折线
- **图表 Y 轴**：下限固定为 0，上限根据数据范围自动缩放

## Capabilities

### New Capabilities

- `billing-incremental-consumed`: API 计费模式下通过遍历余额快照序列、逐段累加余额下降量来计算实际消耗，不受充值影响

### Modified Capabilities

- `balance-history`: pill 预设从 5 个改为 3 个（当天/7天/30天），bucket 时长等比例缩放；折线渲染改为从 y=0 起止
- `balance-consumed-stat`: API 模式费用计算从 head-tail diff 改为增量累加

## Impact

- **Backend**: `backend/routers/stats.py` — `get_billing_summary` 中 API 模式的计算逻辑，需增加按 provider 取全部余额快照并逐段累加的逻辑
- **Frontend**: `frontend/src/views/BalanceView.vue` — presets 数组、`buildConsumption` bucket 逻辑、`renderChart` 的 series padding 和 yAxis 配置
- **无 API breaking changes**：所有接口路径和参数不变
- **无数据库 schema 变更**
