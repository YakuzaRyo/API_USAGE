## Why

当前厂商配置流程需要为每个同分类 Provider 重复填写 base_url、路径、模型等共享信息，认知负担重；主看板的 4 个矩形卡片信息密度低，无法直观展示不同分类/模型/计费模式的占比关系。引入 Category 作为配置模板后，新增 Provider 只需填 name + api_key，主看板升级为 Apple 风格环形仪表盘。

## What Changes

- **Category 分类管理页**：卡片布局展示所有分类，弹窗编辑（billing_mode tab 切换，各自存 url + 路径，模型和货币共享）。右上角删除图标。名称预设下拉 + 可自定义
- **Provider Wizard 重构**：billing_mode 移到 Step 1 顶部；新增 category 下拉，选中后根据 billing_mode 自动填充 url/路径/模型/货币；Step 3 移除 billing_mode
- **主看板 Pill 重组**：从 2 个 pill（用量看板/余额变化）改为 3 个（综合看板/用量分析/余额变化）。原用量趋势和模型分布移入用量分析 pill
- **综合看板环形仪表盘**：4 个纯 CSS/SVG 环形卡片替换原矩形卡片。Token 消耗（单环按模型）、活跃厂商（单环按 category 计数）、当前余额（双环 category/provider）、费用（双环 billing_mode/provider）。图例支持点击过滤，双环联动。环形设计遵循 Neo-Brutalist 风格：直角卡片容器、硬阴影、粗边框、`--color-primary` 主色调、无软渐变
- **数据层**：新增 `categories` 表，Provider 表加 `category_id` FK，stats API 支持按 category 聚合

## Capabilities

### New Capabilities

- `category-management`: Category CRUD（名称预设+自定义、billing_mode 双 tab 配置、模型/货币共享），卡片列表页，删除保护
- `ring-gauge-dashboard`: 4 个环形仪表盘卡片，纯 CSS/SVG 占比分割，无满环概念，图例点击过滤，双环内外联动

### Modified Capabilities

- `vendor-config-wizard`: billing_mode 从 Step 3 移到 Step 1，新增 category 下拉在 Step 1，选中后自动填充对应分类+模式下的配置项
- `pill-mode-selector`: 从 2 pill 扩展为 3 pill（综合看板 / 用量分析 / 余额变化）

## Impact

- **DB**: 新建 `categories` 表（name, api_url, api_usage_path, api_balance_path, tp_url, tp_usage_path, currency_symbol, models），Provider 表加 `category_id` FK（可为 null）
- **Backend**: `GET/POST/PUT/DELETE /categories`，`GET /categories/presets` 预设列表，stats 聚合按 category 分组，Provider CRUD 加 category_id
- **Frontend 新页面**: 分类管理页（CategoryManager.vue）
- **Frontend 重构**: ProviderWizard step 结构、DashboardView pill 布局、环形卡片组件（RingGaugeCard.vue）
- **路由**: 新增 `/categories`
