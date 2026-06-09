<script setup lang="ts">
import BaseButton from '@/components/atoms/BaseButton.vue';
import BaseCheckbox from '@/components/atoms/BaseCheckbox.vue';
import RadioGroup from '@/components/molecules/RadioGroup.vue';
import BaseInput from '@/components/atoms/BaseInput.vue';
import IconInput from '@/components/molecules/IconInput.vue';

interface GenderOption {
  value: string;
  label: string;
}

const props = withDefaults(defineProps<{
  gender?: string;
  firstName?: string;
  lastName?: string;
  email?: string;
  birthDate?: string;
  password?: string;
  passwordConfirm?: string;
  kvkk?: boolean;
  terms?: boolean;
  marketing?: boolean;
  title?: string;
  instruction?: string;
  passwordHint?: string;
  genderOptions?: GenderOption[];
  disabled?: boolean;
}>(), {
  genderOptions: () => []
});

const emit = defineEmits([
  'update:gender',
  'update:firstName', 'update:lastName',
  'update:email', 
  // 'update:phoneNumber', <-- SİLİNDİ
  'update:birthDate',
  'update:password', 'update:passwordConfirm',
  'update:kvkk', 'update:terms', 'update:marketing',
  'submit', 'loginClick'
]);
</script>

<template>
  <div class="signup-form-card">
    <h2 class="form-title">{{ title }}</h2>
    <p class="form-instruction">{{ instruction }}</p>

    <form @submit.prevent="emit('submit')">
      
      <RadioGroup 
        name="gender"
        :options="genderOptions"
        :modelValue="gender"
        @update:modelValue="emit('update:gender', $event)"
      />

      <div class="input-grid">
        <BaseInput 
          placeholder="Ad" 
          :modelValue="firstName"
          @update:modelValue="emit('update:firstName', $event)"
        />
        <BaseInput 
          placeholder="Soyad" 
          :modelValue="lastName"
          @update:modelValue="emit('update:lastName', $event)"
        />
        <BaseInput 
          placeholder="E-Posta" 
          type="email" 
          :modelValue="email"
          @update:modelValue="emit('update:email', $event)"
        />
        
        <BaseInput 
          type="date" 
          :modelValue="birthDate"
          @update:modelValue="emit('update:birthDate', $event)"
        />
        
        <IconInput 
          placeholder="Şifre" 
          type="password" 
          :modelValue="password"
          @update:modelValue="emit('update:password', $event)"
        />
        <IconInput 
          placeholder="Şifre Yeniden" 
          type="password" 
          :modelValue="passwordConfirm"
          @update:modelValue="emit('update:passwordConfirm', $event)"
        />
      </div>

      <p class="password-hint">{{ passwordHint }}</p>
      
      <div class="checkbox-group">
        <BaseCheckbox 
          label="KVKK metnini okudum, kabul ediyorum."
          :modelValue="kvkk"
          @update:modelValue="emit('update:kvkk', $event)"
        />
        <BaseCheckbox 
          label="Kullanıcı sözleşmesini okudum, kabul ediyorum."
          :modelValue="terms"
          @update:modelValue="emit('update:terms', $event)"
        />
        <BaseCheckbox 
          label="SMS ve E-posta gönderimi izni veriyorum."
          :modelValue="marketing"
          @update:modelValue="emit('update:marketing', $event)"
        />
      </div>

      <BaseButton 
        label="Üye Ol" type="submit" :disabled="disabled"
        class="submit-button"
      />
    </form>
    
    <p class="login-link">
      Hesabınız var mı? 
      <a href="#" @click.prevent="emit('loginClick')">Giriş yapın</a>
    </p>
  </div>
</template>

<style scoped>
.signup-form-card {
  background-color: white;
  border-radius: 16px;
  padding: 40px;
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.05);
  max-width: 650px; 
  width: 100%;
  box-sizing: border-box;
}
.form-title { text-align: center; font-size: 1.5rem; }
.form-instruction { text-align: center; color: #777; margin-bottom: 30px; }
.input-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 20px;
  margin-bottom: 15px;
}
.password-hint {
  font-size: 0.8rem;
  color: #c00a00;
  margin-bottom: 20px;
}
.checkbox-group { text-align: left; margin-bottom: 20px; }
.submit-button {
  width: 100%;
  background-color: #e0e0e0;
  color: #999;
}
.submit-button:not(:disabled) {
  background-color: #c00a00;
  color: white;
}
.login-link { text-align: center; margin-top: 20px; }
.login-link a { color: #c00a00; font-weight: 700; text-decoration: none; }
</style>