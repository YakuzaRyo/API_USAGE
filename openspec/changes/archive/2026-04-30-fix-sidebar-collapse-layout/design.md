## Context

The app uses a flex layout: `#app { display: flex }` with `<aside>` (sidebar) and `<main>` (content area) as direct children. The sidebar has `flex-shrink: 0` and transitions between 200px and 52px. The content area has `flex: 1` and correctly expands when the sidebar collapses. However, `.main-inner` (the child of `.main-content`) has `max-width: 1200px`, which prevents visible content from growing beyond that width. This makes the collapse feature visually broken — content shifts left instead of expanding.

## Goals / Non-Goals

**Goals:**
- Content area visually fills the full width when sidebar collapses
- ECharts charts resize to match the new container width after sidebar transition

**Non-Goals:**
- Changing the sidebar collapse/expand animation or behavior
- Adding responsive breakpoints or mobile-specific layout changes
- Changing the backend or API

## Decisions

### Remove `max-width: 1200px` from `.main-inner`

**Choice**: Remove the constraint entirely.

**Alternative considered**: Keep `max-width` but add `margin: 0 auto` to center content. This would leave visible empty space on both sides, which defeats the purpose of collapsing the sidebar — the user collapses to reclaim space.

**Rationale**: The sidebar collapse feature's whole purpose is to give more room to content. Capping content at 1200px while the viewport may be 1920px+ wastes that reclaimed space. The ring gauge grid (`repeat(2, 1fr)`) and chart containers (`width: 100%`) already handle wider layouts gracefully.

### No additional ECharts resize logic needed

The existing chain works: `transitionend` → `window.dispatchEvent(new Event('resize'))` → each chart's `onResize` handler calls `chart?.resize()`. Once `max-width` is removed, the containers will be wider and charts will actually grow when resized.

## Risks / Trade-offs

- **Very wide content on ultra-wide monitors**: Without `max-width`, a 4K display would show ring gauges and charts stretched very wide. → Acceptable: the user chose to collapse the sidebar for this exact reason. The 2-column ring grid and chart containers look fine at wider widths.
- **No migration needed**: Single CSS property change, no data or API changes.
