## Why

多个 LLM 厂商的 API 用量（Token 消耗、费用、余额）分散在不同平台，用户需要统一查看用量趋势和统计。需要一个前端界面，能配置厂商信息、上传查询脚本、并通过可视化 Dashboard 直观展示用量数据。现在开始构建，与后端 Change `llm-usage-monitor-backend` 并行推进。

## What Changes

- 新增 LLM 用量监控前端应用，采用 Vue 3 + TypeScript + Vite 技术栈
- 沿用 workflow_develop 项目的 UI 风格（色系、卡片阴影、布局、导航模式）
- 新增厂商配置管理页面，支持 API Key、Base URL、用量查询 API 路径、追踪模型列表、轮询间隔的完整配置
- 用量数据采集由后端内置 HTTP caller 完成，前端无需脚本管理页面
- 新增用量统计 Dashboard，使用 ECharts 展示用量趋势、模型分布、费用汇总
- 新增应用外壳（路由 + 侧边导航 + 全局样式），保持与 workflow_develop 一致的设计语言

## Capabilities

### New Capabilities

- `app-shell`: 应用框架（侧边导航栏、Vue Router 路由配置、全局 CSS 变量与 neumorphism 风格），初始化 Vite + Vue 3 + TypeScript 项目骨架，两页路由（Dashboard + 厂商管理）
- `provider-config-ui`: 厂商配置管理页面 — 列表展示已配置厂商、新增/编辑/删除厂商表单（名称、API Key、Base URL、用量 API 路径、追踪模型列表、轮询间隔）、连接测试按钮、手动触发采集
- `usage-dashboard`: 用量统计看板 — ECharts 统计图表（用量趋势折线图、模型用量分布柱状图、Provider 筛选器、总览卡牌：Token 总量 / 总费用 / 活跃厂商数）

### Modified Capabilities

无。这是全新项目。

## Impact

- 新建 `frontend/` 目录，包含完整的 Vue 3 + TypeScript 项目
- 依赖：Vue 3, Vue Router 4, Pinia, ECharts 6, Axios, Vite 8
- API 层对接后端 `llm-usage-monitor-backend` 提供的 REST 接口（`/api/providers`, `/api/usage`, `/api/stats`）
- UI 设计语言继承：CSS 变量体系（`--color-surface`, `--color-border`, `--shadow-md/lg`, `--space-*`）、卡片 hover 动效（`translate(-3px, -3px)`）、页面布局结构、字体级联
