# Balance History

## Purpose

Tracks balance changes over time for LLM providers. Persists a balance snapshot at each collection and exposes a time-series API for charting. The frontend renders per-provider line charts with legend-based provider filtering and configurable date ranges.

## ADDED Requirements

### Requirement: Balance snapshot storage
The system SHALL persist a balance value in each `CollectionLog` row when a balance API call succeeds during collection.

#### Scenario: Balance collected successfully
- **WHEN** the collector successfully parses a balance value from the provider's balance API response
- **THEN** a `CollectionLog` row is inserted with `balance = <parsed value>` alongside the existing status and record_count fields

#### Scenario: Balance API fails
- **WHEN** the balance API call returns an error or times out
- **THEN** a `CollectionLog` row is inserted without a balance value (null)

### Requirement: Balance history API
The system SHALL expose an endpoint returning balance time-series data for charting, supporting per-provider filtering and date range constraints.

#### Scenario: Default query (last 30 days, all providers)
- **WHEN** GET /api/stats/balance-history is called without parameters
- **THEN** balance snapshots from the last 30 days for all active providers are returned, each with date, provider_name, and balance

#### Scenario: Provider filter
- **WHEN** GET /api/stats/balance-history?provider_id=1 is called
- **THEN** only balance snapshots for provider 1 are returned

#### Scenario: Custom date range
- **WHEN** GET /api/stats/balance-history?start=2026-04-01&end=2026-04-15 is called
- **THEN** only balance snapshots within that date range are returned

#### Scenario: No data
- **WHEN** no balance snapshots exist (e.g. no provider has been collected yet)
- **THEN** an empty array is returned with HTTP 200

### Requirement: Per-provider line chart with legend toggle
The balance history view SHALL render one line per provider on a shared ECharts time-series chart. The chart legend supports click-to-toggle for individual providers.

#### Scenario: Multiple providers displayed
- **WHEN** the balance history API returns data for 3 providers
- **THEN** 3 separate colored lines are rendered on the chart, each annotated with the provider name in the legend

#### Scenario: Click legend to hide a provider
- **WHEN** user clicks a provider name in the chart legend
- **THEN** that provider's line disappears from the chart and its legend entry turns gray

#### Scenario: Click legend again to show a provider
- **WHEN** user clicks a grayed-out legend entry
- **THEN** the provider's line reappears and its legend entry returns to color

### Requirement: Tooltip with consumption rate
The chart tooltip SHALL display the current balance value, the delta from the previous collection point, and the consumption rate.

#### Scenario: Hover over a data point
- **WHEN** user hovers over a balance data point
- **THEN** the tooltip shows provider name, balance value, delta from previous point (absolute + percentage), and consumption rate per hour

### Requirement: Date range filter
The balance view SHALL provide date inputs to narrow the chart's visible time window, defaulting to the last 30 days.

#### Scenario: Default view
- **WHEN** the balance view first loads
- **THEN** the chart shows the last 30 days of data with start date pre-set to 30 days ago and end date to today

#### Scenario: Custom date range
- **WHEN** user changes the start or end date input
- **THEN** the chart and data are re-fetched for the selected date range

### Requirement: Dashboard integration with Pill selector
The Dashboard SHALL render a PillModeSelector allowing users to switch between the existing usage dashboard and the new balance view, without changing URL routes.

#### Scenario: Pill switches to balance view
- **WHEN** user clicks the "余额变化" capsule
- **THEN** the dashboard content area shows the balance history chart, and the existing token/cost charts are hidden

#### Scenario: Pill switches to usage dashboard
- **WHEN** user clicks the "用量看板" capsule
- **THEN** the dashboard content area shows the original stats cards and usage trend/distribution charts
