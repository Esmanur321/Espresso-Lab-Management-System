import { defineStore } from 'pinia';
import { useNuxtApp } from '#app';
import { useCartStore } from './cart';
import { useI18n } from '~/composables/useI18n';

export const usePaymentStore = defineStore('payment', {
  state: () => ({
    isLoading: false,
    error: null as string | null,
    paymentStatus: 'idle' as 'idle' | 'processing' | 'success' | 'failed',
  }),
  
  actions: {
    async processOnlinePayment(orderId: number, amount: number, source: string) {
      const { $api } = useNuxtApp() as any;
      const cartStore = useCartStore();
      const { t } = useI18n();
      const API_BASE = 'http://localhost:8000';

      this.isLoading = true;
      this.paymentStatus = 'processing';
      this.error = null;

      try {
        // Step 1: Send the payment request to the backend
        await $api(`${API_BASE}/payments/online`, {
          method: 'POST',
          body: {
            order_id: orderId,
            amount: amount,
            currency: 'try',
            source: source
          }
        });

        // Step 2: Since processing is asynchronous, poll the order status until confirmed or cancelled
        let attempts = 0;
        const maxAttempts = 30; // Increased to 30 attempts to support longer background processing times
        const delay = (ms: number) => new Promise(res => setTimeout(res, ms));

        while (attempts < maxAttempts) {
          attempts++;
          await delay(2000); // Wait 2s between polls (increased from 1.5s)

          console.log(`[Payment Store] Polling order ${orderId} status (Attempt ${attempts}/${maxAttempts})...`);
          const order = await $api(`${API_BASE}/orders/${orderId}`);
          
          if (order.payment_status === 'approved') {
            this.paymentStatus = 'success';
            cartStore.clearCart();
            this.isLoading = false;
            return order;
          } else if (order.payment_status === 'rejected') {
            this.paymentStatus = 'failed';
            this.error = t('checkout.error_card_declined');
            this.isLoading = false;
            throw new Error(this.error);
          }
        }

        // If we timeout
        this.paymentStatus = 'failed';
        this.error = t('checkout.error_timeout');
        this.isLoading = false;
        throw new Error(this.error);

      } catch (err: any) {
        this.paymentStatus = 'failed';
        const msg = err.data?.detail || err.message || t('checkout.error_generic');
        this.error = msg;
        this.isLoading = false;
        throw err;
      }
    },

    async processOfflinePayment(orderId: number) {
      const { $api } = useNuxtApp() as any;
      const cartStore = useCartStore();
      const { t } = useI18n();
      const API_BASE = 'http://localhost:8000';

      this.isLoading = true;
      this.error = null;

      try {
        await $api(`${API_BASE}/payments/offline`, {
          method: 'POST',
          params: { order_id: orderId }
        });
        
        cartStore.clearCart();
        this.isLoading = false;
      } catch (err: any) {
        const msg = err.data?.detail || err.message || t('checkout.error_offline_save_failed');
        this.error = msg;
        this.isLoading = false;
        throw err;
      }
    }
  }
});
