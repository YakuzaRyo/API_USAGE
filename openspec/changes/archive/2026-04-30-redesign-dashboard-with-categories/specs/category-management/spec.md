# Category Management

## ADDED Requirements

### Requirement: Category list page with card layout
The system SHALL provide a category management page at `/categories` displaying all categories as a grid of cards. Each card SHALL show the category name tag, billing mode/currency pair, model list, an edit button, and a delete icon at the top-right corner. The page SHALL include a "+ 新增" button for creating new categories.

#### Scenario: Card displays core information
- **WHEN** a category exists with name "OpenAI", billing_mode "api", currency "USD", and models [gpt-4, gpt-3.5]
- **THEN** the card shows tag "OpenAI", text "API · USD", model tags gpt-4 and gpt-3.5, an [编辑] button, and a 🗑 icon at top-right

#### Scenario: Empty state
- **WHEN** no categories exist
- **THEN** a dashed empty-state card prompts the user to add the first category

### Requirement: Category edit modal with billing mode tabs
The category edit modal SHALL contain a name field (preset dropdown with custom input) and two tab pills for "API 模式" and "Token Plan". Each tab SHALL show: base_url, usage_api_path, and balance_api_path (API mode only). Below the tabs, currency_symbol and models SHALL be shared across both tabs. All path fields are optional.

#### Scenario: Create new category
- **WHEN** user clicks "+ 新增" and fills the form
- **THEN** a POST request creates the category and the card appears in the list

#### Scenario: Edit existing category
- **WHEN** user clicks [编辑] on a category card
- **THEN** the modal opens with all fields pre-filled from the category data, and the active tab matches the category's existing billing_mode data

#### Scenario: Switch billing mode tab
- **WHEN** user switches from "API 模式" tab to "Token Plan" tab
- **THEN** the URL and path fields update to show the Token Plan configuration, while currency and models remain unchanged

#### Scenario: Name preset autofill
- **WHEN** user selects "OpenAI" from the preset dropdown
- **THEN** the base_url and models fields pre-fill with sensible defaults for that vendor

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
- **THEN** a JSON array of strings like ["OpenAI", "Anthropic", "Google", "Deepseek", "阿里", "百度", "字节", "智谱", "月之暗面"] is returned

### Requirement: Category CRUD APIs
The system SHALL expose `GET /api/categories`, `POST /api/categories`, `PUT /api/categories/{id}`, and `DELETE /api/categories/{id}`.

#### Scenario: List categories
- **WHEN** GET /api/categories is called
- **THEN** all categories are returned with id, name, api_base_url, api_usage_path, api_balance_path, tp_base_url, tp_usage_path, currency_symbol, and models

#### Scenario: Create category
- **WHEN** POST /api/categories is called with valid data
- **THEN** a new category is created and returned with its id
