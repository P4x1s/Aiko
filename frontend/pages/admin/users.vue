<template>
  <div class="max-w-6xl mx-auto px-4 sm:px-6 py-8">
    <div class="flex justify-between items-center mb-8">
      <div>
        <h1 class="text-xl font-semibold text-gray-900">用户管理</h1>
        <p class="text-sm text-gray-500 mt-1">共 {{ users.length }} 个用户</p>
      </div>
      <NuxtLink to="/admin" class="text-sm text-gray-500 hover:text-gray-900">
        ← 返回
      </NuxtLink>
    </div>

    <!-- Users Table -->
    <div class="border rounded-xl overflow-hidden">
      <table class="w-full">
        <thead class="bg-gray-50">
          <tr>
            <th class="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase">邮箱</th>
            <th class="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase">角色</th>
            <th class="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase">余额</th>
            <th class="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase">注册时间</th>
            <th class="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase">操作</th>
          </tr>
        </thead>
        <tbody class="divide-y">
          <tr v-for="u in users" :key="u.id" class="hover:bg-gray-50">
            <td class="px-4 py-3 text-sm">{{ u.email }}</td>
            <td class="px-4 py-3">
              <span
                :class="u.role === 'admin' ? 'bg-gray-900 text-white' : 'bg-gray-100 text-gray-600'"
                class="px-2 py-0.5 rounded text-xs"
              >
                {{ u.role }}
              </span>
            </td>
            <td class="px-4 py-3 text-sm">¥{{ parseFloat(u.balance || 0).toFixed(2) }}</td>
            <td class="px-4 py-3 text-sm text-gray-500">
              {{ new Date(u.created_at).toLocaleDateString('zh-CN') }}
            </td>
            <td class="px-4 py-3">
              <button
                @click="editUser(u)"
                class="text-xs text-gray-500 hover:text-gray-900 mr-2"
              >
                编辑
              </button>
            </td>
          </tr>
        </tbody>
      </table>

      <div v-if="users.length === 0" class="p-12 text-center text-gray-400">
        暂无用户数据
      </div>
    </div>

    <!-- Edit Modal -->
    <div v-if="editingUser" class="fixed inset-0 bg-black/50 flex items-center justify-center z-50">
      <div class="bg-white rounded-xl p-6 w-full max-w-sm mx-4">
        <h3 class="font-semibold mb-4">编辑用户</h3>
        <div class="space-y-4">
          <div>
            <label class="block text-sm text-gray-600 mb-1.5">邮箱</label>
            <div class="text-sm">{{ editingUser.email }}</div>
          </div>
          <div>
            <label class="block text-sm text-gray-600 mb-1.5">角色</label>
            <select v-model="editForm.role" class="w-full px-3 py-2 border rounded-lg text-sm">
              <option value="user">user</option>
              <option value="admin">admin</option>
            </select>
          </div>
          <div>
            <label class="block text-sm text-gray-600 mb-1.5">余额</label>
            <input
              v-model="editForm.balance"
              type="number"
              step="0.01"
              class="w-full px-3 py-2 border rounded-lg text-sm"
            />
          </div>
        </div>
        <div class="flex justify-end gap-2 mt-6">
          <button
            @click="editingUser = null"
            class="px-4 py-2 text-sm text-gray-600 hover:text-gray-900"
          >
            取消
          </button>
          <button
            @click="saveUser"
            class="px-4 py-2 bg-gray-900 text-white text-sm rounded-lg hover:bg-gray-800"
          >
            保存
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
definePageMeta({
  middleware: 'admin',
})

const users = ref<any[]>([])
const editingUser = ref<any>(null)
const editForm = ref({ role: '', balance: 0 })

const editUser = (user: any) => {
  editingUser.value = user
  editForm.value = { role: user.role, balance: parseFloat(user.balance || 0) }
}

const saveUser = async () => {
  // TODO: Update via API
  editingUser.value = null
}

onMounted(async () => {
  // TODO: Fetch from API
})
</script>
