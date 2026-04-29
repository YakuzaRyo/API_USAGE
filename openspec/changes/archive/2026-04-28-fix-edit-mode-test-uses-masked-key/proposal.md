## Why

When editing a provider, the wizard's "测试" button sends the masked API key (e.g. `...sk-abc`) as a real Bearer token to the upstream LLM provider. This always fails — the upstream provider receives a garbled credential. However, "立即采集" from the card view works correctly because it calls a backend endpoint that decrypts the stored key. The fix ensures the wizard's test feature uses the real stored key when in edit mode.

## What Changes

- **Backend**: Add `POST /api/providers/{provider_id}/test-api` endpoint that decrypts the stored API key and proxies the test request to the upstream provider.
- **Frontend**: Modify `doStep2Test` and `doStep3Test` in `ProviderWizard.vue` to use the new provider-scoped endpoint when `editingId` is set, falling back to the existing form-key endpoint for new (unsaved) providers.
- **Spec**: Update `vendor-config-wizard` requirements for Step 2 and Step 3 test scenarios to describe edit-mode behavior.

## Capabilities

### New Capabilities

None. This is a bug fix within an existing flow.

### Modified Capabilities

- `vendor-config-wizard`: Step 2 and Step 3 "测试" button behavior must use the stored API key (via provider-scoped endpoint) when editing an existing provider, and the form key (via existing endpoint) when creating a new provider.

## Impact

- **Backend**: New route in `routers/providers.py`
- **Frontend**: `ProviderWizard.vue` — `doStep2Test` and `doStep3Test`
- **Frontend**: `api/index.ts` — new `testApiForProvider` function
- **No breaking API changes**: Existing `POST /api/providers/test-api` remains for new-provider flow
- **No dependency changes**
