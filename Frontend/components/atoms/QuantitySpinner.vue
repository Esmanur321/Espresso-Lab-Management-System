<script setup lang="ts">
const props = defineProps({
  modelValue: {
    type: Number,
    required: true
  }
});
const emit = defineEmits(['update:modelValue']);

const increment = () => {
  emit('update:modelValue', props.modelValue + 1);
};

const decrement = () => {
  // Miktar en az 1 olabilir
  if (props.modelValue > 1) {
    emit('update:modelValue', props.modelValue - 1);
  }
};
</script>

<template>
  <div class="quantity-spinner">
    <button type="button" @click="decrement" class="spinner-btn">-</button>
    <span class="quantity-value">{{ modelValue }}</span>
    <button type="button" @click="increment" class="spinner-btn">+</button>
  </div>
</template>

<style scoped>
.quantity-spinner {
  display: flex;
  align-items: center;
  border: 1px solid #ddd;
  border-radius: 50px;
}
.spinner-btn {
  background: none;
  border: none;
  cursor: pointer;
  padding: 8px 15px;
  font-size: 1.2rem;
  color: #555;
}
.quantity-value {
  padding: 0 10px;
  font-size: 1rem;
  font-weight: 600;
  min-width: 20px;
  text-align: center;
}
</style>