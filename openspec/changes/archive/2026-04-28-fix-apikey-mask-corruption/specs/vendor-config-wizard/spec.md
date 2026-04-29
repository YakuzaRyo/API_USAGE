# Vendor Config Wizard — Delta Spec

## MODIFIED Requirements

### Requirement: Step 1 — Connection configuration
Step 1 SHALL contain the following fields. All fields except API Key during edit mode are validated on save.

| Field | Type | Required |
|-------|------|----------|
| 名称 | text input | yes |
| API Key | password input | yes (create) / no (edit, when unchanged) |
| Base URL | text input | yes |
| 追踪模型 | tag input (add/remove) | yes |

#### Scenario: Step 1 validation — missing required fields
- **WHEN** user clicks "保存并继续" on Step 1 with empty name
- **THEN** an inline error message "名称不能为空" is shown and save is blocked

#### Scenario: Step 1 validation — all required fields filled (new provider)
- **WHEN** user clicks "保存并继续" on Step 1 with valid name, api_key, base_url, and at least one model
- **THEN** the provider is saved via API and the wizard advances to Step 2

#### Scenario: API Key field shows masked placeholder on edit
- **WHEN** wizard opens for editing an existing provider
- **THEN** the API Key input displays a masked placeholder value (e.g. `••••••••`) and the field is visually marked as unchanged

#### Scenario: API Key field prevents browser autofill
- **WHEN** the API Key password input is rendered
- **THEN** it includes `autocomplete="off"` to prevent browser password managers from injecting unrelated credentials

#### Scenario: API Key excluded from update when unchanged
- **WHEN** user saves the wizard at any step without explicitly typing into the API Key field
- **THEN** the update payload SHALL NOT include `api_key`, preserving the existing encrypted key on the server

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

## ADDED Requirements

### Requirement: Server-side API key corruption prevention
The backend SHALL defend against accidental re-encryption of masked API key values during provider update.

#### Scenario: Incoming API key matches current masked form
- **WHEN** a PUT request includes an `api_key` value that equals the masked form of the currently stored decrypted key
- **THEN** the server SHALL treat it as unchanged and skip re-encryption

#### Scenario: Incoming API key is genuinely new
- **WHEN** a PUT request includes an `api_key` value that differs from the masked form of the currently stored decrypted key
- **THEN** the server SHALL encrypt the new value and persist it
