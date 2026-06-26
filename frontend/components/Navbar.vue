<template>
  <nav class="border-b bg-white sticky top-0 z-50">
    <div class="max-w-6xl mx-auto px-4 sm:px-6">
      <div class="flex justify-between h-14 items-center">
        <div class="flex items-center space-x-8">
          <NuxtLink to="/" class="flex items-center space-x-2 font-semibold text-gray-900">
            <span class="text-lg">🤖 Aiko</span>
          </NuxtLink>
          <div class="hidden md:flex items-center space-x-6 text-sm text-gray-500">
            <NuxtLink to="/" class="hover:text-gray-900 transition">首页</NuxtLink>
            <a href="#features" class="hover:text-gray-900 transition">功能</a>
            <a href="#models" class="hover:text-gray-900 transition">模型</a>
            <a href="#pricing" class="hover:text-gray-900 transition">价格</a>
          </div>
        </div>
        <div class="flex items-center space-x-3">
          <template v-if="user">
            <NuxtLink to="/dashboard" class="text-sm text-gray-600 hover:text-gray-900">
              控制台
            </NuxtLink>
            <NuxtLink to="/dashboard/keys" class="text-sm text-gray-600 hover:text-gray-900">
              Keys
            </NuxtLink>
            <NuxtLink to="/dashboard/billing" class="text-sm text-gray-600 hover:text-gray-900">
              余额
            </NuxtLink>
            <span class="text-gray-200">|</span>
            <span class="text-sm text-gray-500">{{ user.email }}</span>
            <button
              @click="handleLogout"
              class="text-sm text-gray-400 hover:text-red-500 transition"
            >
              退出
            </button>
          </template>
          <template v-else>
            <NuxtLink
              to="/login"
              class="text-sm text-gray-600 hover:text-gray-900 px-3 py-1.5"
            >
              登录
            </NuxtLink>
            <NuxtLink
              to="/register"
              class="text-sm bg-gray-900 text-white px-4 py-1.5 rounded-md hover:bg-gray-800 transition"
            >
              注册
            </NuxtLink>
          </template>
        </div>
      </div>
    </div>
  </nav>
</template>

<script setup lang="ts">
const user = useSupabaseUser()
const supabase = useSupabaseClient()

const handleLogout = async () => {
  await supabase.auth.signOut()
  navigateTo('/login')
}
</script>
