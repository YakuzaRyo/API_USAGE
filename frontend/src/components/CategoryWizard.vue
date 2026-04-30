<script setup lang="ts">
import { ref, reactive, watch } from 'vue'
import {
  fetchCategoryPresets, createCategory, updateCategory,
  uploadCategoryLogo, deleteCategoryLogo,
  type Category,
} from '../api'

const props = defineProps<{ category: Category | null }>()
const emit = defineEmits<{ close: [] }>()

const currentStep = ref<1 | 2>(1)
const saving = ref(false)
const editingId = ref<number | null>(props.category?.id ?? null)
const presets = ref<string[]>([])

const logoPreviewUrl = ref<string | null>(null)
const pendingLogoFile = ref<File | null>(null)
const logoInputRef = ref<HTMLInputElement | null>(null)

const modelInput = ref('')
const nameError = ref('')

const form = reactive({
  name: '',
  api_base_url: '',
  api_usage_path: '/v1/usage',
  api_balance_path: '',
  tp_base_url: '',
  tp_usage_path: '/v1/usage',
  currency_symbol: 'CNY',
  models: [] as string[],
})

// Load presets
fetchCategoryPresets()
  .then(res => { presets.value = res.data })
  .catch(() => {})

// Init form from category prop
watch(() => props.category, (cat) => {
  if (cat) {
    editingId.value = cat.id
    form.name = cat.name
    form.api_base_url = cat.api_base_url
    form.api_usage_path = cat.api_usage_path
    form.api_balance_path = cat.api_balance_path ?? ''
    form.tp_base_url = cat.tp_base_url
    form.tp_usage_path = cat.tp_usage_path
    form.currency_symbol = cat.currency_symbol
    form.models = [...cat.models]
    logoPreviewUrl.value = cat.logo_path ? `/api/categories/${cat.id}/logo?t=${Date.now()}` : null
  } else {
    editingId.value = null
    form.name = ''
    form.api_base_url = ''
    form.api_usage_path = '/v1/usage'
    form.api_balance_path = ''
    form.tp_base_url = ''
    form.tp_usage_path = '/v1/usage'
    form.currency_symbol = 'CNY'
    form.models = []
    logoPreviewUrl.value = null
  }
  pendingLogoFile.value = null
  currentStep.value = 1
  nameError.value = ''
}, { immediate: true })

function onNamePresetSelect(name: string) {
  form.name = name
}

function addModel() {
  const v = modelInput.value.trim()
  if (v && !form.models.includes(v)) form.models.push(v)
  modelInput.value = ''
}
function removeModel(m: string) {
  form.models = form.models.filter(x => x !== m)
}

function onLogoFileSelect(e: Event) {
  const input = e.target as HTMLInputElement
  if (!input.files?.length) return
  const file = input.files[0]

  if (!editingId.value) {
    // Create mode: cache file, show local preview
    pendingLogoFile.value = file
    logoPreviewUrl.value = URL.createObjectURL(file)
  } else {
    // Edit mode: upload immediately
    doLogoUpload(file)
  }
  input.value = ''
}

async function doLogoUpload(file: File) {
  if (!editingId.value) return
  try {
    await uploadCategoryLogo(editingId.value, file)
    logoPreviewUrl.value = `/api/categories/${editingId.value}/logo?t=${Date.now()}`
  } catch { /* toast handled by caller */ }
}

async function onLogoDelete() {
  if (!editingId.value) return
  try {
    await deleteCategoryLogo(editingId.value)
    logoPreviewUrl.value = null
  } catch { /* silent */ }
}

function validateStep1(): boolean {
  const errs: string[] = []
  if (!form.name.trim()) errs.push('名称不能为空')
  nameError.value = errs.length > 0 ? errs[0] : ''
  return errs.length === 0
}

async function saveAndContinue() {
  if (!validateStep1()) return
  saving.value = true
  try {
    const payload = {
      name: form.name,
      api_base_url: form.api_base_url,
      api_usage_path: form.api_usage_path,
      api_balance_path: form.api_balance_path || null,
      tp_base_url: form.tp_base_url,
      tp_usage_path: form.tp_usage_path,
      currency_symbol: form.currency_symbol,
      models: form.models,
    }

    if (editingId.value) {
      await updateCategory(editingId.value, payload as any)
    } else {
      const created = await createCategory(payload as any)
      if (created.data?.id) editingId.value = created.data.id
    }

    // Upload pending logo if any
    if (pendingLogoFile.value && editingId.value) {
      try {
        await uploadCategoryLogo(editingId.value, pendingLogoFile.value)
        logoPreviewUrl.value = `/api/categories/${editingId.value}/logo?t=${Date.now()}`
      } catch {
        // Category created but logo failed — non-blocking
      }
      pendingLogoFile.value = null
    }

    currentStep.value = 2
  } catch { /* error handling */ }
  finally { saving.value = false }
}

