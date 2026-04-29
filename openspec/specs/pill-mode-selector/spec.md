# Pill Mode Selector

## Purpose

A lightweight dual-option toggle component for switching between two view modes. Uses capsule-shaped buttons with scale transitions and a typewriter description effect, anchored at the top-right of a host card via absolute positioning.

## ADDED Requirements

### Requirement: Capsule button pair
The component SHALL render two capsule-shaped buttons horizontally aligned with a 8px gap. Each button supports an active/inactive visual state via scale transform.

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

### Requirement: Typewriter description
The component SHALL display a description string below the capsule pair. When the selected option changes, the old description is cleared and the new one appears character by character.

#### Scenario: Description animates on switch
- **WHEN** selected mode changes from A to B
- **THEN** the old description is immediately cleared, and the new description appears at 50ms per character

#### Scenario: Rapid toggle interrupts previous animation
- **WHEN** user switches modes twice within 200ms
- **THEN** the first typewriter interval is cancelled and only the final mode's description animates

### Requirement: Responsive positioning
The component SHALL position absolutely at the host card's top-right corner on viewports wider than 768px. On narrower viewports it shall fall back to static document flow.

#### Scenario: Desktop layout
- **WHEN** viewport width > 768px
- **THEN** the selector is positioned at `top: var(--space-md); right: var(--space-md)` with `position: absolute`

#### Scenario: Mobile layout
- **WHEN** viewport width ≤ 768px
- **THEN** the selector uses `position: static` and appears below the card title
