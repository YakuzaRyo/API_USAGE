## Why

当前 JSONPath Tag Cloud 以扁平 tag 列表展示解析出的 leaf 路径（如 `data.0.total_usage`），丢失了 JSON 的层级结构感，用户需要脑补 tag 文本与原始 JSON 之间的映射关系。同时填入输入框的是纯文本路径字符串，视觉效果不直观。

## What Changes

- **JsonPathTagCloud 重写为 JSON 树形视图**：用缩进的递归树展示 JSON 结构，每个 key 可点击
- **默认展开前 2 层**，深层节点折叠，点击三角展开/折叠
- **点击 key → 填入 tag**：输入框以可视化 tag（`[path ×]`）代替纯文本字符串，tag 可 × 删除
- **原始 JSON 折叠 toggle**：默认隐藏，点击"查看原始 JSON"展开
- **长字符串截断**：value 超过 30 字符截断显示 `...`，hover 完整展示
- **ProviderWizard 适配**：删除 `<pre>` 原始 JSON 块，将映射输入框改为 tag-container 形式

## Capabilities

### New Capabilities
- `json-tree-view`: Interactive JSON tree component with collapsible nodes, clickable keys that emit JSONPath, and raw JSON toggle

### Modified Capabilities
- `jsonpath-tag-cloud`: 展示形式从 flat tag 列表改为递归 JSON 树，行为从 emit path 改为 emit path + 输入框以 tag 展示
- `vendor-config-wizard`: Step 2/3 中移除原始 JSON `<pre>` 块，映射输入框改为 tag-container（tag 可删除）

## Impact

- [JsonPathTagCloud.vue](frontend/src/components/JsonPathTagCloud.vue) — 全面重写
- [ProviderWizard.vue](frontend/src/components/ProviderWizard.vue) — `<pre>` 块删除，输入框改为 tag-container
