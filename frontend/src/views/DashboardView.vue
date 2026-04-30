<script setup lang="ts">
import { ref, onMounted, onUnmounted, watch, computed } from 'vue'
import * as echarts from 'echarts'
import { useUsageStore } from '../stores/usage'
import { useProvidersStore } from '../stores/providers'
import { type ECharts } from 'echarts'
import PillModeSelector from '../components/PillModeSelector.vue'
import type { PillOption } from '../components/PillModeSelector.vue'
import BalanceView from './BalanceView.vue'
import RingGaugeCard from '../components/RingGaugeCard.vue'
import { fetchCategories, type Category } from '../api'

const usageStore = useUsageStore()
const providerStore = useProvidersStore()

const mode = ref('dashboard')
const categories = ref<Category[]>([])

const pillOptions: PillOption[] = [
  { label: '综合看板', value: 'dashboard', description: '环形仪表盘：Token 消耗、活跃厂商、当前余额、费用占比' },
  { label: '用量分析', value: 'trends', description: 'Token 消耗趋势与模型使用分布' },
  { label: '余额变化', value: 'balance', description: '各厂商余额消耗速率，点击图例筛选' },
]

// ── Ring card colors ───────────────────
const COLORS = ['#FF6B35', '#1A1A1A', '#6B6B6B', '#FFD23F', '#2ED573', '#FF4757', '#8250df', '#00B4D8']

function categoryName(catId: number | null) {
  if (!catId) return '未分类'
  const c = categories.value.find(c => c.id === catId)
  return c?.name ?? '未分类'
}

// ── Token ring data ────────────────────
const tokenSegments = computed(() => {
  return usageStore.distribution.map((d, i) => ({
    name: d.model,
    value: d.tokens,
    color: COLORS[i % COLORS.length],
  }))
})

// ── Active providers ring data ─────────
const providerSegments = computed(() => {
  const groups: Record<string, number> = {}
  for (const p of providerStore.providers) {
    const cn = categoryName(p.category_id)
    groups[cn] = (groups[cn] || 0) + 1
  }
  return Object.entries(groups).map(([name, count], i) => ({
    name,
    value: count,
    color: COLORS[i % COLORS.length],
  }))
})

// ── Balance ring data (dual) ───────────
const balanceOuterSegments = computed(() => {
  const groups: Record<string, number> = {}
  for (const p of providerStore.providers) {
    if (p.last_balance == null) continue
    const cn = categoryName(p.category_id)
    groups[cn] = (groups[cn] || 0) + p.last_balance
  }
  return Object.entries(groups).map(([name, val], i) => ({
    name,
    value: Math.round(val * 100) / 100,
    color: COLORS[i % COLORS.length],
  }))
})

const balanceInnerSegments = computed(() => {
  return providerStore.providers
    .filter(p => p.last_balance != null)
    .map((p, i) => ({
      name: p.name,
      value: Math.round(p.last_balance! * 100) / 100,
      color: COLORS[i % COLORS.length],
      outerName: categoryName(p.category_id),
    }))
})

const balanceTotal = computed(() =>
  providerStore.providers.reduce((s, p) => s + (p.last_balance || 0), 0)
)

// ── Billing cost ring data (dual) ──────
const costOuterSegments = computed(() => {
  const groups: Record<string, number> = {}
  for (const b of usageStore.billingSummary) {
    const mode = b.billing_mode === 'token_plan' ? 'TokenPlan' : 'API'
    groups[mode] = (groups[mode] || 0) + b.amount
  }
  return Object.entries(groups).map(([name, val], i) => ({
    name,
    value: Math.abs(Math.round(val * 100) / 100),
    color: COLORS[i % COLORS.length],
  }))
})

const costInnerSegments = computed(() => {
  return usageStore.billingSummary.map((b, i) => ({
    name: b.provider_name,
    value: Math.abs(Math.round(b.amount * 100) / 100),
    color: COLORS[i % COLORS.length],
    outerName: b.billing_mode === 'token_plan' ? 'TokenPlan' : 'API',
  }))
})

const costTotal = computed(() =>
  Math.abs(usageStore.billingSummary.reduce((s, i) => s + i.amount, 0))
)

// ── Trends / Distribution charts ────────
const trendChartRef = ref<HTMLDivElement>()
const distChartRef = ref<HTMLDivElement>()
let trendChart: ECharts | null = null
let distChart: ECharts | null = null

