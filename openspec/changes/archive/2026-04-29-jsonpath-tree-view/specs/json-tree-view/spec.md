## ADDED Requirements

### Requirement: JSON tree rendering
The component SHALL render a JSON value as a recursive, indented tree structure instead of a flat tag list. Each node displays its key and value according to type.

#### Scenario: Object node
- **WHEN** a JSON object is rendered
- **THEN** the object's keys appear as child rows indented under the parent, with a collapsed/expanded state toggle

#### Scenario: Array node
- **WHEN** a JSON array is rendered
- **THEN** array elements appear as `[0]`, `[1]`, ... child rows indented under the parent

#### Scenario: Leaf node
- **WHEN** a leaf value (string/number/boolean/null) is rendered
- **THEN** the key is shown in default text and the value in muted gray, truncated to 30 characters with full text in the title attribute

### Requirement: Default expand depth
The tree SHALL default to expanding the first 2 levels of nesting. Deeper nodes start collapsed.

#### Scenario: Deep nesting
- **WHEN** JSON has more than 2 levels of nesting
- **THEN** only the top 2 levels are expanded; deeper nodes show a collapsed indicator and expand on click

### Requirement: Click emits JSONPath
Clicking any key in the tree SHALL emit a `select` event with the full JSONPath from the root to that key.

#### Scenario: Click leaf key
- **WHEN** user clicks the key "total_usage" inside `data[0]`
- **THEN** `{ path: "data.0.total_usage" }` is emitted

#### Scenario: Click non-leaf key
- **WHEN** user clicks an object or array key
- **THEN** the node toggles expand/collapse AND the `select` event is emitted with that key's path

### Requirement: Raw JSON toggle
The component SHALL provide a collapsible toggle to view the raw JSON text. It defaults to collapsed.

#### Scenario: Toggle raw JSON
- **WHEN** user clicks "查看原始 JSON"
- **THEN** the raw formatted JSON string is displayed in a pre block

### Requirement: Tag-container mapping input
Mapping input fields SHALL display selected JSONPath values as removable tag-style chips rather than as plain text in a text input.

#### Scenario: Path filled as tag
- **WHEN** a JSON tree key is clicked while a mapping input is focused
- **THEN** the mapping input shows a tag with the path text and an × button

#### Scenario: Tag removed
- **WHEN** user clicks the × on a mapping tag
- **THEN** the tag is removed and the field value is cleared
