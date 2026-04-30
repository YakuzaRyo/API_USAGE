## MODIFIED Requirements

### Requirement: Category edit modal with billing mode tabs
The category creation/editing interface SHALL use a 2-step wizard component (`CategoryWizard.vue`) instead of a flat modal. Step 1 SHALL contain name field (with preset pills), logo preview with upload/replace/delete buttons, and default model management. Step 2 SHALL contain API section (base_url, usage_api_path, balance_api_path), Token Plan section (tp_base_url, tp_usage_path), and currency_symbol. The wizard SHALL display a step indicator and dot navigation consistent with ProviderWizard. The wizard SHALL support both create mode (no existing category) and edit mode (pre-filled from existing category). Creating a category with a logo SHALL work by creating the entity first then uploading the logo in a single "保存并继续" action.

#### Scenario: Form displays as step wizard
- **WHEN** the user opens create or edit for a category
- **THEN** a wizard appears with 2 steps: "基本信息" → "API 配置", with step indicator and dot navigation

#### Scenario: Create new category
- **WHEN** user clicks "+ 新增" and fills Step 1 fields then clicks "保存并继续"
- **THEN** a POST request creates the category, and the wizard advances to Step 2

#### Scenario: Edit existing category
- **WHEN** user clicks a category's logo in the grid
- **THEN** the wizard opens at Step 1 with all fields pre-filled and logo preview visible

#### Scenario: Upload logo during creation
- **WHEN** user selects a logo file in create mode and clicks "保存并继续"
- **THEN** the category is created first, then the logo is uploaded using the new category's ID, and the wizard advances to Step 2

#### Scenario: Upload logo in edit mode
- **WHEN** user clicks the upload area in Step 1 and selects a PNG file
- **THEN** the logo is uploaded via `POST /api/categories/{id}/logo` and the preview updates immediately

#### Scenario: Remove logo in edit mode
- **WHEN** user clicks the delete button on the logo preview
- **THEN** the logo is removed via `DELETE /api/categories/{id}/logo` and the preview reverts to placeholder

## REMOVED Requirements

### Requirement: Category list page with card layout
**Reason**: The grid layout, spotlight hover, and click-to-edit behavior remain unchanged. Only the modal trigger mechanism changes — the grid itself is not affected at the spec level.
**Migration**: Grid interaction unchanged. The only change is that clicking a logo now opens CategoryWizard instead of the inline modal.

### Requirement: Category deletion
**Reason**: Deletion flow is unchanged — confirmation dialog and provider dissociation remain identical. No spec-level behavior change.
**Migration**: Unchanged. Deletion is handled by CategoryManager.vue independently of the wizard.

### Requirement: Category preset name list
**Reason**: Preset API is unchanged. Preset pills move from inline modal to CategoryWizard Step 1 but the data source and behavior are identical.
**Migration**: Unchanged. `GET /api/categories/presets` still returns the same data.

### Requirement: Category CRUD APIs
**Reason**: Backend APIs are completely unchanged.
**Migration**: No migration needed.
