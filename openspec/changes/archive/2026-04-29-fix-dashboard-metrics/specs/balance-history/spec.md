# Balance History

## ADDED Requirements

### Requirement: Time pill presets use three sliding windows
The balance chart SHALL provide exactly three time-window presets: 当天 (1 day), 7天 (7 days), and 30天 (30 days). Each window is a sliding window whose right edge is the current time (or the selected end date), and whose left edge is the right edge minus the window duration.

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

### Requirement: Chart X-axis range is determined by data bucket extents
The chart X-axis range SHALL be determined by the actual data bucket positions: the minimum SHALL be the earliest data bucket minus one bucket interval, and the maximum SHALL be the latest data bucket plus one bucket interval. The X-axis range SHALL NOT use the sliding window boundaries.

#### Scenario: X-axis extends one bucket before and after data
- **WHEN** a series has its first aggregated data point at bucket T_first and last at bucket T_last
- **THEN** the X-axis minimum is `T_first - bMs` and the X-axis maximum is `T_last + bMs`

#### Scenario: Multiple series with different data ranges
- **WHEN** two series have data spanning T1_first..T1_last and T2_first..T2_last respectively
- **THEN** the X-axis minimum is `min(T1_first, T2_first) - bMs` and maximum is `max(T1_last, T2_last) + bMs`

## MODIFIED Requirements

### Requirement: Per-provider line chart with per-series bucket-anchored rendering
The balance history chart SHALL render one line per provider on a shared ECharts time-series chart. For each provider series, the line MUST start from y=0 at the bucket immediately before its first data point, connect through all aggregated data points, and end at y=0 at the bucket immediately after its last data point. The Y-axis SHALL have its lower bound fixed at 0 and its upper bound automatically scaled to the data range. The chart legend SHALL support click-to-toggle for individual providers.

#### Scenario: Lines anchored at adjacent buckets
- **WHEN** a provider series has aggregated data points at buckets T_1, T_2, ..., T_n
- **THEN** the line starts at `(T_1 - bMs, 0)`, connects through each `(T_i, value_i)`, and ends at `(T_n + bMs, 0)`

#### Scenario: Multiple providers displayed
- **WHEN** the balance history API returns data for 3 providers
- **THEN** 3 separate colored lines are rendered on the chart, each starting and ending at y=0 and annotated with the provider name in the legend

#### Scenario: Click legend to hide a provider
- **WHEN** user clicks a provider name in the chart legend
- **THEN** that provider's line disappears from the chart and its legend entry turns gray

#### Scenario: Click legend again to show a provider
- **WHEN** user clicks a grayed-out legend entry
- **THEN** the provider's line reappears and its legend entry returns to color

#### Scenario: Y-axis lower bound is always zero
- **WHEN** the chart renders with any data
- **THEN** the Y-axis starts at 0 and its upper bound scales automatically to fit the data
