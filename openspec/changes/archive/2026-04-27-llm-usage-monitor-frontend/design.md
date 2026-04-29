## Context

LLM 用量监控平台的前端部分。项目从零新建 `frontend/` 目录，技术栈与架构模式完全继承 `workflow_develop/frontend`，确保 UI 风格、代码组织、状态管理方式统一。与后端 `llm-usage-monitor-backend` 通过 REST API 通信。

## Goals / Non-Goals

**Goals:**
- 提供厂商配置的完整 CRUD 界面，包含用量 API 路径、追踪模型、轮询间隔设置，支持连接测试和手动触发采集
- 提供 ECharts 驱动的用量统计 Dashboard（趋势图、分布图、总计卡牌、Provider 筛选）
- 应用外壳提供侧边导航 + 路由，跨页面状态通过 Pinia 管理
- 组件与风格完全沿用 workflow_develop 的 neumorphism 设计语言

**Non-Goals:**
- 不含用户认证/登录系统
- 不含脚本上传/管理页面（用量采集由后端内置 HTTP caller 完成，前端只需配置 Provider）
- 不含实时 WebSocket 推送（用量数据通过 Axios 手动刷新获取）

## Decisions

### D1: Vue 3 Composition API + `<script setup>`

沿用 workflow_develop 的组件写法，所有组件使用 `<script setup lang="ts">`，不引入 Options API 或 class-style 组件。

### D2: 页面路由

```
/                  → redirect to /dashboard
/dashboard         → 用量统计看板（首页）
/providers         → 厂商配置管理
```

理由：Dashboard 作为首页让用户一打开就看到用量概览。Provider 配置页承载所有厂商相关的设置（凭证、API 路径、追踪模型、轮询间隔、手动采集触发）。取消脚本管理页 — 用量采集由后端内置 HTTP caller 完成，前端无需脚本概念。

### D3: Pinia Store 拆分

```
stores/providers.ts   — 厂商列表 (Provider[]) CRUD + 连接测试 + 手动采集触发
stores/usage.ts       — 用量数据 (UsageSummary, TrendPoint[]) 只读
```

每个 Store 独立管理自己的 API 调用和 loading 状态。不使用全局 user/session store（本项目无认证）。

### D4: API 层设计

`src/api/index.ts` — 单一文件定义所有 Axios 接口、TypeScript 类型、请求函数。完全照搬 workflow_develop 的模式：

```ts
// 类型定义
export interface Provider {
  id: number; name: string; api_key: string; base_url: string
  usage_api_path: string; models: string[]; interval_seconds: number
  created_at: string
}
export interface UsageSummary { total_tokens: number; total_cost: number; active_providers: number }
export interface TrendPoint { date: string; tokens: number; cost: number; provider_name: string }
export interface DistributionPoint { model: string; tokens: number }

// 请求函数
export const fetchProviders = () => api.get<Provider[]>('/providers')
export const createProvider = (data) => api.post<Provider>('/providers', data)
export const updateProvider = (id, data) => api.put<Provider>(`/providers/${id}`, data)
export const deleteProvider = (id) => api.delete(`/providers/${id}`)
export const testProvider = (id) => api.post(`/providers/${id}/test`)
export const triggerCollection = (id) => api.post(`/providers/${id}/collect`)
export const fetchUsageSummary = (params?) => api.get<UsageSummary>('/stats/summary', { params })
export const fetchUsageTrends = (params?) => api.get<TrendPoint[]>('/stats/trends', { params })
export const fetchUsageDistribution = (params?) => api.get<DistributionPoint[]>('/stats/distribution', { params })
```

### D5: UI 设计语言继承

从 workflow_develop 的 `style.css` 和 `StatsDashboard.vue` 提取全局变量与组件风格：

| 元素 | 取值 |
|------|------|
| 卡片背景 | `var(--color-surface)`, 1px `var(--color-border)` solid |
| 卡片阴影 | `var(--shadow-md)`, hover 时 `var(--shadow-lg)` |
| hover 动效 | `translate(-3px, -3px)` + 阴影切换 |
| 页面标题 | `font-size: 24px; font-weight: 800;` |
| 统计数字 | `font-size: 36px; font-weight: 900;` |
| 布局间距 | `var(--space-md)`, `var(--space-lg)`, `var(--space-2xl)` |
| 按钮原色 | `#FF6B35`（品牌橙，从 workflow_develop distribution bar 提取） |

### D6: Vite 代理配置

```ts
// vite.config.ts
proxy: { '/api': 'http://localhost:8000' }
```

与 workflow_develop 完全一致，开发时前端 `localhost:5173` 代理到后端 `localhost:8000`。

## Risks / Trade-offs

- **后端接口未就绪时前端先行** → 前端先 mock 数据类型和页面结构，后续对接真实 API 时只需改 API base layer
- **ECharts 图表在 resize 时需手动销毁重建** → 沿用 workflow_develop 的 `window.addEventListener('resize', () => chart.resize())` 模式，组件卸载时 dispose
- **API Key 在前端明文展示风险** → Provider 编辑页使用 password 类型 input 遮挡，列表中默认脱敏（仅显示后 4 位）
