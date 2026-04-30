## Context

当前 `CategoryManager.vue` 使用 `.form-group` 做 `flex-direction: column` 布局，导致每个字段占两行高度。Logo 网格 spotlight 使用 `.logo-grid:hover .logo-item` 选择器，grid 容器的 gap 区域也属于 hover 范围。

## Goals / Non-Goals

**Goals:**
- 表单字段改为 `label: input` 横排，减少弹窗高度
- spotlight 仅在 hover 到具体 Logo 时触发

**Non-Goals:**
- 不改变弹窗的字段内容或交互逻辑
- 不影响其他页面

## Decisions

### 1. 表单布局：`flex-direction: row` + 固定 label 宽度

```css
.form-group {
  flex-direction: row;
  align-items: center;
}
.form-group label {
  flex-shrink: 0;
  width: 100px;
  text-align: right;
}
.form-group input {
  flex: 1;
}
```

label 右对齐、固定 100px 宽度，input 自动撑满。

### 2. Spotlight 触发：`:has()` 选择器

```css
.logo-grid:has(.logo-item:hover) .logo-item { ... }
.logo-grid:has(.logo-item:hover) .logo-item:hover { ... }
```

`:has()` 浏览器兼容性：Chrome 105+、Firefox 121+、Safari 15.4+，满足现代浏览器需求。

## Risks / Trade-offs

- **[:has() 兼容性]** → 主流浏览器均已支持，风险极低
- **[label 宽度固定]** → 中文 label（如"货币符号"）4 字 = 约 56px，100px 足够；英文名（如"Usage Path"）也在范围内
