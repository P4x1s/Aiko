<template>
  <div class="min-h-[calc(100vh-120px)] flex items-center justify-center py-12 px-4">
    <div class="w-full max-w-sm">
      <div class="text-center mb-8">
        <h1 class="text-xl font-semibold text-gray-900">注册</h1>
        <p class="text-sm text-gray-500 mt-1">创建账号，开始使用</p>
      </div>

      <form @submit.prevent="handleRegister" class="space-y-4">
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

        <div>
          <label class="block text-sm text-gray-600 mb-1.5">密码</label>
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
          {{ loading ? '注册中...' : '注册' }}
        </button>

        <p class="text-center text-sm text-gray-500">
          已有账号？
          <NuxtLink to="/login" class="text-gray-900 hover:underline">立即登录</NuxtLink>
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

  try {
    const { data, error: authError } = await supabase.auth.signUp({
      email: email.value,
      password: password.value,
    })

    if (authError) {
      const msg = authError.message || ''
      if (msg.includes('already registered') || msg.includes('already exists')) {
        error.value = '该邮箱已注册'
      } else if (msg.includes('valid email')) {
        error.value = '请输入有效的邮箱地址'
      } else if (msg.includes('password')) {
        error.value = '密码至少需要6位'
      } else {
        error.value = msg || '注册失败，请稍后重试'
      }
    } else if (data?.user) {
      // Check if email confirmation is required
      if (data.user.identities?.length === 0) {
        error.value = '该邮箱已注册'
      } else {
        success.value = '注册成功！请检查邮箱中的确认链接'
      }
    } else {
      error.value = '注册失败，请稍后重试'
    }
  } catch (e: any) {
    error.value = '网络错误，请稍后重试'
  }

  loading.value = false
}
</script>
