## Context

The wizard's Step 2 (Usage API) and Step 3 (Balance API) each have a "测试" button that calls `POST /api/providers/test-api` with `{ base_url, api_key, api_path }`. The `api_key` comes from `form.api_key`, which in edit mode holds the masked value (`...<last-4>`) returned by `GET /api/providers`.

The existing `test-api` endpoint blindly forwards whatever `api_key` it receives. It has no knowledge of which provider (if any) the request is for. This works for new providers (user typed the real key) but is broken for edit mode.

The `collect_usage` function (used by "立即采集") has no such problem — it reads the provider from DB and decrypts the real key internally.

## Goals / Non-Goals

**Goals:**
- "测试" in edit mode uses the real (decrypted) API key from the database
- "测试" in create mode continues to use the form-entered key
- No regression to collection flow

**Non-Goals:**
- Returning the real key to the frontend (security boundary)
- Changing the UX of the test button

## Decisions

### Decision 1: New provider-scoped test endpoint

Add `POST /api/providers/{provider_id}/test-api` that accepts `{ api_path }` (no `base_url` or `api_key`). The handler:
1. Loads the provider from DB
2. Decrypts `provider.api_key`
3. Constructs the URL from `provider.base_url` + `api_path`
4. Sends the request with `Authorization: Bearer {decrypted_key}`
5. Returns the same response shape as the existing endpoint

**Why not modify the existing endpoint?** The existing endpoint is stateless — it takes explicit `base_url` + `api_key`. Adding optional `provider_id` would create a confusing dual-mode endpoint. A separate endpoint has clear semantics: "test using this provider's stored credentials."

### Decision 2: Frontend routes to correct endpoint

```typescript
// In doStep2Test / doStep3Test:
if (editingId.value) {
  res = await testApiForProvider(editingId.value, { api_path: form.usage_api_path })
} else {
  res = await testApi({ base_url: form.base_url, api_key: form.api_key, api_path: form.usage_api_path })
}
```

The new `testApiForProvider` only sends `api_path` — the backend reads everything else from the stored provider.

## Risks / Trade-offs

- **[Risk] Two endpoints doing similar things** → Mitigation: The new endpoint is thin — it resolves credentials then delegates to the same HTTP logic. They share the response shape.
- **[Trade-off] Create-mode test still requires the frontend to hold the real key in memory** → Acceptable: this is only during initial setup, before the key is persisted. The alternative (saving first, then testing) is worse UX.
