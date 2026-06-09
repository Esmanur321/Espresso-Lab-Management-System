<script setup lang="ts">
import { ref, computed } from 'vue';
import { useAuthStore } from '~/stores/auth';
import { useCartStore } from '~/stores/cart';
import { usePaymentStore } from '~/stores/payment';
import { useRouter } from 'vue-router';
import { useNuxtApp } from '#app';
import { useToast } from '~/composables/useToast';

definePageMeta({
  middleware: 'auth'
});

const store = useAuthStore();
const cartStore = useCartStore();
const paymentStore = usePaymentStore();
const router = useRouter();
const { $t, $api } = useNuxtApp() as any;
const { showToast } = useToast();

const API_BASE = 'http://localhost:8000';
const paymentMethod = ref<'online' | 'offline'>('online');

// Stripe Elements Refs & Focus States
const stripe = ref<any>(null);
const cardNumberElement = ref<any>(null);
const cardExpiryElement = ref<any>(null);
const cardCvcElement = ref<any>(null);

const isCardNumberFocused = ref(false);
const isCardExpiryFocused = ref(false);
const isCardCvcFocused = ref(false);

onMounted(() => {
  if (process.client) {
    const initStripe = () => {
      if ((window as any).Stripe) {
        const stripePublicKey = import.meta.env.VITE_STRIPE_PUBLIC_KEY || 'pk_test_51TYZu1ASBjAQSVkar2Embscbc64R57Q3bZWDFx4ZwijQBHbS2I9D9bmAAVkXzNqwSeNjj9MJdy7brUUANnc6laGz00us2UN76y';
        stripe.value = (window as any).Stripe(stripePublicKey);
        const elements = stripe.value.elements();
        
        const baseStyle = {
          base: {
            fontSize: '16px',
            color: '#333333',
            fontFamily: '"Outfit", sans-serif',
            '::placeholder': {
              color: '#aab7c4'
            }
          },
          invalid: {
            color: '#fa755a',
            iconColor: '#fa755a'
          }
        };

        // Create Split Elements
        cardNumberElement.value = elements.create('cardNumber', { style: baseStyle });
        cardExpiryElement.value = elements.create('cardExpiry', { style: baseStyle });
        cardCvcElement.value = elements.create('cardCvc', { style: baseStyle });

        // Mount Elements
        cardNumberElement.value.mount('#card-number-element');
        cardExpiryElement.value.mount('#card-expiry-element');
        cardCvcElement.value.mount('#card-cvc-element');

        // Track Focus State for custom focus styles
        cardNumberElement.value.on('focus', () => { isCardNumberFocused.value = true; });
        cardNumberElement.value.on('blur', () => { isCardNumberFocused.value = false; });
        cardExpiryElement.value.on('focus', () => { isCardExpiryFocused.value = true; });
        cardExpiryElement.value.on('blur', () => { isCardExpiryFocused.value = false; });
        cardCvcElement.value.on('focus', () => { isCardCvcFocused.value = true; });
        cardCvcElement.value.on('blur', () => { isCardCvcFocused.value = false; });

        console.log('[Stripe Elements] Split elements mounted and bound successfully.');
      } else {
        setTimeout(initStripe, 100);
      }
    };
    initStripe();
  }
});

const isLoading = computed(() => paymentStore.isLoading);
const isOnlinePayment = computed(() => paymentMethod.value === 'online');

const subtotal = computed(() => cartStore.subtotal);
const discountAmount = computed(() => Math.round(subtotal.value * 0.10 * 100) / 100);
const finalTotal = computed(() => Math.round((subtotal.value - discountAmount.value) * 100) / 100);

const buildOrderItems = () =>
  cartStore.items.map(item => ({
    product_id: typeof item.id === 'string' ? parseInt(item.id) : item.id,
    quantity: item.quantity,
    unit_price: item.price
  }));

const createOrder = async (method: 'online' | 'offline') => {
  if (!store.user) {
    throw new Error($t('checkout.error_not_logged_in') || 'Giriş yapmanız gerekiyor.');
  }

  return $api(`${API_BASE}/orders/`, {
    method: 'POST',
    body: {
      user_id: parseInt(store.user.uid || '0'),
      items: buildOrderItems(),
      payment_method: method
    }
  });
};

