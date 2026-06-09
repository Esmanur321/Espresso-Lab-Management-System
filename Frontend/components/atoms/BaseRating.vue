<script setup lang="ts">
defineProps({
  rating: { type: Number, default: 0 },
  maxRating: { type: Number, default: 5 }
});
</script>

<template>
  <div class="rating">
    <span v-for="n in maxRating" :key="n" class="star">
      {{ n <= rating ? '★' : '☆' }}
    </span>
    <span class="rating-text"> ({{ rating }}/{{ maxRating }})</span>
  </div>
</template>

<style scoped>
.rating { font-size: 1rem; color: #777; }
.star { color: #f39c12; /* Altın/Sarı */ }
.rating-text { margin-left: 5px; }
</style>