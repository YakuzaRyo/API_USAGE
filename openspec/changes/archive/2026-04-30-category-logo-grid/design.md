## Context

当前 CategoryManager.vue 使用卡片网格（CSS Grid + `.card`）展示分类，内部用统一的 `.tag` 组件展示名称、计费模式、币种和模型名。Category 模型已有 `api_*` 和 `tp_*` 两组字段，编辑弹窗用 tab 切换。后端通过 `routers/categories.py` 提供 CRUD API。项目使用 SQLite + WAL 模式，异步 aiosqlite，文件存储在 `backend/data/` 目录下。

## Goals / Non-Goals

**Goals:**
- 分类管理页面以厂商 Logo 为主要视觉元素，去掉卡片和标签
- CSS-only spotlight hover 效果（hover 放大 + 显示名称，其余缩小变淡）
- 支持 Logo 图片上传/存储/展示/删除
- 编辑弹窗同时展示 API 和 TokenPlan 两套配置

**Non-Goals:**
- 不做图片压缩或格式转换（用户自行准备透明 PNG）
- 不做从 Logo 自动提取主色
- 不做拖拽排序
- 不影响其他页面（Dashboard、ProviderView）对 category 数据的使用

## Decisions

### 1. Logo 存储方式：文件系统

**决定**: Logo 存储在 `backend/data/logos/{category_id}.png`，通过 API 端点返回图片文件。

**替代方案**: 存入数据库 BLOB — 被否决，因为 SQLite 不适合存二进制大对象，且文件系统方案可利用浏览器缓存（ETag/304）。

**理由**:
- `backend/data/` 目录已在 `.gitignore` 中（含 `app.db`），新增 `logos/` 子目录符合现有结构
- 图片文件名用 `category_id` 而非原始文件名，避免路径问题和重名冲突
- 通过 FastAPI 的 `FileResponse` 返回，自动支持 MIME 类型和缓存头

### 2. Logo API 设计：三个独立端点

```
POST   /api/categories/{id}/logo   → UploadFile, 保存到 data/logos/{id}.png
GET    /api/categories/{id}/logo   → FileResponse, 404 if not exist
DELETE /api/categories/{id}/logo   → 删除文件, 清除 logo_path
```

**理由**:
- 与现有 CRUD 端点（`/api/categories/{id}` 的 PUT/DELETE）正交，不混淆职责
- GET 端点直接返回文件，前端用 `<img src="/api/categories/1/logo">` 即可，无需 Base64
- 上传限制为 PNG/JPG/SVG/WebP，最大 20MB

### 3. Category 模型：新增 `logo_path` 可空字段

```python
logo_path: Mapped[str | None] = mapped_column(String(512), nullable=True, default=None)
```

**理由**:
- 虽然文件名规则固定为 `{id}.png`，但 `logo_path` 字段可以记录原始文件名或验证 Logo 是否存在
- 可空 — 分类可以没有 Logo（如刚创建还未上传）
- 迁移简单 — ALTER TABLE ADD COLUMN，默认 NULL

### 4. Spotlight 交互：纯 CSS 实现

```css
.logo-grid:hover .logo-item {
  transform: scale(0.75);
  opacity: 0.4;
  filter: blur(1px);
}
.logo-grid:hover .logo-item:hover {
  transform: scale(1.2);
  opacity: 1;
  filter: none;
}
```

**理由**:
- 使用 `transform` 和 `opacity` 而非改变布局属性（width/margin），避免触发 reflow
- 所有元素位置不变，只做视觉效果变化，性能最优
- 零 JS 依赖，纯 CSS transition 即可实现平滑过渡

### 5. 网格布局：CSS Grid 固定格子

- 每个格子固定尺寸（如 120×120），Logo 在格子内居中、保持原始比例（`object-fit: contain`）
- `grid-template-columns: repeat(auto-fill, 120px)` 自适应列数
- 间距紧凑（gap: 24px）

### 6. 编辑弹窗：合并 API + TokenPlan 配置

去掉 tab 切换，改为单表单内用分隔线分组：

```
名称
───── API 配置 ─────
Base URL / Usage Path / Balance Path
───── Token Plan ────
Base URL / Usage Path
───── 通用 ──────────
货币符号 / 默认模型
```

两套配置可以同时填写。Provider 创建时根据选择的计费模式使用对应的一套。

## Risks / Trade-offs

- **[Logo 尺寸差异大]** → 使用 `object-fit: contain` 在固定格子内等比缩放，极端尺寸的 Logo 会被缩小到格子内而非溢出
- **[无 Logo 的分类在网格中不可见]** → 对于没有 Logo 的分类，显示类别名首字母作为占位符
- **[文件系统存储不支持分布式]** → 当前是单机 SQLite 方案，文件系统存储与项目架构一致，无需考虑分布式
- **[上传大文件]** → FastAPI `UploadFile` 配合 `max_length` 参数限制为 20MB
