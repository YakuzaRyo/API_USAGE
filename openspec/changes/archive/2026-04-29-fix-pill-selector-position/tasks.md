## 1. CSS 修复

- [x] 1.1 `PillModeSelector.vue`: `.pill-selector` 默认改为 `position: static; align-items: flex-start; margin-bottom: var(--space-lg)`
- [x] 1.2 `PillModeSelector.vue`: `.pill-description` 改为 `text-align: left`

## 2. Dashboard 模板清理

- [x] 2.1 `DashboardView.vue`: 删除 `<h2 class="page-title">{{ mode === 'dashboard' ? '用量看板' : '余额变化' }}</h2>`
- [x] 2.2 验证 Pill 描述文字不被遮挡，标题无重复
