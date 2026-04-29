## Context

对已实现 LLM Usage Monitor 的增量修复和增强。Provider 的用量查询和余额查询需要分离配置，Dashboard 需要展示余额数据，侧边栏需要固定定位。

## Goals / Non-Goals

**Goals:**
- Provider 支持独立的 `balance_api_path`（可选），与 `usage_api_path` 分离
- Collector 在采集时分别调用两个 endpoint
- Dashboard 新增余额卡牌
- 侧边栏 sticky 固定，主内容区独立滚动

**Non-Goals:**
- 不改变现有 UsageRecord 的 balance 字段（保留兼容）
- 不新增专门的 BalanceRecord 表（余额缓存到 Provider.last_balance）

## Decisions

### D1: 余额存储位置

余额是账户级指标（非模型级），存储在 `Provider.last_balance` 而非 UsageRecord 中。每次采集时更新此缓存值。Stats API 的 summary.total_balance 汇总所有非 NULL 的 Provider.last_balance。

### D2: Collector 双路径顺序

先调用 `usage_api_path` 获取用量 → 写 UsageRecord；再调用 `balance_api_path`（如配置）获取余额 → 更新 Provider.last_balance。两个调用独立，用法采集失败不影响余额采集（反之亦然），各自写独立的 CollectionLog。

### D3: Sidebar 布局

```
#app { height: 100vh }              ← 锁视口
.sidebar { position: sticky; top: 0; height: 100vh }  ← 固定
.main-content { overflow-y: auto; height: 100vh }     ← 独立滚动
```

不改变现有 flex 方向或 DOM 结构，仅 CSS 调整。

## Risks / Trade-offs

- **balance_api_path 为空时行为不变** → 向后兼容，仅当字段有值时才发起余额查询
- **余额采集失败不影响用量数据** → 两个 CollectionLog 独立记录
