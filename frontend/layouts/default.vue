<template>
  <div class="min-h-screen bg-gray-50">
    <Navbar />
    <main>
      <slot />
    </main>
    <footer class="bg-white border-t mt-12">
      <div class="max-w-7xl mx-auto py-6 px-4 text-center text-gray-500 text-sm">
        © 2026 艾柯 (Aiko) API 中转站 - 让 AI 调用更简单
      </div>
    </footer>
  </div>
</template>
