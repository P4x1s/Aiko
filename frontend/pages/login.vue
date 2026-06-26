<template>
  <div class="min-h-[calc(100vh-120px)] flex items-center justify-center py-12 px-4">
    <div class="w-full max-w-sm">
      <div class="text-center mb-8">
        <h1 class="text-xl font-semibold text-gray-900">登录</h1>
        <p class="text-sm text-gray-500 mt-1">欢迎回来</p>
      </div>

      <form @submit.prevent="handleLogin" class="space-y-4">
        <div v-if="error" class="bg-red-50 text-red-600 p-3 rounded-lg text-sm">
          {{ error }}
        </div>

        <div>
          <label class="block text-sm text-gray-600 mb-1.5">邮箱</label>
          <input
            v-model="email"
            type="email"
            required
            class="w-full px-3 py-2 border rounded-lg text-sm focus:ring-2 focus:ring-gray-900 focus:border-gray-900 outline-none transition"
            placeholder="your@email.com"
          />
        </div>

        <div>
          <label class="block text-sm text-gray-600 mb-1.5">密码</label>
          <input
            v-model="password"
            type="password"
            required
            class="w-full px-3 py-2 border rounded-lg text-sm focus:ring-2 focus:ring-gray-900 focus:border-gray-900 outline-none transition"
            placeholder="••••••••"
          />
        </div>

        <button
          type="submit"
          :disabled="loading"
          class="w-full bg-gray-900 text-white py-2 rounded-lg text-sm font-medium hover:bg-gray-800 disabled:opacity-50 transition"
        >
          {{ loading ? '登录中...' : '登录' }}
        </button>

        <p class="text-center text-sm text-gray-500">
          还没有账号？
          <NuxtLink to="/register" class="text-gray-900 hover:underline">立即注册</NuxtLink>
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

  try {
    const { error: authError } = await supabase.auth.signInWithPassword({
      email: email.value,
      password: password.value,
    })

    if (authError) {
      const msg = authError.message || ''
      if (msg.includes('Invalid login credentials')) {
        error.value = '邮箱或密码错误'
      } else if (msg.includes('Email not confirmed')) {
        error.value = '请先验证邮箱后再登录'
      } else if (msg.includes('not found')) {
        error.value = '账号不存在，请先注册'
      } else {
        error.value = msg || '登录失败'
      }
    } else {
      navigateTo('/dashboard')
    }
  } catch (e) {
    error.value = '网络错误，请稍后重试'
  }

  loading.value = false
}
</script>
