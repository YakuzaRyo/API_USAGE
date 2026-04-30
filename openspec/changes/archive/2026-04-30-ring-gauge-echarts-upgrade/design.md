## Context

当前 `RingGaugeCard.vue` 使用手绘 SVG `<circle>` + `stroke-dasharray` 画弧线，无 tooltip、无动画、无 hover 反馈、段间无间距。项目已在 `BalanceView.vue`、`DashboardView.vue`（趋势图/分布图）中使用 ECharts 6，具备成熟的 `init → setOption → resize → dispose` 模式。主内容区 `.main-content` 的 `overflow-y: auto` + 四面 `padding: 32px` 导致浏览器滚动条未贴边（距视口右边缘 32px），且默认灰色样式与 neo-brutalist 设计不协调。

## Goals / Non-Goals

**Goals:**
- 将 4 张环形卡片从手绘 SVG 改为 ECharts Pie 渲染，统一项目图表风格
- 增加段间留白、圆角、入场动画、hover 中心文字切换、tooltip
- 双环（余额、费用）实现内外环颜色从属关系（外环标准色，内环 HSL 明度偏浅）
- 修复主内容区滚动条不贴边问题，并定制为 neo-brutalist 风格

**Non-Goals:**
- 不引入新的图表库依赖（ECharts 已满足需求）
- 不改变 `RingGaugeCard` 的 props 接口（`title`, `segments`, `innerSegments`, `formatValue`, `totalOverride`）
- 不改变 `DashboardView.vue` 中 4 张卡片的调用方式
- 不做暗色主题适配（当前只有浅色主题）
- 不做响应式断点调整（保持现有 768px 断点）

## Decisions

### D1: ECharts Pie series 替代手绘 SVG

**选择**: 在 `RingGaugeCard.vue` 内部用 `echarts.init()` 渲染 pie 环形图

**替代方案**:
- 保持 SVG 手绘 + CSS 增强样式：无法获得 tooltip、legend 联动、内置动画，开发量更大且效果不如 ECharts
- 使用其他图表库（Chart.js、D3）：引入新依赖，与项目现有 ECharts 不一致

**理由**: ECharts 6 已是项目依赖，pie 系列 `radius` 配置原生支持环形/双环，tooltip/legend/animation 全部内置，与 `BalanceView` 等已有图表风格一致。

### D2: 单环配置 — 一个 pie series

```
series: [{
  type: 'pie',
  radius: ['55%', '80%'],     // 内径 55%，外径 80%
  padAngle: 3,                // 段间 3° 留白
  itemStyle: {
    borderRadius: 6,          // 圆角端点
    borderColor: '#fff',
    borderWidth: 2,
  },
  emphasis: {
    scale: true,
    scaleSize: 6,
    itemStyle: { shadowBlur: 20, shadowColor: 'rgba(0,0,0,0.3)' },
    label: { show: true, position: 'center', formatter: '{b}\n{d}%', fontSize: 16, fontWeight: 700 },
  },
  label: { show: false },
  animationType: 'scale',
  animationDuration: 800,
  animationEasing: 'cubicOut',
}]
```

### D3: 双环配置 — 两个 pie series 叠加

外环（分类维度）和内环（厂商维度）作为两个独立 pie series 共享同一 `center`：

```
series: [
  { name: 'outer', radius: ['62%', '80%'], ... },  // 外环
  { name: 'inner', radius: ['35%', '55%'], ... },  // 内环
]
```

tooltip 的 `formatter` 通过 `seriesName` 区分外环/内环数据来源。

### D4: 中心文字 — ECharts graphic 组件

默认状态用 `graphic` 组件在中心渲染总数值 + 标题。hover 某段时，通过监听 ECharts 的 `mouseover`/`mouseout` 事件动态更新 `graphic` 子元素文字，从"总数值"切换为"段名 + 值 + 占比"。

**替代方案**: HTML overlay（绝对定位 div 叠在 ECharts 容器上）——简单但与 ECharts 动画/resize 不联动，需手动同步位置。

### D5: 颜色从属关系 — HSL 明度偏浅

外环段使用标准 COLORS 数组色值。内环段根据其所属外环分类的颜色，使用 HSL 明度偏浅变体：

```typescript
function lighten(hex: string, amount: number): string {
  // hex → HSL → L + amount → hex
  // amount: 0.15 ~ 0.25
}
```

同一外环分类下的多个内环段，按顺序递增明度偏移量（+15%, +25%, +35%...），形成层次感。

### D6: 滚动条贴边 — 拆分 padding 层

将 `App.vue` 中 `.main-content` 的 padding 从滚动容器移至内层 wrapper：

```html
<main class="main-content">      <!-- overflow-y: auto, 无 padding -->
  <div class="main-inner">       <!-- padding: var(--space-xl) -->
    <RouterView />
  </div>
</main>
```

这样滚动条贴到 `.main-content` 右边缘（= 视口右边缘），内容仍有 32px 内边距。

### D7: 滚动条样式 — Neo-Brutalist 风格

```css
.main-content::-webkit-scrollbar { width: 6px; }
.main-content::-webkit-scrollbar-track { background: transparent; }
.main-content::-webkit-scrollbar-thumb { background: #1A1A1A; border-radius: 0; }
.main-content::-webkit-scrollbar-thumb:hover { background: #FF6B35; }
/* Firefox */
.main-content { scrollbar-width: thin; scrollbar-color: #1A1A1A transparent; }
```

6px 宽、直角、黑色，hover 变橙色（`--color-primary`），匹配 neo-brutalist 硬边风格。

## Risks / Trade-offs

**[ECharts 实例体积]** → 每张卡片各创建一个 ECharts 实例，4 张卡片共 4 个实例。ECharts 已在页面其他图表使用，tree-shaking 后增量体积可忽略。需确保组件卸载时 `dispose()` 清理。

**[Props 接口兼容]** → `RingGaugeCard` 的 props 接口保持不变，`DashboardView` 无需改动。但内部实现完全重写，需验证 4 张卡片的渲染效果与现有数据兼容。

**[颜色从属计算]** → HSL 明度偏浅需要 hex↔HSL 转换工具函数。极端情况下明度偏移可能超过 100%（底色已经很浅），需 clamp 到 85%。

**[滚动条跨浏览器]** → `::-webkit-scrollbar` 覆盖 Chrome/Edge/Safari，`scrollbar-width` + `scrollbar-color` 覆盖 Firefox。Firefox 不支持自定义宽度/圆角，滚动条外观会有细微差异但功能不受影响。

**[动画性能]** → 4 个 ECharts 实例同时播放入场动画可能在低端设备上有性能影响。可通过 `animationDelay` 错开各卡片动画时间，或检测 `prefers-reduced-motion` 跳过动画。
