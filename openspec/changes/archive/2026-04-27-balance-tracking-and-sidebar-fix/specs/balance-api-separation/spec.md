## ADDED Requirements

### Requirement: Provider supports separate balance API path

The system SHALL add an optional `balance_api_path` field and a `last_balance` cache field to the Provider model. The existing `usage_api_path` SHALL be used only for usage data, while `balance_api_path` SHALL be used only for balance data.

#### Scenario: Provider created with both paths

- **WHEN** a Provider is created with `usage_api_path: "/v1/usage"` and `balance_api_path: "/v1/billing"`
- **THEN** both paths are stored and returned in the Provider response

#### Scenario: Provider created without balance path

- **WHEN** a Provider is created without `balance_api_path`
- **THEN** `balance_api_path` defaults to null and `last_balance` defaults to null, behavior unchanged

### Requirement: Dual-path collection

The system SHALL first call `{base_url}{usage_api_path}` to collect token usage and cost, then call `{base_url}{balance_api_path}` (if set) to collect balance. Each call SHALL create an independent CollectionLog. Balance SHALL be cached to `Provider.last_balance`.

#### Scenario: Both paths succeed

- **WHEN** collector runs for a provider with both paths configured and both APIs return valid data
- **THEN** UsageRecord rows are created and Provider.last_balance is updated with the extracted balance value

#### Scenario: Only usage path configured

- **WHEN** collector runs for a provider without `balance_api_path`
- **THEN** only usage data is collected, Provider.last_balance remains unchanged

#### Scenario: Usage succeeds but balance fails

- **WHEN** usage API returns valid data but balance API returns an error
- **THEN** UsageRecord rows are created with ok CollectionLog, and a separate error CollectionLog is created for the balance call
