<script setup lang="ts">
defineProps({
  isActive: {
    type: Boolean,
    default: false
  }
});
</script>

<template>
  <button :class="['slider-dot', { active: isActive }]"></button>
</template>

<style scoped>
.slider-dot {
  width: 10px;
  height: 10px;
  border-radius: 50%;
  background-color: #ccc;
  border: none;
  padding: 0;
  margin: 0 5px;
  cursor: pointer;
  transition: background-color 0.3s ease;
}
.slider-dot.active {
  background-color: #c00a00; /* Aktif (kırmızı) */
}
</style>