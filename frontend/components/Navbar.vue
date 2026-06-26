<template>
  <nav class="bg-white shadow-sm border-b">
    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
      <div class="flex justify-between h-16">
        <div class="flex items-center">
          <NuxtLink to="/" class="flex items-center space-x-2">
            <span class="text-xl font-bold text-indigo-600">🤖 艾柯 Aiko</span>
          </NuxtLink>
        </div>
        <div class="flex items-center space-x-4">
          <template v-if="user">
            <NuxtLink to="/dashboard" class="text-gray-600 hover:text-indigo-600">
              控制台
            </NuxtLink>
            <NuxtLink to="/dashboard/keys" class="text-gray-600 hover:text-indigo-600">
              API Keys
            </NuxtLink>
            <span class="text-gray-400">|</span>
            <span class="text-gray-600 text-sm">{{ user.email }}</span>
            <button
              @click="handleLogout"
              class="text-gray-500 hover:text-red-600 text-sm"
            >
              退出
            </button>
          </template>
          <template v-else>
            <NuxtLink
              to="/login"
              class="text-gray-600 hover:text-indigo-600"
            >
              登录
            </NuxtLink>
            <NuxtLink
              to="/register"
              class="bg-indigo-600 text-white px-4 py-2 rounded-lg hover:bg-indigo-700 text-sm"
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
