## ADDED Requirements

### Requirement: List all configured providers

The system SHALL display a list of all configured LLM providers with name, API key (masked, showing only last 4 characters), base URL, usage API path, tracked model count, and polling interval. An empty state message SHALL display when no providers are configured.

#### Scenario: Providers list renders

- **WHEN** the user navigates to `/providers` and at least one provider exists
- **THEN** each provider is shown in a card with: name, masked API key (e.g., `sk-...xxxx`), base URL, usage API path, model count (e.g., "3 个模型"), interval label (e.g., "每 5 分钟" or "手动"), and action buttons

#### Scenario: Empty state

- **WHEN** the user navigates to `/providers` and no providers exist
- **THEN** a centered message displays "暂无厂商配置" with a prompt to add one

### Requirement: Create a new provider

The system SHALL provide a form to create a new provider with fields: name (text, required), API key (password, required), base URL (url, required), usage API path (text, default `/v1/usage`), tracked models (tag input, at least one required), polling interval (select: 手动/10s/1min/5min/15min/1h/6h/24h). On submit SHALL call `POST /api/providers` and add the provider to the list.

#### Scenario: Successful provider creation

- **WHEN** user fills in all required fields, adds at least one model, and submits the form
- **THEN** the new provider appears in the list and the form resets

#### Scenario: Validation on empty required fields

- **WHEN** user submits the form with name, API key, or base URL empty
- **THEN** the form shows validation error messages and no API call is made

#### Scenario: Validation on empty model list

- **WHEN** user submits the form without adding at least one model
- **THEN** the model input shows a validation error "至少添加一个模型"

### Requirement: Edit an existing provider

The system SHALL allow editing all provider fields via a pre-filled form. On save SHALL call `PUT /api/providers/{id}`.

#### Scenario: Edit provider details

- **WHEN** user clicks "编辑" on a provider row and modifies the name or interval
- **THEN** the provider's data updates in the list after successful save

### Requirement: Delete a provider

The system SHALL allow deleting a provider after a confirmation dialog. On confirm SHALL call `DELETE /api/providers/{id}` and remove the provider from the list.

#### Scenario: Delete with confirmation

- **WHEN** user clicks "删除" on a provider
- **THEN** a confirmation dialog appears
- **WHEN** user confirms deletion
- **THEN** the provider is removed from the list

#### Scenario: Cancel deletion

- **WHEN** user clicks "取消" in the confirmation dialog
- **THEN** the provider remains in the list unchanged

### Requirement: Test provider connection

The system SHALL provide a "连接测试" button per provider that calls `POST /api/providers/{id}/test` and displays the result (success/failure with error message).

#### Scenario: Successful connection test

- **WHEN** user clicks "连接测试" on a provider with valid credentials
- **THEN** a success toast or inline message "连接成功" is displayed

#### Scenario: Failed connection test

- **WHEN** user clicks "连接测试" on a provider with invalid credentials
- **THEN** an error message with the reason (e.g., "401 Unauthorized") is displayed

### Requirement: Manually trigger usage collection

The system SHALL provide a "立即采集" button per provider that calls `POST /api/providers/{id}/collect`. During collection SHALL show a loading state, then display the result (number of usage records collected, or error).

#### Scenario: Successful collection

- **WHEN** user clicks "立即采集" on a provider with valid config
- **THEN** a loading state appears, then a success message shows the number of collected records (e.g., "已采集 5 条用量记录")

#### Scenario: Collection with error

- **WHEN** user clicks "立即采集" and the API call fails
- **THEN** an error message with the reason is displayed
