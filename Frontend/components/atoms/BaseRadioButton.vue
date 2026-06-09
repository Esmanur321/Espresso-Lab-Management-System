<script setup lang="ts">
defineProps({
  modelValue: String, // v-model
  value: String,      // Bu seçeneğin değeri
  name: String,       // Grup adı
  label: String
});

const emit = defineEmits(['update:modelValue']);
</script>

<template>
  <label class="radio-label">
    <input 
      type="radio"
      :name="name"
      :value="value"
      :checked="modelValue === value"
      @change="emit('update:modelValue', value)"
      class="radio-input"
    >
    <span class="custom-radio"></span>
    <span class="label-text">{{ label }}</span>
  </label>
</template>

<style scoped>
.radio-label {
  display: flex;
  align-items: center;
  cursor: pointer;
  font-size: 0.9rem;
  color: #555;
  margin-right: 20px;
}
.label-text {
  margin-left: 8px;
}
.radio-input {
  display: none;
}
.custom-radio {
  width: 18px;
  height: 18px;
  border: 1px solid #ddd;
  border-radius: 50%;
  display: inline-block;
  position: relative;
}
.radio-input:checked + .custom-radio {
  border-color: #c00a00;
}
.radio-input:checked + .custom-radio::after {
  content: '';
  width: 10px;
  height: 10px;
  background-color: #c00a00;
  border-radius: 50%;
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
}
</style>