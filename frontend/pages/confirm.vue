<template>
  <div class="min-h-screen flex items-center justify-center py-12 px-4">
    <div class="max-w-md w-full text-center">
      <div class="text-6xl mb-4">✉️</div>
      <h1 class="text-2xl font-bold text-gray-900 mb-4">邮箱已确认</h1>
      <p class="text-gray-500 mb-8">你的邮箱已成功验证，现在可以登录了。</p>
      <NuxtLink
        to="/login"
        class="bg-indigo-600 text-white px-6 py-3 rounded-lg hover:bg-indigo-700 transition inline-block"
      >
        立即登录
      </NuxtLink>
    </div>
  </div>
</template>

<script setup lang="ts">
definePageMeta({
  layout: 'default',
})
</script>
