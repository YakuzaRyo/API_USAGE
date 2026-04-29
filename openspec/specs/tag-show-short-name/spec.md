# Tag Show Short Name

## Purpose

Mapping path tags display only the leaf key name instead of the full JSONPath, reducing visual clutter.

## ADDED Requirements

### Requirement: Tag displays leaf key only
Mapping path tags SHALL display only the last segment of the JSONPath, while preserving the full path as the underlying value.

#### Scenario: Tag shows short name
- **WHEN** user clicks a JSON tree key with path `balance_infos.0.total_balance`
- **THEN** the mapping input displays `[total_balance ×]` but the field value remains `balance_infos.0.total_balance`
