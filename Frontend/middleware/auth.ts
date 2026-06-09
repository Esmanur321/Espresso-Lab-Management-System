/**
 * ============================================
 * MIDDLEWARE: auth.ts - Korumalı Rota Kontrolü
 * ============================================
 *
 * WEEK 8 - Navigation Guards
 *
 * Bu middleware şu sayfalarda çalışır:
 * - /profile (definePageMeta ile belirtilmiş)
 *
 * Kullanıcı giriş yapmamışsa /login sayfasına yönlendirir.
 */
export default defineNuxtRouteMiddleware((to, from) => {
  const authStore = useAuthStore();

  // Kullanıcı giriş yapmamışsa login sayfasına yönlendir
  if (!authStore.isAuthenticated) {
    console.log('🔒 Korumalı sayfa: Giriş gerekli →', to.path);
    return navigateTo('/login');
  }
});
