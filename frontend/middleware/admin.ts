export default defineNuxtRouteMiddleware(async (to) => {
  const user = useSupabaseUser()
  const supabase = useSupabaseClient()

  if (!user.value) {
    return navigateTo('/login')
  }

  // 从用户元数据中读取角色
  const role = user.value.user_metadata?.role

  if (role !== 'admin') {
    return navigateTo('/dashboard')
  }
})
