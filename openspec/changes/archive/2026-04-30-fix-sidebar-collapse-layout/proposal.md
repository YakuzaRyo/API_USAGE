## Why

When the sidebar collapses from 200px to 52px, the main content area does not expand to fill the reclaimed space. The root cause is `.main-inner`'s `max-width: 1200px` which prevents content from growing wider than 1200px regardless of the flex container's actual width. Visually, the content shifts left with increasing empty space on the right, making the collapse feature feel broken.

## What Changes

- Remove `max-width: 1200px` from `.main-inner` in `App.vue` so content fills the available flex space
- Ensure ECharts charts resize correctly when the sidebar transitions (verify the existing `transitionend` → `window resize` chain works with unconstrained width)

## Capabilities

### New Capabilities
_(none)_

### Modified Capabilities
- `collapsible-sidebar`: Content area must expand and fill the full width when sidebar collapses, not just shift left

## Impact

- **Frontend only**: `App.vue` (single CSS property change), possible minor adjustments in chart container styles
- **No backend changes**
- **No API changes**
