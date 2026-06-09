<script setup lang="ts">
interface DropdownOption {
  value: string;
  text: string;
}

defineProps<{
  modelValue: string;
  options: DropdownOption[]; // Format: [{ value: '+90', text: 'TR +90' }]
}>();

const emit = defineEmits(['update:modelValue']);

const handleChange = (event: Event) => {
  const target = event.target as HTMLSelectElement;
  emit('update:modelValue', target.value);
};
</script>

<template>
  <div class="dropdown-wrapper">
    <select 
      :value="modelValue"
      @change="handleChange"
      class="base-dropdown"
    >
      <option 
        v-for="option in options" 
        :key="option.value" 
        :value="option.value"
      >
        {{ option.text }}
      </option>
    </select>
  </div>
</template>

<style scoped>
.dropdown-wrapper {
  position: relative;
}
.base-dropdown {
  padding: 12px 10px;
  border: 1px solid #ddd;
  border-radius: 8px;
  font-size: 1rem;
  font-weight: 600;
  color: #c00a00; /* Resimdeki gibi kırmızı metin */
  background-color: white;
  appearance: none; /* Tarayıcı okunu kaldır */
  cursor: pointer;
  height: 47px; /* BaseInput ile aynı yükseklik için */
}
</style>