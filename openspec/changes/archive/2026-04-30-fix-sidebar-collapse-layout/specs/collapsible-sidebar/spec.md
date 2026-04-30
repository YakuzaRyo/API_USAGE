## MODIFIED Requirements

### Requirement: ECharts resize on sidebar transition
When the sidebar width transition completes, the system SHALL dispatch a synthetic `resize` event on `window` so that all ECharts instances re-calculate their dimensions. The main content area SHALL expand to fill all available horizontal space (no `max-width` constraint on `.main-inner`), ensuring charts visually grow wider when the sidebar collapses.

#### Scenario: Charts resize after collapse
- **WHEN** sidebar transition from expanded to collapsed completes
- **THEN** a `resize` event SHALL be dispatched on `window`, the main content area SHALL occupy the full remaining viewport width, and all visible ECharts instances SHALL resize to match the wider container

#### Scenario: Charts resize after expand
- **WHEN** sidebar transition from collapsed to expanded completes
- **THEN** a `resize` event SHALL be dispatched on `window`, the main content area SHALL shrink to the narrower available width, and all visible ECharts instances SHALL resize to match the narrower container

#### Scenario: Content fills available width at all sidebar states
- **WHEN** the sidebar is in either expanded or collapsed state
- **THEN** the `.main-inner` container SHALL NOT have a `max-width` constraint that prevents it from filling the `.main-content` area, and visible content (grids, charts, cards) SHALL expand to fill the full width
