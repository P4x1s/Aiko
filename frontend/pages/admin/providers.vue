<template>
  <div class="max-w-6xl mx-auto px-4 sm:px-6 py-8">
    <div class="flex justify-between items-center mb-8">
      <div>
        <h1 class="text-xl font-semibold text-gray-900">厂商统计</h1>
        <p class="text-sm text-gray-500 mt-1">各 AI 厂商使用情况</p>
      </div>
      <NuxtLink to="/admin" class="text-sm text-gray-500 hover:text-gray-900">
        ← 返回
      </NuxtLink>
    </div>

    <!-- Provider Stats -->
    <div class="grid md:grid-cols-2 lg:grid-cols-3 gap-6">
      <div
        v-for="(stat, provider) in providerStats"
        :key="provider"
        class="border rounded-xl p-6"
      >
        <div class="flex items-center gap-3 mb-4">
          <div
            :class="getProviderColor(provider as string)"
            class="w-10 h-10 rounded-lg flex items-center justify-center text-lg"
          >
            {{ getProviderIcon(provider as string) }}
          </div>
          <div>
            <div class="font-semibold">{{ provider }}</div>
            <div class="text-xs text-gray-500">{{ stat.requests }} 次调用</div>
          </div>
        </div>
        <div class="flex justify-between text-sm">
          <span class="text-gray-500">总消费</span>
          <span class="font-medium">¥{{ stat.cost.toFixed(4) }}</span>
        </div>
      </div>
    </div>

    <div v-if="Object.keys(providerStats).length === 0" class="border rounded-xl p-12 text-center text-gray-400">
      暂无统计数据
    </div>
  </div>
</template>

<script setup lang="ts">
definePageMeta({
  middleware: 'admin',
})

const providerStats = ref<Record<string, { requests: number; cost: number }>>({})

const getProviderIcon = (provider: string) => {
  const icons: Record<string, string> = {
    openai: '🟢',
    anthropic: '🟠',
    google: '🔵',
    baidu: '🔴',
    alibaba: '🟣',
    zhipu: '🔷',
    deepseek: '⚫',
  }
  return icons[provider] || '⚪'
}

const getProviderColor = (provider: string) => {
  const colors: Record<string, string> = {
    openai: 'bg-green-100',
    anthropic: 'bg-orange-100',
    google: 'bg-blue-100',
    baidu: 'bg-red-100',
    alibaba: 'bg-purple-100',
    zhipu: 'bg-cyan-100',
    deepseek: 'bg-gray-100',
  }
  return colors[provider] || 'bg-gray-100'
}

onMounted(async () => {
  // TODO: Fetch from API
})
</script>
