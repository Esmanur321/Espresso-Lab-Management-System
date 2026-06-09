<script setup lang="ts">
import BaseDropdown from '@/components/atoms/BaseDropdown.vue';
import BaseInput from '@/components/atoms/BaseInput.vue';

interface CountryOption {
  value: string;
  text: string;
}

// v-model'i iki yönlü olarak kabul etmek için
defineProps<{
  countryCode: string;
  phoneNumber: string;
  options: CountryOption[];
}>();

const emit = defineEmits(['update:countryCode', 'update:phoneNumber']);
</script>

<template>
  <div class="phone-input-group">
    <BaseDropdown
      :modelValue="countryCode"
      :options="options"
      @update:modelValue="emit('update:countryCode', $event)"
      class="country-code"
    />
    <BaseInput 
      type="tel"
      :modelValue="phoneNumber"
      :placeholder="$t('auth.phone')"
      @update:modelValue="emit('update:phoneNumber', $event)"
      class="phone-number"
    />
  </div>
</template>

<style scoped>
.phone-input-group {
  display: flex;
  gap: 10px;
}
.country-code {
  flex-shrink: 0; /* Küçülmesin */
}
.phone-number {
  flex-grow: 1; /* Kalan tüm alanı kapsasın */
}
</style>