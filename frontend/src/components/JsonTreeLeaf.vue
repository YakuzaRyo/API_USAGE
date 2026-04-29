<script setup lang="ts">
import { ref } from 'vue'

const props = defineProps<{
  nodeKey: string
  value: unknown
  path: string
  depth: number
}>()

const emit = defineEmits<{
  select: [payload: { path: string }]
}>()

const expanded = ref(props.depth < 1)

function isExpandable(val: unknown): boolean {
  if (val === null || val === undefined) return false
  return typeof val === 'object'
}

function isLeaf(val: unknown): boolean {
  return !isExpandable(val)
}

function formatValue(val: unknown): string {
  if (val === null) return 'null'
  if (typeof val === 'string') {
    return val.length > 30 ? `"${val.slice(0, 30)}..."` : `"${val}"`
  }
  if (typeof val === 'boolean') return val ? 'true' : 'false'
  if (typeof val === 'object') return ''
  return String(val)
}

function fullValue(val: unknown): string {
  if (val === null) return 'null'
  if (typeof val === 'string') return val
  return String(val)
}

const children = (): [string, unknown, string][] => {
  if (Array.isArray(props.value)) {
    return props.value.slice(0, 20).map((item, i) => [
      `[${i}]`, item, `${props.path}.${i}`,
    ])
  }
  if (typeof props.value === 'object' && props.value !== null) {
    return Object.entries(props.value as Record<string, unknown>).map(([k, v]) => [
      k, v, `${props.path}.${k}`,
    ])
  }
  return []
}

function handleClick() {
  emit('select', { path: props.path })
  if (isExpandable(props.value)) {
    expanded.value = !expanded.value
  }
}
</script>

<template>
  <div class="jtl-row">
    <div
      class="jtl-node"
      :class="{ 'jtl-leaf': isLeaf(value) }"
      :style="{ paddingLeft: (depth * 16) + 'px' }"
      @click="handleClick"
    >
      <span class="jtl-arrow">
        <template v-if="isExpandable(value)">{{ expanded ? '▼' : '▶' }}</template>
      </span>
      <span class="jtl-key">{{ nodeKey }}</span>
      <template v-if="isLeaf(value)">
        <span class="jtl-colon">: </span>
        <span class="jtl-value" :title="fullValue(value)">{{ formatValue(value) }}</span>
      </template>
    </div>
    <template v-if="isExpandable(value) && expanded">
      <JsonTreeLeaf
        v-for="([ck, cv, cp], i) in children()"
        :key="i"
        :node-key="ck"
        :value="cv"
        :path="cp"
        :depth="depth + 1"
        @select="emit('select', $event)"
      />
    </template>
  </div>
</template>

<style scoped>
.jtl-row {
  display: flex;
  flex-direction: column;
}

.jtl-node {
  display: flex;
  align-items: baseline;
  gap: 2px;
  padding: 1px 4px;
  cursor: pointer;
  transition: background 0.1s;
  min-height: 20px;
  font-size: 13px;
  font-family: var(--font-mono);
}
.jtl-node:hover {
  background: rgba(255, 107, 53, 0.08);
}

.jtl-arrow {
  font-size: 9px;
  width: 12px;
  flex-shrink: 0;
  color: var(--color-text-muted);
}

.jtl-key {
  color: var(--color-text);
  font-weight: 500;
  word-break: break-all;
}
.jtl-node:hover .jtl-key {
  color: var(--color-primary);
}

.jtl-colon {
  color: var(--color-text-muted);
}

.jtl-value {
  color: var(--color-text-muted);
  word-break: break-all;
}
</style>
