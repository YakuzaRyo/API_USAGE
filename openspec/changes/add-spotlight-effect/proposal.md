## Why

项目需要一个独立的交互效果演示页面，用于展示和验证前端视觉技术。首批实践内容为「鼠标跟随聚光灯效果」，参考小米 MiMo Orbit 活动页的深色主题 + 中心聚光视觉风格，给项目增添现代感的交互体验。

## What Changes

- 新增 `/spotlight` 路由和 `SpotlightView.vue` 页面组件
- 实现鼠标跟随径向渐变聚光灯效果（radial-gradient + CSS 变量 + requestAnimationFrame 平滑插值）
- 实现高质量 SVG feTurbulence 噪点纹理背景
- 在侧边栏导航中新增「聚光灯效果」入口
- 使用 lucide-vue-next 的 Sparkles 图标

## Capabilities

### New Capabilities
- `spotlight-effect`: 鼠标跟随聚光灯效果页面，包含深色背景、径向渐变光晕、SVG 噪点纹理、点阵网格、内容卡片等视觉元素

### Modified Capabilities
- `collapsible-sidebar`: 侧边栏新增一个导航项（聚光灯效果页面入口）

## Impact

- **Frontend files**: `SpotlightView.vue`（新增）、`router/index.ts`（添加路由）、`App.vue`（添加导航项 + 新图标导入）
- **No backend changes**: 纯前端页面，不涉及 API 或数据库
- **Dependencies**: 仅使用现有依赖（vue、lucide-vue-next），无需新增 npm 包
