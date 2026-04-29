## Context

当前系统仅支持 API 查询余额模式。需要新增 Token Plan（月费制）计费模式，两种模式在编辑端有互斥的显隐规则，在展示端以 tag 区分。

## Goals / Non-Goals

**Goals:**
- 后端支持两种计费模式的数据存储和查询
- 新增 billing-summary 端点返回所有厂商费用明细（带 mode 字段）
- 修复活跃厂商数统计
- 前端 Step 3 显隐规则、卡片模式 tag、费用前端聚合

**Non-Goals:**
- 不改变 Step 1/2 的内容和行为
- 不修改 balance-history 相关逻辑

## Decisions

### 1. 数据模型

```python
class Provider(Base):
    billing_mode = mapped_column(String(16), default="api")   # 'api' | 'token_plan'
    monthly_fee = mapped_column(Float, nullable=True)          # token_plan only
    sub_start_date = mapped_column(String(16), nullable=True)  # ISO date, token_plan only
```

### 2. billing-summary API

```
GET /api/stats/billing-summary?provider_id=

返回:
[
  {
    "provider_id": 1,
    "provider_name": "OpenAI",
    "billing_mode": "api",
    "amount": 38.50,         // balance_consumed
    "currency_symbol": "CNY"
  },
  {
    "provider_id": 2,
    "provider_name": "Claude",
    "billing_mode": "token_plan",
    "amount": 600.00,        // monthly_fee * months
    "currency_symbol": "USD"
  }
]
```

API 模式：`amount = initial_balance - current_balance`
TokenPlan 模式：`amount = monthly_fee * months_since(sub_start_date)`

### 3. 活跃厂商数修复

```python
# Before
func.count(func.distinct(UsageRecord.provider_id))

# After
select(func.count(Provider.id)).where(Provider.deleted == False)
```

### 4. Step 3 显隐规则

```
billing_mode === 'api':
  - Balance API Path (input + test)
  - Balance JSONPath (tag-container)
  - 货币符号
  - 轮询间隔

billing_mode === 'token_plan':
  - 月费金额 (number input)
  - 订阅起始 (date input)
  - 货币符号
  - 轮询间隔
```

用 `v-if="form.billing_mode === 'api'"` / `v-else` 切换。

### 5. 厂商卡片展示

```html
<!-- API 模式 -->
<span class="tag mode-tag mode-api">API</span>
<span>余额: {{ p.last_balance }} {{ p.currency_symbol }}</span>

<!-- TokenPlan 模式 -->
<span class="tag mode-tag mode-tokenplan">TokenPlan</span>
<span>月费: {{ p.monthly_fee }} {{ p.currency_symbol }}</span>
```

模式 tag 使用不同颜色区分。

### 6. 费用前端聚合

Dashboard 获取 billing-summary 数据，前端 `sum(amount)` 显示总费用。

## Risks / Trade-offs

- TokenPlan 的 `sub_start_date` 如果未填则无法计算月数 → 默认 `created_at` 或返回 0
- API 模式的厂商如果没有余额记录 → amount = 0
