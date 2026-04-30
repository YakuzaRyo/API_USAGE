## Context

The app uses a fixed 200px sidebar (`App.vue`) alongside a flex-grow main content area. Layout is `#app { display: flex }`. The sidebar contains a brand heading and 3 RouterLink nav items. All nav items are text-only — no icons are used anywhere in the project yet.

ECharts instances in `DashboardView`, `BalanceView`, and `RingGaugeCard` all bind `window.addEventListener('resize', ...)` for responsive chart sizing.

Neo-Brutalist design system: solid 2px borders, offset box-shadows, `border-radius: 0`, hover "float up" effects.

## Goals / Non-Goals

**Goals:**
- Sidebar toggles between 200px (expanded, icon + text) and 52px (collapsed, icon-only)
- Toggle button is hidden by default, appears on sidebar hover
- Button position: inside right edge when expanded, outside right edge when collapsed
- Collapsed state persists across page reloads via `localStorage`
- ECharts charts resize correctly after sidebar width transitions

**Non-Goals:**
- Mobile / responsive sidebar (not in scope — desktop-only for now)
- Overlay / drawer mode
- Keyboard shortcut for toggling

## Decisions

### 1. Icon library: `lucide-vue-next`

**Choice:** `lucide-vue-next`
**Alternatives:** Unicode symbols (inconsistent cross-platform), CSS-drawn icons (maintenance burden), heroicons (heavier)
**Rationale:** Lightweight, tree-shakeable, clean line-art style that pairs well with Neo-Brutalist aesthetic. Vue 3 native components.

Icon mapping for nav items:
- 用量看板 → `LayoutDashboard`
- 厂商管理 → `Server`
- 分类管理 → `FolderOpen`

Toggle button icons: `ChevronLeft` (expanded) / `ChevronRight` (collapsed)

### 2. State management: component-local ref + localStorage

**Choice:** `ref<boolean>` in `App.vue` with `localStorage` persistence
**Alternatives:** Pinia store (overkill for single-component UI state), CSS-only via checkbox (no persistence, less control)
**Rationale:** Sidebar collapse state is purely presentational, only `App.vue` needs it. No reason to elevate to a store.

```
collapsed = ref(localStorage.getItem('sidebar-collapsed') === 'true')
watch(collapsed, v => localStorage.setItem('sidebar-collapsed', String(v)))
```

### 3. Toggle button positioning: absolute + conditional right offset

**Choice:** Button uses `position: absolute` on the sidebar (which has `position: relative`). Right offset switches between `4px` (expanded, inside edge) and `-28px` (collapsed, outside edge). Transition follows sidebar width change.
**Alternatives:** Fixed position relative to viewport (breaks on scroll), floating outside DOM (harder to manage)
**Rationale:** Keeps button as a child of sidebar, so hover detection on sidebar naturally reveals it.

### 4. ECharts resize: `transitionend` event on sidebar

**Choice:** Listen to `transitionend` on the sidebar element, then `window.dispatchEvent(new Event('resize'))`
**Alternatives:** `ResizeObserver` on `.main-inner` (more elegant but adds coupling between App.vue and content area), fixed timeout (fragile)
**Rationale:** All existing charts already listen to `window.resize`. Dispatching a synthetic resize event after the CSS transition completes triggers them without any changes to chart components.

### 5. Text hiding: `overflow: hidden` + fixed widths

**Choice:** Sidebar uses `overflow: hidden` with `width` transition. Nav item text naturally clips when width shrinks to 52px. Icons stay visible via fixed-width icon container.
**Alternatives:** Conditional `v-if` on text (causes layout jump), `opacity` toggle (text still takes space)
**Rationale:** Smoothest visual effect — text slides away as sidebar narrows. No layout jumps.

## Risks / Trade-offs

- **[ECharts flash]** → Sidebar transition is 0.15s. Charts may briefly show at old size before resize fires. Mitigation: fast transition + charts already handle resize gracefully.
- **[localStorage unavailable]** → In rare cases (private browsing), localStorage writes may throw. Mitigation: wrap in try/catch, default to expanded.
- **[New icon dependency]** → `lucide-vue-next` adds ~30KB to bundle (tree-shaken). Acceptable tradeoff for consistent iconography.