async function saveOnly() {
  saving.value = true
  try {
    const payload = {
      name: form.name,
      api_base_url: form.api_base_url,
      api_usage_path: form.api_usage_path,
      api_balance_path: form.api_balance_path || null,
      tp_base_url: form.tp_base_url,
      tp_usage_path: form.tp_usage_path,
      currency_symbol: form.currency_symbol,
      models: form.models,
    }

    if (editingId.value) {
      await updateCategory(editingId.value, payload as any)
    } else {
      await createCategory(payload as any)
    }
    emit('close')
  } catch { /* error handling */ }
  finally { saving.value = false }
}

function goBack() {
  if (currentStep.value > 1) currentStep.value--
}

function goToStep(step: 1 | 2) {
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
        <h3 class="modal-title">{{ editingId ? '编辑分类' : '新增分类' }}</h3>
        <button class="wizard-close" @click="close">&times;</button>
      </div>

      <!-- Step indicator -->
      <div class="wizard-steps-label">
        <span :class="{ active: currentStep === 1 }">基本信息</span>
        <span class="step-arrow">&rarr;</span>
        <span :class="{ active: currentStep === 2 }">API 配置</span>
      </div>

      <div class="wizard-body">
        <!-- ====== STEP 1 ====== -->
        <div v-if="currentStep === 1" class="step-panel">
          <!-- Logo + Name row -->
          <div class="top-row">
            <div v-if="logoPreviewUrl" class="top-logo">
              <img :src="logoPreviewUrl" alt="logo" class="top-logo-img" />
            </div>
            <div class="top-fields">
              <div class="preset-row">
                <button
                  v-for="p in presets" :key="p"
                  class="pill-preset"
                  :class="{ active: form.name === p }"
                  @click="onNamePresetSelect(p)"
                >{{ p }}</button>
              </div>
              <input v-model="form.name" placeholder="分类名称..." />
              <span v-if="nameError" class="field-err">{{ nameError }}</span>
              <div class="top-logo-actions">
                <button class="btn-sm" @click="logoInputRef?.click()">
                  {{ logoPreviewUrl ? '更换 Logo' : '上传 Logo' }}
                </button>
                <button v-if="logoPreviewUrl && editingId" class="btn-sm btn-danger" @click="onLogoDelete">删除</button>
                <input
                  ref="logoInputRef"
                  type="file"
                  accept=".png,.jpg,.jpeg,.svg,.webp"
                  style="display: none;"
                  @change="onLogoFileSelect"
                />
              </div>
            </div>
          </div>

          <!-- Default models -->
          <div class="form-group">
            <label>默认模型</label>
            <div class="form-content">
              <div class="model-input-row">
                <input v-model="modelInput" placeholder="模型名" @keyup.enter="addModel" style="flex: 1;" />
                <button type="button" @click="addModel">添加</button>
              </div>
              <div v-if="form.models.length > 0" class="tag-row">
                <span v-for="m in form.models" :key="m" class="tag">{{ m }}<span class="tag-remove" @click="removeModel(m)">&times;</span></span>
              </div>
            </div>
          </div>
        </div>

        <!-- ====== STEP 2 ====== -->
        <div v-if="currentStep === 2" class="step-panel">
          <div class="section-divider">API 配置</div>
          <div class="form-group"><label>Base URL</label><input v-model="form.api_base_url" placeholder="https://api.openai.com" /></div>
          <div class="form-group"><label>Usage Path</label><input v-model="form.api_usage_path" placeholder="/v1/usage" /></div>
          <div class="form-group"><label>Balance Path</label><input v-model="form.api_balance_path" placeholder="/v1/dashboard/billing/..." /></div>

          <div class="section-divider">Token Plan</div>
          <div class="form-group"><label>Base URL</label><input v-model="form.tp_base_url" placeholder="https://api.openai.com" /></div>
          <div class="form-group"><label>Usage Path</label><input v-model="form.tp_usage_path" placeholder="/v1/usage" /></div>

          <div class="section-divider">通用</div>
          <div class="form-group"><label>货币符号</label><input v-model="form.currency_symbol" placeholder="CNY" style="max-width: 80px;" /></div>
        </div>
      </div>

      <!-- Actions -->
      <div class="wizard-actions">
        <button v-if="currentStep > 1" @click="goBack">上一步</button>
        <div style="flex: 1;"></div>
        <button v-if="currentStep < 2" class="btn-primary" :disabled="saving" @click="saveAndContinue">
          {{ saving ? '保存中...' : '保存并继续' }}
        </button>
        <button v-else class="btn-primary" :disabled="saving" @click="saveOnly">
          {{ saving ? '保存中...' : '保存' }}
        </button>
      </div>

      <!-- Dot navigation -->
      <div class="wizard-dots">
        <button
          v-for="s in ([1, 2] as const)"
          :key="s"
          class="wizard-dot"
          :class="{ active: currentStep === s }"
          @click="goToStep(s)"
        ></button>
      </div>
    </div>
  </div>
</template>

<style scoped>
/* ── Wizard Chrome (from ProviderWizard) ── */
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
.wizard-steps-label .active { color: var(--color-primary); }
.step-arrow { color: var(--color-border); font-size: 14px; }

.wizard-body { min-height: 200px; }

.step-panel {
  display: flex;
  flex-direction: column;
  gap: var(--space-md);
}

.wizard-actions {
  display: flex;
  gap: var(--space-sm);
  margin-top: var(--space-lg);
  padding-top: var(--space-md);
  border-top: var(--border-width) solid var(--color-border);
}

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
.wizard-dot:hover { border-color: var(--color-primary); transform: scale(1.15); }
.wizard-dot.active {
  width: 20px;
  height: 20px;
  background: var(--color-primary);
  border-color: var(--color-primary);
}
.wizard-dot.active:hover { transform: scale(1.05); }

/* ── Step 1: Logo + Name ── */
.top-row {
  display: flex;
  gap: var(--space-md);
  align-items: flex-start;
}

.top-logo {
  width: 64px;
  height: 64px;
  flex-shrink: 0;
  display: flex;
  align-items: center;
  justify-content: center;
  border: 2px solid var(--color-border);
  box-shadow: var(--shadow-sm);
  background: var(--color-bg);
}

.top-logo-img {
  max-width: 100%;
  max-height: 100%;
  object-fit: contain;
}

.top-fields {
  flex: 1;
  display: flex;
  flex-direction: column;
  gap: var(--space-xs);
}

.top-logo-actions {
  display: flex;
  gap: var(--space-xs);
  margin-top: 2px;
}

.preset-row {
  display: flex;
  flex-wrap: wrap;
  gap: 4px;
}

.pill-preset {
  border-radius: 12px;
  border: 1.5px solid var(--color-border);
  padding: 2px 10px;
  font-size: 12px;
  font-weight: 600;
  cursor: pointer;
  background: transparent;
  color: var(--color-text-muted);
  transition: all 0.15s;
  box-shadow: none;
}
.pill-preset.active {
  background: var(--color-primary);
  color: #fff;
  border-color: var(--color-primary);
}

/* ── Form ── */
.form-group {
  display: flex;
  flex-direction: row;
  align-items: flex-start;
  gap: var(--space-sm);
  margin-bottom: var(--space-sm);
}
.form-group label {
  font-size: 13px;
  font-weight: 700;
  color: var(--color-text-muted);
  width: 100px;
  text-align: right;
  flex-shrink: 0;
  line-height: 36px;
}
.form-content {
  flex: 1;
  display: flex;
  flex-direction: column;
  gap: var(--space-xs);
}
.form-group input { flex: 1; }

.model-input-row { display: flex; gap: var(--space-xs); }
.tag-row { display: flex; flex-wrap: wrap; gap: var(--space-xs); margin-top: var(--space-xs); }

.section-divider {
  font-size: 12px;
  font-weight: 800;
  text-transform: uppercase;
  letter-spacing: 0.5px;
  color: var(--color-text-muted);
  border-bottom: 2px solid var(--color-border);
  padding-bottom: var(--space-xs);
  margin-bottom: var(--space-md);
  margin-top: var(--space-lg);
}

.field-err {
  color: var(--color-danger);
  font-size: 12px;
}

.btn-sm {
  font-size: 12px;
  padding: 2px 8px;
  border: 1px solid var(--color-border);
  background: transparent;
  color: var(--color-text-muted);
  cursor: pointer;
  border-radius: 4px;
}
.btn-sm:hover { border-color: var(--color-primary); color: var(--color-primary); }
.btn-danger { color: var(--color-danger); border-color: var(--color-danger); }
.btn-danger:hover { background: var(--color-danger); color: #fff; }
</style>
