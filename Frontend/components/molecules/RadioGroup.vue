<script setup lang="ts">
import BaseRadioButton from '@/components/atoms/BaseRadioButton.vue';

interface RadioOption {
  label: string;
  value: string;
}

defineProps<{
  modelValue?: string;
  name: string;
  options: RadioOption[]; // Format: [{ label: '...', value: '...' }]
}>();

const emit = defineEmits(['update:modelValue']);
</script>

<template>
  <div class="radio-group">
    <BaseRadioButton
      v-for="option in options"
      :key="option.value"
      :name="name"
      :label="option.label"
      :value="option.value"
      :modelValue="modelValue"
      @update:modelValue="emit('update:modelValue', $event)"
    />
  </div>
</template>

<style scoped>
.radio-group {
  display: flex;
  justify-content: center;
  margin-bottom: 20px;
}
</style>