## 1. Dependencies

- [x] 1.1 Install `lucide-vue-next` in `frontend/`

## 2. App.vue — State & Logic

- [x] 2.1 Add `collapsed` ref with `localStorage` persistence (key: `sidebar-collapsed`, default: `false`)
- [x] 2.2 Add `toggleSidebar()` function that flips `collapsed`
- [x] 2.3 Add `transitionend` handler on sidebar element that dispatches `window.dispatchEvent(new Event('resize'))`
- [x] 2.4 Update `navItems` array to include icon component references (`LayoutDashboard`, `Server`, `FolderOpen`)

## 3. App.vue — Template

- [x] 3.1 Import and render Lucide icon components in each `RouterLink`
- [x] 3.2 Add toggle button (`ChevronLeft`/`ChevronRight`) with `@click="toggleSidebar"`
- [x] 3.3 Bind sidebar class: `:class="{ collapsed }"`
- [x] 3.4 Adapt brand: show `"LLM Usage"` when expanded, `"L"` when collapsed

## 4. App.vue — Styles

- [x] 4.1 Add `position: relative` to `.sidebar`, `overflow: hidden`, `transition: width 0.15s ease`
- [x] 4.2 Add `.sidebar.collapsed` rule: `width: 52px`
- [x] 4.3 Style `.toggle-btn`: `position: absolute`, conditional `right` offset (4px expanded / -28px collapsed), `opacity: 0` → hover `opacity: 1`, Neo-Brutalist border/shadow
- [x] 4.4 Adjust `.sidebar-brand` and `.sidebar-link` styles for collapsed state (centered icons, no text overflow)

## 5. Verification

- [x] 5.1 Run `npm run dev`, verify toggle works in both directions
- [x] 5.2 Verify `localStorage` persistence across page reloads
- [x] 5.3 Navigate to Dashboard, toggle sidebar, confirm ECharts resize correctly
- [x] 5.4 Run `npm run build` to confirm no type errors
