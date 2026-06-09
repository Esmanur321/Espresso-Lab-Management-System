/**
 * On app load, refresh user role from backend so admin flag stays accurate.
 */
export default defineNuxtPlugin(async () => {
  const authStore = useAuthStore();
  if (authStore.isLoggedIn) {
    await authStore.syncProfileFromServer();
  }
});
