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
  windowMs: number
  bucketMs: number
}
const HOUR_MS = 3600000
const DAY_MS = 86400000
function scaledBucket(windowDays: number): number {
  return Math.round(HOUR_MS + (DAY_MS - HOUR_MS) * (windowDays - 1) / 29)
}
const presets: Preset[] = [
  { label: '当天', windowMs: 1 * DAY_MS,  bucketMs: HOUR_MS },
  { label: '7天',  windowMs: 7 * DAY_MS,  bucketMs: scaledBucket(7) },
  { label: '30天', windowMs: 30 * DAY_MS, bucketMs: DAY_MS },
]

const activePreset = ref<number>(1) // default: 7天
const bucketMs = computed(() => presets[activePreset.value].bucketMs)

// ── Local calendar anchor ─────────────────
function localMidnight(): number {
  const now = new Date()
  return new Date(now.getFullYear(), now.getMonth(), now.getDate()).getTime()
}

// ── Date state ───────────────────────────
function fmtIso(d: Date) { return d.toISOString() }

const datesFromPreset = computed(() => {
  const bMs = bucketMs.value
  const anchor = localMidnight()
  const now = Date.now()
  const windowMs = presets[activePreset.value].windowMs
  // right edge: ceil to next bucket from now
  const endTs = anchor + Math.ceil((now - anchor) / bMs) * bMs
  // left edge: aligned to bucket boundary, ≥ windowMs before end
  const rawStart = endTs - windowMs
  const startTs = anchor + Math.floor((rawStart - anchor) / bMs) * bMs
  return { start: fmtIso(new Date(startTs)), end: fmtIso(new Date(endTs)) }
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
  const anchor = localMidnight()

  for (const [name, points] of map) {
    points.sort((a, b) => a.date.localeCompare(b.date))
    const bucketMap = new Map<number, number>()

    for (let i = 1; i < points.length; i++) {
      const prev = points[i - 1].balance
      const curr = points[i].balance
      const diff = prev - curr
      if (diff <= 0) continue

      const ts = new Date(points[i].date).getTime()
      const bucketKey = anchor + Math.floor((ts - anchor) / bMs) * bMs
      bucketMap.set(bucketKey, (bucketMap.get(bucketKey) || 0) + diff)
    }

    const entries = [...bucketMap.entries()]
    if (entries.length === 0) continue
    entries.sort((a, b) => a[0] - b[0])

    const firstBucket = entries[0][0]
    const lastBucket = entries[entries.length - 1][0]

    const series: [Date, number][] = []
    for (let t = firstBucket; t <= lastBucket; t += bMs) {
      const val = bucketMap.get(t) || 0
      series.push([new Date(t), Math.round(val * 10000) / 10000])
    }
    result.set(name, series)
  }

  return result
}

// ── Render ───────────────────────────────
function renderChart(data: Map<string, [Date, number][]>) {
  if (!chartRef.value) return
  if (!chart) {
    chart = echarts.init(chartRef.value)
  }

  const bMs = bucketMs.value

  // X-axis range = full sliding window
  const xMin = new Date(startDate.value).getTime()
  const xMax = new Date(endDate.value).getTime()

  const seriesData: any[] = []
  for (const [name, pts] of data) {
    // Index existing points by bucket timestamp
    const ptMap = new Map(pts.map(([d, v]) => [d.getTime(), v]))

    // Fill every bucket in the window, y=0 for empty ones
    const padded: [Date, number][] = []
    for (let t = xMin; t <= xMax; t += bMs) {
      const val = ptMap.get(t) ?? 0
      padded.push([new Date(t), Math.round(val * 10000) / 10000])
    }

    seriesData.push({
      name,
      type: 'line',
      data: padded,
      connectNulls: false,
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
      min: xMin,
      max: xMax,
      axisLabel: { fontSize: 10 },
    },
    yAxis: {
      type: 'value',
      min: 0,
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
  min-width: 48px;
  text-align: center;
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