const handleCompleteOrder = async () => {
  if (paymentMethod.value === 'online') {
    if (!stripe.value || !cardNumberElement.value) {
      await showToast($t('checkout.error_stripe_load_failed') || 'Stripe ödeme sistemi yüklenemedi. Lütfen sayfayı yenileyin.', 'warning');
      return;
    }
  }

  paymentStore.isLoading = true;

  try {
    const newOrder = await createOrder(paymentMethod.value);

    if (paymentMethod.value === 'offline') {
      await paymentStore.processOfflinePayment(newOrder.id);
      await showToast(
        $t('checkout.success_offline') || 'Siparişiniz alındı. Havale/EFT onayı sonrası işleme alınacaktır.',
        'success'
      );
      router.push('/profile');
      return;
    }

    if (!stripe.value || !cardNumberElement.value) {
      throw new Error($t('checkout.error_stripe_load_failed') || 'Stripe ödeme sistemi yüklenemedi.');
    }

    console.log('[Stripe Elements] Creating PaymentMethod...');
    const { paymentMethod: pm, error } = await stripe.value.createPaymentMethod({
      type: 'card',
      card: cardNumberElement.value
    });

    if (error) {
      throw new Error(error.message || $t('checkout.error_card_validation_failed') || 'Kart bilgileri doğrulanamadı.');
    }

    if (!pm) {
      throw new Error($t('checkout.error_payment_method_failed') || 'Ödeme yöntemi oluşturulamadı.');
    }

    console.log('[Stripe Elements] PaymentMethod created successfully:', pm.id);

    const amountInCents = Math.round(finalTotal.value * 100);

    // Call the Pinia store action which triggers payment and polls for DB confirmation
    await paymentStore.processOnlinePayment(newOrder.id, amountInCents, pm.id);

    await showToast($t('checkout.success') || 'Ödeme başarılı!', 'success');
    router.push('/profile');
  } catch (error: any) {
    console.error('Payment Error:', error);
    const prefix =
      paymentMethod.value === 'offline'
        ? ($t('checkout.error_offline_failed') || 'Çevrimdışı ödeme kaydı başarısız: ')
        : ($t('checkout.error_payment_failed') || 'Ödeme reddedildi: ');
    // Show descriptive error message in toast
    await showToast(prefix + (error.message || $t('checkout.error_unknown') || 'Bilinmeyen hata.'), 'error');
  } finally {
    paymentStore.isLoading = false;
  }
};
</script>

