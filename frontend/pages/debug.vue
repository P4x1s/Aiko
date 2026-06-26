<template>
  <div class="max-w-6xl mx-auto px-4 sm:px-6 py-8">
    <div class="mb-8">
      <h1 class="text-xl font-semibold text-gray-900">调试信息</h1>
      <p class="text-sm text-gray-500 mt-1">检查用户权限状态</p>
    </div>

    <div class="border rounded-xl p-6 space-y-4">
      <div>
        <div class="text-sm text-gray-500">用户 ID</div>
        <div class="font-mono text-sm">{{ user?.id || '未登录' }}</div>
      </div>
      <div>
        <div class="text-sm text-gray-500">邮箱</div>
        <div class="font-mono text-sm">{{ user?.email || '无' }}</div>
      </div>
      <div>
        <div class="text-sm text-gray-500">角色 (role)</div>
        <div class="font-mono text-sm">{{ user?.user_metadata?.role || 'user' }}</div>
      </div>
      <div>
        <div class="text-sm text-gray-500">是否管理员</div>
        <div class="font-mono text-sm">{{ isAdmin ? '是' : '否' }}</div>
      </div>
      <div>
        <div class="text-sm text-gray-500">用户元数据</div>
        <pre class="font-mono text-xs bg-gray-100 p-2 rounded overflow-auto">{{ JSON.stringify(user?.user_metadata, null, 2) }}</pre>
      </div>
    </div>

    <div class="mt-6 border rounded-xl p-6">
      <h2 class="font-semibold mb-4">设置管理员角色</h2>
      <p class="text-sm text-gray-500 mb-4">在 Supabase SQL Editor 执行以下 SQL：</p>
      <pre class="bg-gray-900 text-green-400 p-4 rounded-lg text-sm overflow-auto"><code>-- 将用户设为管理员（替换用户ID）
UPDATE auth.users
SET raw_user_meta_data = raw_user_meta_data || '{"role": "admin"}'::jsonb
WHERE id = '8e09d6f9-c340-4e10-97f6-cad88e13c670';</code></pre>
      <p class="text-xs text-gray-400 mt-2">执行后需要重新登录才能生效</p>
    </div>
  </div>
</template>

<script setup lang="ts">
const user = useSupabaseUser()

const isAdmin = computed(() => {
  return user.value?.user_metadata?.role === 'admin'
})
</script>
