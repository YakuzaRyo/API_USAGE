<script setup lang="ts">
import { ref, reactive, watch, onMounted } from 'vue'
import { useProvidersStore } from '../stores/providers'
import { testApi, testApiForProvider, fetchCategories, type Provider, type Category } from '../api'
import JsonPathTagCloud from './JsonPathTagCloud.vue'

const props = defineProps<{ provider: Provider | null }>()
const emit = defineEmits<{ close: [] }>()

const store = useProvidersStore()

const currentStep = ref<1 | 2 | 3>(1)
const saving = ref(false)
const editingId = ref<number | null>(props.provider?.id ?? null)
const apiKeyDirty = ref(false)

const intervalOptions = [
  { value: 0, label: '手动' },
  { value: 10, label: '每 10 秒' },
  { value: 60, label: '每 1 分钟' },
  { value: 300, label: '每 5 分钟' },
  { value: 900, label: '每 15 分钟' },
  { value: 3600, label: '每 1 小时' },
  { value: 21600, label: '每 6 小时' },
  { value: 86400, label: '每 24 小时' },
]

const categories = ref<Category[]>([])
const selectedCategoryId = ref<number | null>(null)

onMounted(async () => {
  try { const res = await fetchCategories(); categories.value = res.data }
  catch { /* silent */ }
})

function onCategorySelect(catId: number | null) {
  selectedCategoryId.value = catId
  if (!catId) return
  const cat = categories.value.find(c => c.id === catId)
  if (!cat) return
  if (form.billing_mode === 'api') {
    form.base_url = cat.api_base_url || form.base_url
    form.usage_api_path = cat.api_usage_path || form.usage_api_path
    form.balance_api_path = cat.api_balance_path || form.balance_api_path
  } else {
    form.base_url = cat.tp_base_url || form.base_url
    form.usage_api_path = cat.tp_usage_path || form.usage_api_path
  }
  form.currency_symbol = cat.currency_symbol || form.currency_symbol
  if (cat.models.length > 0) form.models = [...cat.models]
}

function defaultForm() {
  return {
    name: '',
    api_key: '',
    base_url: '',
    usage_api_path: '/v1/usage',
    balance_api_path: '',
    models: [] as string[],
    usage_mapping_total_tokens: '',
    usage_mapping_cost: '',
    balance_mapping_balance: '',
    currency_symbol: 'CNY',
    interval_seconds: 300,
    billing_mode: 'api',
    monthly_fee: null as number | null,
    sub_start_date: null as string | null,
    category_id: null as number | null,
  }
}

const form = reactive(defaultForm())

// Init form from provider if editing
watch(() => props.provider, (p) => {
  if (p) {
    form.name = p.name
    form.api_key = p.api_key
    form.base_url = p.base_url
    form.usage_api_path = p.usage_api_path
    form.balance_api_path = p.balance_api_path ?? ''
    form.models = [...p.models]
    form.usage_mapping_total_tokens = p.usage_mapping?.total_tokens ?? ''
    form.usage_mapping_cost = p.usage_mapping?.cost ?? ''
    form.balance_mapping_balance = p.balance_mapping?.balance ?? ''
    form.currency_symbol = p.currency_symbol ?? 'CNY'
    form.interval_seconds = p.interval_seconds
    form.billing_mode = p.billing_mode ?? 'api'
    form.monthly_fee = p.monthly_fee ?? null
    form.sub_start_date = p.sub_start_date ?? null
    form.category_id = (p as any).category_id ?? null
    selectedCategoryId.value = (p as any).category_id ?? null
    apiKeyDirty.value = false
  }
}, { immediate: true })

// --- Step 1 state ---
const modelInput = ref('')
const step1Errors = ref<Record<string, string>>({})

function addModel() {
  const v = modelInput.value.trim()
  if (v && !form.models.includes(v)) form.models.push(v)
  modelInput.value = ''
}
function removeModel(m: string) {
  form.models = form.models.filter(x => x !== m)
}

