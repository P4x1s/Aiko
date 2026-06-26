<template>
  <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
    <div class="flex justify-between items-center mb-8">
      <div>
        <h1 class="text-2xl font-bold text-gray-900">API Keys</h1>
        <p class="text-gray-500">管理你的访问令牌</p>
      </div>
      <button
        @click="showCreateModal = true"
        class="bg-indigo-600 text-white px-4 py-2 rounded-lg hover:bg-indigo-700 transition"
      >
        + 创建 Key
      </button>
    </div>

    <!-- Keys List -->
    <div class="bg-white rounded-lg shadow-sm border">
      <div v-if="keys.length === 0" class="p-8 text-center text-gray-500">
        <p>还没有 API Key</p>
        <p class="text-sm mt-2">点击上方按钮创建你的第一个 Key</p>
      </div>

      <div v-else class="divide-y">
        <div
          v-for="key in keys"
          :key="key.id"
          class="p-4 flex items-center justify-between"
        >
          <div>
            <div class="font-medium">{{ key.name || 'Unnamed Key' }}</div>
            <div class="text-sm text-gray-500 font-mono">{{ key.key_prefix }}...</div>
            <div class="text-xs text-gray-400 mt-1">
              创建于 {{ new Date(key.created_at).toLocaleDateString('zh-CN') }}
            </div>
          </div>
          <div class="flex items-center space-x-2">
            <span
              :class="key.is_active ? 'bg-green-100 text-green-700' : 'bg-red-100 text-red-700'"
              class="px-2 py-1 rounded text-xs"
            >
              {{ key.is_active ? '活跃' : '已禁用' }}
            </span>
            <button
              @click="deleteKey(key.id)"
              class="text-red-500 hover:text-red-700 text-sm"
            >
              删除
            </button>
          </div>
        </div>
      </div>
    </div>

    <!-- Create Modal -->
    <div v-if="showCreateModal" class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
      <div class="bg-white rounded-lg p-6 w-full max-w-md">
        <h3 class="text-lg font-semibold mb-4">创建 API Key</h3>
        <form @submit.prevent="createKey">
          <div class="mb-4">
            <label class="block text-sm font-medium text-gray-700 mb-1">名称</label>
            <input
              v-model="newKeyName"
              type="text"
              class="w-full px-4 py-2 border rounded-lg focus:ring-2 focus:ring-indigo-500 outline-none"
              placeholder="例如：我的应用"
            />
          </div>
          <div class="flex justify-end space-x-2">
            <button
              type="button"
              @click="showCreateModal = false"
              class="px-4 py-2 text-gray-600 hover:text-gray-800"
            >
              取消
            </button>
            <button
              type="submit"
              :disabled="creating"
              class="px-4 py-2 bg-indigo-600 text-white rounded-lg hover:bg-indigo-700 disabled:opacity-50"
            >
              {{ creating ? '创建中...' : '创建' }}
            </button>
          </div>
        </form>
      </div>
    </div>

    <!-- New Key Display Modal -->
    <div v-if="newKey" class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
      <div class="bg-white rounded-lg p-6 w-full max-w-md">
        <h3 class="text-lg font-semibold mb-2">✅ Key 创建成功</h3>
        <p class="text-sm text-gray-500 mb-4">请保存此 Key，它只会显示一次：</p>
        <div class="bg-gray-100 p-3 rounded font-mono text-sm break-all">
          {{ newKey }}
        </div>
        <button
          @click="newKey = ''"
          class="w-full mt-4 px-4 py-2 bg-indigo-600 text-white rounded-lg hover:bg-indigo-700"
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

const user = useSupabaseUser()
const supabase = useSupabaseClient()

const keys = ref<any[]>([])
const showCreateModal = ref(false)
const newKeyName = ref('')
const creating = ref(false)
const newKey = ref('')

const loadKeys = async () => {
  // TODO: Fetch from API
  keys.value = []
}

const createKey = async () => {
  creating.value = true
  // TODO: Create via API
  creating.value = false
  showCreateModal.value = false
}

const deleteKey = async (id: string) => {
  if (confirm('确定要删除这个 Key 吗？')) {
    // TODO: Delete via API
  }
}

onMounted(() => {
  loadKeys()
})
</script>
