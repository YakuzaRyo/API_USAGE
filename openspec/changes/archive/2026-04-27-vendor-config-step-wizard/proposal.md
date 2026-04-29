## Why

厂商配置表单目前将 10+ 字段堆叠在单个模态窗口中，用户在一页内需要同时理解连接配置、API 路径、JSONPath 映射和轮询参数，认知负担过高。特别是 JSONPath 字段需要用户手动输入 `data.0.total_usage` 这类路径，极易出错且操作低效。

## What Changes

- 将现有的单页编辑弹窗重构为 **3 步 Step Wizard**，拆分字段到独立的步骤页中
- Step 1（连接配置）：名称、API Key、Base URL、追踪模型 — 必填
- Step 2（用量路径，可跳过）：Usage API Path 测试 + JSONPath Tag 云 → Token 总量/费用映射
- Step 3（余额 & 其他，可跳过）：Balance API Path 测试 + JSONPath Tag 云 → 余额映射、货币符号、轮询间隔
- 新增 **JSONPath Tag 云** 组件：将测试响应的 JSON 叶子节点解析为可点击 tag，用户聚焦目标输入框后点击 tag 即自动填入路径
- 支持 **增量保存**：每个 Step 独立保存，仅校验当前步骤字段，允许逐步完成配置
- 下方圆点导航器（`○ ● ○`），当前 step 圆点放大，点击可跳转到任意 step
- 上一步/下一步按钮辅助导航，降低用户学习成本
- 输入框聚焦态使用 **橙色边框**，与全局 UI 风格保持一致

## Capabilities

### New Capabilities
- `vendor-config-wizard`: Step-based multi-page form inside a modal with independent per-step saving, dot navigation, and progressive validation
- `jsonpath-tag-cloud`: Parse leaf-node paths from JSON response and render as clickable tags that auto-fill the currently focused input

### Modified Capabilities
<!-- 无现有能力被修改 -->

## Impact

- [ProviderView.vue](frontend/src/views/ProviderView.vue) — 编辑弹窗部分将大幅重构，提取 Step Wizard 和 Tag Cloud 组件
- [providers.ts](frontend/src/stores/providers.ts) — 增量保存逻辑，需确认后端已支持 partial update
- [index.ts](frontend/src/api/index.ts) — 无需变更，现有 `updateProvider` / `testApi` 已覆盖需求
- 后端 — 无需变更，`PUT /providers/:id` 已支持 partial update
