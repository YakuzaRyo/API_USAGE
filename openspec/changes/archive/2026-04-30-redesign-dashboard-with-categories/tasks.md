## 1. 数据层

- [x] 1.1 创建 `categories` 表（id, name, api_base_url, api_usage_path, api_balance_path, tp_base_url, tp_usage_path, currency_symbol, models JSON）
- [x] 1.2 Provider 表加 `category_id` FK（可为 NULL，兼容存量数据）
- [x] 1.3 创建 Alembic migration 并执行

## 2. 后端

- [x] 2.1 实现 `GET /api/categories/presets` 返回预设分类名称列表
- [x] 2.2 实现 `GET /api/categories` 分类列表
- [x] 2.3 实现 `POST /api/categories` 创建分类
- [x] 2.4 实现 `PUT /api/categories/{id}` 更新分类
- [x] 2.5 实现 `DELETE /api/categories/{id}` 删除分类（关联 provider 的 category_id 置 NULL）
- [x] 2.6 Provider CRUD 加 `category_id` 字段（create/update/response）

## 3. 前端 — Category 管理页

- [x] 3.1 新建 `CategoryManager.vue` 页面（卡片网格布局，显示名称 tag、计费/货币、模型、编辑按钮、右上角删除图标）
- [x] 3.2 实现分类编辑弹窗（名称预设下拉 + billing_mode tab 切换 + 共享模型/货币字段）
- [x] 3.3 实现新增/编辑/删除交互（确认对话框、toast 反馈）
- [x] 3.4 添加路由 `/categories`
- [x] 3.5 侧边栏导航加"分类管理"入口

## 4. 前端 — Provider Wizard 调整

- [x] 4.1 Step 1 顶部加 billing_mode pill（API 查询 / Token Plan）
- [x] 4.2 Step 1 加 category 下拉（预设 + 自定义），选中后按 billing_mode 自动填充 url/路径/模型/货币
- [x] 4.3 Step 3 移除 billing_mode，Token Plan 的月费/订阅日期保留
- [x] 4.4 Provider 列表卡片显示 category tag

## 5. 前端 — Pill 重组

- [x] 5.1 DashboardView 的 pillOptions 改为 3 项：综合看板 / 用量分析 / 余额变化
- [x] 5.2 综合看板 mode 渲染 4 个环形卡片（替换原 stats-cards）
- [x] 5.3 用量分析 mode 渲染原用量趋势 + 模型分布图表
- [x] 5.4 余额变化 mode 保持现有 BalanceView

## 6. 前端 — 环形卡片组件

- [x] 6.1 新建 `RingGaugeCard.vue` 组件（接收 segments 数据、图例配置、双环开关）
- [x] 6.2 实现 SVG stroke-dasharray 环形渲染（单环 + 双环）
- [x] 6.3 实现图例点击过滤（单环直接过滤，双环外环联动内环）
- [x] 6.4 实现 Neo-Brutalist 样式（直角卡片、硬阴影、粗描边、#FF6B35 主色、实色无渐变）
- [x] 6.5 实现 Token 消耗环（数据源：distribution API，按 model）
- [x] 6.6 实现活跃厂商环（数据源：summary API，按 category 计数）
- [x] 6.7 实现当前余额环（数据源：providers API，双环 category/provider）
- [x] 6.8 实现费用环（数据源：billing-summary API，双环 billing_mode/provider）
- [x] 6.9 实现全部 4 环在综合看板中的响应式布局（2×2 网格）

## 7. 验证

- [ ] 7.1-7.5 手动验证各模块
