<template>
  <div>
    <!-- Hero Section -->
    <div class="relative overflow-hidden">
      <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-24">
        <div class="text-center">
          <h1 class="text-4xl font-bold text-gray-900 sm:text-5xl md:text-6xl">
            🤖 艾柯 <span class="text-indigo-600">Aiko</span>
          </h1>
          <p class="mt-3 text-xl text-gray-500 sm:mt-5">
            统一的 AI API 中转站
          </p>
          <p class="mt-2 text-lg text-gray-400">
            一个接口，调用所有 AI 模型
          </p>
          <div class="mt-8 flex justify-center gap-4">
            <NuxtLink
              to="/register"
              class="bg-indigo-600 text-white px-8 py-3 rounded-lg text-lg font-medium hover:bg-indigo-700 transition"
            >
              免费注册
            </NuxtLink>
            <a
              href="#features"
              class="bg-white text-gray-700 px-8 py-3 rounded-lg text-lg font-medium border hover:bg-gray-50 transition"
            >
              了解更多
            </a>
          </div>
        </div>
      </div>
    </div>

    <!-- Pain Points -->
    <div class="py-16 bg-white">
      <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <h2 class="text-3xl font-bold text-center text-gray-900 mb-12">
          解决国内开发者三大痛点
        </h2>
        <div class="grid md:grid-cols-3 gap-8">
          <div class="text-center p-6">
            <div class="text-4xl mb-4">💳</div>
            <h3 class="text-xl font-semibold mb-2">支付门槛</h3>
            <p class="text-gray-500">无需海外信用卡，支持支付宝、微信支付，轻松充值</p>
          </div>
          <div class="text-center p-6">
            <div class="text-4xl mb-4">⚡</div>
            <h3 class="text-xl font-semibold mb-2">网络延迟</h3>
            <p class="text-gray-500">海外服务器部署，国内直连稳定快速，告别卡顿</p>
          </div>
          <div class="text-center p-6">
            <div class="text-4xl mb-4">🔄</div>
            <h3 class="text-xl font-semibold mb-2">多平台管理</h3>
            <p class="text-gray-500">一个接口调用所有模型，统一管理，省时省力</p>
          </div>
        </div>
      </div>
    </div>

    <!-- Features -->
    <div id="features" class="py-16 bg-gray-50">
      <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <h2 class="text-3xl font-bold text-center text-gray-900 mb-12">
          支持的模型
        </h2>
        <div class="grid md:grid-cols-3 gap-6">
          <div class="bg-white p-6 rounded-lg shadow-sm border">
            <h3 class="font-semibold text-lg mb-3">🟢 OpenAI</h3>
            <ul class="text-gray-600 space-y-1">
              <li>GPT-4o</li>
              <li>GPT-4 Turbo</li>
              <li>GPT-4</li>
              <li>GPT-3.5 Turbo</li>
            </ul>
          </div>
          <div class="bg-white p-6 rounded-lg shadow-sm border">
            <h3 class="font-semibold text-lg mb-3">🟣 Anthropic</h3>
            <ul class="text-gray-600 space-y-1">
              <li>Claude 3.5 Sonnet</li>
              <li>Claude 3 Opus</li>
              <li>Claude 3 Haiku</li>
            </ul>
          </div>
          <div class="bg-white p-6 rounded-lg shadow-sm border">
            <h3 class="font-semibold text-lg mb-3">🔵 Google</h3>
            <ul class="text-gray-600 space-y-1">
              <li>Gemini 1.5 Pro</li>
              <li>Gemini 1.5 Flash</li>
              <li>Gemini Pro</li>
            </ul>
          </div>
        </div>
      </div>
    </div>

    <!-- Code Example -->
    <div class="py-16 bg-white">
      <div class="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8">
        <h2 class="text-3xl font-bold text-center text-gray-900 mb-8">
          简单易用
        </h2>
        <p class="text-center text-gray-500 mb-8">
          OpenAI 兼容格式，现有代码无需修改
        </p>
        <div class="bg-gray-900 rounded-lg p-6 overflow-x-auto">
          <pre class="text-green-400 text-sm"><code>curl https://aiko-five.vercel.app/v1/chat/completions \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer your-api-key" \
  -d '{
    "model": "gpt-4",
    "messages": [
      {"role": "user", "content": "你好!"}
    ]
  }'</code></pre>
        </div>
      </div>
    </div>

    <!-- CTA -->
    <div class="py-16 bg-indigo-600">
      <div class="max-w-4xl mx-auto text-center px-4">
        <h2 class="text-3xl font-bold text-white mb-4">
          立即开始使用
        </h2>
        <p class="text-indigo-100 mb-8">
          注册即可获得免费额度，快速体验
        </p>
        <NuxtLink
          to="/register"
          class="bg-white text-indigo-600 px-8 py-3 rounded-lg text-lg font-medium hover:bg-indigo-50 transition inline-block"
        >
          免费注册
        </NuxtLink>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
definePageMeta({
  layout: 'default',
})
</script>
