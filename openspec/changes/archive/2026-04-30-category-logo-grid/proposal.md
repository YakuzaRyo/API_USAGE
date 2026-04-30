## Why

分类管理页面当前使用扁平的卡片+标签布局，所有信息（名称、计费模式、币种、模型）用相同样式的 tag 展示，缺乏视觉层级和品牌辨识度。厂商商标（透明背景 PNG）可以直观代表每个类别，将其作为主要视觉元素能大幅提升页面的品牌感和可识别性。

## What Changes

- **移除卡片布局**：去掉 card 外壳、tag 标签系统，分类管理页面改为纯 Logo 图标网格
- **新增 Logo 上传**：每个分类支持上传商标图片（透明背景 PNG），存放在文件系统 `backend/data/logos/{id}.png`
- **Spotlight 交互**：鼠标移入网格时，hover 的 Logo 放大并显示类别名，其余 Logo 缩小变淡（CSS-only 聚光灯效果）
- **点击编辑**：点击 Logo 弹出编辑弹窗，弹窗内预览当前 Logo 并提供更换/删除 Logo 入口
- **合并计费模式**：编辑弹窗将 API 模式和 Token Plan 配置合并展示在同一表单中（不再用 tab 切换），一个分类可同时拥有两套配置
- **新增后端 API**：`POST /api/categories/{id}/logo`（上传）、`GET /api/categories/{id}/logo`（返回图片）、`DELETE /api/categories/{id}/logo`（删除）
- **Category 模型扩展**：新增 `logo_path` 字段存储 Logo 文件路径

## Capabilities

### New Capabilities
- `category-logo-upload`: 分类 Logo 上传、存储、展示的完整能力，包含后端文件上传 API、文件系统存储、前端 Logo 预览和更换

### Modified Capabilities
- `category-management`: 分类管理页面的展示形式从卡片布局改为 Logo 网格布局；编辑弹窗合并 API/TokenPlan 双配置；交互模式改为 hover spotlight + 点击编辑

## Impact

- **后端**: `models.py`（新增 `logo_path` 字段）、`routers/categories.py`（新增 3 个 Logo 相关端点）、新增 `backend/data/logos/` 目录、Alembic migration
- **前端**: `CategoryManager.vue` 重写模板和样式（移除卡片/tag、改为 Logo 网格 + spotlight CSS）、`api/index.ts` 新增 Logo 上传/删除接口
- **API**: 新增 3 个端点，现有 CRUD 端点返回数据增加 `logo_path` 字段
- **存储**: 新增 `backend/data/logos/` 目录存放图片文件
