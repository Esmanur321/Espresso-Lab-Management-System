<script setup lang="ts">
// Para formatlama
const formatCurrency = (value: number | undefined): string => {
  if (value === undefined) return '₺0,00';
  return `₺${value.toFixed(2).replace('.', ',')}`;
};

defineProps<{
  subtotal?: number;
  discount?: number;
  shipping?: number;
  total?: number;
}>();
</script>

<template>
  <div class="cart-summary">
    <div class="summary-row">
      <span>{{ $t('cart.subtotal') }}</span>
      <span>{{ formatCurrency(subtotal) }}</span>
    </div>
    <div class="summary-row discount">
      <span>{{ $t('cart.discount') }}</span>
      <span>-{{ formatCurrency(discount) }}</span>
    </div>
    <div class="summary-row">
      <span>{{ $t('cart.shipping') }}</span>
      <span>{{ formatCurrency(shipping) }}</span>
    </div>
    <div class="summary-row total">
      <span>{{ $t('cart.total') }}</span>
      <span>{{ formatCurrency(total) }}</span>
    </div>
  </div>
</template>

<style scoped>
.cart-summary {
  font-size: 0.9rem;
}
.summary-row {
  display: flex;
  justify-content: space-between;
  margin-bottom: 15px;
  color: #555;
}
.summary-row.discount {
  color: #27ae60; /* Yeşil indirim */
}
.summary-row.total {
  font-size: 1.2rem;
  font-weight: 700;
  color: #333;
  border-top: 1px dashed #ddd;
  padding-top: 15px;
}
</style>