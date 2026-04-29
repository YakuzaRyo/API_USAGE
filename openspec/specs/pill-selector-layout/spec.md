# Pill Selector Layout

## Purpose

Specifies the layout behavior of the Pill Mode Selector within the host page: left-aligned in normal document flow, replacing the page title element.

## ADDED Requirements

### Requirement: Pill replaces page title in document flow
The Pill Mode Selector SHALL render in the normal document flow (static positioning, left-aligned), replacing any separate page title element.

#### Scenario: Pill in document flow
- **WHEN** the Dashboard renders with a Pill Mode Selector
- **THEN** the pill appears at the top-left of the content area in normal flow, with its description text fully visible and not obscured by adjacent elements

### Requirement: No duplicate title
The Dashboard SHALL NOT render a separate `<h2>` title when a Pill Mode Selector is present, as the active pill label already serves as the page title.

#### Scenario: Duplicate title removed
- **WHEN** the Dashboard renders
- **THEN** no `<h2>` element appears above the dashboard content; the pill capsule label is the sole title indicator
