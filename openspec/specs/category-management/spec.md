# Category Management

## Purpose

厂商分类模板管理，支持预设和自定义分类，每个分类配置 API/TokenPlan 两种计费模式的 URL 和路径模板，用于 Provider 创建时自动填充。

## Requirements

### Requirement: Category list page with card layout
The system SHALL provide a category management page at `/categories` displaying all categories as a Logo icon grid. Each grid cell SHALL display the category's logo image (or a first-letter placeholder if no logo). The grid SHALL use CSS Grid with fixed cell size and `object-fit: contain` for logo images. When the user hovers directly on a `.logo-item` element, it SHALL scale up (1.15x) and display the category name below it, while all other logos SHALL scale down (0.75x) and fade (opacity 0.4, blur 1px). The spotlight effect SHALL only trigger when the mouse is hovering directly on a `.logo-item` element — when the mouse is in the gap between items or in empty grid space, all logos SHALL remain in their normal (unmodified) state. Clicking a logo SHALL open the edit modal. The page SHALL include a "+ 新增" button for creating new categories.

#### Scenario: Grid displays logos with spotlight hover
- **WHEN** the page loads with categories [OpenAI (has logo), Anthropic (no logo), Google (has logo)]
- **THEN** OpenAI and Google show their uploaded logo images, Anthropic shows a placeholder with its first letter "A", all arranged in a compact grid
- **AND WHEN** the user hovers directly on the OpenAI logo
- **THEN** the OpenAI logo scales to 1.15x and "OpenAI" text appears below it, while Anthropic and Google logos shrink to 0.75x with opacity 0.4 and blur 1px

#### Scenario: Mouse in gap between logos
- **WHEN** the mouse is positioned in the gap between two logos (not on any logo)
- **THEN** all logos remain at normal scale (1.0), full opacity (1.0), and no blur

#### Scenario: Mouse hovers a specific logo
- **WHEN** the mouse hovers directly on a logo item
- **THEN** the hovered logo scales to 1.15x with full opacity, and all other logos scale to 0.75x with opacity 0.4 and blur 1px

#### Scenario: Click logo to edit
- **WHEN** the user clicks on a category's logo in the grid
- **THEN** the edit modal opens with all fields pre-filled

#### Scenario: Empty state
- **WHEN** no categories exist
- **THEN** a dashed empty-state area prompts the user to add the first category

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

### Requirement: Category deletion
The system SHALL allow deleting a category. Providers associated with the deleted category SHALL have their category_id set to NULL.

#### Scenario: Delete category with providers
- **WHEN** user clicks 🗑 on a category that has 3 associated providers
- **THEN** the category is deleted, and those 3 providers retain their data but have no category association

#### Scenario: Delete confirmation
- **WHEN** user clicks 🗑 on a category card
- **THEN** a confirmation dialog appears before the deletion proceeds

### Requirement: Category preset name list
The system SHALL expose `GET /api/categories/presets` returning a list of predefined category names.

#### Scenario: Preset list returned
- **WHEN** the API is called
- **THEN** a JSON array of strings is returned (OpenAI, Anthropic, Google, Deepseek, etc.)

### Requirement: Category CRUD APIs
The system SHALL expose `GET /api/categories`, `POST /api/categories`, `PUT /api/categories/{id}`, and `DELETE /api/categories/{id}`.

#### Scenario: List categories
- **WHEN** GET /api/categories is called
- **THEN** all categories are returned with full field set

#### Scenario: Create category
- **WHEN** POST /api/categories is called with valid data
- **THEN** a new category is created and returned with its id
