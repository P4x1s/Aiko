<template>
  <div>
    <!-- Hero -->
    <section class="pt-20 pb-16 px-4">
      <div class="max-w-4xl mx-auto text-center">
        <div class="inline-block px-3 py-1 bg-gray-100 rounded-full text-sm text-gray-600 mb-6">
          让 AI 调用更简单
        </div>
        <h1 class="text-4xl md:text-5xl font-bold text-gray-900 mb-4 leading-tight">
          艾柯 <span class="text-gray-400">Aiko</span>
        </h1>
        <p class="text-lg text-gray-500 mb-8 max-w-2xl mx-auto">
          统一的 AI API 中转站，一个接口调用 OpenAI、Anthropic、Google 等多个厂商的模型
        </p>
        <div class="flex justify-center gap-3">
          <NuxtLink
            to="/register"
            class="bg-gray-900 text-white px-6 py-2.5 rounded-lg text-sm font-medium hover:bg-gray-800 transition"
          >
            免费开始
          </NuxtLink>
          <a
            href="#docs"
            class="bg-white text-gray-700 px-6 py-2.5 rounded-lg text-sm font-medium border hover:bg-gray-50 transition"
          >
            查看文档
          </a>
        </div>
      </div>
    </section>

    <!-- API Example -->
    <section class="pb-16 px-4">
      <div class="max-w-3xl mx-auto">
        <div class="bg-gray-50 rounded-xl p-6 border">
          <div class="flex items-center gap-2 mb-4">
            <div class="w-3 h-3 rounded-full bg-red-400"></div>
            <div class="w-3 h-3 rounded-full bg-yellow-400"></div>
            <div class="w-3 h-3 rounded-full bg-green-400"></div>
            <span class="ml-2 text-xs text-gray-400">terminal</span>
          </div>
          <pre class="text-sm text-gray-700 overflow-x-auto"><code><span class="text-gray-400"># 一行命令，调用任何模型</span>
