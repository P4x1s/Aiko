<template>
  <div class="max-w-6xl mx-auto px-4 sm:px-6 py-8">
    <div class="mb-8">
      <h1 class="text-xl font-semibold text-gray-900">调试信息</h1>
      <p class="text-sm text-gray-500 mt-1">检查用户权限状态</p>
    </div>

    <div class="border rounded-xl p-6 space-y-4">
      <div>
        <div class="text-sm text-gray-500">用户 ID</div>
        <div class="font-mono text-sm">{{ user?.id || '未登录' }}</div>
      </div>
      <div>
        <div class="text-sm text-gray-500">邮箱</div>
        <div class="font-mono text-sm">{{ user?.email || '无' }}</div>
      </div>
      <div>
        <div class="text-sm text-gray-500">角色 (role)</div>
        <div class="font-mono text-sm">{{ role || '未知' }}</div>
      </div>
      <div>
        <div class="text-sm text-gray-500">是否管理员</div>
        <div class="font-mono text-sm">{{ isAdmin ? '是' : '否' }}</div>
      </div>
      <div v-if="error">
        <div class="text-sm text-red-500">错误</div>
        <div class="font-mono text-sm text-red-600">{{ error }}</div>
      </div>
      <div v-if="rawData">
        <div class="text-sm text-gray-500">原始数据</div>
        <pre class="font-mono text-xs bg-gray-100 p-2 rounded overflow-auto">{{ JSON.stringify(rawData, null, 2) }}</pre>
      </div>
    </div>

    <div class="mt-4">
      <button
        @click="refresh"
        class="bg-gray-900 text-white px-4 py-2 rounded-lg text-sm hover:bg-gray-800"
      >
        刷新数据
      </button>
    </div>
  </div>
</template>

<script setup lang="ts">
const user = useSupabaseUser()
const supabase = useSupabaseClient()

const role = ref('')
const isAdmin = ref(false)
const error = ref('')
const rawData = ref<any>(null)

const refresh = async () => {
  if (!user.value) {
    error.value = '未登录'
    return
  }

  try {
    const { data, error: supaError } = await supabase
      .from('profiles')
      .select('*')
      .eq('id', user.value.id)
      .maybeSingle()

    if (supaError) {
      error.value = supaError.message
      return
    }

    rawData.value = data
    role.value = data?.role || '无'
    isAdmin.value = data?.role === 'admin'
    error.value = ''
  } catch (e: any) {
    error.value = e.message
  }
}

onMounted(() => {
  refresh()
})
</script>
