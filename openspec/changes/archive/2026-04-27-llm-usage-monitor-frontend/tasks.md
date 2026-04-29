## 1. 项目骨架

- [x] 1.1 初始化 `frontend/` 项目：`package.json`（Vue 3, Vite 8, TypeScript, Vue Router 4, Pinia, ECharts 6, Axios），`tsconfig.json`，`vite.config.ts`（含 `proxy: { '/api': 'http://localhost:8000' }`）
- [x] 1.2 创建 `src/style.css`：全局 CSS 变量（`--color-surface`, `--color-border`, `--color-text`, `--color-text-muted`, `--shadow-md`, `--shadow-lg`, `--space-xs` ~ `--space-2xl`, `--border-width`），卡片 `.card` 基类（背景、边框、阴影、hover 动效 `translate(-3px, -3px)`），品牌色 `#FF6B35`
- [x] 1.3 创建 `src/App.vue`：侧边导航栏布局（`<aside>` 左侧固定 + `<main>` 右侧内容），导航菜单两项（Dashboard `/dashboard`、厂商管理 `/providers`），当前路由高亮
- [x] 1.4 创建 `src/router/index.ts`：三路由 — `/` redirect → `/dashboard`，`/dashboard` lazy load `DashboardView`，`/providers` lazy load `ProviderView`
- [x] 1.5 创建 `src/main.ts`：挂载 App、注册 Router、注册 Pinia、引入 `style.css`

## 2. 厂商配置管理

- [x] 2.1 创建 `src/api/index.ts`：TypeScript 类型（`Provider`, `UsageSummary`, `TrendPoint`, `DistributionPoint`）和所有 API 请求函数（`fetchProviders`, `createProvider`, `updateProvider`, `deleteProvider`, `testProvider`, `triggerCollection`, `fetchUsageSummary`, `fetchUsageTrends`, `fetchUsageDistribution`）
- [x] 2.2 创建 `src/stores/providers.ts`：Pinia store，state（providers 列表, loading），actions（fetch, create, update, delete, test, collect），error 状态处理
- [x] 2.3 创建 `src/views/ProviderView.vue` 框架：页面标题"厂商管理"，顶部"新增厂商"按钮，加载态/空态提示
- [x] 2.4 实现 Provider 列表卡片：展示名称、脱敏 API Key（仅后 4 位）、Base URL、用量 API 路径、模型数量标签（tag）、轮询间隔标签、操作按钮（编辑/删除/连接测试/立即采集）
- [x] 2.5 实现新增/编辑 Provider 表单（Modal 或展开面板）：name (text, required)、api_key (password, required)、base_url (url, required)、usage_api_path (text, default `/v1/usage`)、models (tag input, 至少一个)、interval (select: 手动/10s/1min/5min/15min/1h/6h/24h)、表单校验
- [x] 2.6 实现删除确认对话框：点击"删除"弹出确认框，确认后执行删除并更新列表
- [x] 2.7 实现连接测试按钮：点击调用 `testProvider`，loading 态，成功/失败 toast 反馈
- [x] 2.8 实现"立即采集"按钮：点击调用 `triggerCollection`，loading 态，成功后显示采集记录数提示

## 3. 用量 Dashboard

- [x] 3.1 创建 `src/stores/usage.ts`：Pinia store，state（summary, trends, distribution, selectedProviderId），actions（fetchSummary, fetchTrends, fetchDistribution），`selectedProviderId` 变化时重新请求
- [x] 3.2 创建 `src/views/DashboardView.vue` 框架：页面标题"用量看板"，Provider 筛选下拉框（"全部" + 各厂商名称），加载态
- [x] 3.3 实现三张总览卡牌："Token 消耗总量"、"预估总费用"（CNY）、"活跃厂商数"，大数字样式（`font-size: 36px; font-weight: 900`），card hover 动效
- [x] 3.4 实现用量趋势折线图（ECharts）：x 轴日期、y 轴 Token 数、smooth 线条 + 0.15 透明 area fill，tooltip，响应式 resize
- [x] 3.5 实现模型用量分布柱状图（ECharts）：x 轴模型名、y 轴 Token 数、`#FF6B35` 柱色，长名称 30° 旋转 + 11px 字号
- [x] 3.6 实现 Provider 筛选联动：下拉选择后同步更新三张卡牌和两张图表数据
- [x] 3.7 图表生命周期管理：`onUnmounted` dispose ECharts 实例，`resize` 事件监听并调用 `chart.resize()`

## 4. 验证

- [x] 4.1 `npm run dev` 启动成功，热更新正常
- [x] 4.2 `npm run build` TypeScript 类型检查 + 构建通过，无错误
- [x] 4.3 两页面路由导航正常，Dashboard 为首页
- [x] 4.4 全局样式与 workflow_develop 一致（卡片 hover、间距、字体级联）
