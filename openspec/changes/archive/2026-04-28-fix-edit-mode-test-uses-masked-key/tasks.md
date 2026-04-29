## 1. Backend — New provider-scoped test endpoint

- [x] 1.1 Add schema `ProviderTestApiRequest` with `api_path: str` in `routers/providers.py`
- [x] 1.2 Add `POST /api/providers/{provider_id}/test-api` route that loads the provider, decrypts `api_key`, constructs the URL from `provider.base_url + api_path`, and proxies the GET request with `Authorization: Bearer {decrypted_key}`
- [x] 1.3 Return the same response shape as the existing `POST /api/providers/test-api` endpoint (`{ status_code, body }`)

## 2. Frontend — API layer

- [x] 2.1 Add `testApiForProvider(providerId: number, data: { api_path: string })` function in `api/index.ts`

## 3. Frontend — Wizard test logic

- [x] 3.1 Modify `doStep2Test` in `ProviderWizard.vue` to call `testApiForProvider` when `editingId.value` is set, otherwise use the existing `testApi`
- [x] 3.2 Modify `doStep3Test` in `ProviderWizard.vue` to call `testApiForProvider` when `editingId.value` is set, otherwise use the existing `testApi`

## 4. Verification

- [ ] 4.1 Create a provider with a valid API key, save, and re-open the wizard
- [ ] 4.2 In edit mode, enter a usage API path and click "测试" — verify the response is correctly parsed with JSONPath tags
- [ ] 4.3 In edit mode, enter a balance API path and click "测试" — verify the response is correctly parsed
- [ ] 4.4 In create mode (new provider), verify both "测试" buttons still work with form-entered credentials
