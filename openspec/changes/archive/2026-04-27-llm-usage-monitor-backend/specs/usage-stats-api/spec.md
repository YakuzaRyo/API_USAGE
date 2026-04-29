## ADDED Requirements

### Requirement: Summary statistics

The system SHALL return aggregate usage summary: total_tokens (sum of tokens_used in the last 7 days), total_cost (sum of cost in the last 7 days), and active_providers (count of distinct providers with usage records in the last 7 days). An optional `?provider_id=` query parameter SHALL filter results to a single provider.

#### Scenario: Summary with all providers

- **WHEN** `GET /api/stats/summary` is called
- **THEN** returns `{"total_tokens": N, "total_cost": M, "active_providers": K}` aggregated across all providers

#### Scenario: Summary filtered by provider

- **WHEN** `GET /api/stats/summary?provider_id=1` is called
- **THEN** returns summary data for provider 1 only

#### Scenario: Summary with no usage data

- **WHEN** `GET /api/stats/summary` is called and no usage records exist
- **THEN** returns `{"total_tokens": 0, "total_cost": 0, "active_providers": 0}`

### Requirement: Daily usage trends

The system SHALL return daily token consumption and cost data grouped by `DATE(recorded_at)`, ordered by date ascending. An optional `?provider_id=` query parameter SHALL filter results.

#### Scenario: Trends across multiple days

- **WHEN** `GET /api/stats/trends` is called with usage data spanning 3 days
- **THEN** returns an array of `{"date": "YYYY-MM-DD", "tokens": N, "cost": M, "provider_name": "..."}` ordered by date

#### Scenario: Trends filtered by provider

- **WHEN** `GET /api/stats/trends?provider_id=1` is called
- **THEN** returns trend data for provider 1 only

### Requirement: Model usage distribution

The system SHALL return token consumption grouped by model, ordered by total tokens descending. An optional `?provider_id=` query parameter SHALL filter results.

#### Scenario: Distribution across models

- **WHEN** `GET /api/stats/distribution` is called with records for ["gpt-4", "claude-opus"]
- **THEN** returns `[{"model": "gpt-4", "tokens": N}, {"model": "claude-opus", "tokens": M}]` ordered by tokens descending

#### Scenario: Distribution filtered by provider

- **WHEN** `GET /api/stats/distribution?provider_id=1` is called
- **THEN** returns distribution data for provider 1 only
