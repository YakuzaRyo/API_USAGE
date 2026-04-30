## 1. Backend — Model & Migration

- [x] 1.1 在 `models.py` 的 Category 模型中新增 `logo_path: Mapped[str | None]` 字段（String(512), nullable, default=None）
- [x] 1.2 创建 Alembic migration，为 categories 表添加 `logo_path` 列
- [x] 1.3 创建 `backend/data/logos/` 目录，确保 gitignore 覆盖该目录

## 2. Backend — Logo API 端点

- [x] 2.1 在 `routers/categories.py` 中实现 `POST /api/categories/{id}/logo`：接收 UploadFile，校验格式（PNG/JPG/SVG/WebP）和大小（≤20MB），保存到 `data/logos/{id}.{ext}`，更新 `logo_path` 字段
- [x] 2.2 实现 `GET /api/categories/{id}/logo`：使用 FastAPI FileResponse 返回图片文件，文件不存在时返回 404
- [x] 2.3 实现 `DELETE /api/categories/{id}/logo`：删除磁盘文件，将 `logo_path` 设为 NULL（无文件时幂等返回 200）
- [x] 2.4 修改 `GET /api/categories` 和 `PUT /api/categories/{id}` 的响应，增加 `logo_path` 字段

## 3. Frontend — API 层

- [x] 3.1 在 `api/index.ts` 中新增 `uploadCategoryLogo(id, file)` 函数，使用 FormData 调用 POST 端点
- [x] 3.2 新增 `deleteCategoryLogo(id)` 函数，调用 DELETE 端点
- [x] 3.3 更新 Category TypeScript interface，增加 `logo_path: string | null` 字段

## 4. Frontend — Logo 网格页面重写

- [x] 4.1 重写 `CategoryManager.vue` 模板：移除 `.card` / `.tag` 布局，改为 `.logo-grid` 容器 + `.logo-item` 图标项
- [x] 4.2 每个 `.logo-item` 包含：`<img>` 展示 Logo（`src="/api/categories/{id}/logo"`）或首字母占位符（无 Logo 时）
- [x] 4.3 实现 spotlight CSS：容器 hover 时所有子项缩小变淡，hover 子项放大显示名称
- [x] 4.4 点击 `.logo-item` 打开编辑弹窗（复用现有 modal 机制）
- [x] 4.5 移除旧的 `.category-card`、`.category-body`、`.category-meta`、`.category-models` 等相关样式

## 5. Frontend — 编辑弹窗改造

- [x] 5.1 弹窗顶部新增 Logo 预览区域：显示当前 Logo + "更换 Logo" 和 "删除" 按钮
- [x] 5.2 新增 Logo 上传交互：点击触发 `<input type="file">`，选择文件后调用 `uploadCategoryLogo`，预览即时更新
- [x] 5.3 移除 API/TokenPlan tab 切换，改为单表单分组布局（API 配置区 + Token Plan 配置区 + 通用区）
- [x] 5.4 表单提交逻辑更新：同时提交两套配置字段