function validateStep1(): boolean {
  const errs: Record<string, string> = {}
  if (!form.name.trim()) errs.name = '名称不能为空'
  if (!form.api_key.trim()) errs.api_key = 'API Key 不能为空'
  if (!form.base_url.trim()) errs.base_url = 'Base URL 不能为空'
  if (form.models.length === 0) errs.models = '至少添加一个模型'
  step1Errors.value = errs
  return Object.keys(errs).length === 0
}

// --- Step 2 state ---
const step2Testing = ref(false)
const step2Result = ref<{ status_code: number; body: unknown } | null>(null)
const focusedTarget = ref<'tokens' | 'cost' | 'balance' | null>(null)
const noFocusHint = ref(false)
let focusTimer: ReturnType<typeof setTimeout> | null = null

async function doStep2Test() {
  step2Testing.value = true
  step2Result.value = null
  try {
    const res = editingId.value
      ? await testApiForProvider(editingId.value, { api_path: form.usage_api_path })
      : await testApi({ base_url: form.base_url, api_key: form.api_key, api_path: form.usage_api_path })
    step2Result.value = res.data
  } catch {
    step2Result.value = { status_code: -1, body: '请求失败' }
  } finally { step2Testing.value = false }
}

function onInputFocus(target: 'tokens' | 'cost' | 'balance') {
  if (focusTimer) { clearTimeout(focusTimer); focusTimer = null }
  focusedTarget.value = target
}
function onInputBlur() {
  focusTimer = setTimeout(() => { focusedTarget.value = null }, 200)
}

function onTagSelect(payload: { path: string }) {
  if (!focusedTarget.value) {
    noFocusHint.value = true
    setTimeout(() => { noFocusHint.value = false }, 2000)
    return
  }
  if (focusedTarget.value === 'tokens') form.usage_mapping_total_tokens = payload.path
  else if (focusedTarget.value === 'cost') form.usage_mapping_cost = payload.path
  else if (focusedTarget.value === 'balance') form.balance_mapping_balance = payload.path
}

// --- Step 3 state ---
const step3Testing = ref(false)
const step3Result = ref<{ status_code: number; body: unknown } | null>(null)

async function doStep3Test() {
  step3Testing.value = true
  step3Result.value = null
  try {
    const res = editingId.value
      ? await testApiForProvider(editingId.value, { api_path: form.balance_api_path })
      : await testApi({ base_url: form.base_url, api_key: form.api_key, api_path: form.balance_api_path })
    step3Result.value = res.data
  } catch {
    step3Result.value = { status_code: -1, body: '请求失败' }
  } finally { step3Testing.value = false }
}

// --- Save logic ---
function buildPayload() {
  const usage_mapping: Record<string, string> = {}
  if (form.usage_mapping_total_tokens) usage_mapping.total_tokens = form.usage_mapping_total_tokens
  if (form.usage_mapping_cost) usage_mapping.cost = form.usage_mapping_cost
  const balance_mapping: Record<string, string> = {}
  if (form.balance_mapping_balance) balance_mapping.balance = form.balance_mapping_balance
  const payload: Record<string, unknown> = {
    name: form.name,
    base_url: form.base_url,
    usage_api_path: form.usage_api_path,
    balance_api_path: form.balance_api_path || null,
    models: form.models,
    usage_mapping: Object.keys(usage_mapping).length > 0 ? usage_mapping : null,
    balance_mapping: Object.keys(balance_mapping).length > 0 ? balance_mapping : null,
    currency_symbol: form.currency_symbol,
    interval_seconds: form.interval_seconds,
    billing_mode: form.billing_mode,
    monthly_fee: form.monthly_fee,
    sub_start_date: form.sub_start_date,
    category_id: selectedCategoryId.value,
  }
  if (!editingId.value || apiKeyDirty.value) {
    payload.api_key = form.api_key
  }
  return payload
}

async function saveAndContinue() {
  if (currentStep.value === 1) {
    if (!validateStep1()) return
    saving.value = true
    try {
      const payload = buildPayload()
      if (editingId.value) {
        await store.update(editingId.value, payload as any)
      } else {
        const created = await store.create(payload as any)
        if (created) editingId.value = created.id
      }
      currentStep.value = 2
    } catch { /* toast handled by store */ }
    finally { saving.value = false }
  } else if (currentStep.value === 2) {
    saving.value = true
    try {
      const payload = buildPayload()
      if (editingId.value) {
        await store.update(editingId.value, payload as any)
      } else {
        const created = await store.create(payload as any)
        if (created) editingId.value = created.id
      }
      currentStep.value = 3
    } catch { /* toast handled by store */ }
    finally { saving.value = false }
  } else {
    await saveOnly()
  }
}

