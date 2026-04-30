## ADDED Requirements

### Requirement: Sidebar toggle between expanded and collapsed modes
The sidebar SHALL support two visual states: expanded (200px, icon + text label per nav item) and collapsed (52px, icon only). The collapsed state SHALL hide nav item text via `overflow: hidden` on the sidebar container.

#### Scenario: Initial load with no saved preference
- **WHEN** the app loads and `localStorage` has no `sidebar-collapsed` key
- **THEN** the sidebar SHALL render in expanded mode (200px)

#### Scenario: Initial load with saved collapsed preference
- **WHEN** the app loads and `localStorage` has `sidebar-collapsed` set to `"true"`
- **THEN** the sidebar SHALL render in collapsed mode (52px)

#### Scenario: Toggle from expanded to collapsed
- **WHEN** user clicks the toggle button while sidebar is expanded
- **THEN** the sidebar SHALL transition to 52px width over 0.15s and `localStorage` SHALL be updated to `"true"`

#### Scenario: Toggle from collapsed to expanded
- **WHEN** user clicks the toggle button while sidebar is collapsed
- **THEN** the sidebar SHALL transition to 200px width over 0.15s and `localStorage` SHALL be updated to `"false"`

### Requirement: Toggle button visibility and positioning
The toggle button SHALL be hidden by default (`opacity: 0`) and SHALL become fully visible (`opacity: 1`) when the user hovers over the sidebar area. The button SHALL use `position: absolute` within the sidebar.

#### Scenario: Toggle button position in expanded state
- **WHEN** sidebar is expanded and user hovers over the sidebar
- **THEN** the toggle button SHALL appear near the right inner edge of the sidebar, displaying a left-pointing chevron icon

#### Scenario: Toggle button position in collapsed state
- **WHEN** sidebar is collapsed and user hovers over the sidebar
- **THEN** the toggle button SHALL appear to the right of the sidebar's outer edge, displaying a right-pointing chevron icon

#### Scenario: Toggle button hidden when not hovering
- **WHEN** the user's cursor is not over the sidebar
- **THEN** the toggle button SHALL have `opacity: 0`

### Requirement: Nav item icons
Each nav item SHALL display a `lucide-vue-next` icon component alongside its text label. In collapsed mode, only the icon SHALL be visible (text clipped by `overflow: hidden`).

#### Scenario: Icon mapping
- **WHEN** the sidebar renders
- **THEN** each nav item SHALL display its assigned icon: 用量看板 → `LayoutDashboard`, 厂商管理 → `Server`, 分类管理 → `FolderOpen`

#### Scenario: Collapsed mode shows icons only
- **WHEN** sidebar is in collapsed mode (52px)
- **THEN** nav item text SHALL be clipped and only icons SHALL be fully visible

### Requirement: ECharts resize on sidebar transition
When the sidebar width transition completes, the system SHALL dispatch a synthetic `resize` event on `window` so that all ECharts instances re-calculate their dimensions.

#### Scenario: Charts resize after collapse
- **WHEN** sidebar transition from expanded to collapsed completes
- **THEN** a `resize` event SHALL be dispatched on `window`, causing all visible ECharts instances to resize to the wider content area

#### Scenario: Charts resize after expand
- **WHEN** sidebar transition from collapsed to expanded completes
- **THEN** a `resize` event SHALL be dispatched on `window`, causing all visible ECharts instances to resize to the narrower content area

### Requirement: Brand display adapts to sidebar state
The sidebar brand area SHALL display "LLM Usage" in expanded mode and the letter "L" in collapsed mode.

#### Scenario: Expanded brand
- **WHEN** sidebar is expanded
- **THEN** the brand area SHALL display the text "LLM Usage"

#### Scenario: Collapsed brand
- **WHEN** sidebar is collapsed
- **THEN** the brand area SHALL display only the letter "L"
