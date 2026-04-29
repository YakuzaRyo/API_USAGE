# Balance Consumption Chart

## Purpose

Replace the raw balance line chart with a smooth consumption-rate curve derived from balance history. Display per-time-bucket spending amount with preset granularity pills and a date picker in a card-fixed header bar.

## ADDED Requirements

### Requirement: Consumption data transformation
The system SHALL transform raw balance history into consumption-per-bucket data on the client side. Balance points are sorted by date, adjacent differences computed (previous minus current), positive differences summed into time buckets defined by the selected granularity.

#### Scenario: Compute consumption from balance sequence
- **WHEN** balance history contains `[(t0, 10.0), (t1, 9.8), (t2, 9.5), (t3, 9.5)]`
- **THEN** the computed consumption is `[(t0-t1_bucket, 0.2), (t1-t2_bucket, 0.3)]` and the zero-diff point `(t2-t3, 0.0)` is excluded

#### Scenario: Multiple balance changes within same bucket
- **WHEN** two balance decreases of 0.2 and 0.3 fall within the same time bucket
- **THEN** the bucket's consumption value is 0.5 (the sum)

#### Scenario: Balance increase or no change
- **WHEN** balance increases (refill) or remains unchanged between consecutive points
- **THEN** the system SHALL exclude those intervals from the consumption data

### Requirement: Preset granularity pills
The system SHALL display four preset granularity pills in the header bar left side: 5分钟, 1小时, 7天, and 30天. Each pill sets both the time bucket size and the default date range.

| Pill | Bucket Size | Default Range |
|------|-------------|---------------|
| 5分钟 | 5 minutes | Last 5 minutes |
| 1小时 | 1 minute | Last 1 hour |
| 7天 | 1 hour | Last 7 days |
| 30天 | 1 day | Last 30 days |

#### Scenario: Click preset pill
- **WHEN** user clicks "7天" pill
- **THEN** the chart refreshes with 1-hour bucket consumption data for the last 7 days; the "7天" pill is visually active

#### Scenario: Active pill state
- **WHEN** a pill is selected
- **THEN** it displays with the primary color fill and other pills display as outlined

### Requirement: Date range picker
The system SHALL display a date range picker (start and end date inputs) in the header bar right side. The picker overrides the preset pill's date range but preserves its granularity.

#### Scenario: Custom date range with preset granularity
- **WHEN** "7天" pill is active (1h buckets) and user sets start/end dates to 2026-04-01 through 2026-04-15
- **THEN** the chart displays 1-hour bucket consumption data for April 1-15, 2026

#### Scenario: Date picker after preset selection
- **WHEN** user selects a custom date range then clicks a preset pill
- **THEN** the date picker values are reset to the preset's default range

### Requirement: Time-aware X axis
The chart SHALL use ECharts `xAxis: { type: 'time' }` with automatic label formatting and spacing. Data points SHALL be formatted as `[Date, number]` tuples.

#### Scenario: Hourly granularity labels
- **WHEN** chart displays 7 days of hourly data
- **THEN** the X axis automatically shows date labels at readable intervals without overlapping

#### Scenario: Daily granularity labels
- **WHEN** chart displays 30 days of daily data
- **THEN** the X axis shows labels like "04/01", "04/08", "04/15", "04/22", "04/29" spaced evenly

### Requirement: Smooth consumption curve
The chart SHALL render consumption data as a smooth curve line with area fill. The curve SHALL use `smooth: 0.3` for controlled curvature that preserves data shape.

#### Scenario: Curve renders with data
- **WHEN** consumption data has 10+ points
- **THEN** a smooth curved line with subtle area fill below renders on the chart

#### Scenario: Curve with few points
- **WHEN** consumption data has only 2 points
- **THEN** the curve still renders as a straight line between the two points

### Requirement: Header bar layout
The header bar containing preset pills and date picker SHALL be fixed at the top of the chart card, forming a single visual unit. Pills SHALL be left-aligned and the date picker SHALL be right-aligned within the bar.

#### Scenario: Header bar visual attachment
- **WHEN** the balance view is displayed
- **THEN** the preset pills and date picker appear in a bar immediately above the chart canvas, within the same card container, with no visual gap separating them

### Requirement: Consumption Y axis
The Y axis SHALL display consumption amount in the provider's currency unit, labeled with the currency symbol.

#### Scenario: Single currency display
- **WHEN** all providers use CNY
- **THEN** the Y axis label reads "消耗 (CNY)"

#### Scenario: Y axis value format
- **WHEN** consumption values range from 0.01 to 1.00
- **THEN** the Y axis shows values formatted to 2 decimal places
