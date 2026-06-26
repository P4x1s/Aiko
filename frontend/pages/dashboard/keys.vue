<template>
  <div class="max-w-6xl mx-auto px-4 sm:px-6 py-8">
    <div class="flex justify-between items-center mb-8">
      <div>
        <h1 class="text-xl font-semibold text-gray-900">API Keys</h1>
        <p class="text-sm text-gray-500 mt-1">管理你的访问令牌</p>
      </div>
      <button
        @click="showCreateModal = true"
        class="bg-gray-900 text-white px-4 py-2 rounded-lg text-sm hover:bg-gray-800 transition"
      >
        + 创建
      </button>
    </div>

    <!-- Keys List -->
    <div class="border rounded-xl overflow-hidden">
      <div v-if="keys.length === 0" class="p-12 text-center text-gray-400">
        <p>还没有 API Key</p>
        <p class="text-sm mt-1">点击上方按钮创建</p>
      </div>

      <div v-else class="divide-y">
        <div
          v-for="key in keys"
          :key="key.id"
          class="p-4 flex items-center justify-between hover:bg-gray-50 transition"
        >
          <div>
            <div class="font-medium text-sm">{{ key.name || 'Unnamed' }}</div>
            <div class="text-xs text-gray-400 font-mono mt-1">{{ key.key_prefix }}...</div>
          </div>
          <div class="flex items-center gap-3">
            <span
              :class="key.is_active ? 'bg-green-50 text-green-600' : 'bg-gray-100 text-gray-500'"
              class="px-2 py-0.5 rounded text-xs"
            >
              {{ key.is_active ? '活跃' : '禁用' }}
            </span>
            <button
              @click="deleteKey(key.id)"
              class="text-xs text-gray-400 hover:text-red-500 transition"
            >
              删除
            </button>
          </div>
        </div>
      </div>
    </div>

    <!-- Create Modal -->
    <div v-if="showCreateModal" class="fixed inset-0 bg-black/50 flex items-center justify-center z-50">
      <div class="bg-white rounded-xl p-6 w-full max-w-sm mx-4">
        <h3 class="font-semibold mb-4">创建 API Key</h3>
        <form @submit.prevent="createKey">
          <div class="mb-4">
            <label class="block text-sm text-gray-600 mb-1.5">名称</label>
            <input
              v-model="newKeyName"
              type="text"
              class="w-full px-3 py-2 border rounded-lg text-sm focus:ring-2 focus:ring-gray-900 outline-none"
              placeholder="例如：我的应用"
            />
          </div>
          <div class="flex justify-end gap-2">
            <button
              type="button"
              @click="showCreateModal = false"
              class="px-4 py-2 text-sm text-gray-600 hover:text-gray-900"
            >
              取消
            </button>
            <button
              type="submit"
              :disabled="creating"
              class="px-4 py-2 bg-gray-900 text-white text-sm rounded-lg hover:bg-gray-800 disabled:opacity-50"
            >
              {{ creating ? '创建中...' : '创建' }}
            </button>
          </div>
        </form>
      </div>
    </div>

    <!-- New Key Display -->
    <div v-if="newKey" class="fixed inset-0 bg-black/50 flex items-center justify-center z-50">
      <div class="bg-white rounded-xl p-6 w-full max-w-sm mx-4">
        <h3 class="font-semibold mb-2">✅ 创建成功</h3>
        <p class="text-sm text-gray-500 mb-4">请保存此 Key，只会显示一次：</p>
        <div class="bg-gray-100 p-3 rounded-lg font-mono text-sm break-all">
          {{ newKey }}
        </div>
        <button
          @click="newKey = ''"
          class="w-full mt-4 px-4 py-2 bg-gray-900 text-white text-sm rounded-lg hover:bg-gray-800"
        >
          我已保存
        </button>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
definePageMeta({
  middleware: 'auth',
})

const keys = ref<any[]>([])
const showCreateModal = ref(false)
const newKeyName = ref('')
const creating = ref(false)
const newKey = ref('')

const loadKeys = async () => {
  keys.value = []
}

const createKey = async () => {
  creating.value = true
  creating.value = false
  showCreateModal.value = false
}

const deleteKey = async (id: string) => {
  if (confirm('确定删除？')) {
    // TODO
  }
}

onMounted(() => {
  loadKeys()
})
</script>
