## ADDED Requirements

### Requirement: Active providers count from Provider table
The summary API SHALL count all non-deleted providers as active providers, rather than counting distinct provider IDs from UsageRecord.

#### Scenario: Newly registered provider counted
- **WHEN** a provider exists with deleted=False but has no UsageRecord entries
- **THEN** the `active_providers` count includes this provider

#### Scenario: Deleted provider excluded
- **WHEN** a provider has deleted=True
- **THEN** it is excluded from the `active_providers` count
