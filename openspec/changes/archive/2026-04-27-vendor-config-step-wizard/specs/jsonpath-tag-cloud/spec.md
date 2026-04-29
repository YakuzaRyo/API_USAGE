## ADDED Requirements

### Requirement: Parse JSON into leaf paths
The tag cloud component SHALL recursively traverse an arbitrary JSON object and extract all leaf-node paths using dot notation. A leaf node is defined as any value of type `string`, `number`, `boolean`, or `null`.

#### Scenario: Parse nested object
- **WHEN** given `{ "data": { "total": 100, "name": "test" } }`
- **THEN** paths `["data.total", "data.name"]` are extracted

#### Scenario: Parse array
- **WHEN** given `{ "items": [{ "id": 1 }, { "id": 2 }] }`
- **THEN** paths `["items.0.id", "items.1.id"]` are extracted

#### Scenario: Parse empty object
- **WHEN** given `{}`
- **THEN** an empty array `[]` is returned

#### Scenario: Parse null value
- **WHEN** given `{ "key": null }`
- **THEN** paths `["key"]` is extracted (null is a leaf)

### Requirement: Render paths as clickable tags
The component SHALL render each extracted path as an inline tag element. Tags are displayed in a flexible wrap layout with a small gap between them.

#### Scenario: Tag click emits select event
- **WHEN** user clicks a tag with path `data.0.total_usage`
- **THEN** a `select` event is emitted with payload `{ path: "data.0.total_usage" }`

#### Scenario: Tags are sorted by depth
- **WHEN** tags are rendered
- **THEN** shallower paths (fewer `.` segments) appear before deeper paths

### Requirement: Limit displayed paths
The component SHALL display at most 50 leaf paths. If the JSON contains more than 50 leaf nodes, only the first 50 (sorted by depth) are shown.

#### Scenario: Exceed 50 leaf nodes
- **WHEN** JSON response contains 60 leaf nodes
- **THEN** only 50 tags are rendered and a hint text "显示前 50 个路径" is shown

### Requirement: Visual style
Tags SHALL use a style consistent with the existing `.tag` CSS class: small, rounded, with a background subtle fill and a border matching `var(--color-border)`. Tags are interactive — hover changes the background to `var(--color-primary)` with a transition.

#### Scenario: Tag hover state
- **WHEN** user hovers over a tag
- **THEN** the tag background transitions to `var(--color-primary)` and text color to white within 150ms

### Requirement: No target hint
If the parent page has no focused mapping input when a tag is clicked, a temporary hint message SHALL be displayed.

#### Scenario: Click tag with no focused input
- **WHEN** user clicks a tag but no mapping input is currently focused
- **THEN** a hint text "请先点击目标输入框" appears near the tag cloud and fades out after 2 seconds