async function saveOnly() {
  saving.value = true
  try {
    const payload = buildPayload()
    if (editingId.value) {
      await store.update(editingId.value, payload as any)
    } else {
      const created = await store.create(payload as any)
      if (created) editingId.value = created.id
    }
    emit('close')
  } catch { /* toast handled by store */ }
  finally { saving.value = false }
}

function goBack() {
  if (currentStep.value > 1) currentStep.value--
}

function goToStep(step: 1 | 2 | 3) {
  currentStep.value = step
}

function close() {
  emit('close')
}
</script>

<template>
  <div class="modal-overlay" @click.self="close">
    <div class="modal-content wizard-modal">
      <div class="wizard-header">
        <h3 class="modal-title">{{ editingId ? '编辑厂商' : '新增厂商' }}</h3>
        <button class="wizard-close" @click="close">&times;</button>
      </div>

      <!-- Step indicator -->
      <div class="wizard-steps-label">
        <span :class="{ active: currentStep === 1 }">连接配置</span>
        <span class="step-arrow">&rarr;</span>
        <span :class="{ active: currentStep === 2 }">用量路径</span>
        <span class="step-arrow">&rarr;</span>
        <span :class="{ active: currentStep === 3 }">余额 &amp; 其他</span>
      </div>

      <div class="wizard-body">
        <!-- ====== STEP 1 ====== -->
        <div v-if="currentStep === 1" class="step-panel">
          <div class="form-group">
            <label>计费方式</label>
            <div class="pill-group">
              <button type="button" class="pill" :class="form.billing_mode === 'api' ? 'active' : 'inactive'" @click="form.billing_mode = 'api'; onCategorySelect(selectedCategoryId)">API 查询</button>
              <button type="button" class="pill" :class="form.billing_mode === 'token_plan' ? 'active' : 'inactive'" @click="form.billing_mode = 'token_plan'; onCategorySelect(selectedCategoryId)">Token Plan</button>
            </div>
          </div>
          <div class="form-group">
            <label>分类</label>
            <select v-model="selectedCategoryId" @change="onCategorySelect(selectedCategoryId)">
              <option :value="null">无分类</option>
              <option v-for="cat in categories" :key="cat.id" :value="cat.id">{{ cat.name }}</option>
            </select>
          </div>
          <div class="form-group">
            <label>名称 *</label>
            <input v-model="form.name" placeholder="如 OpenAI-GPT4" />
            <span v-if="step1Errors.name" class="field-err">{{ step1Errors.name }}</span>
          </div>
          <div class="form-group">
            <label>API Key *</label>
            <input v-model="form.api_key" type="password" placeholder="sk-..." autocomplete="off" @input="apiKeyDirty = true" />
            <span v-if="step1Errors.api_key" class="field-err">{{ step1Errors.api_key }}</span>
          </div>
          <div class="form-group">
            <label>Base URL *</label>
            <input v-model="form.base_url" placeholder="https://api.openai.com" />
            <span v-if="step1Errors.base_url" class="field-err">{{ step1Errors.base_url }}</span>
          </div>
          <div class="form-group">
            <label>追踪模型 *</label>
            <div class="model-input-row">
              <input v-model="modelInput" placeholder="模型名" @keyup.enter="addModel" style="flex: 1;" />
              <button type="button" @click="addModel">添加</button>
            </div>
            <div v-if="form.models.length > 0" class="tag-row">
              <span v-for="m in form.models" :key="m" class="tag">{{ m }}<span class="tag-remove" @click="removeModel(m)">&times;</span></span>
            </div>
            <span v-if="step1Errors.models" class="field-err">{{ step1Errors.models }}</span>
          </div>
        </div>

        <!-- ====== STEP 2 ====== -->
        <div v-if="currentStep === 2" class="step-panel">
          <div class="form-group">
            <label>Usage API Path</label>
            <div class="input-btn-row">
              <input v-model="form.usage_api_path" placeholder="/v1/usage" style="flex: 1;" />
              <button :disabled="step2Testing" @click="doStep2Test">{{ step2Testing ? '...' : '测试' }}</button>
            </div>
          </div>
          <div class="form-group" v-if="step2Result && step2Result.status_code !== -1">
            <JsonPathTagCloud :json="step2Result.body" @select="onTagSelect" />
            <p v-if="noFocusHint" class="field-err" style="margin-top: 4px;">请先点击目标输入框</p>
          </div>
          <div class="form-group">
            <label>Token 总量 JSONPath</label>
            <div class="mapping-tag-container" :class="{ focused: focusedTarget === 'tokens' }" @click="onInputFocus('tokens')" tabindex="0" @focus="onInputFocus('tokens')" @blur="onInputBlur">
              <span v-if="form.usage_mapping_total_tokens" class="mapping-tag">
                {{ form.usage_mapping_total_tokens.split('.').pop() }}
                <span class="tag-remove" @click.stop="form.usage_mapping_total_tokens = ''">&times;</span>
              </span>
              <span v-else class="mapping-placeholder">点击 JSON 树中的 key 填入路径</span>
            </div>
          </div>
          <div class="form-group">
            <label>费用 JSONPath</label>
            <div class="mapping-tag-container" :class="{ focused: focusedTarget === 'cost' }" @click="onInputFocus('cost')" tabindex="0" @focus="onInputFocus('cost')" @blur="onInputBlur">
              <span v-if="form.usage_mapping_cost" class="mapping-tag">
                {{ form.usage_mapping_cost.split('.').pop() }}
                <span class="tag-remove" @click.stop="form.usage_mapping_cost = ''">&times;</span>
              </span>
              <span v-else class="mapping-placeholder">点击 JSON 树中的 key 填入路径</span>
            </div>
          </div>
        </div>

        <!-- ====== STEP 3 ====== -->
        <div v-if="currentStep === 3" class="step-panel">
          <!-- API mode -->
          <template v-if="form.billing_mode === 'api'">
            <div class="form-group">
              <label>Balance API Path</label>
              <div class="input-btn-row">
                <input v-model="form.balance_api_path" placeholder="/user/balance" style="flex: 1;" />
                <button :disabled="step3Testing" @click="doStep3Test">{{ step3Testing ? '...' : '测试' }}</button>
              </div>
            </div>
            <div class="form-group" v-if="step3Result && step3Result.status_code !== -1">
              <JsonPathTagCloud :json="step3Result.body" @select="onTagSelect" />
              <p v-if="noFocusHint" class="field-err" style="margin-top: 4px;">请先点击目标输入框</p>
            </div>
            <div class="form-group">
              <label>余额 JSONPath</label>
              <div class="mapping-tag-container" :class="{ focused: focusedTarget === 'balance' }" @click="onInputFocus('balance')" tabindex="0" @focus="onInputFocus('balance')" @blur="onInputBlur">
                <span v-if="form.balance_mapping_balance" class="mapping-tag">
                  {{ form.balance_mapping_balance.split('.').pop() }}
                  <span class="tag-remove" @click.stop="form.balance_mapping_balance = ''">&times;</span>
                </span>
                <span v-else class="mapping-placeholder">点击 JSON 树中的 key 填入路径</span>
              </div>
            </div>
          </template>

          <!-- Token Plan mode -->
          <template v-else>
            <div class="form-group">
              <label>月费金额</label>
              <input v-model.number="form.monthly_fee" type="number" placeholder="如 200" min="0" step="0.01" />
            </div>
            <div class="form-group">
              <label>订阅起始日期</label>
              <input v-model="form.sub_start_date" type="date" />
            </div>
          </template>

          <div class="form-group">
            <label>货币符号</label>
            <input v-model="form.currency_symbol" placeholder="CNY" style="max-width: 80px;" />
          </div>
          <div class="form-group">
            <label>轮询间隔</label>
            <select v-model="form.interval_seconds">
              <option v-for="opt in intervalOptions" :key="opt.value" :value="opt.value">{{ opt.label }}</option>
            </select>
          </div>
        </div>
      </div>

      <!-- Actions -->
      <div class="wizard-actions">
        <button v-if="currentStep > 1" @click="goBack">上一步</button>
        <div style="flex: 1;"></div>
        <button v-if="currentStep < 3" class="btn-primary" :disabled="saving" @click="saveAndContinue">
          {{ saving ? '保存中...' : '保存并继续' }}
        </button>
        <button v-else class="btn-primary" :disabled="saving" @click="saveOnly">
          {{ saving ? '保存中...' : '保存' }}
        </button>
      </div>

      <!-- Dot navigation -->
      <div class="wizard-dots">
        <button
          v-for="s in ([1, 2, 3] as const)"
          :key="s"
          class="wizard-dot"
          :class="{ active: currentStep === s }"
          :title="`Step ${s}`"
          @click="goToStep(s)"
        ></button>
      </div>
    </div>
  </div>
