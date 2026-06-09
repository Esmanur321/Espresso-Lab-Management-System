<script setup lang="ts">
import SliderDot from '@/components/atoms/SliderDot.vue';

defineProps({
  count: { type: Number, required: true },
  activeIndex: { type: Number, required: true }
});

const emit = defineEmits(['dotClick']);
</script>

<template>
  <div class="dots-group">
    <SliderDot
      v-for="n in count"
      :key="n"
      :isActive="n - 1 === activeIndex"
      @click="emit('dotClick', n - 1)"
    />
  </div>
</template>

<style scoped>
.dots-group {
  display: flex;
  justify-content: center;
  padding: 10px 0;
}
</style>