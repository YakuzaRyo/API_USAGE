## 1. Spotlight 触发修复

- [x] 1.1 将 `.logo-grid:hover .logo-item` 改为 `.logo-grid:has(.logo-item:hover) .logo-item`
- [x] 1.2 将 `.logo-grid:hover .logo-item:hover` 改为 `.logo-grid:has(.logo-item:hover) .logo-item:hover`
- [x] 1.3 将 `.logo-grid:hover .logo-item:hover .logo-name` 改为 `.logo-grid:has(.logo-item:hover) .logo-item:hover .logo-name`

## 2. 表单横排布局

- [x] 2.1 修改 `.form-group` 从 `flex-direction: column` 改为 `flex-direction: row`，添加 `align-items: center`
- [x] 2.2 修改 `.form-group label` 添加固定宽度 `width: 100px`、`text-align: right`、`flex-shrink: 0`
- [x] 2.3 修改 `.form-group input` 添加 `flex: 1`，移除 `width: 100%`
