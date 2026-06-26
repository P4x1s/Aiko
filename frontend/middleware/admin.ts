export default defineNuxtRouteMiddleware(async (to) => {
  const user = useSupabaseUser()
  const supabase = useSupabaseClient()

  if (!user.value) {
    return navigateTo('/login')
  }

  // Check if user is admin
  const { data } = await supabase
    .from('profiles')
    .select('role')
    .eq('id', user.value.id)
    .single()

  if (!data || data.role !== 'admin') {
    return navigateTo('/dashboard')
  }
})
