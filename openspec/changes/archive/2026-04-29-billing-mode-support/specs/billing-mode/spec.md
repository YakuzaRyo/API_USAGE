## ADDED Requirements

### Requirement: Provider billing mode field
Each provider SHALL have a `billing_mode` field accepting values `'api'` or `'token_plan'`, defaulting to `'api'`.

#### Scenario: New provider defaults to API
- **WHEN** a provider is created without explicit billing mode
- **THEN** `billing_mode` is set to `'api'`

### Requirement: Token Plan fields
Providers with `billing_mode = 'token_plan'` SHALL store `monthly_fee` (float) and `sub_start_date` (ISO date string). These fields are nullable for API-mode providers.

#### Scenario: Token Plan provider has fee and start date
- **WHEN** a provider with billing_mode 'token_plan' is created
- **THEN** `monthly_fee` of 200.0 and `sub_start_date` of "2026-01-01" are persisted

### Requirement: Step 3 field visibility by billing mode
The provider configuration wizard Step 3 SHALL show balance API fields when billing_mode is 'api', and monthly fee + subscription start fields when billing_mode is 'token_plan'.

#### Scenario: API mode shows balance fields
- **WHEN** billing_mode is 'api' in Step 3
- **THEN** Balance API Path and Balance JSONPath are visible; monthly_fee and sub_start_date are hidden

#### Scenario: Token Plan mode shows fee fields
- **WHEN** billing_mode is 'token_plan' in Step 3
- **THEN** monthly_fee and sub_start_date inputs are visible; Balance API Path and Balance JSONPath are hidden

### Requirement: Billing summary API
The system SHALL expose `GET /api/stats/billing-summary` returning per-provider cost with billing_mode and amount.

#### Scenario: API mode provider in summary
- **WHEN** a provider with billing_mode 'api' has balance_consumed of 38.50
- **THEN** its billing-summary entry has billing_mode "api" and amount 38.50

#### Scenario: Token Plan provider in summary
- **WHEN** a provider with billing_mode 'token_plan' has monthly_fee 200 and sub_start_date 3 months ago
- **THEN** its billing-summary entry has billing_mode "token_plan" and amount 600.00

### Requirement: Provider card mode tag
The provider list card SHALL display a colored tag indicating the billing mode ('API' or 'TokenPlan') and show the corresponding financial value (balance or monthly fee).

#### Scenario: API mode card
- **WHEN** a provider in API mode has last_balance 87.50
- **THEN** the card shows an "API" tag and displays "余额: 87.50 CNY"

#### Scenario: Token Plan mode card
- **WHEN** a provider in TokenPlan mode has monthly_fee 200
- **THEN** the card shows a "TokenPlan" tag and displays "月费: 200.00 CNY"

### Requirement: Frontend cost aggregation
The dashboard cost stat card SHALL compute total cost as the sum of all provider amounts from the billing-summary API.

#### Scenario: Cost aggregated from billing summary
- **WHEN** billing-summary returns 3 providers with amounts [10, 20, 15]
- **THEN** the cost stat card displays "45.00"
