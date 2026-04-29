## Context

Pill Mode Selector 按设计文档使用 `position: absolute` 铆钉右上角。Dashboard 页面同时有一个 `<h2>` 标题，与 Pill 显示的当前模式名称重复。Absolute 定位导致 Pill 的描述文字被下方内容遮挡。

## Goals / Non-Goals

**Goals:**
- Pill 融入页面文档流，替代 `<h2>` 标题
- 消除文字遮挡

**Non-Goals:**
- 不改变 Pill 组件的 Props/Emits 接口
- 不影响移动端响应式行为

## Decisions

### 布局调整

**DashboardView.vue** — 删除 `<h2 class="page-title">`。

**PillModeSelector.vue** — `.pill-selector` 默认样式改为：
```css
.pill-selector {
  position: static;        /* 而非 absolute */
  align-items: flex-start; /* 左对齐 */
  margin-bottom: var(--space-lg);
}
.pill-description {
  text-align: left;        /* 而非 center */
}
```

响应式无需修改 — ≤768px 时已经是 `static`。

## Risks / Trade-offs

- 无。改动局限于 2 个文件、~5 行 CSS。
