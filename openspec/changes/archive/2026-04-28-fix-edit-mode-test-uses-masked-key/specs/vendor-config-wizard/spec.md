# Vendor Config Wizard — Delta Spec

## MODIFIED Requirements

### Requirement: Step 2 — Usage API path and mapping
Step 2 SHALL contain fields for configuring the usage API path and JSONPath mappings. All fields are optional — this step can be skipped.

| Field | Type | Required |
|-------|------|----------|
| Usage API Path | text input + "测试" button | no |
| Test response | JSON pre block (shown after test) | — |
| JSONPath tag cloud | clickable tags parsed from response | — |
| Token 总量 JSONPath | text input (filled by tag click) | no |
| 费用 JSONPath | text input (filled by tag click) | no |

#### Scenario: Test usage API path for new provider
- **WHEN** user enters a path and clicks "测试" while creating a new provider
- **THEN** the test API is called with the form's base_url, api_key, and the path; the JSON response is displayed below

#### Scenario: Test usage API path for existing provider
- **WHEN** user enters a path and clicks "测试" while editing an existing provider
- **THEN** the test API is called using the provider's stored (decrypted) credentials from the database; the JSON response is displayed below

#### Scenario: Skip Step 2
- **WHEN** user clicks "保存并继续" on Step 2 without filling any fields
- **THEN** the current form state is saved (no validation errors) and wizard advances to Step 3

### Requirement: Step 3 — Balance path, currency, and polling
Step 3 SHALL contain fields for balance API configuration and other settings. All fields are optional.

| Field | Type | Required |
|-------|------|----------|
| Balance API Path | text input + "测试" button | no |
| Test response | JSON pre block | — |
| JSONPath tag cloud | clickable tags | — |
| 余额 JSONPath | text input (filled by tag click) | no |
| 货币符号 | text input (default: CNY) | no |
| 轮询间隔 | select dropdown | no |

#### Scenario: Test balance API path for new provider
- **WHEN** user enters a balance path and clicks "测试" while creating a new provider
- **THEN** the test API is called with the form's base_url, api_key, and the path; the JSON response is displayed with parsed tag cloud

#### Scenario: Test balance API path for existing provider
- **WHEN** user enters a balance path and clicks "测试" while editing an existing provider
- **THEN** the test API is called using the provider's stored (decrypted) credentials from the database; the JSON response is displayed with parsed tag cloud

#### Scenario: Save on Step 3
- **WHEN** user clicks "保存" on Step 3
- **THEN** the full form state is saved via API and the wizard closes

## ADDED Requirements

### Requirement: Provider-scoped test API endpoint
The backend SHALL provide an endpoint `POST /api/providers/{provider_id}/test-api` that uses the stored and decrypted API key to proxy test requests to the upstream LLM provider.

#### Scenario: Successful test with stored credentials
- **WHEN** a POST request is made to `/api/providers/{provider_id}/test-api` with `{ "api_path": "/v1/usage" }`
- **THEN** the backend decrypts the provider's stored API key, constructs the full URL, and returns the upstream response with `status_code` and `body`

#### Scenario: Provider not found
- **WHEN** a POST request is made with a non-existent `provider_id`
- **THEN** the backend returns HTTP 404 with detail "Provider not found"