<template>
  <main class="page-content">
    <div class="content-container">
      <h1 class="page-title">{{ $t('checkout.title') }}</h1>
      <p class="desc">{{ $t('checkout.subtitle') }}</p>

      <div v-if="cartStore.items.length > 0" class="checkout-grid">
        <div class="summary-section">
          <h2>{{ $t('checkout.order_summary') }}</h2>
          <div class="summary-card">
            <ul class="summary-list">
              <li v-for="item in cartStore.items" :key="item.id" class="summary-item">
                <span class="item-name">{{ $t(item.name) }} <b>x{{ item.quantity }}</b></span>
                <span class="item-price">₺{{ (item.price * item.quantity).toFixed(2) }}</span>
              </li>
            </ul>
            <div class="summary-details">
              <div class="summary-detail-row">
                <span>{{ $t('checkout.subtotal') || 'Ara Toplam' }}</span>
                <span>₺{{ subtotal.toFixed(2) }}</span>
              </div>
              <div class="summary-detail-row discount">
                <span>{{ $t('checkout.discount') || 'İndirim (%10)' }}</span>
                <span>-₺{{ discountAmount.toFixed(2) }}</span>
              </div>
            </div>
            <div class="summary-total">
              <span>{{ $t('checkout.total') }}</span>
              <span class="total-price">₺{{ finalTotal.toFixed(2) }}</span>
            </div>
          </div>
        </div>

        <div class="payment-section">
          <div class="payment-card">
            <h3 class="section-heading">{{ $t('checkout.payment_method') }}</h3>
            <div class="payment-method-options">
              <label class="method-option" :class="{ active: paymentMethod === 'online' }">
                <input type="radio" value="online" v-model="paymentMethod" />
                <span class="method-icon">💳</span>
                <span class="method-label">{{ $t('checkout.payment_online') }}</span>
              </label>
              <label class="method-option" :class="{ active: paymentMethod === 'offline' }">
                <input type="radio" value="offline" v-model="paymentMethod" />
                <span class="method-icon">🏦</span>
                <span class="method-label">{{ $t('checkout.payment_offline') }}</span>
              </label>
            </div>

            <p v-if="!isOnlinePayment" class="offline-note">
              {{ $t('checkout.offline_note') }}
            </p>

            <template v-if="isOnlinePayment">
              <div class="payment-header">
                <h3>{{ $t('checkout.payment_info') }}</h3>
                <div class="card-icons">
                  <svg width="32" height="20" viewBox="0 0 32 20" fill="none"><rect width="32" height="20" rx="4" fill="#1434CB"/><circle cx="11" cy="10" r="6" fill="#EA001B"/><circle cx="21" cy="10" r="6" fill="#FFA200" fill-opacity="0.8"/></svg>
                </div>
              </div>

              <div class="cc-input-group">
                <label>{{ $t('checkout.card_number') }}</label>
                <div class="cc-input-wrapper stripe-element-container" :class="{ focused: isCardNumberFocused }">
                  <svg class="cc-icon" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><rect x="1" y="4" width="22" height="16" rx="2" ry="2"></rect><line x1="1" y1="10" x2="23" y2="10"></line></svg>
                  <div id="card-number-element" class="stripe-field"></div>
                </div>
              </div>

              <div class="cc-row">
                <div class="cc-input-group flex-2">
                  <label>{{ $t('checkout.expiry_date') }}</label>
                  <div class="stripe-element-container" :class="{ focused: isCardExpiryFocused }">
                    <div id="card-expiry-element" class="stripe-field"></div>
                  </div>
                </div>
                <div class="cc-input-group flex-1">
                  <label>{{ $t('checkout.cvc') }}</label>
                  <div class="stripe-element-container" :class="{ focused: isCardCvcFocused }">
                    <div id="card-cvc-element" class="stripe-field"></div>
                  </div>
                </div>
              </div>


            </template>

            <button class="pay-btn" @click="handleCompleteOrder" :disabled="isLoading">
              {{ isLoading ? '...' : (isOnlinePayment ? $t('checkout.complete_order') : $t('checkout.complete_order_offline')) }}
            </button>
          </div>
        </div>
      </div>
      <div v-else>
        <p>{{ $t('checkout.empty_cart') }}</p>
        <button class="pay-btn" @click="router.push('/store')">{{ $t('checkout.continue_shopping') }}</button>
      </div>
    </div>
  </main>
</template>

<style scoped>
.page-content {
  padding: 60px 0;
  background-color: #fff;
  min-height: 60vh;
}
.content-container {
  max-width: 900px;
  margin: 0 auto;
  text-align: center;
}
.page-title {
  font-size: 2rem;
  font-weight: 800;
  margin-bottom: 20px;
  color: #333;
}
.desc {
  margin-bottom: 40px;
}
.checkout-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 40px;
  text-align: left;
}

.section-heading {
  font-size: 1.1rem;
  font-weight: 700;
  margin: 0 0 14px 0;
  color: #333;
}

.payment-method-options {
  display: flex;
  flex-direction: column;
  gap: 10px;
  margin-bottom: 20px;
}

.method-option {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 14px 16px;
  border: 2px solid #eaeaea;
  border-radius: 10px;
  cursor: pointer;
  transition: border-color 0.2s, background-color 0.2s;
}

.method-option input {
  accent-color: #c00a00;
}

.method-option.active {
  border-color: #c00a00;
  background-color: #fff8f8;
}

.method-icon {
  font-size: 1.3rem;
}

.method-label {
  font-weight: 600;
  color: #333;
}

.offline-note {
  background: #f8f9fa;
  border: 1px solid #e9ecef;
  border-radius: 8px;
  padding: 14px;
  font-size: 0.92rem;
  color: #555;
  line-height: 1.5;
  margin-bottom: 20px;
}

