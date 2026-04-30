# Pill Mode Selector

## MODIFIED Requirements

### Requirement: Capsule button pair
The component SHALL render a variable number of capsule-shaped buttons horizontally aligned with an 8px gap. The number of capsules is determined by the `options` prop array. Each button supports an active/inactive visual state via scale transform.

#### Scenario: Active state
- **WHEN** a capsule is the currently selected option
- **THEN** it renders with `transform: scale(1.05)`, opacity 1, `background: var(--color-surface)`, `box-shadow: var(--shadow-sm)`, and `border: 2px solid var(--color-border)`

#### Scenario: Inactive state
- **WHEN** a capsule is not the currently selected option
- **THEN** it renders with `transform: scale(0.95)`, opacity 0.55, transparent background, and `border: 1.5px solid var(--color-border)`

#### Scenario: Click switches selection
- **WHEN** user clicks an inactive capsule
- **THEN** it becomes active, the previously active capsule becomes inactive, and `update:modelValue` is emitted with the new value

#### Scenario: Hover feedback
- **WHEN** user hovers over any capsule
- **THEN** the background transitions toward `var(--color-primary)` within 150ms

#### Scenario: Three pills in dashboard
- **WHEN** the Dashboard renders the PillModeSelector
- **THEN** three capsules are displayed: 综合看板, 用量分析, 余额变化

#### Scenario: Default selection
- **WHEN** the Dashboard first loads
- **THEN** the 综合看板 capsule is active
