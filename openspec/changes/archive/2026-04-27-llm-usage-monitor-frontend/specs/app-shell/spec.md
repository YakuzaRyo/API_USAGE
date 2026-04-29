## ADDED Requirements

### Requirement: Application scaffold with Vue 3 + TypeScript + Vite

The system SHALL provide a `frontend/` project initialized with Vite 8, Vue 3, TypeScript, and the same dependency set as workflow_develop (Vue Router 4, Pinia, ECharts 6, Axios).

#### Scenario: Project boots successfully

- **WHEN** user runs `npm install && npm run dev` from `frontend/`
- **THEN** the dev server starts on `http://localhost:5173` with hot reload enabled

#### Scenario: TypeScript compiles without errors

- **WHEN** user runs `npm run build` (which includes `vue-tsc` type checking)
- **THEN** the build completes successfully with no TypeScript errors

### Requirement: Sidebar navigation with two routes

The system SHALL provide a sidebar navigation bar with two menu items: Dashboard (`/dashboard`), 厂商管理 (`/providers`). The root path `/` SHALL redirect to `/dashboard`.

#### Scenario: Navigate to each page via sidebar

- **WHEN** user clicks "Dashboard" in the sidebar
- **THEN** the router navigates to `/dashboard` and the Dashboard component renders
- **WHEN** user clicks "厂商管理"
- **THEN** the router navigates to `/providers`

#### Scenario: Root path redirects to dashboard

- **WHEN** user navigates to `/`
- **THEN** the browser is redirected to `/dashboard`

### Requirement: Global style system matching workflow_develop

The system SHALL provide global CSS variables (`--color-surface`, `--color-border`, `--color-text-muted`, `--shadow-md`, `--shadow-lg`, `--space-xs` through `--space-2xl`) matching the neumorphism design language of workflow_develop. Card components SHALL use `border`, `box-shadow`, and hover `translate(-3px, -3px)` transitions.

#### Scenario: Cards render with consistent neumorphism style

- **WHEN** any page renders a `.card` element
- **THEN** it displays with `var(--color-surface)` background, `var(--shadow-md)` box-shadow, and 1px `var(--color-border)` border
- **WHEN** user hovers over the card
- **THEN** the card animates with `translate(-3px, -3px)` and `var(--shadow-lg)`

#### Scenario: Brand color is applied

- **WHEN** charts or accent elements render
- **THEN** they use `#FF6B35` as the primary brand accent color
