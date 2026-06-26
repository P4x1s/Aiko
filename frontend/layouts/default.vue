<template>
  <div class="min-h-screen bg-white">
    <Navbar />
    <main>
      <slot />
    </main>
    <footer class="border-t mt-16">
      <div class="max-w-6xl mx-auto py-8 px-4 text-center text-gray-400 text-sm">
        © 2026 艾柯 (Aiko) API 中转站
      </div>
    </footer>
  </div>
</template>
