# JSON Tree Render Fix

## Purpose

Fixes JSON tree rendering to use Vue template recursion instead of `h()` render functions, preventing main-thread freezes.

## ADDED Requirements

### Requirement: Template-based recursive tree rendering
The JSON tree component SHALL render nodes using Vue template syntax with recursive component self-reference, not via `h()` render functions mixed with `v-for`.

#### Scenario: Object renders as collapsible tree
- **WHEN** a JSON object is passed as prop
- **THEN** top-level keys render as collapsible rows with indentation, using `<JsonTreeLeaf>` recursive component

#### Scenario: No main-thread freeze
- **WHEN** a JSON response with 100+ nodes is rendered
- **THEN** the UI remains responsive with no perceptible freeze

### Requirement: Unchanged component interface
The component SHALL maintain the same props (`json: unknown`) and emits (`select { path: string }`) as before.

#### Scenario: Click emits path
- **WHEN** user clicks a key in the tree
- **THEN** `select` event is emitted with `{ path: "<JSONPath>" }` — same interface as the tag cloud
