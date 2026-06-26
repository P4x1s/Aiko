<template>
  <div class="max-w-6xl mx-auto px-4 sm:px-6 py-8">
    <div class="flex justify-between items-center mb-8">
      <div>
        <h1 class="text-xl font-semibold text-gray-900">请求日志</h1>
        <p class="text-sm text-gray-500 mt-1">最近的 API 调用记录</p>
      </div>
      <NuxtLink to="/admin" class="text-sm text-gray-500 hover:text-gray-900">
        ← 返回
      </NuxtLink>
    </div>

    <!-- Requests Table -->
    <div class="border rounded-xl overflow-hidden">
      <table class="w-full">
        <thead class="bg-gray-50">
          <tr>
            <th class="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase">用户</th>
            <th class="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase">模型</th>
            <th class="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase">输入 Tokens</th>
            <th class="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase">输出 Tokens</th>
            <th class="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase">费用</th>
            <th class="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase">延迟</th>
            <th class="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase">时间</th>
          </tr>
        </thead>
        <tbody class="divide-y">
          <tr v-for="req in requests" :key="req.id" class="hover:bg-gray-50">
            <td class="px-4 py-3 text-sm">{{ req.profiles?.email || '-' }}</td>
            <td class="px-4 py-3 text-sm font-mono">{{ req.model }}</td>
            <td class="px-4 py-3 text-sm">{{ req.tokens_input }}</td>
            <td class="px-4 py-3 text-sm">{{ req.tokens_output }}</td>
            <td class="px-4 py-3 text-sm">¥{{ req.cost?.toFixed(4) }}</td>
            <td class="px-4 py-3 text-sm">{{ req.latency_ms }}ms</td>
            <td class="px-4 py-3 text-sm text-gray-500">
              {{ new Date(req.created_at).toLocaleString('zh-CN') }}
            </td>
          </tr>
        </tbody>
      </table>

      <div v-if="requests.length === 0" class="p-12 text-center text-gray-400">
        暂无请求记录
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
definePageMeta({
  middleware: 'admin',
})

const requests = ref<any[]>([])

onMounted(async () => {
  // TODO: Fetch from API
})
</script>
