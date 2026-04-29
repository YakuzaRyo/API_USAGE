## 1. Frontend — API Key dirty tracking

- [x] 1.1 Add `apiKeyDirty` ref (default `false`) to `ProviderWizard.vue`
- [x] 1.2 Set `apiKeyDirty = false` when the wizard opens in edit mode (inside the `watch` on `props.provider`)
- [x] 1.3 Add `@input="apiKeyDirty = true"` to the API Key `<input>` element to detect user modification
- [x] 1.4 Modify `buildPayload()` to exclude `api_key` from the returned object when `apiKeyDirty` is `false` and `editingId` is not null (edit mode)

## 2. Frontend — Browser autofill prevention

- [x] 2.1 Add `autocomplete="off"` attribute to the API Key password `<input>` in Step 1

## 3. Backend — Defensive check against masked key re-encryption

- [x] 3.1 In `routers/providers.py` `update_provider`, before calling `encrypt(data.api_key)`, decrypt the current key and compare: if `data.api_key == mask_key(decrypt(provider.api_key))`, skip the `api_key` assignment
- [x] 3.2 Import `mask_key` and `decrypt` if not already in scope at the update handler

## 4. Verification

- [ ] 4.1 Create a provider with a valid API key via the wizard
- [ ] 4.2 Click "编辑" on the provider card, make no changes to the API key field, save at Step 1
- [ ] 4.3 Verify the provider's API key still works by clicking "测试" on Step 2 usage API path
- [ ] 4.4 Edit the provider, explicitly change the API key to a new value, save, and verify the new key is active
- [ ] 4.5 Confirm browser autofill no longer interferes (check with Chrome/Firefox password manager enabled)
