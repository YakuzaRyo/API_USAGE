## 1. Scrollbar: Layout Restructure

- [x] 1.1 In `App.vue`, wrap `<RouterView />` inside a `<div class="main-inner">` within `.main-content`
- [x] 1.2 Move `padding: var(--space-xl)` from `.main-content` to `.main-inner`, remove padding from `.main-content`

## 2. Scrollbar: Neo-Brutalist Style

- [x] 2.1 Add `::-webkit-scrollbar` rules to `.main-content` in `style.css`: 6px width, transparent track, black thumb, no border-radius
- [x] 2.2 Add `::-webkit-scrollbar-thumb:hover` rule: color changes to `--color-primary` (#FF6B35)
- [x] 2.3 Add Firefox fallback: `scrollbar-width: thin; scrollbar-color: var(--color-border) transparent;` on `.main-content`

## 3. Color Utility

- [x] 3.1 Create `lighten(hex, amount)` utility function in `RingGaugeCard.vue` (or a shared util file) that converts hex → HSL → increases lightness by `amount` (0–1) → clamps to max 85% → returns hex
- [x] 3.2 Create `deriveInnerColors(outerSegments, innerSegments)` function that maps each inner segment to its parent outer segment's color lightened, incrementing the offset (+15%, +25%, +35%…) for siblings under the same outer category

## 4. RingGaugeCard: ECharts Single Ring

- [x] 4.1 Remove all SVG-related code from `RingGaugeCard.vue` (template `<svg>`, `ringArcs` function, SVG circles, CSS for ring-svg/ring-center)
- [x] 4.2 Add a `<div ref="chartRef">` container in template for ECharts mounting
- [x] 4.3 Implement `echarts.init()` on mount, `dispose()` on unmount, `resize` on window resize
- [x] 4.4 Implement `buildOption()` that generates ECharts pie config for single ring: `radius: ['55%', '80%']`, `padAngle: 3`, `borderRadius: 6`, `borderColor: '#fff'`, `borderWidth: 2`
- [x] 4.5 Configure entrance animation: `animationType: 'scale'`, `animationDuration: 800`, `animationEasing: 'cubicOut'`
- [x] 4.6 Configure emphasis: `scale: true, scaleSize: 6`, `shadowBlur: 20`, `shadowColor: 'rgba(0,0,0,0.3)'`
- [x] 4.7 Add ECharts `graphic` component for center text (total value + title), styled with bold weight
- [x] 4.8 Listen to `mouseover`/`mouseout` events to dynamically switch center text from total to hovered segment info (name + value + percentage)

## 5. RingGaugeCard: ECharts Dual Ring

- [x] 5.1 Extend `buildOption()` for dual-ring mode: two pie series sharing `center`, outer `radius: ['62%', '80%']`, inner `radius: ['35%', '55%']`
- [x] 5.2 Apply `deriveInnerColors()` to inner ring data so inner segments use lightened variants of their parent outer color
- [x] 5.3 Configure tooltip `formatter` that uses `seriesName` to distinguish outer vs inner ring data in the tooltip content

## 6. RingGaugeCard: Legend and Tooltip

- [x] 6.1 Enable ECharts built-in tooltip with `trigger: 'item'` showing name, formatted value, and percentage
- [x] 6.2 Configure ECharts legend at bottom with `type: 'scroll'` for long model lists, matching current toggle behavior
- [x] 6.3 Remove the old hand-drawn legend HTML/CSS from the template

## 7. Cleanup and Verification

- [x] 7.1 Remove unused CSS from `RingGaugeCard.vue` scoped styles (`.ring-svg`, `.ring-center`, `.ring-value`, `.ring-legend`, `.legend-*` classes)
- [x] 7.2 Verify all 4 ring cards render correctly in the dashboard with sample data (Token消耗 single ring, 活跃厂商 single ring, 当前余额 dual ring, 费用 dual ring)
- [x] 7.3 Verify scrollbar is flush with viewport edge on Windows Chrome/Edge and Firefox
- [x] 7.4 Verify entrance animation plays on page load and hover center text switching works on all 4 cards
