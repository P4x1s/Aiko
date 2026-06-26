export default defineNuxtRouteMiddleware(async (to) => {
  const user = useSupabaseUser()
  const supabase = useSupabaseClient()

  // 公开页面不需要检查
  const publicPages = ['/', '/login', '/register', '/forgot-password', '/reset-password', '/confirm']
  if (publicPages.includes(to.path)) {
    return
  }

  // 如果没有用户，跳过
  if (!user.value) {
    return
  }

  // 检查用户是否还在数据库中
  const { data } = await supabase
    .from('profiles')
    .select('id')
    .eq('id', user.value.id)
    .single()

  // 如果用户不存在，登出并跳转到登录页
  if (!data) {
    await supabase.auth.signOut()
    return navigateTo('/login')
  }
})
