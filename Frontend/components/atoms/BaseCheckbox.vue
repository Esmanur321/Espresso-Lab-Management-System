<script setup lang="ts">
defineProps({
  modelValue: { // v-model
    type: Boolean,
    default: false
  },
  label: {
    type: String,
    required: true
  }
});

const emit = defineEmits(['update:modelValue']);
</script>

<template>
  <label class="checkbox-label">
    <input 
      type="checkbox"
      :checked="modelValue"
      @change="emit('update:modelValue', ($event.target as HTMLInputElement).checked)"
      class="checkbox-input"
    >
    <span class="custom-checkbox"></span>
    <span class="label-text">{{ label }}</span>
  </label>
</template>

<style scoped>
.checkbox-label {
  display: flex;
  align-items: center;
  cursor: pointer;
  font-size: 0.9rem;
  color: #555;
  margin-bottom: 12px;
}
.label-text {
  margin-left: 8px;
}
.checkbox-input {
  display: none; /* Varsayılanı gizle */
}
.custom-checkbox {
  width: 18px;
  height: 18px;
  border: 1px solid #ddd;
  border-radius: 4px;
  display: inline-block;
  position: relative;
}
.checkbox-input:checked + .custom-checkbox {
  background-color: #c00a00;
  border-color: #c00a00;
}
.checkbox-input:checked + .custom-checkbox::after {
  content: '✔';
  font-size: 12px;
  color: white;
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
}
</style>