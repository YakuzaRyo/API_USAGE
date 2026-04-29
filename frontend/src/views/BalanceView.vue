<script setup lang="ts">
import { ref, onMounted, onUnmounted, computed, nextTick } from 'vue'
import * as echarts from 'echarts'
import { useUsageStore } from '../stores/usage'
import { useProvidersStore } from '../stores/providers'
import { type ECharts } from 'echarts'

const usageStore = useUsageStore()
const providerStore = useProvidersStore()

const chartRef = ref<HTMLDivElement>()
let chart: ECharts | null = null

// ── Presets ──────────────────────────────
interface Preset {
  label: string
  bucketMs: number
  defaultDays: number
}
const presets: Preset[] = [
  { label: '5分钟', bucketMs: 5 * 60 * 1000, defaultDays: 0 },
  { label: '1小时', bucketMs: 1 * 60 * 1000, defaultDays: 0 },
  { label: '7天',   bucketMs: 1 * 60 * 60 * 1000, defaultDays: 7 },
  { label: '30天',  bucketMs: 24 * 60 * 60 * 1000, defaultDays: 30 },
]

const activePreset = ref<number>(2) // default: 7天
const bucketMs = computed(() => presets[activePreset.value].bucketMs)

// ── Date state ───────────────────────────
function fmt(d: Date) { return d.toISOString().slice(0, 10) }

const presetDefaultDays = computed(() => presets[activePreset.value].defaultDays)
const datesFromPreset = computed(() => {
  const days = presetDefaultDays.value
  if (days === 0) return { start: fmt(new Date()), end: fmt(new Date()) }
  const end = new Date()
  const start = new Date()
  start.setDate(start.getDate() - days)
  return { start: fmt(start), end: fmt(end) }
})

const startDate = ref(datesFromPreset.value.start)
const endDate = ref(datesFromPreset.value.end)
const customRange = ref(false)

// ── Data loading ─────────────────────────
async function loadData() {
  await usageStore.fetchBalanceHistoryData({ start: startDate.value, end: endDate.value })
  if (providerStore.providers.length === 0) await providerStore.fetch()
  const data = buildConsumption()
  hasConsumption.value = data.size > 0
  await nextTick()
  if (data.size > 0) renderChart(data)
}

// ── Consumption transform ────────────────
const hasConsumption = ref(false)

function buildConsumption(): Map<string, [Date, number][]> {
  const map = new Map<string, { date: string; balance: number }[]>()
  for (const p of usageStore.balanceHistory) {
    if (!map.has(p.provider_name)) map.set(p.provider_name, [])
    map.get(p.provider_name)!.push({ date: p.date, balance: p.balance })
  }

  const result = new Map<string, [Date, number][]>()
  const bMs = bucketMs.value

  for (const [name, points] of map) {
    points.sort((a, b) => a.date.localeCompare(b.date))
    const bucketMap = new Map<number, number>()

    for (let i = 1; i < points.length; i++) {
      const prev = points[i - 1].balance
      const curr = points[i].balance
      const diff = prev - curr
      if (diff <= 0) continue

      const ts = new Date(points[i].date).getTime()
      const bucketKey = Math.floor(ts / bMs) * bMs
      bucketMap.set(bucketKey, (bucketMap.get(bucketKey) || 0) + diff)
    }

    const series: [Date, number][] = []
    for (const [key, val] of bucketMap) {
      series.push([new Date(key), Math.round(val * 10000) / 10000])
    }
    series.sort((a, b) => a[0].getTime() - b[0].getTime())
    if (series.length > 0) result.set(name, series)
  }

  return result
}

