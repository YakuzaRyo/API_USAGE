## Context

`JsonPathTagCloud.vue` 中 `<details>` 内的 `<pre>` 直接展示 JSON 字符串，无格式化。改为正则替换语法高亮。

## Decisions

```typescript
function highlightJson(obj: unknown): string {
  const json = JSON.stringify(obj, null, 2)
  return json.replace(
    /("(?:[^"\\]|\\.)*")\s*:/g,           // keys
    '<span class="json-key">$1</span>:'
  ).replace(
    /:\s*("(?:[^"\\]|\\.)*")/g,            // string values
    ': <span class="json-string">$1</span>'
  ).replace(
    /:\s*(\d+\.?\d*)/g,                    // number values
    ': <span class="json-number">$1</span>'
  ).replace(
    /:\s*(true|false)/g,                   // boolean values
    ': <span class="json-bool">$1</span>'
  ).replace(
    /:\s*(null)/g,                         // null values
    ': <span class="json-null">$1</span>'
  )
}
```

颜色方案（与 `--color-primary` #FF6B35 协调）：
- key: `#0550ae`（蓝）
- string: `#0a3069`（深蓝）
- number: `#cf222e` / `var(--color-primary)`（橙色）
- boolean: `#8250df`（紫）
- null: `#6e7781`（灰）

背景：`#f6f8fa`（浅灰，与 GitHub 一致），`font-family: var(--font-mono)` 确保等宽。

## Risks

- `v-html` 用于注入 HTML。输入是 `JSON.stringify` 的输出，已转义，无 XSS 风险。
