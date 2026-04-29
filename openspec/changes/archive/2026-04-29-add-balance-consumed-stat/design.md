## Context

现有 `/api/stats/summary` 返回 `total_tokens`、`total_cost`、`active_providers`、`total_balance`。新增 `balance_consumed` 表示从首次采集到现在的余额总消耗。

## Decisions

### balance_consumed 计算逻辑

```python
# 每个厂商的首次余额（最早的 CollectionLog.balance）
first_balances = (
    select(func.sum(CollectionLog.balance))
    .where(
        CollectionLog.id.in_(
            select(func.min(CollectionLog.id))
            .where(CollectionLog.balance.isnot(None))
            .group_by(CollectionLog.provider_id)
        )
    )
)
initial_total = (await db.execute(first_balances)).scalar() or 0.0

# 当前余额
current_total = (await db.execute(_build_balance_query(provider_id))).scalar() or 0.0

# 消耗 = 初始 - 当前
balance_consumed = round(float(initial_total - current_total), 4)
```

如果值为负（余额增加了），显示为负消耗。

### 前端展示

新增第 5 张 stat card，与其他 4 张同风格，标签"余额消耗"，值带货币符号：

```html
<div class="stat-card">
  <p class="stat-label">余额消耗</p>
  <p class="stat-value">-{{ balance_consumed }} <span>CNY</span></p>
</div>
```

## Risks

- 如果厂商从未配置余额路径，首次余额为 null，不计入消耗 → fallback 到 0
