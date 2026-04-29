import { defineStore } from 'pinia'
import { ref, watch } from 'vue'
import {
  fetchUsageSummary,
  fetchUsageTrends,
  fetchUsageDistribution,
  fetchBalanceHistory,
  fetchBillingSummary,
  type UsageSummary,
  type TrendPoint,
  type DistributionPoint,
  type BalancePoint,
  type BillingItem,
} from '../api'

export const useUsageStore = defineStore('usage', () => {
  const summary = ref<UsageSummary | null>(null)
  const trends = ref<TrendPoint[]>([])
  const distribution = ref<DistributionPoint[]>([])
  const selectedProviderId = ref<number | undefined>(undefined)
  const loading = ref(false)
  const error = ref<string | null>(null)

  async function fetchAll() {
    loading.value = true
    error.value = null
    const params = selectedProviderId.value ? { provider_id: selectedProviderId.value } : undefined
    try {
      const [s, t, d] = await Promise.all([
        fetchUsageSummary(params),
        fetchUsageTrends(params),
        fetchUsageDistribution(params),
      ])
      summary.value = s.data
      trends.value = t.data
      distribution.value = d.data
    } catch (e: unknown) {
      error.value = e instanceof Error ? e.message : '获取用量数据失败'
    } finally {
      loading.value = false
    }
  }

  const balanceHistory = ref<BalancePoint[]>([])
  const balanceLoading = ref(false)

  async function fetchBalanceHistoryData(params?: { provider_id?: number; days?: number; start?: string; end?: string }) {
    balanceLoading.value = true
    try {
      const res = await fetchBalanceHistory(params)
      balanceHistory.value = res.data
    } catch (e: unknown) {
      error.value = e instanceof Error ? e.message : '获取余额历史失败'
    } finally {
      balanceLoading.value = false
    }
  }

  function setProviderId(id: number | undefined) {
    selectedProviderId.value = id
  }

  watch(selectedProviderId, () => fetchAll())

  const billingSummary = ref<BillingItem[]>([])

  async function fetchBillingSummaryData(params?: { provider_id?: number }) {
    try {
      const res = await fetchBillingSummary(params)
      billingSummary.value = res.data
    } catch { /* silent */ }
  }

  return { summary, trends, distribution, selectedProviderId, loading, error, fetchAll, setProviderId, balanceHistory, balanceLoading, fetchBalanceHistoryData, billingSummary, fetchBillingSummaryData }
})
