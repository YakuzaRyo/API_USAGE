## Context

当前 `CategoryManager.vue` 将列表（logo grid）和编辑 modal 混在一个文件中。Modal 使用平铺表单，Logo 上传仅在编辑模式下可用（`v-if="editing"`），创建时无法设置 Logo。ProviderWizard 已建立了分步 wizard 的 UI 模式（step indicator、dot navigation、保存并继续），Category 应复用这一模式以保持一致性。

后端 API 无需修改 — `POST /categories`、`PUT /categories/{id}`、`POST /categories/{id}/logo` 均已就绪。

## Goals / Non-Goals

**Goals:**
- 创建 Category 时就能上传 Logo
- 创建和编辑使用统一的 2 步 wizard 交互
- 与 ProviderWizard 保持视觉和交互一致性
- CategoryManager.vue 只负责列表展示和触发 wizard

**Non-Goals:**
- 不修改后端 API
- 不改变路由结构
- 不为 Category 增加 API 测试功能（Category 是模板，不是实际连接）

## Decisions

### D1: 2 步而非 3 步

**决定：** 2 步（基本信息 → API 配置）

**理由：** Category 字段比 Provider 少得多（无 API Key、无 JSONPath mapping、无测试按钮）。Provider 需要 3 步是因为 Step 2/3 有测试 API 的重交互。Category 没有这个需求，强行拆 3 步会让某个 step 内容空洞。

**Step 划分：**
- Step 1（基本信息）：Logo 预览/上传/删除 + 预设名称 pill + 名称输入 + 默认模型
- Step 2（API 配置）：API Base URL / Usage Path / Balance Path + TP Base URL / TP Usage Path + 货币符号

### D2: Logo 上传时序 — 先创建再上传

**决定：** Step 1 "保存并继续" 时先 `POST /categories` 创建实体，拿到 ID 后立即 `POST /categories/{id}/logo` 上传 Logo。

**备选方案：**
- A) 修改后端 POST /categories 支持 multipart — 需改后端，破坏现有 JSON API 契约
- B) 前端生成临时 ID — 不实际，SQLite 自增 ID 由后端分配
- C) 选用方案（先创建再上传）— 零后端改动，复用 ProviderWizard 的 `saveAndContinue()` 模式

**实现：** 用 `pendingLogoFile: ref<File | null>` 缓存用户选择的文件。`saveAndContinue()` 创建成功后检查此 ref，有值则调用 `uploadCategoryLogo()`。

### D3: 组件结构

**决定：** 新建 `CategoryWizard.vue` 组件，`CategoryWizard` 接收 props 并 emit 事件。

```
CategoryManager.vue (列表页)
  ├─ logo-grid 列表
  ├─ "+ 新增" 按钮
  └─ <CategoryWizard
       :category="selectedCategory | null"
       @close="onWizardClose"
     />
```

**Props/Events 接口：**
- `category: Category | null` — null 为创建模式，非 null 为编辑模式
- `@close` — wizard 关闭时触发，列表页刷新数据

### D4: 复用 ProviderWizard 的样式

**决定：** 直接复制 ProviderWizard 的 CSS 类名和结构（`.wizard-modal`、`.wizard-steps-label`、`.wizard-dot`、`.wizard-actions`），不抽取共享 CSS。

**理由：** 两个 wizard 的样式差异可能随迭代分化（Provider 有 pill-group billing mode，Category 有 preset pills），提前抽象会增加耦合。后续如果出现第三个 wizard 再考虑抽取共享样式。

### D5: 编辑模式的 Logo 处理

**决定：** 编辑模式打开时，Step 1 的 Logo 区域直接显示当前 Logo（通过 `/api/categories/{id}/logo` URL）。上传/删除逻辑与当前实现一致，无需特殊处理。

## Risks / Trade-offs

- **[Logo 上传失败] →** Step 1 创建成功但 Logo 上传失败时，Category 已存在但无 Logo。用 toast 提示用户"分类已创建，但 Logo 上传失败"，用户可后续编辑上传。不影响主流程。
- **[样式重复] →** 与 ProviderWizard 存在 CSS 重复。短期内可接受，等出现第三个 wizard 时再抽象。
- **[Step 划分是否合理] →** 2 步在当前字段量下合适。如果未来 Category 增加更多字段，可能需要调整步数。但这属于 YAGNI，先不预设计。