// ── Render ───────────────────────────────
function renderChart(data: Map<string, [Date, number][]>) {
  if (!chartRef.value) return
  if (!chart) {
    chart = echarts.init(chartRef.value)
  }

  const seriesData: any[] = []
  for (const [name, pts] of data) {
    seriesData.push({
      name,
      type: 'line',
      data: pts,
      smooth: 0.3,
      showSymbol: false,
      lineStyle: { width: 2 },
      areaStyle: { opacity: 0.08 },
    })
  }

  const currency = providerStore.providers[0]?.currency_symbol || 'CNY'

  chart.setOption({
    tooltip: {
      trigger: 'axis',
      valueFormatter: (value: unknown) =>
        typeof value === 'number' ? `¥${value.toFixed(4)}` : String(value),
    },
    legend: {
      type: 'scroll',
      bottom: 0,
      textStyle: { fontSize: 12 },
    },
    grid: { left: 70, right: 20, top: 20, bottom: 40 },
    xAxis: {
      type: 'time',
      axisLabel: { fontSize: 10 },
    },
    yAxis: {
      type: 'value',
      name: `消耗 (${currency})`,
      nameTextStyle: { fontSize: 12 },
      axisLabel: {
        formatter: (v: number) => v.toFixed(2),
      },
    },
    series: seriesData,
  }, true)
}

function onResize() { chart?.resize() }

// ── Preset / date interactions ───────────
async function selectPreset(idx: number) {
  activePreset.value = idx
  customRange.value = false
  startDate.value = datesFromPreset.value.start
  endDate.value = datesFromPreset.value.end
  await loadData()
}

function onDateChange() {
  customRange.value = true
  if (startDate.value && endDate.value) loadData()
}

// ── Lifecycle ────────────────────────────
onMounted(async () => {
  await loadData()
  window.addEventListener('resize', onResize)
})

onUnmounted(() => {
  chart?.dispose()
  chart = null
  window.removeEventListener('resize', onResize)
})
</script>

<template>
  <div class="balance-view">
    <!-- Header bar fixed to card top -->
    <div class="balance-bar">
      <div class="preset-pills">
        <button
          v-for="(p, i) in presets"
          :key="p.label"
          class="pill"
          :class="{ active: activePreset === i && !customRange }"
          @click="selectPreset(i)"
        >{{ p.label }}</button>
      </div>
      <div class="date-filter">
        <input type="date" v-model="startDate" @change="onDateChange" />
        <span>—</span>
        <input type="date" v-model="endDate" @change="onDateChange" />
      </div>
    </div>

    <!-- Empty state: only when definitely no data and not loading -->
    <div v-if="!usageStore.balanceLoading && !hasConsumption" class="loading">
      暂无消耗数据
    </div>

    <!-- Chart: always in DOM (v-show), ECharts needs a persistent container -->
    <div v-show="usageStore.balanceLoading || hasConsumption" class="chart-wrapper">
      <div ref="chartRef" class="chart-container"></div>
      <div v-if="usageStore.balanceLoading" class="loading-overlay">加载中...</div>
    </div>
  </div>
</template>

<style scoped>
.balance-view {
  display: flex;
  flex-direction: column;
  gap: 0;
}

.balance-bar {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding-bottom: var(--space-md);
  border-bottom: 1px solid var(--color-border);
  margin-bottom: var(--space-md);
}

.preset-pills {
  display: flex;
  gap: 8px;
}

.pill {
  border-radius: 16px;
  border: 1.5px solid var(--color-border);
  padding: 4px 12px;
  font-size: 12px;
  font-weight: 600;
  cursor: pointer;
  background: transparent;
  color: var(--color-text-muted);
  transition: all 0.15s;
}

.pill:hover {
  border-color: var(--color-primary);
  color: var(--color-primary);
}

.pill.active {
  background: var(--color-primary);
  color: #fff;
  border-color: var(--color-primary);
}

.date-filter {
  display: flex;
  align-items: center;
  gap: 4px;
  font-size: 13px;
  color: var(--color-text-muted);
}

.date-filter input {
  padding: 2px 6px;
  font-size: 12px;
  border: 1px solid var(--color-border);
  border-radius: 4px;
  background: transparent;
  color: var(--color-text);
}

.chart-wrapper {
  position: relative;
}

.chart-container {
  width: 100%;
  height: 380px;
}

.loading {
  display: flex;
  align-items: center;
  justify-content: center;
  height: 200px;
  color: var(--color-text-muted);
  font-size: 14px;
}

.loading-overlay {
  position: absolute;
  inset: 0;
  display: flex;
  align-items: center;
  justify-content: center;
  background: rgba(255,255,255,0.6);
  color: var(--color-text-muted);
  font-size: 13px;
  z-index: 2;
}
</style>
