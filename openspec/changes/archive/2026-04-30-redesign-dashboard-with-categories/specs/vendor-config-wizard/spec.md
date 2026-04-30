# Vendor Config Wizard

## MODIFIED Requirements

### Requirement: Step 1 — Connection configuration
Step 1 SHALL contain the following fields. billing_mode and category appear first and control auto-fill of subsequent fields. All fields except API Key during edit mode are validated on save.

| Field | Type | Required |
|-------|------|----------|
| 计费方式 | pill toggle (API 查询 / Token Plan) | yes |
| 分类 | select dropdown (preset names + custom) | no |
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

#### Scenario: API Key field shows masked placeholder on edit
- **WHEN** wizard opens for editing an existing provider
- **THEN** the API Key input displays a masked placeholder value and the field is visually marked as unchanged

#### Scenario: API Key field prevents browser autofill
- **WHEN** the API Key password input is rendered
- **THEN** it includes `autocomplete="off"` to prevent browser password managers from injecting unrelated credentials

#### Scenario: API Key excluded from update when unchanged
- **WHEN** user saves the wizard at any step without explicitly typing into the API Key field
- **THEN** the update payload SHALL NOT include `api_key`, preserving the existing encrypted key on the server

#### Scenario: Category auto-fill on selection
- **WHEN** user selects a category from the dropdown and billing_mode is "API 查询"
- **THEN** base_url, usage_api_path, balance_api_path, models, and currency_symbol are pre-filled from the category's API tab configuration

#### Scenario: Category auto-fill respects billing mode
- **WHEN** user switches billing_mode to "Token Plan" and selects a category
- **THEN** base_url, usage_api_path, models, and currency_symbol are pre-filled from the category's Token Plan tab configuration

#### Scenario: Switching billing mode clears and re-fills
- **WHEN** user has a category selected and switches billing_mode
- **THEN** the auto-filled fields update to reflect the new mode's category configuration

### Requirement: Step 3 — Balance path, currency, and polling
Step 3 SHALL contain fields for balance API configuration and other settings. All fields are optional. billing_mode has been moved to Step 1.

| Field | Type | Required |
|-------|------|----------|
| Balance API Path | text input + "测试" button | no |
| Test response | JSON pre block | — |
| JSONPath tag cloud | clickable tags | — |
| 余额 JSONPath | text input (filled by tag click) | no |
| 货币符号 | text input, auto-filled from category | no |
| 轮询间隔 | select dropdown | no |
| 月费金额 (Token Plan only) | number input | no |
| 订阅起始日期 (Token Plan only) | date input | no |

#### Scenario: Test balance API path for new provider
- **WHEN** user enters a balance path and clicks "测试" while creating a new provider
- **THEN** the test API is called with the form's base_url, api_key, and the path; the JSON response is displayed with parsed tag cloud

#### Scenario: Test balance API path for existing provider
- **WHEN** user enters a balance path and clicks "测试" while editing an existing provider
- **THEN** the test API is called using the provider's stored (decrypted) credentials from the database; the JSON response is displayed with parsed tag cloud

#### Scenario: Save on Step 3
- **WHEN** user clicks "保存" on Step 3
- **THEN** the full form state is saved via API and the wizard closes

#### Scenario: Currency pre-filled from category
- **WHEN** user has a category selected
- **THEN** the currency_symbol field is pre-filled with the category's currency value and can be overridden
