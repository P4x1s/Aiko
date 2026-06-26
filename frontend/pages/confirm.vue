<template>
  <div class="min-h-[calc(100vh-120px)] flex items-center justify-center py-12 px-4">
    <div class="w-full max-w-sm text-center">
      <div v-if="loading" class="text-gray-500">
        <div class="text-4xl mb-4">⏳</div>
        <p>正在验证邮箱...</p>
      </div>

      <div v-else-if="error" class="text-red-600">
        <div class="text-4xl mb-4">❌</div>
        <p class="mb-4">{{ error }}</p>
        <NuxtLink to="/login" class="text-gray-900 hover:underline">
          返回登录
        </NuxtLink>
      </div>

      <div v-else>
        <div class="text-4xl mb-4">✅</div>
        <h1 class="text-xl font-semibold text-gray-900 mb-2">邮箱已验证</h1>
        <p class="text-gray-500 mb-6">你的邮箱已成功验证，现在可以登录了。</p>
        <NuxtLink
          to="/login"
          class="bg-gray-900 text-white px-6 py-2 rounded-lg text-sm hover:bg-gray-800 transition inline-block"
        >
          立即登录
        </NuxtLink>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
definePageMeta({
  layout: 'default',
})

const route = useRoute()
const supabase = useSupabaseClient()

const loading = ref(true)
const error = ref('')

onMounted(async () => {
  const { hash } = route.query

  if (hash) {
    const { error: authError } = await supabase.auth.exchangeCodeForSession(hash as string)
    if (authError) {
      error.value = authError.message
    }
  }

  loading.value = false
})
</script>
