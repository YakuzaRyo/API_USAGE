## 1. Create CategoryWizard component

- [x] 1.1 Create `frontend/src/components/CategoryWizard.vue` with props (`category: Category | null`) and emit (`close`), set up 2-step state (`currentStep: ref<1 | 2>`)
- [x] 1.2 Build Step 1 template: logo preview area (with upload/replace/delete buttons), preset pill row, name input, default model tag input — matching ProviderWizard's `.wizard-modal` / `.wizard-steps-label` / `.step-panel` CSS classes
- [x] 1.3 Build Step 2 template: API section (base_url, usage_path, balance_path), Token Plan section (tp_base_url, tp_usage_path), currency symbol input
- [x] 1.4 Add wizard chrome: step indicator ("基本信息 → API 配置"), dot navigation, action buttons ("上一步" / "保存并继续" / "保存"), close button

## 2. Implement wizard logic

- [x] 2.1 Implement form state initialization — create mode: empty defaults; edit mode: pre-fill from `category` prop including logo URL (`/api/categories/{id}/logo?t={timestamp}`)
- [x] 2.2 Implement Step 1 validation — name must be non-empty, show inline error on "保存并继续" if empty
- [x] 2.3 Implement `saveAndContinue()` for Step 1 — create mode: `POST /categories` → if `pendingLogoFile` exists call `POST /categories/{id}/logo` → advance to Step 2; edit mode: `PUT /categories/{id}` → advance to Step 2
- [x] 2.4 Implement `pendingLogoFile` ref for create mode — file input caches to ref, preview via `URL.createObjectURL()`, uploaded after entity creation in `saveAndContinue()`
- [x] 2.5 Implement `saveOnly()` for Step 2 — `PUT /categories/{id}` with API config fields → emit `close`
- [x] 2.6 Implement logo upload/delete in edit mode — upload calls `uploadCategoryLogo(id, file)` and refreshes preview; delete calls `deleteCategoryLogo(id)` and clears preview
- [x] 2.7 Implement step navigation — `goBack()`, `goToStep()`, dot click handlers

## 3. Refactor CategoryManager.vue

- [x] 3.1 Remove modal template, form reactive state, `onLogoSelect`/`onLogoDelete`/`save`/`openCreate`/`openEdit` functions from CategoryManager.vue
- [x] 3.2 Add `CategoryWizard` import and render with `v-if="showWizard"`, passing `selectedCategory` prop and `@close` handler
- [x] 3.3 Update grid item click and "+ 新增" button to set `selectedCategory` and `showWizard = true` instead of opening the old modal
- [x] 3.4 Remove unused CSS (`.top-row`, `.top-logo`, `.top-fields`, `.top-logo-actions`, `.section-divider`, `.preset-row`, `.pill-preset`, form group styles)
- [x] 3.5 Keep toast, delete confirmation dialog, and loading/empty state in CategoryManager.vue unchanged

## 4. Copy wizard styles from ProviderWizard

- [x] 4.1 Copy ProviderWizard's scoped CSS classes into CategoryWizard: `.wizard-modal`, `.wizard-header`, `.wizard-close`, `.wizard-steps-label`, `.step-arrow`, `.wizard-body`, `.step-panel`, `.wizard-actions`, `.wizard-dots`, `.wizard-dot`
- [x] 4.2 Add Category-specific styles: logo preview area, preset pill row, model tag input

## 5. Verify

- [ ] 5.1 Test create flow: "+ 新增" → fill name → select logo → "保存并继续" → verify category created with logo → fill Step 2 → "保存" → verify in grid
- [ ] 5.2 Test edit flow: click logo in grid → verify Step 1 pre-filled with name, logo, models → modify → "保存并继续" → modify Step 2 → "保存" → verify updates
- [ ] 5.3 Test logo failure case: create with invalid logo file → verify category still created, error toast shown
- [ ] 5.4 Test delete confirmation still works from grid context menu