.summary-card {
  background: #fcfcfc;
  border: 1px solid #eaeaea;
  border-radius: 12px;
  padding: 25px;
}
.summary-list {
  list-style: none;
  padding: 0;
  margin: 0 0 20px 0;
  border-bottom: 1px solid #eaeaea;
}
.summary-item {
  display: flex;
  justify-content: space-between;
  margin-bottom: 15px;
  font-size: 1rem;
}
.item-name b {
  color: #c00a00;
  margin-left: 5px;
}
.summary-details {
  border-bottom: 1px solid #eaeaea;
  padding-bottom: 15px;
  margin-bottom: 15px;
}
.summary-detail-row {
  display: flex;
  justify-content: space-between;
  margin-bottom: 8px;
  font-size: 0.95rem;
  color: #666;
}
.summary-detail-row.discount {
  color: #c00a00;
  font-weight: 600;
}
.summary-total {
  display: flex;
  justify-content: space-between;
  font-size: 1.2rem;
  font-weight: 800;
  color: #333;
}
.total-price { color: #c00a00; }

.payment-card {
  background: #fff;
  border: 1px solid #eaeaea;
  border-radius: 12px;
  padding: 30px;
  box-shadow: 0 10px 30px rgba(0,0,0,0.05);
}
.payment-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 25px;
}
.payment-header h3 {
  margin: 0;
  font-size: 1.2rem;
  font-weight: 700;
}
.cc-input-group {
  margin-bottom: 20px;
}
.cc-input-group label {
  display: block;
  font-size: 0.9rem;
  font-weight: 600;
  margin-bottom: 8px;
  color: #555;
}
.cc-input-wrapper {
  position: relative;
  display: flex;
  align-items: center;
}
.cc-icon {
  position: absolute;
  left: 12px;
  color: #999;
}
.cc-input {
  width: 100%;
  padding: 14px 14px 14px 45px;
  border: 1px solid #dcdcdc;
  border-radius: 8px;
  font-size: 1rem;
  background-color: #fcfcfc;
  transition: border-color 0.2s;
  box-sizing: border-box;
}
.cc-input:focus {
  border-color: #c00a00;
  outline: none;
}
.cc-row .cc-input {
  padding: 14px;
}
.cc-row {
  display: flex;
  gap: 20px;
}
.flex-1 { flex: 1; }
.flex-2 { flex: 2; }

.expiry-select-group {
  display: flex;
  align-items: center;
  gap: 10px;
}
.expiry-divider {
  font-size: 1.2rem;
  color: #999;
}
.cc-select {
  cursor: pointer;
  appearance: none;
  background-image: url('data:image/svg+xml;utf8,<svg fill="%23999" height="24" viewBox="0 0 24 24" width="24" xmlns="http://www.w3.org/2000/svg"><path d="M7 10l5 5 5-5z"/><path d="M0 0h24v24H0z" fill="none"/></svg>');
  background-repeat: no-repeat;
  background-position-x: 95%;
  background-position-y: center;
}

.failure-toggle {
  display: flex;
  align-items: center;
  gap: 10px;
  margin-top: 10px;
  color: #c00a00;
  font-weight: 600;
  font-size: 0.9rem;
  cursor: pointer;
  background: #FFF5F5;
  padding: 10px;
  border-radius: 8px;
}

.pay-btn {
  background-color: #c00a00;
  color: #fff;
  border: none;
  padding: 16px;
  font-size: 1.1rem;
  font-weight: 700;
  border-radius: 50px;
  cursor: pointer;
  margin-top: 25px;
  width: 100%;
  transition: background-color 0.2s;
  text-transform: uppercase;
  letter-spacing: 0.5px;
}
.pay-btn:hover { background-color: #a00800; }
.pay-btn:disabled {
  background-color: #ccc;
  cursor: not-allowed;
}

.stripe-element-container {
  width: 100%;
  padding: 14px;
  border: 1px solid #dcdcdc;
  border-radius: 8px;
  background-color: #fcfcfc;
  box-sizing: border-box;
  transition: border-color 0.2s;
}

.stripe-element-container.focused {
  border-color: #c00a00;
}

.cc-input-wrapper.stripe-element-container {
  padding-left: 45px;
}

.stripe-field {
  width: 100%;
}

@media (max-width: 768px) {
  .checkout-grid {
    grid-template-columns: 1fr;
  }
}
</style>
