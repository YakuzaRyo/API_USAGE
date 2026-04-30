## Why

The sidebar occupies 200px of horizontal space at all times. On smaller screens or when viewing ECharts-heavy dashboards, every pixel of content width matters. A collapsible sidebar lets users reclaim that space when they don't need navigation.

## What Changes

- Add a collapsed state to the sidebar that shrinks it to icon-only mode (52px wide)
- Introduce `lucide-vue-next` as the icon library for nav items and toggle button
- Toggle button appears on hover only — positioned inside the sidebar's right edge when expanded, outside when collapsed
- Sidebar collapsed state persists in `localStorage`
- ECharts charts re-resize after sidebar transition completes

## Capabilities

### New Capabilities
- `collapsible-sidebar`: Sidebar can toggle between expanded (200px, icon + text) and collapsed (52px, icon-only) modes. Toggle via a hover-reveal button. State persisted to localStorage.

### Modified Capabilities
_(none)_

## Impact

- **Frontend**: `App.vue` (layout + sidebar styles), `package.json` (new dep `lucide-vue-next`)
- **No backend changes**
- **No API changes**
- **ECharts**: Charts in `DashboardView`, `BalanceView`, `RingGaugeCard` must re-resize after sidebar width transitions — a `transitionend` → `window.dispatchEvent(resize)` hook in `App.vue` handles this
