<script setup lang="ts">
import { ref, computed, watch, onMounted, onUnmounted, nextTick } from 'vue'
import * as echarts from 'echarts'
import type { ECharts } from 'echarts'

export interface RingSegment {
  name: string
  value: number
  color: string
}

export interface InnerSegment {
  name: string
  value: number
  color: string
  outerName: string
}

const props = defineProps<{
  title: string
  segments: RingSegment[]
  innerSegments?: InnerSegment[]
  formatValue?: (v: number) => string
  totalOverride?: number
}>()

const chartRef = ref<HTMLDivElement>()
let chart: ECharts | null = null

const hasDual = computed(() => (props.innerSegments || []).length > 0)

const displayTotal = computed(() => {
  if (props.totalOverride != null) return props.totalOverride
  return props.segments.reduce((s, v) => s + v.value, 0)
})

function fmt(v: number) {
  if (props.formatValue) return props.formatValue(v)
  if (v >= 1_000_000) return `${(v / 1_000_000).toFixed(1)}M`
  if (v >= 1000) return `${(v / 1000).toFixed(1)}K`
  return v.toFixed(1)
}

// ── Color utilities ────────────────────

function hexToHSL(hex: string): { h: number; s: number; l: number } {
  let r = parseInt(hex.slice(1, 3), 16) / 255
  let g = parseInt(hex.slice(3, 5), 16) / 255
  let b = parseInt(hex.slice(5, 7), 16) / 255
  const max = Math.max(r, g, b), min = Math.min(r, g, b)
  let h = 0, s = 0
  const l = (max + min) / 2
  if (max !== min) {
    const d = max - min
    s = l > 0.5 ? d / (2 - max - min) : d / (max + min)
    if (max === r) h = ((g - b) / d + (g < b ? 6 : 0)) / 6
    else if (max === g) h = ((b - r) / d + 2) / 6
    else h = ((r - g) / d + 4) / 6
  }
  return { h: h * 360, s: s * 100, l: l * 100 }
}

function hslToHex(h: number, s: number, l: number): string {
  s /= 100; l /= 100
  const a = s * Math.min(l, 1 - l)
  const f = (n: number) => {
    const k = (n + h / 30) % 12
    const color = l - a * Math.max(Math.min(k - 3, 9 - k, 1), -1)
    return Math.round(255 * Math.max(0, Math.min(1, color))).toString(16).padStart(2, '0')
  }
  return `#${f(0)}${f(8)}${f(4)}`
}

function lighten(hex: string, amount: number): string {
  const { h, s, l } = hexToHSL(hex)
  const newL = Math.min(85, l + amount * 100)
  return hslToHex(h, s, newL)
}

function deriveInnerColors(outers: RingSegment[], inners: InnerSegment[]): InnerSegment[] {
  const outerColorMap = new Map(outers.map(o => [o.name, o.color]))
  const siblingCounts = new Map<string, number>()
  const siblingIndices = new Map<string, number>()

  return inners.map(seg => {
    const base = outerColorMap.get(seg.outerName) || seg.color
    const idx = siblingIndices.get(seg.outerName) || 0
    siblingIndices.set(seg.outerName, idx + 1)
    const count = siblingCounts.get(seg.outerName) || 0
    siblingCounts.set(seg.outerName, count + 1)
    return {
      ...seg,
      color: lighten(base, 0.12 + idx * 0.10),
    }
  })
}

// ── ECharts option builder ─────────────

const baseItemStyle = {
  borderRadius: 6,
  borderColor: '#fff',
  borderWidth: 2,
}

const baseEmphasis = {
  scale: true,
  scaleSize: 6,
  itemStyle: {
    shadowBlur: 20,
    shadowColor: 'rgba(0,0,0,0.3)',
  },
}

