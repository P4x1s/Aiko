<template>
  <div class="max-w-6xl mx-auto px-4 sm:px-6 py-8">
    <div class="mb-8">
      <h1 class="text-xl font-semibold text-gray-900">余额 & 充值</h1>
      <p class="text-sm text-gray-500 mt-1">管理你的账户余额</p>
    </div>

    <!-- Balance Card -->
    <div class="border rounded-xl p-6 mb-8">
      <div class="flex items-center justify-between">
        <div>
          <div class="text-sm text-gray-500">当前余额</div>
          <div class="text-3xl font-semibold mt-1">¥{{ balance.toFixed(2) }}</div>
        </div>
        <button
          @click="showRechargeModal = true"
          class="bg-gray-900 text-white px-5 py-2 rounded-lg text-sm hover:bg-gray-800 transition"
        >
          充值
        </button>
      </div>
    </div>

    <!-- Usage Stats -->
    <div class="grid md:grid-cols-2 gap-6 mb-8">
      <div class="border rounded-xl p-6">
        <div class="text-sm text-gray-500 mb-1">本月调用次数</div>
        <div class="text-2xl font-semibold">{{ stats.total_requests }}</div>
      </div>
      <div class="border rounded-xl p-6">
        <div class="text-sm text-gray-500 mb-1">本月消费</div>
        <div class="text-2xl font-semibold">¥{{ stats.total_cost.toFixed(4) }}</div>
      </div>
    </div>

    <!-- Transaction History -->
    <div class="border rounded-xl overflow-hidden">
      <div class="px-6 py-4 border-b">
        <h2 class="font-semibold">交易记录</h2>
      </div>
      <div v-if="loading" class="p-12 text-center text-gray-400">
        加载中...
      </div>
      <div v-else-if="transactions.length === 0" class="p-12 text-center text-gray-400">
        暂无交易记录
      </div>
      <div v-else class="divide-y">
        <div
          v-for="tx in transactions"
          :key="tx.id"
          class="px-6 py-3 flex items-center justify-between"
        >
          <div>
            <div class="text-sm">{{ tx.description }}</div>
            <div class="text-xs text-gray-400 mt-0.5">
              {{ new Date(tx.created_at).toLocaleString('zh-CN') }}
            </div>
          </div>
          <div :class="tx.amount > 0 ? 'text-green-600' : 'text-gray-900'" class="font-medium text-sm">
            {{ tx.amount > 0 ? '+' : '' }}¥{{ Math.abs(tx.amount).toFixed(4) }}
          </div>
        </div>
      </div>
    </div>

    <!-- Recharge Modal -->
    <div v-if="showRechargeModal" class="fixed inset-0 bg-black/50 flex items-center justify-center z-50">
      <div class="bg-white rounded-xl p-6 w-full max-w-md mx-4">
        <h3 class="font-semibold mb-4">选择充值金额</h3>

        <!-- Pricing Tiers -->
        <div class="grid grid-cols-2 gap-3 mb-6">
          <button
            v-for="tier in tiers"
            :key="tier.id"
            @click="selectedTier = tier"
            :class="selectedTier?.id === tier.id ? 'border-gray-900 bg-gray-50' : 'border-gray-200'"
            class="border-2 rounded-lg p-3 text-left hover:border-gray-400 transition"
          >
            <div class="font-semibold">¥{{ tier.amount }}</div>
            <div v-if="tier.bonus > 0" class="text-xs text-green-600">送 ¥{{ tier.bonus }}</div>
          </button>
        </div>

        <!-- Payment Method -->
        <div class="mb-6">
          <div class="text-sm text-gray-600 mb-2">支付方式</div>
          <div class="flex gap-2">
            <button
              v-for="method in paymentMethods"
              :key="method.id"
              @click="selectedMethod = method.id"
              :class="selectedMethod === method.id ? 'border-gray-900 bg-gray-50' : 'border-gray-200'"
              class="border-2 rounded-lg px-4 py-2 text-sm hover:border-gray-400 transition"
            >
              {{ method.icon }} {{ method.name }}
            </button>
          </div>
        </div>

        <!-- Actions -->
        <div class="flex justify-end gap-2">
          <button
            @click="showRechargeModal = false"
            class="px-4 py-2 text-sm text-gray-600 hover:text-gray-900"
          >
            取消
          </button>
          <button
            @click="handlePayment"
            :disabled="!selectedTier || !selectedMethod || paying"
            class="px-4 py-2 bg-gray-900 text-white text-sm rounded-lg hover:bg-gray-800 disabled:opacity-50"
          >
            {{ paying ? '处理中...' : '立即支付' }}
          </button>
        </div>
      </div>
    </div>

    <!-- Payment Result Modal -->
    <div v-if="paymentResult" class="fixed inset-0 bg-black/50 flex items-center justify-center z-50">
      <div class="bg-white rounded-xl p-6 w-full max-w-sm mx-4 text-center">
        <div class="text-4xl mb-4">📱</div>
        <h3 class="font-semibold mb-2">扫码支付</h3>
        <p class="text-sm text-gray-500 mb-4">请使用{{ selectedMethod === 'alipay' ? '支付宝' : '微信' }}扫码</p>
        <div class="bg-gray-100 p-4 rounded-lg mb-4">
          <div class="text-2xl font-semibold">¥{{ paymentResult.total }}</div>
        </div>
        <button
          @click="paymentResult = null"
          class="w-full px-4 py-2 bg-gray-100 text-gray-700 text-sm rounded-lg hover:bg-gray-200"
        >
          取消支付
        </button>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
definePageMeta({
  middleware: 'auth',
})

const config = useRuntimeConfig()
const apiBase = config.public.apiBase

const balance = ref(0)
const transactions = ref<any[]>([])
const stats = ref({ total_requests: 0, total_cost: 0 })
const tiers = ref<any[]>([])
const loading = ref(true)
const showRechargeModal = ref(false)
const selectedTier = ref<any>(null)
const selectedMethod = ref('alipay')
const paying = ref(false)
const paymentResult = ref<any>(null)

const paymentMethods = [
  { id: 'alipay', name: '支付宝', icon: '💙' },
  { id: 'wechat', name: '微信支付', icon: '💚' },
  { id: 'crypto', name: '加密货币', icon: '₿' },
]

const loadData = async () => {
  loading.value = true
  try {
    const [balanceRes, historyRes, statsRes, tiersRes] = await Promise.all([
      $fetch<{ balance: number }>(`${apiBase}/api/billing/balance`),
      $fetch<{ transactions: any[] }>(`${apiBase}/api/billing/history`),
      $fetch<{ total_requests: number; total_cost: number }>(`${apiBase}/api/billing/stats`),
      $fetch<{ tiers: any[] }>(`${apiBase}/api/billing/pricing`),
    ])
    balance.value = balanceRes.balance
    transactions.value = historyRes.transactions || []
    stats.value = statsRes
    tiers.value = tiersRes.tiers || []
  } catch (e) {
    console.error('Failed to load billing data:', e)
  }
  loading.value = false
}

const handlePayment = async () => {
  paying.value = true
  try {
    const response = await $fetch<any>(`${apiBase}/api/billing/create-payment`, {
      method: 'POST',
      body: {
        tier_id: selectedTier.value.id,
        payment_method: selectedMethod.value,
      },
    })
    paymentResult.value = response
    showRechargeModal.value = false
  } catch (e) {
    console.error('Failed to create payment:', e)
  }
  paying.value = false
}

onMounted(() => {
  loadData()
})
</script>
