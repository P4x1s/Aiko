<template>
  <div class="min-h-[calc(100vh-120px)] flex items-center justify-center py-12 px-4">
    <div class="w-full max-w-sm">
      <div class="text-center mb-8">
        <h1 class="text-xl font-semibold text-gray-900">找回密码</h1>
        <p class="text-sm text-gray-500 mt-1">输入邮箱获取重置链接</p>
      </div>

      <form @submit.prevent="handleReset" class="space-y-4">
        <div v-if="error" class="bg-red-50 text-red-600 p-3 rounded-lg text-sm">
          {{ error }}
        </div>

        <div v-if="success" class="bg-green-50 text-green-600 p-3 rounded-lg text-sm">
          {{ success }}
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

        <button
          type="submit"
          :disabled="loading"
          class="w-full bg-gray-900 text-white py-2 rounded-lg text-sm font-medium hover:bg-gray-800 disabled:opacity-50 transition"
        >
          {{ loading ? '发送中...' : '发送重置链接' }}
        </button>

        <p class="text-center text-sm text-gray-500">
          <NuxtLink to="/login" class="text-gray-900 hover:underline">返回登录</NuxtLink>
        </p>
      </form>
    </div>
  </div>
</template>

<script setup lang="ts">
definePageMeta({
  layout: 'default',
})

const user = useSupabaseUser()
const supabase = useSupabaseClient()

if (user.value) {
  navigateTo('/dashboard')
}

const email = ref('')
const loading = ref(false)
const error = ref('')
const success = ref('')

const handleReset = async () => {
  loading.value = true
  error.value = ''
  success.value = ''

  const { error: authError } = await supabase.auth.resetPasswordForEmail(email.value, {
    redirectTo: `${window.location.origin}/reset-password`,
  })

  if (authError) {
    error.value = authError.message || '发送失败'
  } else {
    success.value = '重置链接已发送，请检查邮箱'
  }

  loading.value = false
}
</script>
