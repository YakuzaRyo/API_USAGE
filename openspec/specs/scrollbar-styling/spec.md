# Scrollbar Styling

## Purpose

Custom scrollbar styling for the main content area, providing a consistent Neo-Brutalist scrollbar appearance across Chromium and Firefox browsers with the scrollbar flush against the viewport edge.

## Requirements

### Requirement: Scrollbar flush with viewport edge
The main content area scrollbar SHALL be positioned flush against the right edge of the viewport. The `.main-content` element SHALL have `overflow-y: auto` with no right padding; an inner wrapper element SHALL apply the content padding instead.

#### Scenario: Scrollbar at viewport edge
- **WHEN** the page is rendered at any viewport width
- **THEN** the scrollbar thumb and track are visually flush with the right edge of the viewport with no gap

#### Scenario: Content retains padding
- **WHEN** the main content area is rendered
- **THEN** all child content has `var(--space-xl)` padding on all four sides via the inner wrapper

### Requirement: Neo-Brutalist scrollbar style on Chromium browsers
On Chromium-based browsers (Chrome, Edge), the scrollbar SHALL use `::-webkit-scrollbar` pseudo-elements with a 6px thin black track, zero-radius thumb matching `--color-border`, and hover state matching `--color-primary`.

#### Scenario: Default scrollbar appearance
- **WHEN** content overflows vertically in the main content area on a Chromium browser
- **THEN** the scrollbar track is transparent and the thumb is 6px wide, black (`--color-border`), with no border-radius

#### Scenario: Scrollbar hover state
- **WHEN** the user hovers over the scrollbar thumb
- **THEN** the thumb color changes to `--color-primary` (#FF6B35)

### Requirement: Firefox scrollbar style
On Firefox, the scrollbar SHALL use `scrollbar-width: thin` and `scrollbar-color` with the same color scheme as Chromium (black thumb, transparent track).

#### Scenario: Firefox scrollbar rendering
- **WHEN** the page is viewed in Firefox
- **THEN** the scrollbar is thin with a black thumb and transparent track
