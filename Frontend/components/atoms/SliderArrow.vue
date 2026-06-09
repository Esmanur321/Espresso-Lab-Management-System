<script setup lang="ts">
defineProps({
  direction: {
    type: String,
    default: 'right' // 'left' or 'right'
  }
});
</script>

<template>
  <button class="slider-arrow">
    <span v-if="direction === 'left'">&lt;</span>
    <span v-else>&gt;</span>
  </button>
</template>

<style scoped>
.slider-arrow {
  background-color: #ffffff;
  border: 1px solid #f0f0f0;
  border-radius: 50%;
  width: 50px;
  height: 50px;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
  transition: all 0.3s ease;
  font-size: 1.5rem;
  color: #555;
}
.slider-arrow:hover {
  background-color: #f9f9f9;
  transform: scale(1.05);
}
</style>