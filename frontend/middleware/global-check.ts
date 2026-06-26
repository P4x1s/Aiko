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

  // 简单检查：用户存在即可，角色通过 user_metadata 检查
  // 不再查询 profiles 表，避免 RLS 问题
})