</template>

<style scoped>
.wizard-modal {
  max-width: 560px;
  max-height: 90vh;
  overflow-y: auto;
  padding: var(--space-lg);
}

.wizard-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: var(--space-md);
}

.wizard-close {
  background: none;
  border: none;
  font-size: 24px;
  cursor: pointer;
  color: var(--color-text-muted);
  line-height: 1;
  padding: 0;
}
.wizard-close:hover { color: var(--color-text); }

.wizard-steps-label {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: var(--space-sm);
  font-size: 13px;
  color: var(--color-text-muted);
  margin-bottom: var(--space-lg);
  font-weight: 600;
}
.wizard-steps-label .active {
  color: var(--color-primary);
}
.step-arrow {
  color: var(--color-border);
  font-size: 14px;
}

.wizard-body {
  min-height: 200px;
}

.step-panel {
  display: flex;
  flex-direction: column;
  gap: var(--space-md);
}

.form-group {
  display: flex;
  flex-direction: column;
  gap: var(--space-xs);
}
.form-group label {
  font-size: 13px;
  font-weight: 600;
  color: var(--color-text);
}

.field-err {
  color: var(--color-danger);
  font-size: 12px;
}

.model-input-row, .input-btn-row {
  display: flex;
  gap: var(--space-xs);
}

