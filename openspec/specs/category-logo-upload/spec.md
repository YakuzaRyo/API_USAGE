# Category Logo Upload

## Purpose

Category logo image management: upload, serve, and delete logo images for vendor categories, stored on local disk.

## Requirements

### Requirement: Upload category logo image
The system SHALL provide `POST /api/categories/{id}/logo` endpoint that accepts a multipart file upload. The endpoint SHALL accept PNG, JPG, SVG, and WebP formats with a maximum size of 20MB. The uploaded file SHALL be saved to `backend/data/logos/{id}.{ext}` where `{ext}` matches the uploaded file extension. The `logo_path` field on the Category record SHALL be updated to the stored file path.

#### Scenario: Upload PNG logo
- **WHEN** a POST request is sent to `/api/categories/1/logo` with a valid PNG file (5MB)
- **THEN** the file is saved to `backend/data/logos/1.png`, the Category's `logo_path` is set to `data/logos/1.png`, and a 200 response with `{"logo_path": "data/logos/1.png"}` is returned

#### Scenario: Upload exceeds size limit
- **WHEN** a POST request is sent with a 25MB file
- **THEN** a 413 response is returned with an error message indicating the 20MB limit

#### Scenario: Upload to non-existent category
- **WHEN** a POST request is sent to `/api/categories/999/logo` and category 999 does not exist
- **THEN** a 404 response is returned

#### Scenario: Upload replaces existing logo
- **WHEN** a category already has a logo at `data/logos/1.png` and a new file is uploaded
- **THEN** the old file is deleted, the new file replaces it, and `logo_path` is updated

### Requirement: Serve category logo image
The system SHALL provide `GET /api/categories/{id}/logo` endpoint that returns the logo image file as a `FileResponse` with the correct MIME type.

#### Scenario: Retrieve existing logo
- **WHEN** a GET request is sent to `/api/categories/1/logo` and the logo exists at `data/logos/1.png`
- **THEN** the image file is returned with `Content-Type: image/png`

#### Scenario: Logo not found
- **WHEN** a GET request is sent to `/api/categories/1/logo` and no logo file exists
- **THEN** a 404 response is returned

### Requirement: Delete category logo image
The system SHALL provide `DELETE /api/categories/{id}/logo` endpoint that removes the logo file from disk and sets the Category's `logo_path` to NULL.

#### Scenario: Delete existing logo
- **WHEN** a DELETE request is sent to `/api/categories/1/logo` and the logo file exists
- **THEN** the file is removed from disk, `logo_path` is set to NULL, and a 200 response is returned

#### Scenario: Delete when no logo exists
- **WHEN** a DELETE request is sent to `/api/categories/1/logo` and no logo file exists
- **THEN** a 200 response is returned (idempotent)

### Requirement: Category model includes logo_path field
The Category model SHALL include a nullable `logo_path` column of type String(512) with a default of NULL.

#### Scenario: New category has no logo
- **WHEN** a new Category is created
- **THEN** its `logo_path` field is NULL

### Requirement: Category list response includes logo_path
The `GET /api/categories` endpoint SHALL include the `logo_path` field in each category object returned.

#### Scenario: Category with logo appears in list
- **WHEN** a category with `logo_path = "data/logos/1.png"` exists
- **THEN** the list response includes `{"id": 1, ..., "logo_path": "data/logos/1.png"}`

#### Scenario: Category without logo appears in list
- **WHEN** a category with `logo_path = null` exists
- **THEN** the list response includes `{"id": 2, ..., "logo_path": null}`
