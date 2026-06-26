export default defineNuxtConfig({
  devtools: { enabled: true },
  modules: [
    '@nuxtjs/supabase',
    '@nuxtjs/tailwindcss',
  ],
  supabase: {
    redirectOptions: {
      login: '/login',
      callback: '/confirm',
      include: undefined,
      exclude: ['/', '/register', '/forgot-password', '/reset-password'],
      cookieRedirect: false,
    }
  },
  runtimeConfig: {
    public: {
      apiBase: process.env.NUXT_PUBLIC_API_BASE || 'https://aiko-five.vercel.app',
    }
  },
  app: {
    head: {
      title: '艾柯 (Aiko) API 中转站',
      meta: [
        { charset: 'utf-8' },
        { name: 'viewport', content: 'width=device-width, initial-scale=1' },
        { name: 'description', content: '统一的 AI API 中转站，让国内开发者轻松调用多个厂商的模型' },
      ],
    }
  },
  compatibilityDate: '2024-11-01',
})
