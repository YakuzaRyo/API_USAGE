# Ring Gauge Dashboard

## ADDED Requirements

### Requirement: Four ring gauge cards replace stat cards on comprehensive dashboard
The comprehensive dashboard SHALL render four SVG-based ring gauge cards replacing the existing rectangular stat cards. Each ring SHALL display proportional arc segments split by a data dimension, with a total value in the center. No "full ring" reference value exists — the ring represents 100% of the currently visible data.

#### Scenario: Ring cards are displayed
- **WHEN** the 综合看板 pill is active
- **THEN** four ring gauge cards are rendered in a grid

#### Scenario: Empty state
- **WHEN** no data exists for a ring
- **THEN** the ring shows a full gray arc and the center displays 0 or "—"

### Requirement: Token consumption ring card
The Token 消耗 card SHALL display a single ring with arc segments proportional to each model's token share of total consumption. A legend below the ring SHALL list each model by name with a colored indicator. Clicking a legend item SHALL toggle that model's segment visibility and recalculate proportions.

#### Scenario: Model segments rendered
- **WHEN** token consumption data for models [gpt-4: 60%, gpt-3.5: 25%, claude: 15%] is available
- **THEN** the ring shows 3 colored arc segments with proportional lengths, and the center shows the total token count

#### Scenario: Legend filter toggles segment
- **WHEN** user clicks "gpt-3.5" in the legend
- **THEN** the gpt-3.5 arc segment disappears, the ring redraws with gpt-4 and claude segments rescaled to fill 100%, and the center total updates to the filtered sum

### Requirement: Active provider count ring card
The 活跃厂商 card SHALL display a single ring with arc segments proportional to each category's provider count. A legend below the ring SHALL list each category with a colored indicator and count.

#### Scenario: Category count segments
- **WHEN** there are 3 OpenAI providers, 2 Anthropic providers, and 1 Deepseek provider
- **THEN** the ring shows 3 arcs: OpenAI 50%, Anthropic 33%, Deepseek 17%, and the center displays total count 6

### Requirement: Current balance ring card (dual ring)
The 当前余额 card SHALL display two concentric rings. The outer ring SHALL split by category (sum of provider balances per category). The inner ring SHALL split by individual provider balance. Two legend groups SHALL be shown: outer ring legend and inner ring legend. Filtering the outer ring category SHALL hide both the outer segment and all inner segments belonging to that category. Filtering an inner ring provider SHALL hide only that provider's segment.

#### Scenario: Dual ring rendered
- **WHEN** balance data has categories [OpenAI: ¥3.0, Deepseek: ¥2.0] and providers [OpenAI-GPT4: ¥2.0, OpenAI-GPT3: ¥1.0, Deepseek-Chat: ¥2.0]
- **THEN** outer ring shows 2 segments (OpenAI 60%, Deepseek 40%), inner ring shows 3 segments (OpenAI-GPT4 40%, OpenAI-GPT3 20%, Deepseek-Chat 40%), and center shows total balance ¥5.0

#### Scenario: Outer category filter hides inner providers
- **WHEN** user clicks "Deepseek" in the outer legend
- **THEN** the outer Deepseek segment and the inner Deepseek-Chat segment both disappear, remaining segments rescale

### Requirement: Billing cost ring card (dual ring)
The 费用 card SHALL display two concentric rings. The outer ring SHALL split by billing_mode (API vs TokenPlan). The inner ring SHALL split by provider. Two legend groups with toggle interaction identical to the balance card.

#### Scenario: Billing mode outer ring
- **WHEN** billing summary has API mode ¥8.0 and TokenPlan ¥4.0
- **THEN** outer ring shows 2 segments (API 67%, TokenPlan 33%), inner ring shows per-provider breakdown, and center shows total ¥12.0

### Requirement: Neo-Brutalist visual style for ring cards
Ring cards SHALL follow the site's Neo-Brutalist design: zero-radius card containers, 2px solid black borders, hard offset shadows, thick ring strokes (≥10px) with solid colors and no gradients, and bold typography using the existing `--font-sans` stack. The first segment color SHALL be `--color-primary: #FF6B35`.

#### Scenario: Card style matches site
- **WHEN** a ring card is rendered
- **THEN** the card container has `border-radius: 0`, `border: 2px solid var(--color-border)`, `box-shadow: var(--shadow-md)`, and hover translates with `var(--shadow-lg)`

### Requirement: SVG stroke-dasharray implementation
Ring arc segments SHALL be implemented using SVG `<circle>` elements with `stroke-dasharray` and `stroke-dashoffset` calculated from data proportions. No external chart library SHALL be required.

#### Scenario: Single segment ring
- **WHEN** data has only one category with 100%
- **THEN** the ring renders a full circle arc with the segment color

#### Scenario: Multiple segments
- **WHEN** data has 3 categories with proportions 40%, 35%, 25%
- **THEN** 3 SVG circle elements are rendered, each with stroke-dasharray and offset calculated such that arcs are contiguous around the ring
