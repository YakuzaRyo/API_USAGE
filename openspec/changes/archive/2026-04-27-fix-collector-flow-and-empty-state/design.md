## Context

两个小的缺陷修复，不涉及架构变更。

## Goals / Non-Goals

**Goals:**
- Usage API 失败时继续尝试 balance API 采集
- 前端空状态仅一个触发入口：虚线框卡片

**Non-Goals:**
- 不改变 API 响应格式
- 不新增组件

## Decisions

### D1: Collector 解耦

将 `collect_usage` 中 usage 和 balance 分为两个独立 try/except 块，各自记录 CollectionLog。返回值改为 `list[CollectionLog]` 或在 router 层处理。

保持向后兼容：router 层调用逻辑不变，collect_usage 内部 usage 失败不再 return，balance 始终会被尝试。

### D2: 空状态虚线卡片

```css
.empty-add {
  border: 2px dashed var(--color-border);
  padding: var(--space-2xl);
  text-align: center;
  cursor: pointer;
  transition: transform 0.15s, box-shadow 0.15s;
}
.empty-add:hover {
  border-color: var(--color-primary);
  transform: translate(-3px, -3px);
  box-shadow: var(--shadow-md);
}
```

点击触发 `openCreate()`。仅在 `store.providers.length === 0` 且非 loading 时展示。
