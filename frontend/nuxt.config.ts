// https://nuxt.com/docs/api/configuration/nuxt-config
export default defineNuxtConfig({
  ssr: false,
  compatibilityDate: '2024-04-03',
  devtools: { enabled: true },
  modules: [
    '@pinia/nuxt',
    '@nuxtjs/tailwindcss'
  ],
  pinia: {
    autoImports: ['defineStore', 'storeToRefs'],
  },
  tailwindcss: {
    config: {
      content: [
        './components/**/*.{js,vue,ts}',
        './layouts/**/*.vue',
        './pages/**/*.vue',
        './plugins/**/*.{js,ts}',
        './app.vue',
      ],
    }
  },
  runtimeConfig: {
    public: {
      apiBaseUrl: process.env.BACKEND_API_URL || 'http://localhost:8000'
    }
  }
})