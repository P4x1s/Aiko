<template>
  <div class="min-h-screen flex items-center justify-center py-12 px-4">
    <div class="max-w-md w-full">
      <div class="text-center mb-8">
        <h1 class="text-3xl font-bold text-gray-900">注册</h1>
        <p class="mt-2 text-gray-500">创建账号，开始使用艾柯 Aiko</p>
      </div>

      <form @submit.prevent="handleRegister" class="bg-white p-8 rounded-lg shadow-sm border space-y-4">
        <div v-if="error" class="bg-red-50 text-red-600 p-3 rounded text-sm">
          {{ error }}
        </div>

        <div v-if="success" class="bg-green-50 text-green-600 p-3 rounded text-sm">
          {{ success }}
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
            minlength="6"
            class="w-full px-4 py-2 border rounded-lg focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500 outline-none"
            placeholder="至少6位密码"
          />
        </div>

        <div>
          <label class="block text-sm font-medium text-gray-700 mb-1">确认密码</label>
          <input
            v-model="confirmPassword"
            type="password"
            required
            class="w-full px-4 py-2 border rounded-lg focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500 outline-none"
            placeholder="再次输入密码"
          />
        </div>

        <button
          type="submit"
          :disabled="loading"
          class="w-full bg-indigo-600 text-white py-2 rounded-lg hover:bg-indigo-700 disabled:opacity-50 transition"
        >
          {{ loading ? '注册中...' : '注册' }}
        </button>

        <p class="text-center text-gray-500 text-sm">
          已有账号？
          <NuxtLink to="/login" class="text-indigo-600 hover:underline">立即登录</NuxtLink>
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
const confirmPassword = ref('')
const loading = ref(false)
const error = ref('')
const success = ref('')

const handleRegister = async () => {
  loading.value = true
  error.value = ''
  success.value = ''

  if (password.value !== confirmPassword.value) {
    error.value = '两次输入的密码不一致'
    loading.value = false
    return
  }

  const { error: authError } = await supabase.auth.signUp({
    email: email.value,
    password: password.value,
  })

  if (authError) {
    error.value = authError.message === 'User already registered'
      ? '该邮箱已注册'
      : authError.message
  } else {
    success.value = '注册成功！请检查邮箱确认链接'
  }

  loading.value = false
}
</script>
