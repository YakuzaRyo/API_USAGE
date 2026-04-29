<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useProvidersStore } from '../stores/providers'
import { type Provider } from '../api'
import ProviderWizard from '../components/ProviderWizard.vue'

const store = useProvidersStore()

const showWizard = ref(false)
const wizardProvider = ref<Provider | null>(null)
const deleteTarget = ref<{ id: number; name: string } | null>(null)
const toast = ref<{ text: string; kind: 'success' | 'error' } | null>(null)
const collecting = ref<number | null>(null)

function showToast(text: string, kind: 'success' | 'error') {
  toast.value = { text, kind }
  setTimeout(() => { toast.value = null }, 3000)
}

function maskKey(key: string) {
  if (key.length <= 4) return '****'
  return `...${key.slice(-4)}`
}

function intervalLabel(sec: number) {
  if (sec === 0) return '手动'
  const opts = [10, 60, 300, 900, 3600, 21600, 86400]
  const found = opts.find(o => o === sec)
  if (found) {
    const labels: Record<number, string> = { 10: '每 10 秒', 60: '每 1 分钟', 300: '每 5 分钟', 900: '每 15 分钟', 3600: '每 1 小时', 21600: '每 6 小时', 86400: '每 24 小时' }
    return labels[found] ?? `${sec}s`
  }
  return `${sec}s`
}

function mappingLabel(m: Record<string, string> | null | undefined) {
  if (!m || Object.keys(m).length === 0) return '未配置'
  return Object.entries(m).map(([k, v]) => `${k}: ${v}`).join(', ')
}

function openCreate() {
  wizardProvider.value = null
  showWizard.value = true
}

function openEdit(p: Provider) {
  wizardProvider.value = p
  showWizard.value = true
}

function onWizardClose() {
  showWizard.value = false
  wizardProvider.value = null
}

function confirmDelete(id: number, name: string) { deleteTarget.value = { id, name } }

async function doDelete() {
  if (!deleteTarget.value) return
  try { await store.remove(deleteTarget.value.id); showToast('厂商已删除', 'success') }
  catch { showToast('删除失败', 'error') }
  finally { deleteTarget.value = null }
}

async function doCollect(id: number) {
  collecting.value = id
  try {
    const res = await store.collect(id)
    const parts: string[] = []
    if (res.usage?.status === 'ok') parts.push(`用量: ${res.usage.record_count} 条`)
    else parts.push(`用量失败: ${res.usage?.message ?? '未知'}`)
    if (res.balance?.status === 'ok') parts.push(`余额: ${res.balance.balance ?? 'N/A'}`)
    else if (res.balance) parts.push(`余额失败: ${res.balance.message ?? '未知'}`)
    showToast(parts.join(' | '), res.usage?.status === 'ok' || res.balance?.status === 'ok' ? 'success' : 'error')
  } catch { showToast('采集失败', 'error') }
  finally { collecting.value = null }
}

onMounted(() => store.fetch())
</script>

<template>
  <div class="page">
    <div style="display: flex; justify-content: space-between; align-items: center;">
      <h2 class="page-title">厂商管理</h2>
      <button class="btn-primary" @click="openCreate">+ 新增厂商</button>
    </div>

    <div v-if="store.loading && store.providers.length === 0" class="loading">加载中...</div>

    <div v-else-if="store.providers.length === 0" class="empty-add" @click="openCreate">
      <p style="font-size: 18px; font-weight: 700; color: var(--color-text-muted);">+ 添加厂商</p>
      <p style="font-size: 13px; color: var(--color-text-muted); margin-top: var(--space-xs);">点击此处配置第一个 LLM 厂商</p>
    </div>

    <template v-else>
      <div v-for="p in store.providers" :key="p.id" class="card provider-card">
        <div class="provider-info">
          <div class="provider-header">
            <span class="provider-name">{{ p.name }}</span>
            <span class="tag">{{ intervalLabel(p.interval_seconds) }}</span>
            <span class="tag" style="background: var(--color-primary); color: var(--color-surface);">{{ p.currency_symbol }}</span>
            <span class="tag" :class="p.billing_mode === 'token_plan' ? 'mode-tag-tp' : 'mode-tag-api'">{{ p.billing_mode === 'token_plan' ? 'TokenPlan' : 'API' }}</span>
          </div>
          <div class="provider-meta">
            <span>Key: {{ maskKey(p.api_key) }}</span>
            <span>{{ p.base_url }}{{ p.usage_api_path }}</span>
          </div>
          <div class="provider-meta" style="font-size: 11px;">
            <span>用法映射: {{ mappingLabel(p.usage_mapping) }}</span>
            <span v-if="p.balance_api_path">余额映射: {{ mappingLabel(p.balance_mapping) }}</span>
            <span v-if="p.billing_mode !== 'token_plan' && p.last_balance != null">余额: {{ p.last_balance }} {{ p.currency_symbol }}</span>
            <span v-if="p.billing_mode === 'token_plan' && p.monthly_fee != null">月费: {{ p.monthly_fee }} {{ p.currency_symbol }}</span>
          </div>
          <div class="provider-models">
            <span v-for="m in p.models" :key="m" class="tag">{{ m }}</span>
          </div>
        </div>
        <div class="provider-actions">
          <button class="btn-primary" :disabled="!!collecting" @click="doCollect(p.id)">
            {{ collecting === p.id ? '采集中...' : '立即采集' }}
          </button>
          <button @click="openEdit(p)">编辑</button>
          <button class="btn-danger" @click="confirmDelete(p.id, p.name)">删除</button>
        </div>
      </div>
    </template>

    <!-- Wizard -->
    <ProviderWizard
      v-if="showWizard"
      :provider="wizardProvider"
      @close="onWizardClose"
    />

    <!-- Delete confirmation -->
    <div v-if="deleteTarget" class="modal-overlay" @click.self="deleteTarget = null">
      <div class="modal-content" style="max-width: 360px;">
        <h3 class="modal-title">确认删除</h3>
        <p style="margin-bottom: var(--space-lg);">确定要删除厂商 "{{ deleteTarget.name }}" 吗？此操作不可撤销。</p>
        <div style="display: flex; gap: var(--space-sm); justify-content: flex-end;">
          <button @click="deleteTarget = null">取消</button>
          <button class="btn-danger" @click="doDelete">确认删除</button>
        </div>
      </div>
    </div>

    <div v-if="toast" class="toast" :class="`toast-${toast.kind}`">{{ toast.text }}</div>
  </div>
</template>

<style scoped>
.provider-card { display: flex; justify-content: space-between; align-items: flex-start; gap: var(--space-md); }
.provider-info { display: flex; flex-direction: column; gap: var(--space-xs); flex: 1; }
.provider-header { display: flex; align-items: center; gap: var(--space-sm); }
.provider-name { font-size: 16px; font-weight: 800; }
.provider-meta { display: flex; gap: var(--space-lg); font-size: 13px; color: var(--color-text-muted); font-family: var(--font-mono); }
.provider-models { display: flex; flex-wrap: wrap; align-items: center; gap: var(--space-xs); margin-top: var(--space-xs); }
.provider-actions { display: flex; gap: var(--space-xs); flex-shrink: 0; }
.mode-tag-api { background: var(--color-primary); color: var(--color-surface); }
.mode-tag-tp { background: #8250df; color: #fff; }
</style>
