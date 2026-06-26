<template>
  <div class="max-w-6xl mx-auto px-4 sm:px-6 py-8">
    <div class="mb-8">
      <h1 class="text-xl font-semibold text-gray-900">管理后台</h1>
      <p class="text-sm text-gray-500 mt-1">系统管理与监控</p>
    </div>

    <!-- Stats Cards -->
    <div class="grid grid-cols-2 md:grid-cols-5 gap-4 mb-8">
      <div class="border rounded-xl p-4">
        <div class="text-sm text-gray-500 mb-1">总用户数</div>
        <div class="text-2xl font-semibold">{{ stats.total_users }}</div>
      </div>
      <div class="border rounded-xl p-4">
        <div class="text-sm text-gray-500 mb-1">总 API Keys</div>
        <div class="text-2xl font-semibold">{{ stats.total_api_keys }}</div>
      </div>
      <div class="border rounded-xl p-4">
        <div class="text-sm text-gray-500 mb-1">今日调用</div>
        <div class="text-2xl font-semibold">{{ stats.today_requests }}</div>
      </div>
      <div class="border rounded-xl p-4">
        <div class="text-sm text-gray-500 mb-1">今日消费</div>
        <div class="text-2xl font-semibold">¥{{ stats.today_cost }}</div>
      </div>
      <div class="border rounded-xl p-4">
        <div class="text-sm text-gray-500 mb-1">总余额</div>
        <div class="text-2xl font-semibold">¥{{ stats.total_balance }}</div>
      </div>
    </div>

    <!-- Quick Links -->
    <div class="grid md:grid-cols-3 gap-6">
      <NuxtLink
        to="/admin/users"
        class="border rounded-xl p-6 hover:border-gray-400 transition"
      >
        <div class="text-2xl mb-2">👥</div>
        <div class="font-semibold">用户管理</div>
        <div class="text-sm text-gray-500 mt-1">查看和管理所有用户</div>
      </NuxtLink>
      <NuxtLink
        to="/admin/requests"
        class="border rounded-xl p-6 hover:border-gray-400 transition"
      >
        <div class="text-2xl mb-2">📊</div>
        <div class="font-semibold">请求日志</div>
        <div class="text-sm text-gray-500 mt-1">查看 API 调用记录</div>
      </NuxtLink>
      <NuxtLink
        to="/admin/providers"
        class="border rounded-xl p-6 hover:border-gray-400 transition"
      >
        <div class="text-2xl mb-2">🔌</div>
        <div class="font-semibold">厂商统计</div>
        <div class="text-sm text-gray-500 mt-1">各厂商使用情况</div>
      </NuxtLink>
    </div>
  </div>
</template>

<script setup lang="ts">
definePageMeta({
  middleware: 'auth',
})

const stats = ref({
  total_users: 0,
  total_api_keys: 0,
  today_requests: 0,
  today_cost: 0,
  total_balance: 0,
})

onMounted(async () => {
  // TODO: Fetch from API
})
</script>
