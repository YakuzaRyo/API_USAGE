import { defineStore } from 'pinia'
import { ref } from 'vue'
import {
  fetchProviders,
  createProvider,
  updateProvider,
  deleteProvider,
  triggerCollection,
  type Provider,
} from '../api'

export const useProvidersStore = defineStore('providers', () => {
  const providers = ref<Provider[]>([])
  const loading = ref(false)
  const error = ref<string | null>(null)

  async function fetch() {
    loading.value = true
    error.value = null
    try {
      const res = await fetchProviders()
      providers.value = res.data
    } catch (e: unknown) {
      error.value = e instanceof Error ? e.message : '获取厂商列表失败'
    } finally {
      loading.value = false
    }
  }

  async function create(data: Omit<Provider, 'id' | 'created_at'>) {
    loading.value = true
    error.value = null
    try {
      const res = await createProvider(data)
      providers.value.push(res.data)
      return res.data
    } catch (e: unknown) {
      error.value = e instanceof Error ? e.message : '创建厂商失败'
      throw e
    } finally {
      loading.value = false
    }
  }

  async function update(id: number, data: Partial<Omit<Provider, 'id' | 'created_at'>>) {
    loading.value = true
    error.value = null
    try {
      const res = await updateProvider(id, data)
      const idx = providers.value.findIndex(p => p.id === id)
      if (idx !== -1) providers.value[idx] = res.data
    } catch (e: unknown) {
      error.value = e instanceof Error ? e.message : '更新厂商失败'
      throw e
    } finally {
      loading.value = false
    }
  }

  async function remove(id: number) {
    loading.value = true
    error.value = null
    try {
      await deleteProvider(id)
      providers.value = providers.value.filter(p => p.id !== id)
    } catch (e: unknown) {
      error.value = e instanceof Error ? e.message : '删除厂商失败'
      throw e
    } finally {
      loading.value = false
    }
  }

  async function collect(id: number) {
    const res = await triggerCollection(id)
    return res.data
  }

  return { providers, loading, error, fetch, create, update, remove, collect }
})
