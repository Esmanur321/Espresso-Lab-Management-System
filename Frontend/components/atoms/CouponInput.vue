<script setup lang="ts">
import { ref } from 'vue';
import BaseInput from './BaseInput.vue';
import BaseButton from './BaseButton.vue';

const couponCode = ref('');

// Dışarıya 'applyCoupon' olayı (event) yayacağız
const emit = defineEmits(['applyCoupon']);

const apply = () => {
  emit('applyCoupon', couponCode.value);
};
</script>

<template>
  <div class="coupon-input-group">
    <BaseInput 
      v-model="couponCode"
      placeholder="Kupon kodu ekle"
      class="coupon-input"
    />
    <BaseButton 
      label="Uygula" 
      variant="solid" 
      @click="apply"
      :disabled="!couponCode"
      class="coupon-button"
    />
  </div>
</template>

<style scoped>
.coupon-input-group {
  display: flex;
  gap: 5px;
}
.coupon-input {
  /* BaseInput'un varsayılan stilini ez */
  :deep(.base-input) {
    height: 45px;
    border-radius: 8px;
  }
}
.coupon-button {
  height: 45px;
  /* BaseButton'un pasif (disabled) stilini ezerek
     resimdeki gibi gri yapalım */
  background-color: #f0f0f0;
  color: #999;
  border-color: #f0f0f0;
}
.coupon-button:not(:disabled) {
  /* Aktifken kırmızı olsun */
  background-color: #c00a00;
  border-color: #c00a00;
  color: white;
}
</style>