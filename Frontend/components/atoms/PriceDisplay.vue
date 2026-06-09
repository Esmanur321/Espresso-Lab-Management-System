<script setup lang="ts">
defineProps<{
  price: number;
  originalPrice?: number | null;
}>();

// Basit bir para formatlama
const formatCurrency = (value: number): string => {
  return `₺${value.toFixed(2).replace('.', ',')}`;
};
</script>

<template>
  <div class="price-display">
    <span class="current-price">{{ formatCurrency(price) }}</span>
    <span v-if="originalPrice" class="original-price">
      {{ formatCurrency(originalPrice) }}
    </span>
  </div>
</template>

<style scoped>
.price-display {
  display: flex;
  align-items: center;
  gap: 10px;
  margin: 15px 0;
}
.current-price {
  font-size: 1.8rem;
  font-weight: 700;
  color: #333;
}
.original-price {
  font-size: 1.2rem;
  color: #999;
  text-decoration: line-through;
}
</style>