<template>
  <div class="min-h-screen flex items-center justify-center py-12 px-4">
    <div class="max-w-md w-full">
      <div class="text-center mb-8">
        <h1 class="text-3xl font-bold text-gray-900">登录</h1>
        <p class="mt-2 text-gray-500">欢迎回到艾柯 Aiko</p>
      </div>

      <form @submit.prevent="handleLogin" class="bg-white p-8 rounded-lg shadow-sm border space-y-4">
        <div v-if="error" class="bg-red-50 text-red-600 p-3 rounded text-sm">
          {{ error }}
        </div>

        <div>
          <label class="block text-sm font-medium text-gray-700 mb-1">邮箱</label>
          <input
            v-model="email"
            type="email"
            required
            class="w-full px-4 py-2 border rounded-lg focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500 outline-none"
            placeholder="your@email.com"
          />
        </div>

        <div>
          <label class="block text-sm font-medium text-gray-700 mb-1">密码</label>
          <input
            v-model="password"
            type="password"
            required
            class="w-full px-4 py-2 border rounded-lg focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500 outline-none"
            placeholder="••••••••"
          />
        </div>

        <button
          type="submit"
          :disabled="loading"
          class="w-full bg-indigo-600 text-white py-2 rounded-lg hover:bg-indigo-700 disabled:opacity-50 transition"
        >
          {{ loading ? '登录中...' : '登录' }}
        </button>

        <p class="text-center text-gray-500 text-sm">
          还没有账号？
          <NuxtLink to="/register" class="text-indigo-600 hover:underline">立即注册</NuxtLink>
        </p>
      </form>
    </div>
  </div>
</template>

<script setup lang="ts">
definePageMeta({
  layout: 'default',
})

const supabase = useSupabaseClient()
const email = ref('')
const password = ref('')
const loading = ref(false)
const error = ref('')

const handleLogin = async () => {
  loading.value = true
  error.value = ''

  const { error: authError } = await supabase.auth.signInWithPassword({
    email: email.value,
    password: password.value,
  })

  if (authError) {
    error.value = authError.message === 'Invalid login credentials'
      ? '邮箱或密码错误'
      : authError.message
  } else {
    navigateTo('/dashboard')
  }

  loading.value = false
}
</script>
