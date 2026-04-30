## Why

综合看板的环形仪表盘当前使用手绘 SVG `<circle>` + `stroke-dasharray` 实现，视觉效果简陋：无段间留白、无圆角、无渐变、无动画、无 tooltip、无 hover 交互。同时，主内容区的默认浏览器滚动条没有贴边（padding 导致偏移 32px）且样式与 neo-brutalist 设计不协调。项目已依赖 ECharts 6（趋势图、分布图、余额图均使用），用 ECharts Pie 环形图替换手绘 SVG 可统一图表风格、复用内置交互能力，显著提升展示效果。

## What Changes

- **BREAKING** 移除 `RingGaugeCard.vue` 内的手绘 SVG 实现（`stroke-dasharray` 弧线、`ringArcs` 计算函数），替换为 ECharts Pie 环形图渲染
- 环形段间增加留白（`padAngle`）、圆角端点（`borderRadius`）
- 入场动画：进度条式展开（`stroke-dashoffset` 从 circumference 过渡到目标值）
- hover 交互：悬浮段外扩 + 阴影光晕，中心文字从"总数值"切换为"段名 + 值 + 占比"
- 双环（余额、费用）内外环颜色从属关系：外环使用标准色，内环使用同色系 HSL 明度偏浅变体
- 单环（Token 消耗、活跃厂商）使用 ECharts 内置 tooltip 和图例
- 主内容区 `.main-content` 滚动条贴边：padding 从滚动容器移至内层 wrapper
- 主内容区滚动条样式定制：细黑条 + hover 变橙色，匹配 neo-brutalist 风格

## Capabilities

### New Capabilities
- `scrollbar-styling`: 主内容区滚动条贴边布局和 neo-brutalist 风格自定义样式

### Modified Capabilities
- `ring-gauge-dashboard`: 渲染方式从手绘 SVG 改为 ECharts Pie 环形图；新增段间留白、圆角、入场动画、hover 中心切换、tooltip；颜色策略增加双环从属关系（HSL 明度变体）

## Impact

- **前端组件**: `RingGaugeCard.vue` 完全重写内部实现（props 接口不变），`DashboardView.vue` 无需改动
- **App.vue**: `main-content` 结构需拆分为外层滚动容器 + 内层 padding wrapper
- **style.css**: 新增自定义滚动条样式（`::-webkit-scrollbar` + `scrollbar-width`）
- **依赖**: 无新增依赖（ECharts 6 已在项目中）
- **现有 spec**: `openspec/specs/ring-gauge-dashboard/spec.md` 中 "SVG stroke-dasharray implementation" 和 "No external chart library required" 两条需求将被替换
