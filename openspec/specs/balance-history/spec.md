# Balance History

## Purpose

Tracks balance changes over time for LLM providers. Persists a balance snapshot at each collection and exposes a time-series API for charting. The frontend renders per-provider line charts with legend-based provider filtering and configurable date ranges.

## Requirements

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

### Requirement: Time pill presets use three sliding windows
The balance chart SHALL provide exactly three time-window presets: 当天 (1 day), 7天 (7 days), and 30天 (30 days). Each window is a sliding window whose right edge is the current time (ceiling-aligned to the next bucket boundary), and whose left edge is the right edge minus the window duration, aligned to a bucket boundary.

#### Scenario: Default view uses 7-day window
- **WHEN** the balance view first loads
- **THEN** the 7天 pill is active, and the chart window spans from 7 days ago to now

#### Scenario: Switch to one-day window
- **WHEN** user clicks the 当天 pill
- **THEN** the chart window spans from 24 hours ago to now, with bucket size 1 hour

#### Scenario: Switch to 30-day window
- **WHEN** user clicks the 30天 pill
- **THEN** the chart window spans from 30 days ago to now, with bucket size 1 day (24 hours)

### Requirement: Bucket size scales proportionally with window size
The bucket (aggregation interval) SHALL scale linearly between 1 hour (at 1-day window) and 24 hours (at 30-day window).

#### Scenario: Bucket size for each pill
- **WHEN** the active pill is 当天 (1 day)
- **THEN** bucket size is 3,600,000 ms (1 hour)
- **WHEN** the active pill is 7天 (7 days)
- **THEN** bucket size is approximately 20,738,000 ms (~5.76 hours), computed as `1h + (24h - 1h) × (7 - 1) / (30 - 1)`
- **WHEN** the active pill is 30天 (30 days)
- **THEN** bucket size is 86,400,000 ms (24 hours)

#### Scenario: All three pills produce chart data
- **WHEN** balance history data exists spanning at least 30 days
- **THEN** all three pills render a line chart with at least one data point per bucket period

### Requirement: Per-provider line chart with full-window bucket-anchored rendering
The balance history chart SHALL render one line per provider on a shared ECharts time-series chart. The X-axis SHALL span the full sliding window. Every bucket position within the window SHALL have a data point — y=0 for empty buckets, actual consumption value for buckets with data. The Y-axis SHALL have its lower bound fixed at 0 and its upper bound automatically scaled. The chart legend SHALL support click-to-toggle for individual providers.

#### Scenario: Full-window bucket fill
- **WHEN** the chart renders with a 24-hour window and 1-hour buckets
- **THEN** each series contains exactly 25 points (one per bucket from window start to window end), with y=0 for buckets without consumption

#### Scenario: Multiple providers displayed
- **WHEN** the balance history API returns data for 3 providers
- **THEN** 3 separate colored lines are rendered on the chart, each spanning the full window and annotated with the provider name in the legend

#### Scenario: Click legend to hide a provider
- **WHEN** user clicks a provider name in the chart legend
- **THEN** that provider's line disappears from the chart and its legend entry turns gray

#### Scenario: Click legend again to show a provider
- **WHEN** user clicks a grayed-out legend entry
- **THEN** the provider's line reappears and its legend entry returns to color

#### Scenario: Y-axis lower bound is always zero
- **WHEN** the chart renders with any data
- **THEN** the Y-axis starts at 0 and its upper bound scales automatically to fit the data

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
