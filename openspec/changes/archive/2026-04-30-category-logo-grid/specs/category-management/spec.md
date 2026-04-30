## MODIFIED Requirements

### Requirement: Category list page with card layout
The system SHALL provide a category management page at `/categories` displaying all categories as a Logo icon grid. Each grid cell SHALL display the category's logo image (or a first-letter placeholder if no logo). The grid SHALL use CSS Grid with fixed cell size and `object-fit: contain` for logo images. When the user hovers over a logo, it SHALL scale up (1.2×) and display the category name below it, while all other logos SHALL scale down (0.75×) and fade (opacity 0.4, blur 1px). Clicking a logo SHALL open the edit modal. The page SHALL include a "+ 新增" button for creating new categories.

#### Scenario: Grid displays logos with spotlight hover
- **WHEN** the page loads with categories [OpenAI (has logo), Anthropic (no logo), Google (has logo)]
- **THEN** OpenAI and Google show their uploaded logo images, Anthropic shows a placeholder with its first letter "A", all arranged in a compact grid
- **AND WHEN** the user hovers over the OpenAI logo
- **THEN** the OpenAI logo scales to 1.2× and "OpenAI" text appears below it, while Anthropic and Google logos shrink to 0.75× with opacity 0.4 and blur 1px

#### Scenario: Click logo to edit
- **WHEN** the user clicks on a category's logo in the grid
- **THEN** the edit modal opens with all fields pre-filled

#### Scenario: Empty state
- **WHEN** no categories exist
- **THEN** a dashed empty-state area prompts the user to add the first category

### Requirement: Category edit modal with billing mode tabs
The category edit modal SHALL contain a name field (preset dropdown with custom input), a logo preview section with upload/replace/delete buttons, and a single form displaying both API mode and Token Plan configurations simultaneously (no tabs). The form SHALL show: API section (base_url, usage_api_path, balance_api_path), Token Plan section (base_url, usage_api_path), and shared fields (currency_symbol, models).

#### Scenario: Create new category
- **WHEN** user clicks "+ 新增" and fills the form
- **THEN** a POST request creates the category and the logo appears in the grid

#### Scenario: Edit existing category with logo
- **WHEN** user clicks a category's logo in the grid
- **THEN** the modal opens with the current logo preview visible, name pre-filled, and both API and Token Plan sections showing their respective values

#### Scenario: Upload logo in edit modal
- **WHEN** user clicks the upload area in the edit modal and selects a PNG file
- **THEN** the logo is uploaded via `POST /api/categories/{id}/logo` and the preview updates immediately

#### Scenario: Remove logo in edit modal
- **WHEN** user clicks the delete button on the logo preview
- **THEN** the logo is removed via `DELETE /api/categories/{id}/logo` and the grid reverts to showing the first-letter placeholder
