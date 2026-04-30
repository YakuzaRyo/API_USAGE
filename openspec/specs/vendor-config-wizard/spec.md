# Vendor Config Wizard

## Purpose

A step-based wizard modal for creating and editing LLM provider configurations. Splits a complex single-page form into 3 navigable steps with independent per-step saving and progressive validation.

## ADDED Requirements

### Requirement: Step-based wizard modal
The system SHALL present the vendor configuration form as a modal with 3 step pages, replacing the single-page form. Each step displays a subset of fields to reduce cognitive load.

#### Scenario: Wizard opens for new provider
- **WHEN** user clicks "+ 新增厂商"
- **THEN** the wizard modal opens at Step 1 with all fields in default state

#### Scenario: Wizard opens for editing provider
- **WHEN** user clicks "编辑" on an existing provider card
- **THEN** the wizard modal opens at Step 1 with all fields pre-filled from the provider data

### Requirement: Step 1 — Connection configuration
Step 1 SHALL contain the following fields. billing_mode and category appear first and control auto-fill of subsequent fields. All fields except API Key during edit mode are validated on save.

| Field | Type | Required |
|-------|------|----------|
| 计费方式 | pill toggle (API 查询 / Token Plan) | yes |
| 分类 | select dropdown (categories list) | no |
| 名称 | text input | yes |
| API Key | password input | yes (create) / no (edit, when unchanged) |
| Base URL | text input, auto-filled from category | yes |
| 追踪模型 | tag input (add/remove), auto-filled from category | yes |

#### Scenario: Step 1 validation — missing required fields
- **WHEN** user clicks "保存并继续" on Step 1 with empty name
- **THEN** an inline error message "名称不能为空" is shown and save is blocked

#### Scenario: Step 1 validation — all required fields filled (new provider)
- **WHEN** user clicks "保存并继续" on Step 1 with valid name, api_key, base_url, and at least one model
- **THEN** the provider is saved via API and the wizard advances to Step 2

#### Scenario: Category auto-fill on selection
- **WHEN** user selects a category and billing_mode is "API 查询"
- **THEN** base_url, usage_api_path, balance_api_path, models, and currency_symbol are pre-filled from the category's API tab

#### Scenario: Category auto-fill respects billing mode
- **WHEN** user switches billing_mode to "Token Plan" and selects a category
- **THEN** fields are pre-filled from the category's Token Plan tab

#### Scenario: API Key field shows masked placeholder on edit
- **WHEN** wizard opens for editing an existing provider
- **THEN** the API Key input displays a masked placeholder value

#### Scenario: API Key excluded from update when unchanged
- **WHEN** user saves the wizard without explicitly typing into the API Key field
- **THEN** the update payload SHALL NOT include `api_key`

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
Step 3 SHALL contain fields for balance API configuration and other settings. billing_mode has been moved to Step 1. Token Plan exclusive fields (月费, 订阅日期) appear only when billing_mode is "token_plan".

| Field | Type | Required |
|-------|------|----------|
| Balance API Path | text input + "测试" button (API mode only) | no |
| Test response | JSON pre block | — |
| JSONPath tag cloud | clickable tags | — |
| 余额 JSONPath | text input (filled by tag click) | no |
| 货币符号 | text input, auto-filled from category | no |
| 轮询间隔 | select dropdown | no |
| 月费金额 (Token Plan) | number input | no |
| 订阅起始日期 (Token Plan) | date input | no |

#### Scenario: Test balance API path for new provider
- **WHEN** user enters a balance path and clicks "测试" while creating a new provider
- **THEN** the test API is called with the form's base_url, api_key, and the path; the JSON response is displayed with parsed tag cloud

#### Scenario: Test balance API path for existing provider
- **WHEN** user enters a balance path and clicks "测试" while editing an existing provider
- **THEN** the test API is called using the provider's stored (decrypted) credentials from the database; the JSON response is displayed with parsed tag cloud

#### Scenario: Save on Step 3
- **WHEN** user clicks "保存" on Step 3
- **THEN** the full form state is saved via API and the wizard closes

