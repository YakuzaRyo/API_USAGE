<script setup lang="ts">
import { computed } from 'vue'
import JsonTreeLeaf from './JsonTreeLeaf.vue'

const props = defineProps<{ json: unknown }>()

const emit = defineEmits<{ select: [payload: { path: string }] }>()

const rootEntries = computed(() => {
  if (!props.json || typeof props.json !== 'object') return []
  if (Array.isArray(props.json)) {
    return props.json.slice(0, 20).map((item, i) => [`[${i}]`, item, `${i}`])
  }
  return Object.entries(props.json as Record<string, unknown>).map(([k, v]) => [k, v, k])
})

function onSelect(payload: { path: string }) {
  emit('select', payload)
}

function highlightJson(obj: unknown): string {
  const json = JSON.stringify(obj, null, 2)
  return json
    .replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;')
    .replace(/("(?:[^"\\]|\\.)*")\s*:/g,
      '<span class="hl-key">$1</span>:')
    .replace(/: \s*("(?:[^"\\]|\\.)*")/g,
      ': <span class="hl-string">$1</span>')
    .replace(/: \s*(-?\d+\.?\d*(?:e[+-]?\d+)?)/gi,
      ': <span class="hl-number">$1</span>')
    .replace(/: \s*(true|false)/gi,
      ': <span class="hl-bool">$1</span>')
    .replace(/: \s*(null)/gi,
      ': <span class="hl-null">$1</span>')
}
</script>

<template>
  <div class="jt-container" v-if="json && typeof json === 'object'">
    <div class="jt-label">JSON 结构（点击 key 填入下方映射）</div>
    <div class="jt-tree">
      <template v-for="([key, val, path], i) in rootEntries" :key="i">
        <JsonTreeLeaf
          :node-key="key"
          :value="val"
          :path="path"
          :depth="0"
          @select="onSelect"
        />
      </template>
    </div>
    <details class="jt-raw-toggle">
      <summary>查看原始 JSON</summary>
      <pre class="jt-raw" v-html="highlightJson(json)"></pre>
    </details>
  </div>
  <div v-else class="jt-empty">无可用 JSON 数据</div>
</template>

<style scoped>
.jt-container {
  display: flex;
  flex-direction: column;
  gap: var(--space-xs);
  font-size: 13px;
  font-family: var(--font-mono);
  border: var(--border-width) solid var(--color-border);
  padding: var(--space-sm);
  max-height: 320px;
  overflow: auto;
}

.jt-label {
  font-size: 12px;
  color: var(--color-text-muted);
  font-weight: 600;
  margin-bottom: 2px;
}

.jt-tree {
  display: flex;
  flex-direction: column;
}

.jt-raw-toggle {
  border-top: var(--border-width) solid var(--color-border);
  padding-top: var(--space-xs);
  margin-top: 2px;
  font-size: 11px;
  color: var(--color-text-muted);
}
.jt-raw-toggle summary {
  cursor: pointer;
  font-weight: 600;
}
.jt-raw {
  font-size: 12px;
  font-family: var(--font-mono), 'Cascadia Code', 'Fira Code', 'JetBrains Mono', 'Courier New', monospace;
  background: transparent;
  color: var(--color-text);
  padding: var(--space-sm);
  max-height: 200px;
  overflow: auto;
  margin-top: var(--space-xs);
  white-space: pre-wrap;
  word-break: break-all;
  line-height: 1.5;
}

:deep(.hl-key) { color: #0550ae; }
:deep(.hl-string) { color: #0a3069; }
:deep(.hl-number) { color: var(--color-primary); }
:deep(.hl-bool) { color: #8250df; }
:deep(.hl-null) { color: #6e7781; }

.jt-empty {
  font-size: 12px;
  color: var(--color-text-muted);
}
</style>
