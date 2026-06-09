/**
 * Admin-only routes (e.g. /admin).
 * Requires login + role admin from backend-synced profile.
 */
export default defineNuxtRouteMiddleware(async () => {
  const authStore = useAuthStore();

  if (!authStore.isAuthenticated) {
    return navigateTo('/login?redirect=/admin');
  }

  await authStore.syncProfileFromServer();

  if (!authStore.isAdmin) {
    return navigateTo('/profile');
  }
});