### Requirement: Dot navigation
The wizard SHALL display a horizontal dot indicator at the bottom, with exactly 3 dots representing the 3 steps. The dot for the current step is enlarged and filled with the primary color. All dots are clickable at any time.

#### Scenario: Dot visual states
- **WHEN** the wizard is on Step 2
- **THEN** the Step 1 dot is a 12px outlined circle, Step 2 dot is a 20px filled circle in `--color-primary`, Step 3 dot is a 12px outlined circle

#### Scenario: Click dot to jump
- **WHEN** user is on Step 3 and clicks the Step 1 dot
- **THEN** the wizard immediately displays Step 1 content without saving

#### Scenario: Click current dot
- **WHEN** user clicks the dot for the current step
- **THEN** nothing happens (no-op)

### Requirement: Previous / Next navigation buttons
The wizard SHALL display navigation buttons to guide step transitions.

#### Scenario: Step 1 navigation buttons
- **WHEN** wizard is on Step 1
- **THEN** only "保存并继续" button is visible (no "上一步" button)

#### Scenario: Step 2 navigation buttons
- **WHEN** wizard is on Step 2
- **THEN** both "上一步" and "保存并继续" buttons are visible

#### Scenario: Step 3 navigation buttons
- **WHEN** wizard is on Step 3
- **THEN** "上一步" and "保存" buttons are visible ("保存并继续" is replaced by "保存")

#### Scenario: Previous button behavior
- **WHEN** user clicks "上一步"
- **THEN** wizard displays the previous step content without saving current step changes to the server (form state remains in memory)

### Requirement: Incremental save
The wizard SHALL support partial saves — each step's "保存" action persists only the fields known so far, allowing progressive configuration across multiple sessions. The `api_key` field SHALL only be included when the user has explicitly modified it (create flow or explicit edit).

#### Scenario: Create provider with Step 1 only
- **WHEN** a new provider is saved at Step 1 with name, api_key, base_url, and models
- **THEN** a POST request creates the provider record; subsequent Step 2/3 saves use PUT to update the same record

#### Scenario: Edit provider with partial update
- **WHEN** editing an existing provider and saving at Step 2
- **THEN** a PUT request updates the provider with all currently accumulated field values, excluding `api_key` unless the user explicitly changed it

#### Scenario: Edit provider and change API key
- **WHEN** editing an existing provider, the user explicitly types a new value into the API Key field, and saves
- **THEN** the PUT request includes the new `api_key` value, and the server encrypts and stores it

### Requirement: Modal close
The wizard modal SHALL be closable by clicking the overlay backdrop or a close button.

#### Scenario: Close without saving unsaved changes
- **WHEN** user clicks the overlay backdrop with unsaved changes in the current step
- **THEN** the wizard closes and unsaved changes to the current step are discarded

### Requirement: Server-side API key corruption prevention
The backend SHALL defend against accidental re-encryption of masked API key values during provider update.

#### Scenario: Incoming API key matches current masked form
- **WHEN** a PUT request includes an `api_key` value that equals the masked form of the currently stored decrypted key
- **THEN** the server SHALL treat it as unchanged and skip re-encryption

#### Scenario: Incoming API key is genuinely new
- **WHEN** a PUT request includes an `api_key` value that differs from the masked form of the currently stored decrypted key
- **THEN** the server SHALL encrypt the new value and persist it

### Requirement: Provider-scoped test API endpoint
The backend SHALL provide an endpoint `POST /api/providers/{provider_id}/test-api` that uses the stored and decrypted API key to proxy test requests to the upstream LLM provider.

#### Scenario: Successful test with stored credentials
- **WHEN** a POST request is made to `/api/providers/{provider_id}/test-api` with `{ "api_path": "/v1/usage" }`
- **THEN** the backend decrypts the provider's stored API key, constructs the full URL, and returns the upstream response with `status_code` and `body`

#### Scenario: Provider not found
- **WHEN** a POST request is made with a non-existent `provider_id`
- **THEN** the backend returns HTTP 404 with detail "Provider not found"
