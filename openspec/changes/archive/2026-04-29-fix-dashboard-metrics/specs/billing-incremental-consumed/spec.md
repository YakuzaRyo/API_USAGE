# Billing Incremental Consumed

## ADDED Requirements

### Requirement: API billing fee is computed by incremental diff accumulation
For API-billed providers, the system SHALL compute total consumed amount by iterating all balance snapshots in chronological order and summing every positive balance decrease between consecutive snapshots. A balance increase between consecutive snapshots (indicating a top-up) SHALL be skipped and MUST NOT affect the accumulated total.

#### Scenario: Normal consumption without top-up
- **WHEN** a provider's balance snapshots are [100, 80, 65, 50]
- **THEN** the accumulated consumed amount is (100-80) + (80-65) + (65-50) = 50.0

#### Scenario: Consumption with mid-series top-up
- **WHEN** a provider's balance snapshots are [100, 80, 70, 120, 100, 90]
- **THEN** the accumulated consumed amount is (100-80) + (80-70) + (120-100) + (100-90) = 60.0, and the 70→120 increase is not counted

#### Scenario: Consumption with consecutive top-ups
- **WHEN** a provider's balance snapshots are [100, 90, 150, 120]
- **THEN** the accumulated consumed amount is (100-90) + (150-120) = 40.0

#### Scenario: No balance history
- **WHEN** a provider has no balance snapshots with non-null balance
- **THEN** the consumed amount is 0.0

#### Scenario: Single balance snapshot
- **WHEN** a provider has only one balance snapshot (e.g., just added)
- **THEN** the consumed amount is 0.0

### Requirement: API billing fee is monotonically non-decreasing
The consumed amount for an API-billed provider SHALL never decrease as new balance snapshots are collected, regardless of top-ups.

#### Scenario: Fee only increases after top-up
- **WHEN** a provider with consumed amount 30.0 receives a top-up of 50.0 and later consumes 20.0
- **THEN** the consumed amount becomes 50.0, not 20.0 or any lower value

### Requirement: Billing summary returns incremental consumed for API providers
The billing summary endpoint SHALL use the incremental diff accumulation method when computing the `amount` field for providers with `billing_mode = "api"`.

#### Scenario: API provider in billing summary
- **WHEN** GET /api/stats/billing-summary is called and an API provider has balance snapshots [100, 80]
- **THEN** the provider's amount is 20.0

#### Scenario: Token-plan provider unchanged
- **WHEN** GET /api/stats/billing-summary is called for a provider with `billing_mode = "token_plan"`
- **THEN** the provider's amount is computed as before (months × monthly_fee), unaffected by this change
