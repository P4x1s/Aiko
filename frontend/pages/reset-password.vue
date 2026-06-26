<template>
  <div class="min-h-[calc(100vh-120px)] flex items-center justify-center py-12 px-4">
    <div class="w-full max-w-sm">
      <div class="text-center mb-8">
        <h1 class="text-xl font-semibold text-gray-900">重置密码</h1>
        <p class="text-sm text-gray-500 mt-1">设置新密码</p>
      </div>

      <form @submit.prevent="handleReset" class="space-y-4">
        <div v-if="error" class="bg-red-50 text-red-600 p-3 rounded-lg text-sm">
          {{ error }}
        </div>

        <div v-if="success" class="bg-green-50 text-green-600 p-3 rounded-lg text-sm">
          {{ success }}
        </div>

        <div>
          <label class="block text-sm text-gray-600 mb-1.5">新密码</label>
          <input
            v-model="password"
            type="password"
            required
            minlength="6"
            class="w-full px-3 py-2 border rounded-lg text-sm focus:ring-2 focus:ring-gray-900 focus:border-gray-900 outline-none transition"
            placeholder="至少6位密码"
          />
        </div>

        <div>
          <label class="block text-sm text-gray-600 mb-1.5">确认密码</label>
          <input
            v-model="confirmPassword"
            type="password"
            required
            class="w-full px-3 py-2 border rounded-lg text-sm focus:ring-2 focus:ring-gray-900 focus:border-gray-900 outline-none transition"
            placeholder="再次输入密码"
          />
        </div>

        <button
          type="submit"
          :disabled="loading"
          class="w-full bg-gray-900 text-white py-2 rounded-lg text-sm font-medium hover:bg-gray-800 disabled:opacity-50 transition"
        >
          {{ loading ? '重置中...' : '重置密码' }}
        </button>
      </form>
    </div>
  </div>
</template>

<script setup lang="ts">
definePageMeta({
  layout: 'default',
})

const route = useRoute()
const supabase = useSupabaseClient()
const password = ref('')
const confirmPassword = ref('')
const loading = ref(false)
const error = ref('')
const success = ref('')

const handleReset = async () => {
  if (password.value !== confirmPassword.value) {
    error.value = '两次输入的密码不一致'
    return
  }

  loading.value = true
  error.value = ''

  const { error: authError } = await supabase.auth.updateUser({
    password: password.value,
  })

  if (authError) {
    error.value = authError.message || '重置失败'
  } else {
    success.value = '密码已重置，正在跳转...'
    setTimeout(() => navigateTo('/login'), 2000)
  }

  loading.value = false
}
</script>
