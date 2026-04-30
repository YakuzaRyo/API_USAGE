## Why

Category 新增时无法上传 Logo — Logo 上传按钮被 `v-if="editing"` 守卫完全隐藏，用户必须先创建再编辑才能设置 Logo，体验断裂。同时，Category 的创建/编辑 modal 是一个冗长的平铺表单，与 ProviderWizard 的分步引导模式不一致，增加了认知负担。

## What Changes

- 将 Category 创建/编辑 modal 拆分为 2 步 wizard 组件 (`CategoryWizard.vue`)，复用 ProviderWizard 的 step 模式（step indicator、dot navigation、保存并继续）
- Step 1（基本信息）：名称（含预设 pill 选择）、Logo 上传/预览/删除、默认模型管理
- Step 2（API 配置）：API 模式路径（Base URL / Usage Path / Balance Path）、Token Plan 路径（Base URL / Usage Path）、货币符号
- 创建模式下 Step 1 的"保存并继续"先 POST 创建 category 拿到 ID，再调用 Logo 上传 API，解决新建时无 ID 的问题
- 编辑模式同样使用 step wizard，保持与创建模式一致的交互逻辑
- `CategoryManager.vue` 瘦身为纯列表页，通过事件触发 `CategoryWizard`

## Capabilities

### New Capabilities

- `category-step-wizard`: Category 创建/编辑的分步向导组件，包含 2 步流程（基本信息 → API 配置），支持 Logo 在创建时上传

### Modified Capabilities

- `category-management`: Category 编辑 modal 从平铺表单变为分步 wizard；创建流程增加 Logo 上传能力

## Impact

- **前端新增文件**: `frontend/src/components/CategoryWizard.vue`
- **前端修改文件**: `frontend/src/views/CategoryManager.vue`（移除 modal 逻辑，改为触发 wizard 组件）
- **后端无变更**: 现有 CRUD + Logo upload API 完全满足需求
- **路由无变更**: `/categories` 路径不变
