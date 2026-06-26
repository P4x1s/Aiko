<template>
  <div class="max-w-4xl mx-auto px-4 sm:px-6 py-8">
    <div class="mb-8">
      <h1 class="text-2xl font-semibold text-gray-900">接入指南</h1>
      <p class="text-sm text-gray-500 mt-1">快速接入艾柯 Aiko API</p>
    </div>

    <!-- Quick Start -->
    <section class="mb-12">
      <h2 class="text-lg font-semibold mb-4">快速开始</h2>
      <div class="space-y-4">
        <div class="border rounded-xl p-4">
          <div class="flex items-center gap-3 mb-2">
            <span class="w-6 h-6 bg-gray-900 text-white rounded-full flex items-center justify-center text-sm">1</span>
            <span class="font-medium">获取 API Key</span>
          </div>
          <p class="text-sm text-gray-500 ml-9">在<a href="/dashboard/keys" class="text-gray-900 hover:underline">控制台</a>创建 API Key</p>
        </div>
        <div class="border rounded-xl p-4">
          <div class="flex items-center gap-3 mb-2">
            <span class="w-6 h-6 bg-gray-900 text-white rounded-full flex items-center justify-center text-sm">2</span>
            <span class="font-medium">替换 API 地址</span>
          </div>
          <p class="text-sm text-gray-500 ml-9">将 OpenAI API 地址替换为艾柯 Aiko 地址</p>
        </div>
        <div class="border rounded-xl p-4">
          <div class="flex items-center gap-3 mb-2">
            <span class="w-6 h-6 bg-gray-900 text-white rounded-full flex items-center justify-center text-sm">3</span>
            <span class="font-medium">开始使用</span>
          </div>
          <p class="text-sm text-gray-500 ml-9">使用标准 OpenAI SDK 调用即可</p>
        </div>
      </div>
    </section>

    <!-- API Base URL -->
    <section class="mb-12">
      <h2 class="text-lg font-semibold mb-4">API 地址</h2>
      <div class="bg-gray-100 rounded-lg p-4 font-mono text-sm">
        {{ apiBase }}
      </div>
    </section>

    <!-- Supported Models -->
    <section class="mb-12">
      <h2 class="text-lg font-semibold mb-4">支持的模型</h2>
      <div class="grid md:grid-cols-2 gap-4">
        <div class="border rounded-lg p-4">
          <div class="font-medium mb-2">OpenAI</div>
          <div class="text-sm text-gray-500 space-y-1">
            <div>gpt-4o / gpt-4 / gpt-3.5-turbo</div>
          </div>
        </div>
        <div class="border rounded-lg p-4">
          <div class="font-medium mb-2">Anthropic</div>
          <div class="text-sm text-gray-500 space-y-1">
            <div>claude-3-sonnet / claude-3-opus / claude-3-haiku</div>
          </div>
        </div>
        <div class="border rounded-lg p-4">
          <div class="font-medium mb-2">Google</div>
          <div class="text-sm text-gray-500 space-y-1">
            <div>gemini-1.5-pro / gemini-1.5-flash</div>
          </div>
        </div>
        <div class="border rounded-lg p-4">
          <div class="font-medium mb-2">国内厂商</div>
          <div class="text-sm text-gray-500 space-y-1">
            <div>qwen-max / ernie-4.0 / glm-4 / deepseek-chat</div>
          </div>
        </div>
      </div>
    </section>

    <!-- Python Example -->
    <section class="mb-12">
      <h2 class="text-lg font-semibold mb-4">Python 示例</h2>
      <div class="bg-gray-900 rounded-lg p-4 overflow-x-auto">
        <pre class="text-green-400 text-sm"><code>from openai import OpenAI

client = OpenAI(
    api_key="your-api-key",
    base_url="{{ apiBase }}"
)

response = client.chat.completions.create(
    model="gpt-4",
    messages=[
        {"role": "user", "content": "你好！"}
    ]
)

print(response.choices[0].message.content)</code></pre>
      </div>
    </section>

    <!-- JavaScript Example -->
    <section class="mb-12">
      <h2 class="text-lg font-semibold mb-4">JavaScript 示例</h2>
      <div class="bg-gray-900 rounded-lg p-4 overflow-x-auto">
        <pre class="text-green-400 text-sm"><code>import OpenAI from 'openai'

const client = new OpenAI({
  apiKey: 'your-api-key',
  baseURL: '{{ apiBase }}'
})

