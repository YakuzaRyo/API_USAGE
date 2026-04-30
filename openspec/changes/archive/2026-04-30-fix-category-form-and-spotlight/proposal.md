## Why

分类管理页面有两个体验问题：1) 编辑弹窗的表单采用上下堆叠布局（label 在上、input 在下），导致弹窗过高、大量空白浪费；2) Logo 网格的 spotlight 效果使用 `.logo-grid:hover` 选择器，鼠标只要进入 grid 容器（包括 gap 空白区域）就会触发所有 Logo 变模糊，而非仅在 hover 到具体 Logo 时才触发。

## What Changes

- 编辑弹窗表单改为横排布局：`label: [input]` 在同一行，label 固定宽度，input 撑满剩余空间
- Logo 网格 spotlight 触发条件改为 `:has(.logo-item:hover)`，仅在鼠标真正 hover 到某个 Logo 上时才触发聚焦效果

## Capabilities

### New Capabilities

（无）

### Modified Capabilities

- `category-management`: 编辑弹窗表单布局从纵向堆叠改为横向排列；spotlight 交互触发条件从 grid hover 改为 item hover

## Impact

- **前端**: `CategoryManager.vue` 的 scoped CSS 修改（`.form-group` 布局、`.logo-grid:hover` 选择器）
- **无后端改动**
