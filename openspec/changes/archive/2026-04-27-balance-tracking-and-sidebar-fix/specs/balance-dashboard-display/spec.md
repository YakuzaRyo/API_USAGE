## ADDED Requirements

### Requirement: Balance summary in stats API

The system SHALL include `total_balance` in the `/api/stats/summary` response, computed as the sum of all non-null `Provider.last_balance` values. Trends SHALL include per-date balance data.

#### Scenario: Summary with balance data

- **WHEN** `GET /api/stats/summary` is called and providers have last_balance set
- **THEN** the response includes `total_balance` with the sum of all provider balances

#### Scenario: Summary without balance data

- **WHEN** no providers have last_balance set
- **THEN** `total_balance` returns 0 or null

### Requirement: Balance card on dashboard

The system SHALL display a 4th statistics card "当前余额" on the Dashboard page, showing the aggregated balance amount in CNY format next to the existing Token, Cost, and Active Providers cards.

#### Scenario: Dashboard with balance

- **WHEN** the Dashboard loads and summary includes total_balance > 0
- **THEN** a fourth card "当前余额" displays the balance amount with "CNY" suffix

#### Scenario: Dashboard without balance

- **WHEN** no balance data is available
- **THEN** the balance card displays "0.00 CNY"

### Requirement: Provider form includes balance API path

The system SHALL add a `balance_api_path` input field to the Provider create/edit form, with placeholder text indicating it's optional (e.g., "/v1/billing").

#### Scenario: Form with balance path field

- **WHEN** user opens the create or edit Provider form
- **THEN** a text input labeled "余额 API 路径" is displayed, optional, with no default value
