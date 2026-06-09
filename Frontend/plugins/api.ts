export default defineNuxtPlugin((nuxtApp) => {
  const api = $fetch.create({
    onRequest({ request, options }) {
      console.log('[API Request Interceptor] Calling API:', request);
      options.headers = options.headers || {};
      
      let bearer: string | undefined;
      if (process.client) {
        const jwt = localStorage.getItem('auth_token');
        if (jwt && jwt.split('.').length === 3) {
          bearer = jwt;
        }
      }
      if (!bearer) {
        try {
          const { useAuthStore } = require('~/stores/auth');
          const authStore = useAuthStore();
          if (authStore.isAuthenticated && authStore.user?.uid) {
            bearer = authStore.user.uid;
          }
        } catch {
          /* ignore */
        }
      }
      (options.headers as any).Authorization = bearer
        ? `Bearer ${bearer}`
        : 'Bearer fake-token-for-syllabus';
    },
    onResponse({ request, response, options }) {
      console.log('[API Response Interceptor] Response from API:', request, response.status);
    },
    onResponseError({ request, response, options }) {
      console.error('[API Error Interceptor] Error from API:', request, response.status);
      
      if (process.client) {
        const { showToast } = useToast();
        
        if (response.status === 402) {
          // Stripe Payment Required / Decline
          const errorMsg = response._data?.detail || 'Kartınız reddedildi veya ödeme başarısız oldu. Lütfen kart bilgilerinizi kontrol edin.';
          showToast(errorMsg, 'error');
        } else if (response.status === 400) {
          // Validation / Bad Request
          const errorMsg = response._data?.detail || 'Geçersiz istek parametreleri gönderildi.';
          showToast(errorMsg, 'warning');
        } else if (response.status === 403) {
          // Forbidden
          showToast('Bu işlem için yetkiniz bulunmamaktadır.', 'error');
        } else if (response.status >= 500) {
          // Internal Server Error
          showToast('Sunucu kaynaklı bir hata oluştu. Lütfen daha sonra tekrar deneyin.', 'error');
        }
      }
    }
  });

  return {
    provide: {
      api
    }
  };
});