function buildGraphic(centerValue: string, subtitle: string) {
  return [{
    type: 'group' as const,
    left: 'center' as const,
    top: 'center' as const,
    children: [
      {
        type: 'text' as const,
        style: {
          text: centerValue,
          fontSize: 20,
          fontWeight: 900,
          fill: '#1A1A1A',
          textAlign: 'center' as const,
          lineHeight: 24,
        },
      },
      {
        type: 'text' as const,
        style: {
          text: subtitle,
          fontSize: 11,
          fill: '#6B6B6B',
          textAlign: 'center' as const,
          lineHeight: 16,
        },
        position: [0, 22],
      },
    ],
  }]
}

function buildOption() {
  const outerData = props.segments
  const innerData = hasDual.value
    ? deriveInnerColors(props.segments, props.innerSegments || [])
    : []
  const total = fmt(displayTotal.value)

  const series: any[] = []

  if (hasDual.value) {
    series.push({
      name: 'outer',
      type: 'pie',
      radius: ['62%', '80%'],
      center: ['50%', '45%'],
      data: outerData.map(s => ({ name: s.name, value: s.value, itemStyle: { color: s.color } })),
      padAngle: 3,
      itemStyle: baseItemStyle,
      emphasis: baseEmphasis,
      label: { show: false },
      animationType: 'scale',
      animationDuration: 800,
      animationEasing: 'cubicOut',
    })
    series.push({
      name: 'inner',
      type: 'pie',
      radius: ['35%', '55%'],
      center: ['50%', '45%'],
      data: innerData.map(s => ({ name: s.name, value: s.value, itemStyle: { color: s.color } })),
      padAngle: 3,
      itemStyle: { ...baseItemStyle, borderWidth: 1 },
      emphasis: { ...baseEmphasis, scaleSize: 4 },
      label: { show: false },
      animationType: 'scale',
      animationDuration: 800,
      animationEasing: 'cubicOut',
      animationDelay: 200,
    })
  } else {
    series.push({
      name: 'outer',
      type: 'pie',
      radius: ['55%', '80%'],
      center: ['50%', '45%'],
      data: outerData.map(s => ({ name: s.name, value: s.value, itemStyle: { color: s.color } })),
      padAngle: 3,
      itemStyle: baseItemStyle,
      emphasis: baseEmphasis,
      label: { show: false },
      animationType: 'scale',
      animationDuration: 800,
      animationEasing: 'cubicOut',
    })
  }

  const allData = [...outerData, ...innerData]
  const legendData = allData.map(s => s.name)

  return {
    tooltip: {
      trigger: 'item',
      formatter: (params: any) => {
        const ring = params.seriesName === 'inner' ? '内环' : '外环'
        return `<strong>${params.name}</strong><br/>${ring} · ${fmt(params.value)} · ${params.percent}%`
      },
    },
    legend: {
      type: 'scroll',
      bottom: 0,
      textStyle: { fontSize: 11, color: '#6B6B6B' },
      data: legendData,
      itemWidth: 10,
      itemHeight: 10,
    },
    graphic: buildGraphic(total, props.title),
    series,
  }
}

function renderChart() {
  if (!chartRef.value) return
  if (!chart) chart = echarts.init(chartRef.value)
  chart.setOption(buildOption(), true)

  chart.off('mouseover')
  chart.off('mouseout')
  chart.on('mouseover', (params: any) => {
    if (params.componentType === 'series') {
      chart?.setOption({
        graphic: buildGraphic(fmt(params.value), params.name),
      })
    }
  })
  chart.on('mouseout', () => {
    chart?.setOption({
      graphic: buildGraphic(fmt(displayTotal.value), props.title),
    })
  })
}

function onResize() { chart?.resize() }

watch(
  () => [props.segments, props.innerSegments, props.totalOverride],
  () => { nextTick(() => renderChart()) },
  { deep: true },
)

onMounted(() => {
  renderChart()
  window.addEventListener('resize', onResize)
})

onUnmounted(() => {
  chart?.dispose()
  chart = null
  window.removeEventListener('resize', onResize)
})
</script>

<template>
  <div class="ring-card card">
    <div ref="chartRef" class="ring-chart"></div>
  </div>
</template>

<style scoped>
.ring-card {
  display: flex;
  flex-direction: column;
  padding: var(--space-md);
}

.ring-chart {
  width: 100%;
  height: 260px;
}
</style>
