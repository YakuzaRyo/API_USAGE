# Ring Gauge Dashboard

## Purpose

Neo-Brutalist 风格的 ECharts 环形仪表盘组件，用于综合看板展示 4 个占比分割环形卡片（Token 消耗、活跃厂商、当前余额、费用），支持图例点击过滤和双环内外联动。

## Requirements

### Requirement: Four ring gauge cards on comprehensive dashboard
The comprehensive dashboard SHALL render four ECharts Pie-based ring gauge cards in a 2x2 grid. Each ring SHALL display proportional arc segments split by a data dimension, with a total value rendered via ECharts `graphic` component in the center. No full-ring reference value exists.

#### Scenario: Ring cards displayed
- **WHEN** the 综合看板 pill is active
- **THEN** four ECharts Pie ring gauge cards are rendered in a grid

#### Scenario: Empty state
- **WHEN** no data exists for a ring
- **THEN** the ring shows a full gray arc and the center displays 0 or "—"

### Requirement: Token consumption ring card
The Token 消耗 card SHALL display a single ECharts Pie ring split by model token share. The chart SHALL provide ECharts built-in tooltip on hover and a legend below the chart. Clicking a legend item toggles that model's visibility and recalculates proportions.

#### Scenario: Model segments
- **WHEN** token consumption data is available
- **THEN** the ring shows colored arc segments proportional to each model's token share, center shows total

#### Scenario: Tooltip interaction
- **WHEN** user hovers over a ring segment
- **THEN** a tooltip displays the model name, token value, and percentage share

### Requirement: Active provider count ring card
The 活跃厂商 card SHALL display a single ECharts Pie ring with arc segments by category's provider count.

#### Scenario: Category count segments
- **WHEN** there are providers in multiple categories
- **THEN** arcs are proportional to each category's provider count, center shows total

### Requirement: Current balance ring card (dual ring)
The 当前余额 card SHALL display two concentric ECharts Pie rings — outer by category, inner by provider. Filtering outer hides both outer segment and its inner members. Filtering inner hides only that provider.

#### Scenario: Dual ring interaction
- **WHEN** user clicks outer ring category
- **THEN** that category's outer arc and all its inner provider arcs disappear, rescaling remaining

### Requirement: Billing cost ring card (dual ring)
The 费用 card SHALL display two concentric ECharts Pie rings — outer by billing_mode, inner by provider. Same toggle interaction as balance card.

### Requirement: Neo-Brutalist visual style
Ring cards SHALL use zero-radius containers, 2px solid black borders, hard offset shadows, and bold typography. The ECharts Pie segments SHALL use `padAngle: 3` for inter-segment gaps, `borderRadius: 6` for rounded segment endpoints, and `borderColor: #fff` with `borderWidth: 2`. First segment color is `--color-primary: #FF6B35`.

### Requirement: ECharts Pie rendering implementation
Ring arcs SHALL use ECharts `pie` series with `radius` configuration for ring shape (`['55%', '80%']` for single ring, `['62%', '80%']` outer + `['35%', '55%']` inner for dual ring). Each `RingGaugeCard` instance SHALL manage its own ECharts instance lifecycle (`init`, `setOption`, `resize`, `dispose`).

#### Scenario: ECharts instance lifecycle
- **WHEN** a RingGaugeCard component is mounted
- **THEN** an ECharts instance is created on the container element

#### Scenario: ECharts cleanup
- **WHEN** a RingGaugeCard component is unmounted
- **THEN** the ECharts instance is disposed and resize listener is removed

### Requirement: Entrance animation
Ring segments SHALL animate into view with a progress-bar-style entrance (segments grow from zero to target length). Animation duration SHALL be 800ms with `cubicOut` easing.

#### Scenario: Initial render animation
- **WHEN** a ring card first renders with data
- **THEN** segments animate from zero-length to their target proportional length over 800ms

### Requirement: Hover center text switching
The center text area SHALL display the total value by default. When the user hovers over a segment, the center text SHALL switch to display the segment name, value, and percentage. When hover ends, the center text SHALL return to the total value.

#### Scenario: Default center text
- **WHEN** no segment is hovered
- **THEN** the center displays the formatted total value and card title

#### Scenario: Hovered segment center text
- **WHEN** user hovers over a segment
- **THEN** the center displays the segment name, formatted value, and percentage share

#### Scenario: Hover ends
- **WHEN** user moves cursor away from all segments
- **THEN** the center text returns to the formatted total value and card title

### Requirement: Hover segment emphasis
Hovering over a segment SHALL scale that segment outward (`scaleSize: 6`) and apply a shadow glow effect (`shadowBlur: 20`).

#### Scenario: Segment hover emphasis
- **WHEN** user hovers over a ring segment
- **THEN** the segment visually expands outward and gains a drop shadow

### Requirement: Dual ring color hierarchy (HSL lightness)
For dual-ring cards, inner ring segments SHALL use HSL lightness-shifted variants of their parent outer ring category color. Each inner segment under the same outer category SHALL receive incrementally higher lightness values (starting at +15%) to create visual hierarchy. Lightness SHALL be clamped to a maximum of 85%.

#### Scenario: Inner ring color derived from outer
- **WHEN** a dual-ring card renders with category "API服务" (outer color #FF6B35) and providers "OpenAI" and "Claude" (inner)
- **THEN** "OpenAI" inner segment uses a lighter variant of #FF6B35 (+15% lightness) and "Claude" uses an even lighter variant (+25% lightness)

#### Scenario: Lightness clamping
- **WHEN** the computed lightness exceeds 85%
- **THEN** the value is clamped to 85%