const response = await client.chat.completions.create({
  model: 'gpt-4',
  messages: [
    { role: 'user', content: '你好！' }
  ]
})

console.log(response.choices[0].message.content)</code></pre>
      </div>
    </section>

    <!-- Curl Example -->
    <section class="mb-12">
      <h2 class="text-lg font-semibold mb-4">cURL 示例</h2>
      <div class="bg-gray-900 rounded-lg p-4 overflow-x-auto">
        <pre class="text-green-400 text-sm"><code>curl {{ apiBase }}/v1/chat/completions \
  -H "Authorization: Bearer your-api-key" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "gpt-4",
    "messages": [
      {"role": "user", "content": "你好！"}
    ]
  }'</code></pre>
      </div>
    </section>

    <!-- Streaming Example -->
    <section class="mb-12">
      <h2 class="text-lg font-semibold mb-4">流式响应</h2>
      <div class="bg-gray-900 rounded-lg p-4 overflow-x-auto">
        <pre class="text-green-400 text-sm"><code>curl {{ apiBase }}/v1/chat/completions \
  -H "Authorization: Bearer your-api-key" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "gpt-4",
    "stream": true,
    "messages": [
      {"role": "user", "content": "你好！"}
    ]
  }'</code></pre>
      </div>
    </section>

    <!-- Pricing -->
    <section class="mb-12">
      <h2 class="text-lg font-semibold mb-4">价格参考</h2>
      <div class="overflow-x-auto">
        <table class="w-full border rounded-lg overflow-hidden">
          <thead class="bg-gray-50">
            <tr>
              <th class="px-4 py-3 text-left text-sm font-medium text-gray-500">模型</th>
              <th class="px-4 py-3 text-left text-sm font-medium text-gray-500">输入 (元/千tokens)</th>
              <th class="px-4 py-3 text-left text-sm font-medium text-gray-500">输出 (元/千tokens)</th>
            </tr>
          </thead>
          <tbody class="divide-y">
            <tr><td class="px-4 py-3 text-sm">GPT-4o</td><td class="px-4 py-3 text-sm">¥0.035</td><td class="px-4 py-3 text-sm">¥0.105</td></tr>
            <tr><td class="px-4 py-3 text-sm">GPT-4</td><td class="px-4 py-3 text-sm">¥0.21</td><td class="px-4 py-3 text-sm">¥0.42</td></tr>
            <tr><td class="px-4 py-3 text-sm">Claude 3.5 Sonnet</td><td class="px-4 py-3 text-sm">¥0.021</td><td class="px-4 py-3 text-sm">¥0.105</td></tr>
            <tr><td class="px-4 py-3 text-sm">Gemini 1.5 Pro</td><td class="px-4 py-3 text-sm">¥0.035</td><td class="px-4 py-3 text-sm">¥0.105</td></tr>
            <tr><td class="px-4 py-3 text-sm">Qwen Max</td><td class="px-4 py-3 text-sm">¥0.02</td><td class="px-4 py-3 text-sm">¥0.06</td></tr>
            <tr><td class="px-4 py-3 text-sm">DeepSeek Chat</td><td class="px-4 py-3 text-sm">¥0.002</td><td class="px-4 py-3 text-sm">¥0.008</td></tr>
          </tbody>
        </table>
      </div>
    </section>

    <!-- FAQ -->
    <section class="mb-12">
      <h2 class="text-lg font-semibold mb-4">常见问题</h2>
      <div class="space-y-4">
        <div class="border rounded-lg p-4">
          <div class="font-medium mb-2">如何获取 API Key？</div>
          <p class="text-sm text-gray-500">注册账号后，在<a href="/dashboard/keys" class="text-gray-900 hover:underline">控制台 → API Keys</a>中创建。</p>
        </div>
        <div class="border rounded-lg p-4">
          <div class="font-medium mb-2">支持哪些模型？</div>
          <p class="text-sm text-gray-500">支持 OpenAI、Anthropic、Google、百度、阿里、智谱、DeepSeek 等厂商的模型。</p>
        </div>
        <div class="border rounded-lg p-4">
          <div class="font-medium mb-2">如何充值？</div>
          <p class="text-sm text-gray-500">在<a href="/dashboard/billing" class="text-gray-900 hover:underline">控制台 → 余额</a>中充值，支持支付宝、微信支付。</p>
        </div>
      </div>
    </section>
  </div>
</template>

<script setup lang="ts">
definePageMeta({
  layout: 'default',
})

const config = useRuntimeConfig()
const apiBase = config.public.apiBase
</script>