function renderTrendChart() {
  if (!trendChartRef.value) return
  if (!trendChart) trendChart = echarts.init(trendChartRef.value)
  trendChart.setOption({
    tooltip: { trigger: 'axis' },
    grid: { left: 80, right: 20, top: 10, bottom: 30 },
    xAxis: { type: 'category', data: usageStore.trends.map(d => d.date) },
    yAxis: { type: 'value', name: 'Token' },
    series: [{
      type: 'line', data: usageStore.trends.map(d => d.tokens),
      smooth: true, areaStyle: { opacity: 0.15 }, itemStyle: { color: '#FF6B35' },
    }],
  })
}

function renderDistChart() {
  if (!distChartRef.value) return
  if (!distChart) distChart = echarts.init(distChartRef.value)
  distChart.setOption({
    tooltip: { trigger: 'axis' },
    grid: { left: 80, right: 20, top: 10, bottom: 60 },
    xAxis: { type: 'category', data: usageStore.distribution.map(d => d.model), axisLabel: { rotate: 30, fontSize: 11 } },
    yAxis: { type: 'value', name: 'Token' },
    series: [{
      type: 'bar', data: usageStore.distribution.map(d => d.tokens),
      itemStyle: { color: '#FF6B35' },
    }],
  })
}

function onResize() { trendChart?.resize(); distChart?.resize() }

watch([() => usageStore.trends, () => usageStore.distribution], () => {
  if (mode.value === 'trends') {
    if (usageStore.trends.length > 0) renderTrendChart()
    if (usageStore.distribution.length > 0) renderDistChart()
  }
})

onMounted(async () => {
  await Promise.all([
    usageStore.fetchAll(),
    providerStore.fetch(),
    usageStore.fetchBillingSummaryData(),
    fetchCategories().then(r => { categories.value = r.data }).catch(() => {}),
  ])
  renderTrendChart()
  renderDistChart()
  window.addEventListener('resize', onResize)
})

onUnmounted(() => {
  trendChart?.dispose(); distChart?.dispose()
  window.removeEventListener('resize', onResize)
})

function formatTokens(n: number): string {
  if (n >= 1_000_000) return `${(n / 1_000_000).toFixed(1)}M`
  if (n >= 1_000) return `${(n / 1_000).toFixed(1)}K`
  return String(n)
}
</script>

<template>
  <div class="page" style="position: relative;">
    <PillModeSelector v-model="mode" :options="pillOptions" />

    <!-- 综合看板 -->
    <template v-if="mode === 'dashboard'">
      <div v-if="usageStore.loading && !usageStore.summary" class="loading">加载中...</div>
      <div v-else class="ring-grid">
        <RingGaugeCard
          title="Token 消耗"
          :segments="tokenSegments"
          :format-value="formatTokens"
        />
        <RingGaugeCard
          title="活跃厂商"
          :segments="providerSegments"
        />
        <RingGaugeCard
          title="当前余额"
          :segments="balanceOuterSegments"
          :inner-segments="balanceInnerSegments"
          :format-value="(v: number) => `¥${v.toFixed(2)}`"
          :total-override="Math.round(balanceTotal * 100) / 100"
        />
        <RingGaugeCard
          title="费用"
          :segments="costOuterSegments"
          :inner-segments="costInnerSegments"
          :format-value="(v: number) => `¥${v.toFixed(2)}`"
          :total-override="Math.round(costTotal * 100) / 100"
        />
      </div>
    </template>

    <!-- 用量分析 -->
    <template v-if="mode === 'trends'">
      <div v-if="usageStore.trends.length === 0" class="loading">暂无趋势数据</div>
      <div v-else class="card" style="margin-bottom: var(--space-lg);">
        <div ref="trendChartRef" class="chart-container"></div>
      </div>
      <div v-if="usageStore.distribution.length === 0" class="loading">暂无模型分布数据</div>
      <div v-else class="card">
        <div ref="distChartRef" class="chart-container"></div>
      </div>
    </template>

    <!-- 余额变化 -->
    <div v-if="mode === 'balance'" class="card">
      <BalanceView />
    </div>
  </div>
</template>

<style scoped>
.ring-grid {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: var(--space-md);
}

@media (max-width: 768px) {
  .ring-grid {
    grid-template-columns: 1fr;
  }
}

.chart-container {
  height: 350px;
}
</style>
