<script setup lang="ts">
import { ref, watch, onUnmounted } from 'vue'

export interface PillOption {
  label: string
  value: string
  description: string
}

const props = defineProps<{
  modelValue: string
  options: PillOption[]
}>()

const emit = defineEmits<{ 'update:modelValue': [value: string] }>()

const displayText = ref('')
let typeInterval: ReturnType<typeof setInterval> | null = null

function typewrite(text: string) {
  if (typeInterval) { clearInterval(typeInterval); typeInterval = null }
  displayText.value = ''
  let i = 0
  typeInterval = setInterval(() => {
    displayText.value = text.slice(0, i + 1)
    i++
    if (i >= text.length) {
      if (typeInterval) { clearInterval(typeInterval); typeInterval = null }
    }
  }, 50)
}

function select(value: string) {
  if (value !== props.modelValue) {
    emit('update:modelValue', value)
  }
}

watch(() => props.modelValue, (val) => {
  const opt = props.options.find(o => o.value === val)
  if (opt) typewrite(opt.description)
}, { immediate: true })

onUnmounted(() => {
  if (typeInterval) { clearInterval(typeInterval); typeInterval = null }
})
</script>

<template>
  <div class="pill-selector">
    <div class="pill-group">
      <button
        v-for="opt in options"
        :key="opt.value"
        type="button"
        class="pill"
        :class="modelValue === opt.value ? 'active' : 'inactive'"
        @click="select(opt.value)"
      >{{ opt.label }}</button>
    </div>
    <p class="pill-description"><span>{{ displayText }}</span><span class="cursor"></span></p>
  </div>
</template>

<style scoped>
.pill-selector {
  display: flex;
  flex-direction: column;
  align-items: flex-start;
  gap: 6px;
  position: static;
  margin-bottom: var(--space-lg);
  transition: none;
}

.pill-group {
  display: flex;
  gap: 8px;
}

.pill {
  border-radius: 20px;
  border: 2px solid var(--color-border);
  padding: 6px 16px;
  font-weight: 600;
  cursor: pointer;
  user-select: none;
  white-space: nowrap;
  transition: all 0.15s ease;
  background: transparent;
  color: var(--color-text);
  font-size: 14px;
}

.pill.active {
  transform: scale(1.05);
  opacity: 1;
  background: var(--color-surface);
  box-shadow: var(--shadow-sm);
}

.pill.inactive {
  transform: scale(0.95);
  opacity: 0.55;
  background: transparent;
  border-width: 1.5px;
}

.pill-description {
  display: flex;
  align-items: flex-end;
  font-size: 11px;
  line-height: 1;
  color: var(--color-text-muted);
  opacity: 0.7;
  white-space: nowrap;
  min-height: 16px;
  width: 100%;
  text-align: left;
  margin: 0;
  padding-left: 2px;
}

.pill-description span:first-child {
  padding-bottom: 2px;
}

.cursor {
  display: inline-block;
  width: 1.5px;
  height: 11px;
  background: var(--color-text-muted);
  opacity: 0.7;
  margin-left: 1px;
  flex-shrink: 0;
  animation: blink 1s step-end infinite;
}

@keyframes blink {
  0%, 100% { opacity: 1; }
  50% { opacity: 0; }
}

@media (max-width: 768px) {
  .pill-selector {
    position: static;
    margin-bottom: var(--space-sm);
  }
}
</style>
