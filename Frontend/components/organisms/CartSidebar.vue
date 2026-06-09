<script setup lang="ts">
import CouponInput from '@/components/atoms/CouponInput.vue';
import CartSummary from '@/components/molecules/CartSummary.vue';
import BaseButton from '@/components/atoms/BaseButton.vue'; // Yeniden kullanım

interface CartSummaryData {
  subtotal: number;
  discount: number;
  shipping: number;
  total: number;
}

defineProps<{
  summary?: CartSummaryData; // { subtotal, discount, shipping, total }
}>();

const emit = defineEmits(['applyCoupon', 'checkout', 'continueShopping']);
</script>

<template>
  <aside class="cart-sidebar">
    <CartSummary 
      :subtotal="summary?.subtotal"
      :discount="summary?.discount"
      :shipping="summary?.shipping"
      :total="summary?.total"
      class="summary-box"
    />
    
    <div class="button-group">
      <BaseButton 
        :label="$t('cart.checkout')" 
        variant="solid"
        @click="emit('checkout')"
      />
      <BaseButton 
        :label="$t('cart.continue_shopping')" 
        variant="outline"
        @click="emit('continueShopping')"
      />
    </div>
  </aside>
</template>

<style scoped>
.cart-sidebar {
  background-color: #fdfdfd;
  border: 1px solid #f0f0f0;
  border-radius: 12px;
  padding: 20px;
}
.summary-box {
  margin: 20px 0;
}
.button-group {
  display: flex;
  flex-direction: column;
  gap: 10px;
}
/* Butonların tam genişlik kaplamasını sağla */
.button-group :deep(.base-button) {
  width: 100%;
}
</style>