.tag-row {
  display: flex;
  flex-wrap: wrap;
  gap: var(--space-xs);
  margin-top: var(--space-xs);
}

.mapping-tag-container {
  display: flex;
  align-items: center;
  min-height: 36px;
  padding: 4px 8px;
  border: var(--border-width) solid var(--color-border);
  cursor: pointer;
  transition: border-color 0.15s, box-shadow 0.15s;
}
.mapping-tag-container.focused {
  border-color: var(--color-primary);
  box-shadow: 0 0 0 2px var(--color-primary);
}

.mapping-tag {
  display: inline-flex;
  align-items: center;
  gap: 4px;
  padding: 2px 8px;
  font-size: 12px;
  font-family: var(--font-mono);
  color: var(--color-text);
  background: var(--color-bg);
  border: var(--border-width) solid var(--color-border);
  cursor: default;
  user-select: none;
}

.mapping-placeholder {
  font-size: 13px;
  color: var(--color-text-muted);
}

/* Actions */
.wizard-actions {
  display: flex;
  gap: var(--space-sm);
  margin-top: var(--space-lg);
  padding-top: var(--space-md);
  border-top: var(--border-width) solid var(--color-border);
}

/* Dot navigation */
.wizard-dots {
  display: flex;
  justify-content: center;
  align-items: center;
  gap: 16px;
  margin-top: var(--space-md);
  padding-bottom: var(--space-xs);
}

.wizard-dot {
  width: 12px;
  height: 12px;
  border-radius: 50%;
  border: 2px solid var(--color-border);
  background: transparent;
  cursor: pointer;
  padding: 0;
  transition: width 0.2s, height 0.2s, background 0.2s, border-color 0.2s, transform 0.2s;
}
.wizard-dot:hover {
  border-color: var(--color-primary);
  transform: scale(1.15);
}
.wizard-dot.active {
  width: 20px;
  height: 20px;
  background: var(--color-primary);
  border-color: var(--color-primary);
}
.wizard-dot.active:hover {
  transform: scale(1.05);
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
}
</style>
