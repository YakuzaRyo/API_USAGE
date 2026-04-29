## Why

Pill Mode Selector 目前使用 `position: absolute` 铆钉在 Dashboard 右上角，文档流不为其保留空间，导致下方 `<h2>` 标题和统计卡片压在 pill 的描述文字上。同时 Pill 与 `<h2>` 标题显示相同文字，造成视觉重复。

## What Changes

- Pill 从 `position: absolute` 改为 `position: static` 左对齐，融入正常文档流
- 删除 Dashboard 中与 Pill 重复的 `<h2>` 标题
- 描述文字从居中改为左对齐

## Capabilities

### New Capabilities
- `pill-selector-layout`: Pill Mode Selector 布局修正 — 文档流左对齐取代页面标题

### Modified Capabilities
- `pill-mode-selector`: Pill 默认定位从 absolute 右上改为 static 左对齐（仅默认样式变更，不影响组件接口）

## Impact

- [PillModeSelector.vue](frontend/src/components/PillModeSelector.vue) — 调整 `.pill-selector` CSS
- [DashboardView.vue](frontend/src/views/DashboardView.vue) — 删除 `<h2>`
