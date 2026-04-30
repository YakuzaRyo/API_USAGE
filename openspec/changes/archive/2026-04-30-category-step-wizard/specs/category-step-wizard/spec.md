## ADDED Requirements

### Requirement: Category wizard 2-step flow
The system SHALL provide a `CategoryWizard.vue` component that presents category creation and editing as a 2-step wizard. Step 1 SHALL contain name (with preset pill selection), logo upload/preview/delete, and default model management. Step 2 SHALL contain API configuration fields (API Base URL, Usage Path, Balance Path), Token Plan fields (TP Base URL, TP Usage Path), and currency symbol. The wizard SHALL display a step indicator bar and dot navigation matching the ProviderWizard visual pattern.

#### Scenario: Create new category through wizard
- **WHEN** the user clicks "+ 新增" in the category list
- **THEN** the CategoryWizard opens at Step 1 with all fields empty and default values (Usage Path: `/v1/usage`, Currency: `CNY`)
- **AND** the step indicator shows "① 基本信息 → ② API 配置" with Step 1 active

#### Scenario: Navigate through wizard steps
- **WHEN** the user clicks "保存并继续" on Step 1 after filling required fields
- **THEN** the category is saved and the wizard advances to Step 2
- **AND** the dot navigation updates to show Step 2 active

#### Scenario: Navigate backward in wizard
- **WHEN** the user clicks "上一步" on Step 2
- **THEN** the wizard returns to Step 1 without saving

#### Scenario: Dot navigation between steps
- **WHEN** the user clicks a dot in the dot navigation
- **THEN** the wizard jumps to the corresponding step

### Requirement: Logo upload during category creation
The system SHALL allow logo file selection during category creation (Step 1). When the user selects a logo file, the system SHALL cache the file in a reactive ref (`pendingLogoFile`). The logo SHALL NOT be uploaded until the category entity is created. When "保存并继续" is clicked, the system SHALL first call `POST /api/categories` to create the entity, then immediately call `POST /api/categories/{id}/logo` with the cached file. A local preview of the selected file SHALL be shown using `URL.createObjectURL()`.

#### Scenario: Select logo file before creating category
- **WHEN** the user is in create mode (no existing category) and selects a PNG file via the file input
- **THEN** a local preview of the selected image is shown in the logo area
- **AND** the file is stored in `pendingLogoFile` ref but not yet uploaded

#### Scenario: Save and upload logo atomically
- **WHEN** the user clicks "保存并继续" with a pending logo file and valid name
- **THEN** the system creates the category via `POST /api/categories`
- **AND** immediately uploads the logo via `POST /api/categories/{newId}/logo`
- **AND** the wizard advances to Step 2 with the logo preview showing the uploaded image URL

#### Scenario: Logo upload fails after category creation
- **WHEN** the category is created successfully but the logo upload fails
- **THEN** a toast message SHALL display "分类已创建，但 Logo 上传失败"
- **AND** the wizard still advances to Step 2 with the category ID available for editing

#### Scenario: No logo selected during creation
- **WHEN** the user clicks "保存并继续" without selecting a logo
- **THEN** the category is created without a logo, `pendingLogoFile` is null, and no upload call is made

### Requirement: Logo management in edit mode
The system SHALL display the current logo in Step 1 when editing an existing category, using the URL `/api/categories/{id}/logo` with a cache-busting query parameter. The upload and delete buttons SHALL be visible and functional.

#### Scenario: Edit mode shows existing logo
- **WHEN** the user opens a category that has a logo
- **THEN** Step 1 displays the logo image fetched from `/api/categories/{id}/logo?t={timestamp}`

#### Scenario: Replace logo in edit mode
- **WHEN** the user clicks "更换 Logo" and selects a new file
- **THEN** the file is uploaded via `POST /api/categories/{id}/logo` and the preview updates immediately

#### Scenario: Delete logo in edit mode
- **WHEN** the user clicks "删除" on the logo preview
- **THEN** the logo is removed via `DELETE /api/categories/{id}/logo` and the preview is replaced with a placeholder

### Requirement: Wizard component props and events
The CategoryWizard component SHALL accept `category: Category | null` as a prop (null for create mode, Category object for edit mode) and emit a `close` event when the wizard is dismissed or save is completed.

#### Scenario: Open wizard in create mode
- **WHEN** `category` prop is null
- **THEN** the wizard title shows "新增分类" and all form fields are initialized with defaults

#### Scenario: Open wizard in edit mode
- **WHEN** `category` prop is a Category object
- **THEN** the wizard title shows "编辑分类" and all form fields are pre-filled with the category's current values, and the category's ID is stored for update operations

#### Scenario: Close wizard after save
- **WHEN** the user completes Step 2 and clicks "保存"
- **THEN** the component emits the `close` event

### Requirement: Step 1 form validation
The system SHALL validate that the category name is non-empty before allowing the user to proceed from Step 1. If validation fails, an error message SHALL be displayed next to the name field.

#### Scenario: Empty name on save
- **WHEN** the user clicks "保存并继续" with an empty name field
- **THEN** an error message "名称不能为空" appears and the wizard does not advance

#### Scenario: Valid name on save
- **WHEN** the user clicks "保存并继续" with a non-empty name
- **THEN** the category is created/updated and the wizard advances to Step 2
