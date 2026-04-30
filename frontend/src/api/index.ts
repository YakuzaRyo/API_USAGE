import axios from 'axios'

const api = axios.create({
  baseURL: '/api',
  timeout: 30000,
})

// ── Types ──────────────────────────────

export interface Provider {
  id: number
  name: string
  api_key: string
  base_url: string
  usage_api_path: string
  balance_api_path: string | null
  last_balance?: number | null
  models: string[]
  usage_mapping: Record<string, string> | null
  balance_mapping: Record<string, string> | null
  currency_symbol: string
  interval_seconds: number
  billing_mode: string
  monthly_fee: number | null
  sub_start_date: string | null
  category_id: number | null
  created_at: string
}

export interface UsageSummary {
  total_tokens: number
  total_cost: number
  active_providers: number
  total_balance: number
  balance_consumed: number
  currency_symbol: string
}

export interface TrendPoint {
  date: string
  tokens: number
  cost: number
  balance: number
  provider_name: string
}

export interface DistributionPoint {
  model: string
  tokens: number
}

export interface BalancePoint {
  date: string
  provider_name: string
  balance: number
  currency_symbol: string
}

// ── Provider APIs ──────────────────────

export const fetchProviders = () =>
  api.get<Provider[]>('/providers')

export const createProvider = (data: Omit<Provider, 'id' | 'created_at'>) =>
  api.post<Provider>('/providers', data)

export const updateProvider = (id: number, data: Partial<Omit<Provider, 'id' | 'created_at'>>) =>
  api.put<Provider>(`/providers/${id}`, data)

export const deleteProvider = (id: number) =>
  api.delete(`/providers/${id}`)

export const testApi = (data: { base_url: string; api_key: string; api_path: string }) =>
  api.post<{ status_code: number; body: unknown }>('/providers/test-api', data)

export const testApiForProvider = (providerId: number, data: { api_path: string }) =>
  api.post<{ status_code: number; body: unknown }>(`/providers/${providerId}/test-api`, data)

export const triggerCollection = (id: number) =>
  api.post<{ usage: { status: string; record_count?: number; message?: string }; balance: { status: string; balance?: number; message?: string } | null }>(`/providers/${id}/collect`)

// ── Stats APIs ─────────────────────────

export const fetchUsageSummary = (params?: { provider_id?: number }) =>
  api.get<UsageSummary>('/stats/summary', { params })

export const fetchUsageTrends = (params?: { provider_id?: number }) =>
  api.get<TrendPoint[]>('/stats/trends', { params })

export const fetchUsageDistribution = (params?: { provider_id?: number }) =>
  api.get<DistributionPoint[]>('/stats/distribution', { params })

export const fetchBalanceHistory = (params?: { provider_id?: number; days?: number; start?: string; end?: string }) =>
  api.get<BalancePoint[]>('/stats/balance-history', { params })

export interface BillingItem {
  provider_id: number
  provider_name: string
  billing_mode: string
  amount: number
  currency_symbol: string
}

export const fetchBillingSummary = (params?: { provider_id?: number }) =>
  api.get<BillingItem[]>('/stats/billing-summary', { params })

// ── Category APIs ──────────────────────

export interface Category {
  id: number
  name: string
  api_base_url: string
  api_usage_path: string
  api_balance_path: string | null
  tp_base_url: string
  tp_usage_path: string
  currency_symbol: string
  models: string[]
  logo_path: string | null
}

export const fetchCategories = () =>
  api.get<Category[]>('/categories')

export const fetchCategoryPresets = () =>
  api.get<string[]>('/categories/presets')

export const createCategory = (data: Omit<Category, 'id'>) =>
  api.post<{ id: number; name: string }>('/categories', data)

export const updateCategory = (id: number, data: Partial<Omit<Category, 'id'>>) =>
  api.put<{ id: number; name: string }>(`/categories/${id}`, data)

export const deleteCategory = (id: number) =>
  api.delete(`/categories/${id}`)

export const uploadCategoryLogo = (id: number, file: File) => {
  const form = new FormData()
  form.append('file', file)
  return api.post<{ logo_path: string }>(`/categories/${id}/logo`, form)
}

export const deleteCategoryLogo = (id: number) =>
  api.delete(`/categories/${id}/logo`)
