<script setup lang="ts">
import PhoneInputGroup from '@/components/molecules/PhoneInputGroup.vue';
import BaseButton from '@/components/atoms/BaseButton.vue';

interface CountryOption {
  value: string;
  text: string;
}

const props = withDefaults(defineProps<{
  title?: string;
  instruction?: string;
  buttonText?: string;
  countryCode?: string;
  phoneNumber?: string;
  countryOptions?: CountryOption[];
  disabled?: boolean;
}>(), {
  countryOptions: () => []
});

const emit = defineEmits([
  'update:countryCode', 
  'update:phoneNumber',
  'submit'
]);
</script>

<template>
  <div class="phone-form-card">
    <h2 class="form-title">{{ title }}</h2>
    <p class="form-instruction">{{ instruction }}</p>

    <form @submit.prevent="emit('submit')">
      <div class="input-wrapper">
        <PhoneInputGroup
          :countryCode="countryCode ?? ''"
          :phoneNumber="phoneNumber ?? ''"
          :options="countryOptions"
          @update:countryCode="emit('update:countryCode', $event)"
          @update:phoneNumber="emit('update:phoneNumber', $event)"
        />
      </div>

      <button 
        type="submit" 
        class="login-btn"
        :disabled="disabled"
      >
        {{ buttonText }}
      </button>
    </form>
  </div>
</template>

<style scoped>
/* KART TASARIMI */
.phone-form-card {
  background-color: #fff;
  /* Hafif bir sınır çizgisi ve çok hafif gölge */
  border: 1px solid #f0f0f0;
  border-radius: 20px; /* Köşeler yuvarlak */
  padding: 50px 40px;
  width: 100%;
  max-width: 480px; /* Kart genişliği */
  text-align: center;
  box-shadow: 0 5px 20px rgba(0,0,0,0.02);
}

.form-title {
  font-size: 1.2rem;
  font-weight: 700;
  color: #000;
  margin-bottom: 15px;
  font-family: 'Inter', sans-serif;
}

.form-instruction {
  font-size: 0.9rem;
  color: #666; /* Gri açıklama */
  line-height: 1.5;
  margin-bottom: 30px;
  font-family: 'Inter', sans-serif;
}

.input-wrapper {
  margin-bottom: 20px;
}

/* BUTON TASARIMI (Görseldeki Gri Buton) */
.login-btn {
  width: 100%;
  padding: 15px;
  background-color: #D1D5DB; /* Pasif Gri Renk */
  color: #fff;
  border: none;
  border-radius: 50px; /* Tam yuvarlak kenarlar */
  font-size: 1rem;
  font-weight: 700;
  cursor: pointer;
  transition: background-color 0.3s;
}

/* Eğer buton aktifse (disabled değilse) rengi değişebilir */
.login-btn:not(:disabled) {
  background-color: #c00a00; /* Aktifken kırmızı olsun isterseniz */
}
.login-btn:disabled {
  cursor: not-allowed;
}
</style>