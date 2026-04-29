<script setup lang="ts">
import { ref, onMounted, onUnmounted, watch } from 'vue'
import * as echarts from 'echarts'
import { useUsageStore } from '../stores/usage'
import { useProvidersStore } from '../stores/providers'
import { type ECharts } from 'echarts'
import PillModeSelector from '../components/PillModeSelector.vue'
import type { PillOption } from '../components/PillModeSelector.vue'
import BalanceView from './BalanceView.vue'

const usageStore = useUsageStore()
const providerStore = useProvidersStore()

const mode = ref('dashboard')

const pillOptions: PillOption[] = [
  { label: '用量看板', value: 'dashboard', description: 'Token 消耗趋势与模型使用分布' },
  { label: '余额变化', value: 'balance', description: '各厂商余额消耗速率，点击图例筛选' },
]

// ── Chart refs ─────────────────────────
const trendChartRef = ref<HTMLDivElement>()
const distChartRef = ref<HTMLDivElement>()
let trendChart: ECharts | null = null
let distChart: ECharts | null = null

// ── Render helpers ─────────────────────
function renderTrendChart() {
  if (!trendChartRef.value) return
  if (!trendChart) trendChart = echarts.init(trendChartRef.value)
  trendChart.setOption({
    title: { text: '用量趋势', left: 'center', textStyle: { fontSize: 16, fontWeight: 700 } },
    tooltip: { trigger: 'axis' },
    grid: { left: 80, right: 20, top: 50, bottom: 30 },
    xAxis: { type: 'category', data: usageStore.trends.map(d => d.date) },
    yAxis: { type: 'value', name: 'Token' },
    series: [
      {
        type: 'line',
        data: usageStore.trends.map(d => d.tokens),
        smooth: true,
        areaStyle: { opacity: 0.15 },
        itemStyle: { color: '#FF6B35' },
      },
    ],
  })
}

function renderDistChart() {
  if (!distChartRef.value) return
  if (!distChart) distChart = echarts.init(distChartRef.value)
  distChart.setOption({
    title: { text: '模型用量分布', left: 'center', textStyle: { fontSize: 16, fontWeight: 700 } },
    tooltip: { trigger: 'axis' },
    grid: { left: 80, right: 20, top: 50, bottom: 60 },
    xAxis: {
      type: 'category',
      data: usageStore.distribution.map(d => d.model),
      axisLabel: { rotate: 30, fontSize: 11 },
    },
    yAxis: { type: 'value', name: 'Token' },
    series: [
      {
        type: 'bar',
        data: usageStore.distribution.map(d => d.tokens),
        itemStyle: { color: '#FF6B35' },
      },
    ],
  })
}

function onResize() {
  trendChart?.resize()
  distChart?.resize()
}

// ── Lifecycle ──────────────────────────
watch([() => usageStore.trends, () => usageStore.distribution], () => {
  if (usageStore.trends.length > 0) renderTrendChart()
  if (usageStore.distribution.length > 0) renderDistChart()
})

onMounted(async () => {
  await Promise.all([usageStore.fetchAll(), providerStore.fetch(), usageStore.fetchBillingSummaryData()])
  if (usageStore.trends.length > 0) renderTrendChart()
  if (usageStore.distribution.length > 0) renderDistChart()
  window.addEventListener('resize', onResize)
})

onUnmounted(() => {
  trendChart?.dispose()
  distChart?.dispose()
  trendChart = null
  distChart = null
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

    <!-- Dashboard Mode -->
    <template v-if="mode === 'dashboard'">
      <!-- Loading -->
      <div v-if="usageStore.loading && !usageStore.summary" class="loading">加载中...</div>

      <template v-else>
        <div class="stats-cards">
          <div class="stat-card">
            <p class="stat-label">Token 消耗总量</p>
            <p class="stat-value">{{ formatTokens(usageStore.summary?.total_tokens ?? 0) }}</p>
          </div>
          <div class="stat-card">
            <p class="stat-label">活跃厂商数</p>
            <p class="stat-value">{{ usageStore.summary?.active_providers ?? 0 }}</p>
          </div>
          <div class="stat-card">
            <p class="stat-label">当前余额</p>
            <p class="stat-value">{{ (usageStore.summary?.total_balance ?? 0).toFixed(2) }}<span style="font-size: 18px;"> {{ usageStore.summary?.currency_symbol ?? 'CNY' }}</span></p>
          </div>
          <div class="stat-card">
            <p class="stat-label">费用</p>
            <p class="stat-value">{{ Math.abs(usageStore.billingSummary.reduce((s, i) => s + i.amount, 0)).toFixed(2) }}<span style="font-size: 18px;"> {{ usageStore.summary?.currency_symbol ?? 'CNY' }}</span></p>
          </div>
        </div>

        <div class="card">
          <div v-if="usageStore.trends.length === 0" class="loading">暂无趋势数据</div>
          <div v-else ref="trendChartRef" class="chart-container"></div>
        </div>

        <div class="card">
          <div v-if="usageStore.distribution.length === 0" class="loading">暂无模型分布数据</div>
          <div v-else ref="distChartRef" class="chart-container"></div>
        </div>
      </template>
    </template>

    <!-- Balance Mode -->
    <div v-else class="card">
      <BalanceView />
    </div>

  </div>
</template>
