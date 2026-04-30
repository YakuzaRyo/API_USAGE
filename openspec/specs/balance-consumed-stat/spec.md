# Balance Consumed Stat

## Purpose

Tracks total balance consumed since first collection in the dashboard stats cards.

## Requirements

### Requirement: Balance consumed in billing summary for API providers
The billing summary API SHALL compute the consumed amount for API-billed providers by iterating all balance snapshots in chronological order and summing every positive balance decrease between consecutive snapshots. Balance increases (top-ups) SHALL be skipped.

#### Scenario: Continuous consumption without top-up
- **WHEN** a provider has balance snapshots [100, 80, 65, 50]
- **THEN** the consumed amount is (100-80) + (80-65) + (65-50) = 50.0

#### Scenario: Consumption with top-up between snapshots
- **WHEN** a provider has balance snapshots [100, 80, 120, 90]
- **THEN** the consumed amount is (100-80) + (120-90) = 50.0, and the 80→120 top-up does not affect the total

#### Scenario: No balance history
- **WHEN** no provider has balance collection history
- **THEN** the consumed amount is 0.0

### Requirement: Balance consumed stat card
The Dashboard SHALL display a stat card showing the total balance consumed amount, styled identically to the existing cards.

#### Scenario: Card visible with API providers
- **WHEN** the dashboard loads with API-billed providers that have consumed balance
- **THEN** a card labeled "费用" appears with the incrementally-computed consumed amount and currency symbol

#### Scenario: Card visible with token-plan providers
- **WHEN** the dashboard loads with only token-plan providers
- **THEN** the "费用" card shows the accumulated subscription fees (unchanged behavior)
