## Why

When re-editing a vendor card without touching the API key field, the masked key (e.g. `...sk-abc`) displayed in the password input is sent back to the server and re-encrypted as if it were a new plaintext key. This permanently corrupts the stored API key — the original key is lost after any edit-and-save cycle. Subsequently, API test calls and data collection fail because the stored value is no longer a valid credential. The user must delete and re-create the provider to recover, which also loses all historical usage records.

## What Changes

- **Frontend**: Add `autocomplete="off"` to the API key password input to prevent browser autofill interference.
- **Frontend**: Track whether the user has actually modified the API key field. When unchanged, omit `api_key` from the update payload so the server retains the existing value.
- **Backend**: Add a defensive check — if the incoming `api_key` value matches the masked form of the current key, treat it as unchanged and skip re-encryption.
- **Spec**: Update `vendor-config-wizard` requirements for Step 1 API key field to describe masked display and "only send on modification" behavior.

## Capabilities

### New Capabilities

None. This is a bug fix, not a new capability.

### Modified Capabilities

- `vendor-config-wizard`: API key field in Step 1 must display a masked placeholder when editing, and the update payload must not include `api_key` unless the user explicitly changes it.

## Impact

- **Frontend**: `ProviderWizard.vue` — form state tracking, `buildPayload()`, and template for API key input
- **Backend**: `routers/providers.py` — `update_provider` endpoint, `ProviderUpdate` schema
- **No API breaking changes**: Request/response schemas remain compatible
- **No dependency changes**
