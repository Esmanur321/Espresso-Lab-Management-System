// https://nuxt.com/docs/api/configuration/nuxt-config
export default defineNuxtConfig({
  compatibilityDate: '2024-11-01',
  devtools: { enabled: true },
  modules: [
    // WEEK 8: Pinia State Management aktif edildi
    '@pinia/nuxt'
  ],

  imports: {
    dirs: ['stores']
  },
  components: [
    { path: '~/components', pathPrefix: false }
  ],

  app: {
    head: {
      script: [
        {
          src: 'https://js.stripe.com/v3/',
          defer: true
        }
      ]
    }
  }
})
