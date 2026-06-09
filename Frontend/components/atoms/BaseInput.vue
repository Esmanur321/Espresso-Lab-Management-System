<script setup lang="ts">
const props = withDefaults(defineProps<{
  modelValue?: string;
  placeholder?: string;
  type?: string;
}>(), {
  type: 'text'
});

const emit = defineEmits(['update:modelValue']);

const handleInput = (event: Event) => {
  const target = event.target as HTMLInputElement;
  emit('update:modelValue', target.value);
};
</script>

<template>
  <input 
    :type="type"
    :value="modelValue"
    :placeholder="placeholder"
    @input="handleInput"
    class="base-input"
  >
</template>

<style scoped>
.base-input {
  width: 100%;
  padding: 12px 15px;
  border: 1px solid #ddd;
  border-radius: 8px;
  font-size: 1rem;
  box-sizing: border-box; 
  height: 47px; /* Diğer inputlarla aynı yükseklik */
}

.base-input:focus {
  outline: none;
  border-color: #c00a00;
  box-shadow: 0 0 0 2px rgba(192, 10, 0, 0.1);
}

/* type="date" olan input'un placeholder'ı soluk görünmesin */
.base-input[type="date"] {
  color: #333;
}
/* Tarayıcı varsayılan metnini (gg.aa.yyyy) göstermesi için */
.base-input[type="date"]:invalid {
  color: #777;
}
</style>