## Context

The backend stores API keys encrypted with Fernet. When returning providers via `GET /api/providers`, the response includes `api_key` as a masked value (`...<last-4-chars>`). The frontend `ProviderWizard` populates the Step 1 API key password input with this masked value on edit.

When the user saves (any step), `buildPayload()` always includes the current `form.api_key`. If the user never touched the field — which is the common case since the password dots obscure whether the value is real or masked — the masked string is sent to `PUT /api/providers/{id}`. The backend's `update_provider` encrypts whatever string it receives.

Additionally, the password input lacks `autocomplete` attributes, so browser password managers may autofill unrelated credentials, further corrupting the stored key.

```
Current corrupt flow:
  DB encrypt(real) → decrypt → mask → GET → form → PUT → encrypt(masked) → DB
```

## Goals / Non-Goals

**Goals:**
- Ensure that saving the wizard without editing the API key field preserves the original key
- Prevent browser autofill from injecting unrelated passwords into the API key field
- Add a server-side safety net so a masked-sentinel value is never re-encrypted

**Non-Goals:**
- Changing the encryption mechanism (Fernet is fine)
- Showing the full plaintext key in the UI (security; keep it masked)
- Adding a "reveal/hide" toggle for the password field (out of scope)

## Decisions

### Decision 1: Track dirty state on the API key field (frontend)

Add a `ref<boolean>` that becomes `true` only when the user types into the API key input. When `dirty` is false, `buildPayload()` excludes `api_key` from the sent object entirely. The backend `ProviderUpdate.api_key` is already `str | None = None`, so omitting the key is already supported.

**Alternatives considered:**
- *Compare form value to masked original*: Fragile — the masked string itself changes after each corruption, and browser autofill changes the value without user intent.
- *Send a sentinel like `"__UNCHANGED__"`*: Adds coupling between frontend and backend; dirtier than just omitting the field.
- *Fix purely in backend*: Backend can't distinguish "user typed a new key that happens to look masked" from "unchanged value". The `...` prefix check is a defense layer but not sufficient alone.

### Decision 2: Add autocomplete="off" on the password input (frontend)

The API key field is `type="password"`. Without `autocomplete="off"`, browsers treat it as a login password and autofill saved credentials. This is a one-line template change.

### Decision 3: Backend skips update if the value looks like a masked key (backend)

As a defense-in-depth measure: before encrypting, compare `data.api_key` against `mask_key(decrypt(provider.api_key))`. If they match, skip the `api_key` update. This catches any path where a masked value reaches the backend, including direct API calls or future UI changes.

Alternative: Check if value starts with `...` — simpler but would incorrectly block a real key that genuinely starts with `...`.

## Risks / Trade-offs

- **[Risk] Frontend-only fix could regress if another UI path edits providers** → Mitigation: Backend defense layer catches any masked value regardless of source.
- **[Risk] Legitimate keys matching `...<4chars>` pattern are rejected** → Mitigation: The check compares against the *actual* masked form of the *currently stored* decrypted key, not just a `...` prefix pattern. A genuine key would only be blocked if it exactly equals the masked version of the current key, which is astronomically unlikely.
- **[Trade-off] The user must explicitly type to change the API key** → Acceptable UX: changing credentials is an explicit action; a blank/unchanged field preserving the existing value is expected behavior.
