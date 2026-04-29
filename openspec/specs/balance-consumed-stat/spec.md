# Balance Consumed Stat

## Purpose

Tracks total balance consumed since first collection in the dashboard stats cards.

## ADDED Requirements

### Requirement: Balance consumed in summary API
The stats summary API SHALL return a `balance_consumed` field representing the total balance decrease since each provider's first collection.

#### Scenario: Balance consumed computed
- **WHEN** a provider has initial balance 100 and current balance 70
- **THEN** `balance_consumed` is 30.0

#### Scenario: No balance history
- **WHEN** no provider has balance collection history
- **THEN** `balance_consumed` is 0.0

### Requirement: Balance consumed stat card
The Dashboard SHALL display a fifth stat card showing balance consumed total, styled identically to the existing four cards.

#### Scenario: Card visible
- **WHEN** the dashboard loads with balance data
- **THEN** a card labeled "余额消耗" appears with the consumed amount and currency symbol
