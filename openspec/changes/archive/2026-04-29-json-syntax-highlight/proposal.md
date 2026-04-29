## Why

原始 JSON toggle 使用 `<pre>` + `{{ JSON.stringify() }}` 展示，字体可能落到宋体，无任何语法着色，与 Postman/VS Code 等产品的 JSON 展示体验差距大。

## What Changes

- `JsonPathTagCloud.vue`: 原始 JSON 展示加入语法高亮（key/string/number/boolean/null 分色），强制等宽字体

## Capabilities

### New Capabilities
- `json-syntax-highlight`: JSON syntax highlighting in raw toggle view

## Impact

- [JsonPathTagCloud.vue](frontend/src/components/JsonPathTagCloud.vue) — 新增 `highlightJson()` 函数 + 替换 `<pre>` 内容