curl https://aiko-five.vercel.app/v1/chat/completions \
  -H "Authorization: Bearer YOUR_KEY" \
  -H "Content-Type: application/json" \
  -d '{"model":"gpt-4","messages":[{"role":"user","content":"你好"}]}'</code></pre>
        </div>
      </div>
    </section>

    <!-- Pain Points -->
    <section id="features" class="py-16 px-4 bg-gray-50">
      <div class="max-w-6xl mx-auto">
        <h2 class="text-2xl font-bold text-center text-gray-900 mb-3">为什么选择 Aiko</h2>
        <p class="text-center text-gray-500 mb-12">解决国内开发者的三大痛点</p>
        <div class="grid md:grid-cols-3 gap-6">
          <div class="bg-white p-6 rounded-xl border">
            <div class="w-10 h-10 bg-gray-100 rounded-lg flex items-center justify-center mb-4 text-xl">
              💳
            </div>
            <h3 class="font-semibold text-gray-900 mb-2">支付便捷</h3>
            <p class="text-sm text-gray-500">无需海外信用卡，支持支付宝、微信支付，轻松充值</p>
          </div>
          <div class="bg-white p-6 rounded-xl border">
            <div class="w-10 h-10 bg-gray-100 rounded-lg flex items-center justify-center mb-4 text-xl">
              ⚡
            </div>
            <h3 class="font-semibold text-gray-900 mb-2">低延迟</h3>
            <p class="text-sm text-gray-500">海外服务器部署，国内直连稳定快速，告别卡顿</p>
          </div>
          <div class="bg-white p-6 rounded-xl border">
            <div class="w-10 h-10 bg-gray-100 rounded-lg flex items-center justify-center mb-4 text-xl">
              🔄
            </div>
            <h3 class="font-semibold text-gray-900 mb-2">统一管理</h3>
            <p class="text-sm text-gray-500">一个接口调用所有模型，统一管理，省时省力</p>
          </div>
        </div>
      </div>
    </section>

    <!-- Models -->
    <section id="models" class="py-16 px-4">
      <div class="max-w-6xl mx-auto">
        <h2 class="text-2xl font-bold text-center text-gray-900 mb-3">支持的模型</h2>
        <p class="text-center text-gray-500 mb-12">主流 AI 厂商全覆盖</p>
        <div class="grid md:grid-cols-3 gap-6">
          <div class="border rounded-xl p-6">
            <div class="flex items-center gap-3 mb-4">
              <div class="w-8 h-8 bg-green-100 rounded-full flex items-center justify-center text-sm">🟢</div>
              <span class="font-semibold">OpenAI</span>
            </div>
            <ul class="space-y-2 text-sm text-gray-600">
              <li class="flex items-center gap-2"><span class="w-1.5 h-1.5 bg-gray-300 rounded-full"></span>GPT-4o</li>
              <li class="flex items-center gap-2"><span class="w-1.5 h-1.5 bg-gray-300 rounded-full"></span>GPT-4 Turbo</li>
              <li class="flex items-center gap-2"><span class="w-1.5 h-1.5 bg-gray-300 rounded-full"></span>GPT-4</li>
              <li class="flex items-center gap-2"><span class="w-1.5 h-1.5 bg-gray-300 rounded-full"></span>GPT-3.5 Turbo</li>
            </ul>
          </div>
          <div class="border rounded-xl p-6">
            <div class="flex items-center gap-3 mb-4">
              <div class="w-8 h-8 bg-orange-100 rounded-full flex items-center justify-center text-sm">🟠</div>
              <span class="font-semibold">Anthropic</span>
            </div>
            <ul class="space-y-2 text-sm text-gray-600">
              <li class="flex items-center gap-2"><span class="w-1.5 h-1.5 bg-gray-300 rounded-full"></span>Claude 3.5 Sonnet</li>
              <li class="flex items-center gap-2"><span class="w-1.5 h-1.5 bg-gray-300 rounded-full"></span>Claude 3 Opus</li>
              <li class="flex items-center gap-2"><span class="w-1.5 h-1.5 bg-gray-300 rounded-full"></span>Claude 3 Haiku</li>
            </ul>
          </div>
          <div class="border rounded-xl p-6">
            <div class="flex items-center gap-3 mb-4">
              <div class="w-8 h-8 bg-blue-100 rounded-full flex items-center justify-center text-sm">🔵</div>
              <span class="font-semibold">Google</span>
            </div>
            <ul class="space-y-2 text-sm text-gray-600">
              <li class="flex items-center gap-2"><span class="w-1.5 h-1.5 bg-gray-300 rounded-full"></span>Gemini 1.5 Pro</li>
              <li class="flex items-center gap-2"><span class="w-1.5 h-1.5 bg-gray-300 rounded-full"></span>Gemini 1.5 Flash</li>
              <li class="flex items-center gap-2"><span class="w-1.5 h-1.5 bg-gray-300 rounded-full"></span>Gemini Pro</li>
            </ul>
          </div>
        </div>
      </div>
    </section>

    <!-- Pricing -->
    <section id="pricing" class="py-16 px-4 bg-gray-50">
      <div class="max-w-6xl mx-auto">
        <h2 class="text-2xl font-bold text-center text-gray-900 mb-3">透明定价</h2>
        <p class="text-center text-gray-500 mb-12">按实际使用量计费，无隐藏费用</p>
        <div class="grid md:grid-cols-3 gap-6 max-w-4xl mx-auto">
          <div class="bg-white border rounded-xl p-6">
            <h3 class="font-semibold mb-2">GPT-4o</h3>
            <div class="text-2xl font-bold mb-1">¥0.15</div>
            <div class="text-sm text-gray-500">/ 千 tokens</div>
          </div>
          <div class="bg-white border rounded-xl p-6">
            <h3 class="font-semibold mb-2">Claude 3.5 Sonnet</h3>
            <div class="text-2xl font-bold mb-1">¥0.20</div>
            <div class="text-sm text-gray-500">/ 千 tokens</div>
          </div>
          <div class="bg-white border rounded-xl p-6">
            <h3 class="font-semibold mb-2">Gemini 1.5 Pro</h3>
            <div class="text-2xl font-bold mb-1">¥0.10</div>
            <div class="text-sm text-gray-500">/ 千 tokens</div>
          </div>
        </div>
      </div>
    </section>

    <!-- CTA -->
    <section class="py-16 px-4">
      <div class="max-w-2xl mx-auto text-center">
        <h2 class="text-2xl font-bold text-gray-900 mb-4">开始使用</h2>
        <p class="text-gray-500 mb-6">注册即可获得免费额度</p>
        <NuxtLink
          to="/register"
          class="bg-gray-900 text-white px-6 py-2.5 rounded-lg text-sm font-medium hover:bg-gray-800 transition inline-block"
        >
          免费注册
        </NuxtLink>
      </div>
    </section>
  </div>
</template>

<script setup lang="ts">
definePageMeta({
  layout: 'default',
})
</script>
