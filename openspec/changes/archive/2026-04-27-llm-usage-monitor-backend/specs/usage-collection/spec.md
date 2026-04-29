## ADDED Requirements

### Requirement: Collect usage data for a provider

The system SHALL make an HTTP GET request to `{provider.base_url}{provider.usage_api_path}` with `Authorization: Bearer {decrypted_api_key}`, parse the JSON response using `response_mapping` to extract tokens_used, cost, and balance, then write one UsageRecord per tracked model. A CollectionLog SHALL be created recording the outcome.

#### Scenario: Successful collection

- **WHEN** `POST /api/providers/{id}/collect` is called and the external API returns valid usage data
- **THEN** UsageRecord rows are inserted for each tracked model, a CollectionLog with status "ok" is created, and the response returns `{"status": "ok", "record_count": N}`

#### Scenario: Collection with API error

- **WHEN** `POST /api/providers/{id}/collect` is called and the external API returns an error
- **THEN** a CollectionLog with status "error" and error_message is created, and the response returns `{"status": "error", "message": "<reason>"}`

#### Scenario: Collection for non-existent provider

- **WHEN** `POST /api/providers/999/collect` is called
- **THEN** returns 404

### Requirement: Store usage records per tracked model

For each model in `provider.models`, the system SHALL extract the corresponding usage data from the API response and create a UsageRecord with provider_id, model name, tokens_used, cost, balance, and recorded_at timestamp.

#### Scenario: Multiple models collected

- **WHEN** a provider tracks ["gpt-4", "gpt-3.5-turbo"] and the API response contains usage for both
- **THEN** two UsageRecord rows are created, each with the corresponding model name

### Requirement: Response mapping for different provider formats

The system SHALL support a `response_mapping` JSON field on Provider that defines dot-notation paths to extract usage fields from the API response. If mapping is not configured, the system SHALL attempt auto-detection for known providers (OpenAI, Anthropic).

#### Scenario: Custom response mapping

- **WHEN** a provider has `response_mapping: {"total_tokens": "data.daily_usage.tokens"}` and the API response matches this structure
- **THEN** tokens_used is extracted from `response["data"]["daily_usage"]["tokens"]`

#### Scenario: Auto-detection for OpenAI format

- **WHEN** a provider has no response_mapping and the API response matches OpenAI `/v1/usage` format
- **THEN** tokens_used and cost are extracted correctly from the known structure
