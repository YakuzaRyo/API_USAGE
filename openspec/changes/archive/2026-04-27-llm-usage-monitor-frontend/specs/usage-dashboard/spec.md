## ADDED Requirements

### Requirement: Summary statistics cards

The system SHALL display three summary cards at the top of `/dashboard`: total token consumption across all providers, total cost estimate, and count of active providers with recent usage. Each card SHALL show a label and a large numeric value.

#### Scenario: Summary cards render with data

- **WHEN** the dashboard loads and usage data exists
- **THEN** three cards display: "Token 消耗总量" with a formatted number, "预估总费用" with a CNY amount, and "活跃厂商数" with a count

#### Scenario: Summary cards show zero state

- **WHEN** the dashboard loads and no usage data exists
- **THEN** all three summary cards display 0 or "暂无数据"

### Requirement: Usage trend line chart

The system SHALL render an ECharts line chart showing daily token consumption trend over time. The x-axis SHALL display dates, the y-axis SHALL display token count, and the line SHALL be smooth with area fill at low opacity.

#### Scenario: Trend chart with data

- **WHEN** usage data spans multiple days
- **THEN** the line chart renders with dates on the x-axis, token counts on the y-axis, a smooth line, and area fill with 0.15 opacity

#### Scenario: Trend chart empty state

- **WHEN** no trend data is available
- **THEN** the chart area displays an empty state message

### Requirement: Model usage distribution bar chart

The system SHALL render an ECharts bar chart showing usage distribution across different models. Each bar SHALL represent a model name, colored with the brand accent color `#FF6B35`.

#### Scenario: Distribution chart with data

- **WHEN** usage data includes multiple models
- **THEN** the bar chart renders with model names on the x-axis, token counts on the y-axis, and bars colored `#FF6B35`

#### Scenario: Distribution chart with long model names

- **WHEN** model names are long (e.g., `claude-opus-4-7-20251001`)
- **THEN** the x-axis labels rotate 30 degrees and use reduced font size (11px)

### Requirement: Charts respond to window resize

The system SHALL resize all ECharts instances when the browser window is resized. On component unmount, all chart instances SHALL be disposed to prevent memory leaks.

#### Scenario: Window resize triggers chart resize

- **WHEN** user resizes the browser window
- **THEN** all visible ECharts instances resize to fit their containers

#### Scenario: Leaving dashboard cleans up charts

- **WHEN** user navigates away from `/dashboard`
- **THEN** all ECharts instances are disposed

### Requirement: Provider filter for dashboard

The system SHALL provide a provider filter dropdown above the charts that filters usage data by selected provider. When "全部" is selected, SHALL show aggregated data from all providers.

#### Scenario: Filter by single provider

- **WHEN** user selects "OpenAI" from the provider filter dropdown
- **THEN** the summary cards and charts update to show only OpenAI usage data

#### Scenario: Filter set to all providers

- **WHEN** user selects "全部" from the provider filter dropdown
- **THEN** the summary cards and charts show aggregated data from all providers
