<template>
  <div class="max-w-6xl mx-auto px-4 sm:px-6 py-8">
    <div class="mb-8">
      <h1 class="text-xl font-semibold text-gray-900">控制台</h1>
      <p class="text-sm text-gray-500 mt-1">{{ user?.email }}</p>
    </div>

    <!-- Stats -->
    <div class="grid grid-cols-3 gap-4 mb-8">
      <div class="border rounded-xl p-4">
        <div class="text-sm text-gray-500 mb-1">余额</div>
        <div class="text-2xl font-semibold">¥{{ balance.toFixed(2) }}</div>
      </div>
      <div class="border rounded-xl p-4">
        <div class="text-sm text-gray-500 mb-1">API Keys</div>
        <div class="text-2xl font-semibold">{{ apiKeys.length }}</div>
      </div>
      <div class="border rounded-xl p-4">
        <div class="text-sm text-gray-500 mb-1">本月调用</div>
        <div class="text-2xl font-semibold">{{ requestCount }}</div>
      </div>
    </div>

    <!-- Quick Actions -->
    <div class="grid md:grid-cols-2 gap-6">
      <div class="border rounded-xl p-6">
        <h2 class="font-semibold mb-4">快速开始</h2>
        <div class="space-y-3">
          <NuxtLink
            to="/dashboard/keys"
            class="block p-3 bg-gray-50 rounded-lg hover:bg-gray-100 transition text-sm"
          >
            <div class="font-medium">🔑 创建 API Key</div>
            <div class="text-gray-500 mt-1">获取访问令牌</div>
          </NuxtLink>
          <a
            href="https://github.com/P4x1s/Aiko"
            target="_blank"
            class="block p-3 bg-gray-50 rounded-lg hover:bg-gray-100 transition text-sm"
          >
            <div class="font-medium">📖 查看文档</div>
            <div class="text-gray-500 mt-1">接入指南和示例代码</div>
          </a>
        </div>
      </div>

      <div class="border rounded-xl p-6">
        <h2 class="font-semibold mb-4">API 示例</h2>
        <div class="bg-gray-900 rounded-lg p-4 overflow-x-auto">
          <pre class="text-green-400 text-xs"><code>curl {{ apiBase }}/v1/chat/completions \
  -H "Authorization: Bearer YOUR_KEY" \
  -H "Content-Type: application/json" \
  -d '{"model":"gpt-4","messages":[{"role":"user","content":"Hi"}]}'</code></pre>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
definePageMeta({
  middleware: 'auth',
})

const user = useSupabaseUser()
const config = useRuntimeConfig()
const apiBase = config.public.apiBase

const balance = ref(0)
const apiKeys = ref<any[]>([])
const requestCount = ref(0)
</script>
