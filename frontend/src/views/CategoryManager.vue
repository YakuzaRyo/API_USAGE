<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { fetchCategories, deleteCategory, type Category } from '../api'
import CategoryWizard from '../components/CategoryWizard.vue'

const categories = ref<Category[]>([])
const loading = ref(true)
const toast = ref<{ text: string; kind: 'success' | 'error' } | null>(null)

const deleting = ref<number | null>(null)
const showWizard = ref(false)
const selectedCategory = ref<Category | null>(null)

function toastMsg(text: string, kind: 'success' | 'error') {
  toast.value = { text, kind }
  setTimeout(() => { toast.value = null }, 3000)
}

async function load() {
  loading.value = true
  try {
    const res = await fetchCategories()
    categories.value = res.data
  } catch {
    toastMsg('加载分类失败，请确认后端已启动', 'error')
  } finally {
    loading.value = false
  }
}

function openCreate() {
  selectedCategory.value = null
  showWizard.value = true
}

function openEdit(cat: Category) {
  selectedCategory.value = cat
  showWizard.value = true
}

function onWizardClose() {
  showWizard.value = false
  selectedCategory.value = null
  load()
}

async function doDelete(id: number) {
  try {
    await deleteCategory(id)
    toastMsg('已删除', 'success')
    deleting.value = null
    await load()
  } catch { toastMsg('删除失败', 'error') }
}

onMounted(load)
</script>

<template>
  <div class="page">
    <div style="display: flex; justify-content: space-between; align-items: center;">
      <h2 class="page-title">分类管理</h2>
      <button class="btn-primary" @click="openCreate">+ 新增</button>
    </div>

    <div v-if="loading" class="loading">加载中...</div>

    <div v-else-if="categories.length === 0" class="empty-add" @click="openCreate">
      <p style="font-size: 18px; font-weight: 700; color: var(--color-text-muted);">+ 添加分类</p>
      <p style="font-size: 13px; color: var(--color-text-muted); margin-top: var(--space-xs);">配置厂商分类模板</p>
    </div>

    <div v-else class="logo-grid">
      <div
        v-for="cat in categories"
        :key="cat.id"
        class="logo-item"
        @click="openEdit(cat)"
        @contextmenu.prevent="deleting = cat.id"
      >
        <div class="logo-img-wrap">
          <img
            v-if="cat.logo_path"
            :src="`/api/categories/${cat.id}/logo`"
            :alt="cat.name"
            class="logo-img"
          />
          <span v-else class="logo-placeholder">{{ cat.name.charAt(0).toUpperCase() }}</span>
        </div>
        <span class="logo-name">{{ cat.name }}</span>
      </div>
    </div>

    <!-- Category Wizard -->
    <CategoryWizard
      v-if="showWizard"
      :category="selectedCategory"
      @close="onWizardClose"
    />

    <!-- Delete confirm -->
    <div v-if="deleting" class="modal-overlay" @click.self="deleting = null">
      <div class="modal-content" style="max-width: 340px;">
        <h3 class="modal-title">确认删除</h3>
        <p style="margin-bottom: var(--space-lg);">删除后关联的 Provider 将不再属于该分类。</p>
        <div style="display: flex; gap: var(--space-sm); justify-content: flex-end;">
          <button @click="deleting = null">取消</button>
          <button class="btn-danger" @click="doDelete(deleting)">确认删除</button>
        </div>
      </div>
    </div>

    <div v-if="toast" class="toast" :class="`toast-${toast.kind}`">{{ toast.text }}</div>
  </div>
</template>

<style scoped>
/* ── Logo Grid ────────────────────────── */
.logo-grid {
  display: flex;
  flex-wrap: wrap;
  justify-content: center;
  gap: 20px;
  padding: var(--space-md) 0;
}

.logo-item {
  display: flex;
  flex-direction: column;
  align-items: center;
  cursor: pointer;
  transition: opacity 0.3s ease, filter 0.3s ease;
}

.logo-name {
  font-size: 11px;
  font-weight: 600;
  color: var(--color-text-muted);
  line-height: 1;
  max-height: 0;
  opacity: 0;
  overflow: hidden;
  transition: max-height 0.3s ease, opacity 0.2s ease;
  white-space: nowrap;
  pointer-events: none;
}

/* Spotlight: dim all items only when a specific logo is hovered */
.logo-grid:has(.logo-item:hover) .logo-item {
  opacity: 0.3;
  filter: grayscale(0.8) blur(1px);
}

.logo-grid:has(.logo-item:hover) .logo-item:not(:hover) .logo-img-wrap {
  transform: scale(0.7);
}

/* Spotlight: hovered item — only scale the image, not the whole container */
.logo-grid:has(.logo-item:hover) .logo-item:hover {
  opacity: 1;
  filter: none;
}

.logo-grid:has(.logo-item:hover) .logo-item:hover .logo-img-wrap {
  transform: scale(1.6);
}

.logo-grid:has(.logo-item:hover) .logo-item:hover .logo-name {
  max-height: 14px;
  opacity: 1;
  margin-top: 2px;
}

.logo-img-wrap {
  width: 120px;
  height: 120px;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: transform 0.4s cubic-bezier(0.34, 1.56, 0.64, 1);
}

.logo-img {
  max-width: 100%;
  max-height: 100%;
  object-fit: contain;
}

.logo-placeholder {
  width: 88px;
  height: 88px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 36px;
  font-weight: 900;
  border: 2px solid var(--color-border);
  box-shadow: var(--shadow-sm);
  background: var(--color-bg);
  color: var(--color-text);
}
</style>
