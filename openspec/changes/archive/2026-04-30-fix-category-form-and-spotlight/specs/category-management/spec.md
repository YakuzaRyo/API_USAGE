## MODIFIED Requirements

### Requirement: Category edit modal with billing mode tabs
The category edit modal form fields SHALL use horizontal layout with label and input on the same row. Labels SHALL be right-aligned with a fixed width. Input fields SHALL fill the remaining horizontal space.

#### Scenario: Form displays fields horizontally
- **WHEN** the edit modal is opened
- **THEN** each form field shows as "Label: [input____]" on a single row, with labels right-aligned at a fixed width and inputs stretching to fill remaining space

### Requirement: Category list page with card layout
The Logo grid spotlight effect SHALL only trigger when the mouse is hovering directly on a `.logo-item` element. When the mouse is in the gap between items or in empty grid space, all logos SHALL remain in their normal (unmodified) state.

#### Scenario: Mouse in gap between logos
- **WHEN** the mouse is positioned in the gap between two logos (not on any logo)
- **THEN** all logos remain at normal scale (1.0), full opacity (1.0), and no blur

#### Scenario: Mouse hovers a specific logo
- **WHEN** the mouse hovers directly on a logo item
- **THEN** the hovered logo scales to 1.15× with full opacity, and all other logos scale to 0.75× with opacity 0.4 and blur 1px
