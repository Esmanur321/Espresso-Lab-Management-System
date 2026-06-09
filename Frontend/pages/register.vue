<script setup lang="ts">
import { ref, reactive, computed, onMounted } from 'vue';
import { useAuthStore } from '~/stores/auth';
import { useRouter, useRoute } from 'vue-router';
import { useForm, useField } from 'vee-validate';
import * as yup from 'yup';
import { useToast } from '~/composables/useToast';
import { useI18n } from '~/composables/useI18n';

definePageMeta({
  layout: 'auth'
});

const store = useAuthStore();
const router = useRouter();
const route = useRoute();
const { t, locale } = useI18n();
const { showToast } = useToast();

const placeholders = computed(() => {
  void locale.value;
  return {
    name: t('register.placeholder_name'),
    surname: t('register.placeholder_surname'),
    email: t('register.placeholder_email'),
    birthDate: t('register.birthdate_placeholder'),
    password: t('register.placeholder_password'),
    rePassword: t('register.placeholder_password_confirm')
  };
});

const showPassword = ref(false);
const showRePassword = ref(false);

const schema = computed(() => {
  void locale.value;
  return yup.object({
    name: yup.string().required(t('register.err_name_req')),
    surname: yup.string().required(t('register.err_surname_req')),
    email: yup.string().email(t('register.err_email_invalid')).required(t('register.err_email_req')),
    password: yup.string().min(6, t('register.err_pass_min')).required(t('register.err_pass_req')),
    rePassword: yup.string()
      .oneOf([yup.ref('password')], t('register.err_pass_match'))
      .required(t('register.err_repass_req'))
  });
});

const { handleSubmit, errors } = useForm({
  validationSchema: schema,
});

const { value: name } = useField('name');
const { value: surname } = useField('surname');
const { value: email } = useField('email');
const { value: password } = useField('password');
const { value: rePassword } = useField('rePassword');

const formData = reactive({
  gender: 'belirtmem',
  phone: '', 
  birthDate: '',
  agreements: {
    kvkk: false,
    userAgreement: false,
    communication: false
  }
});

onMounted(() => {
  if (route.query.phone) {
    formData.phone = String(route.query.phone);
  }
});

const isFormValid = computed(() => {
  return (
    name.value && surname.value && email.value && password.value && rePassword.value &&
    Object.keys(errors.value).length === 0 &&
    formData.agreements.kvkk &&
    formData.agreements.userAgreement
  );
});

const handleRegister = handleSubmit(async (values) => {
  if (!formData.agreements.kvkk || !formData.agreements.userAgreement) {
    await showToast(t('register.error_agreement'), 'warning');
    return;
  }

  try {
    await store.register({
      name: String(values.name),
      surname: String(values.surname),
      email: String(values.email),
      phone: formData.phone,
      password: String(values.password),
      gender: formData.gender,
      birthDate: formData.birthDate
    });
    await showToast(t('register.success'), 'success');
    const redirectPath = route.query.redirect ? String(route.query.redirect) : '/';
    router.push(redirectPath);
  } catch (error) {
    await showToast(t('register.error') + ' ' + (error as Error).message, 'error');
  }
});
</script>

<template>
  <div class="main-wrapper">
    
    <div class="left-side-form">
      <div class="logo-container">
        <NuxtLink to="/">
          <img src="/images/EslabHeader.png" alt="Espressolab Online Mağaza" class="top-left-logo" />
        </NuxtLink>
      </div>

      <div class="form-center-content" :key="locale">
        <h2 class="form-title">{{ t('auth.register') }}</h2>
        <p class="form-subtitle">{{ t('register.subtitle') }}</p>

        <div class="radio-group-gender">
          <label class="radio-label">
            <input type="radio" name="gender" value="kadin" v-model="formData.gender" />
            <span class="radio-custom"></span> {{ t('register.gender_female') }}
          </label>
          <label class="radio-label">
            <input type="radio" name="gender" value="erkek" v-model="formData.gender" />
            <span class="radio-custom"></span> {{ t('register.gender_male') }}
          </label>
          <label class="radio-label">
            <input type="radio" name="gender" value="belirtmem" v-model="formData.gender" />
            <span class="radio-custom"></span> {{ t('register.gender_none') }}
          </label>
        </div>

        <div class="input-row">
          <div class="input-col">
            <div class="input-group" :class="{'has-error': errors.name}">
              <span class="input-icon">👤</span>
              <input type="text" :placeholder="placeholders.name" v-model="name" />
            </div>
            <span class="error-msg" v-if="errors.name">{{ errors.name }}</span>
          </div>
          <div class="input-col">
            <div class="input-group" :class="{'has-error': errors.surname}">
              <span class="input-icon">👤</span>
              <input type="text" :placeholder="placeholders.surname" v-model="surname" />
            </div>
            <span class="error-msg" v-if="errors.surname">{{ errors.surname }}</span>
          </div>
        </div>

        <div class="input-row">
          <div class="input-col">
            <div class="input-group" :class="{'has-error': errors.email}">
              <span class="input-icon">✉️</span>
              <input type="email" :placeholder="placeholders.email" v-model="email" />
            </div>
            <span class="error-msg" v-if="errors.email">{{ errors.email }}</span>
          </div>
          <div class="input-col">
            <div class="input-group">
              <span class="input-icon">📅</span>
              <input type="text" :placeholder="placeholders.birthDate" onfocus="(this.type='date')" onblur="(this.type='text')" v-model="formData.birthDate" />
            </div>
          </div>
        </div>

        <div class="input-row">
          <div class="input-col">
            <div class="input-group" :class="{'has-error': errors.password}">
              <span class="input-icon">🔑</span>
              <input 
                :type="showPassword ? 'text' : 'password'" 
                :placeholder="placeholders.password" 
                v-model="password"
              />
              <span class="password-eye" @click="showPassword = !showPassword">
                {{ showPassword ? '🙈' : '👁️' }}
              </span>
            </div>
            <span class="error-msg" v-if="errors.password">{{ errors.password }}</span>
          </div>

          <div class="input-col">
            <div class="input-group" :class="{'has-error': errors.rePassword}">
              <span class="input-icon">🔑</span>
              <input 
                :type="showRePassword ? 'text' : 'password'" 
                :placeholder="placeholders.rePassword" 
                v-model="rePassword"
              />
              <span class="password-eye" @click="showRePassword = !showRePassword">
                {{ showRePassword ? '🙈' : '👁️' }}
              </span>
            </div>
            <span class="error-msg" v-if="errors.rePassword">{{ errors.rePassword }}</span>
          </div>
        </div>

        <p class="password-rule">
          {{ t('register.password_rule') }}
        </p>

        <div class="checkbox-group">
          <label class="checkbox-label">
            <input type="checkbox" v-model="formData.agreements.kvkk" />
            <span class="checkmark"></span>
            <span>{{ t('register.kvkk') }}</span>
          </label>
          <label class="checkbox-label">
            <input type="checkbox" v-model="formData.agreements.userAgreement" />
            <span class="checkmark"></span>
            <span>{{ t('register.user_agreement') }}</span>
          </label>
          <label class="checkbox-label">
            <input type="checkbox" v-model="formData.agreements.communication" />
            <span class="checkmark"></span>
            <span>{{ t('register.communication') }}</span>
          </label>
        </div>

        <button 
          class="register-btn" 
          :class="{ 'active': isFormValid }"
          @click="handleRegister"
        >
          {{ t('auth.register') }}
        </button>

        <p class="login-link">
          {{ t('auth.already_member') }} <NuxtLink to="/login">{{ t('auth.login') }}</NuxtLink>
        </p>
      </div>

      <p class="copyright-text">{{ t('footer.copyright') }}</p>
    </div>

    <div class="right-side-image">
      <img src="/images/GirişYapResmi.jpg" alt="Espressolab Kahve Deneyimi" />
    </div>

  </div>
</template>

<style scoped>
/* Kutu Modeli Sıfırlama */
* {
  box-sizing: border-box;
}

/* --- ANA YAPI --- */
.main-wrapper {
  display: flex;
  min-height: 100vh;
  width: 100%;
  background-color: var(--bg-color);
  color: var(--text-color);
  transition: background-color 0.3s, color 0.3s;
}

/* --- SOL KISIM (FORM) --- */
.left-side-form {
  flex: 1;
  display: flex;
  flex-direction: column;
  padding: 40px 60px;
  position: relative;
  justify-content: space-between;
}

/* 1. Sol Üst Logo Stili */
.logo-container {
  margin-bottom: 40px;
}
.top-left-logo {
  height: 60px;
  width: auto;
  cursor: pointer; /* Tıklanabilir olduğunu göstermek için */
}

/* Form İçerik Ortalaması */
.form-center-content {
  max-width: 550px;
  margin: 0 auto;
  width: 100%;
}

/* --- SAĞ KISIM (GÖRSEL) --- */
.right-side-image {
  flex: 1;
  background-color: #f4f4f4;
  overflow: hidden;
}

.right-side-image img {
  width: 100%;
  height: 100%;
  object-fit: cover;
  display: block;
}

/* --- FORM STİLLERİ --- */
.form-title {
  text-align: center;
  font-size: 1.8rem;
  font-weight: 700;
  color: var(--text-color);
  margin-bottom: 15px;
}

.form-subtitle {
  text-align: center;
  color: var(--text-color);
  opacity: 0.8;
  font-size: 0.95rem;
  margin-bottom: 30px;
}

/* Cinsiyet Radyo Butonları */
.radio-group-gender {
  display: flex;
  justify-content: center;
  gap: 30px;
  margin-bottom: 30px;
}
.radio-label {
  display: flex;
  align-items: center;
  cursor: pointer;
  font-size: 0.95rem;
  color: var(--text-color);
  opacity: 0.8;
}
.radio-label input { display: none; }
.radio-custom {
  width: 20px; height: 20px;
  border: 2px solid var(--border-color); border-radius: 50%;
  margin-right: 10px; position: relative;
}
.radio-label input:checked + .radio-custom { border-color: #c00a00; }
.radio-label input:checked + .radio-custom::after {
  content: ''; position: absolute;
  top: 50%; left: 50%; transform: translate(-50%, -50%);
  width: 10px; height: 10px;
  background-color: #c00a00; border-radius: 50%;
}

/* Input Alanları */
.input-row {
  display: flex; gap: 20px; margin-bottom: 20px;
}
.input-col {
  flex: 1;
  display: flex;
  flex-direction: column;
}
.input-group {
  position: relative;
  border: 1px solid var(--border-color); border-radius: 8px;
  padding: 12px 15px; background-color: var(--card-bg);
  display: flex; align-items: center;
  transition: border-color 0.2s, background-color 0.2s;
}
.input-group.has-error {
  border-color: #c00a00;
}
.error-msg {
  color: #c00a00;
  font-size: 0.75rem;
  margin-top: 5px;
  padding-left: 5px;
}
.input-group input {
  border: none; outline: none; width: 100%;
  font-size: 1rem; color: var(--text-color); background: transparent;
  padding-left: 10px;
}
.input-icon { color: #aaa; font-size: 1.1rem; }

/* Göz İkonu Düzenlemesi */
.password-eye { 
  color: #aaa; 
  cursor: pointer; 
  margin-left: 10px;
  user-select: none;
}
.password-eye:hover {
  color: #666;
}

/* Şifre Kuralı */
.password-rule {
  font-size: 0.8rem; color: var(--text-color); opacity: 0.7; margin-bottom: 25px;
}
.red-text { color: #c00a00; font-weight: 600; }

/* Checkboxlar */
.checkbox-group {
  display: flex; flex-direction: column; gap: 15px; margin-bottom: 30px;
}
.checkbox-label {
  display: flex; align-items: center; cursor: pointer; font-size: 0.9rem; color: var(--text-color); opacity: 0.8;
}
.checkbox-label input { display: none; }
.checkmark {
  width: 20px; height: 20px; border: 2px solid var(--border-color); border-radius: 4px;
  margin-right: 12px; display: flex; align-items: center; justify-content: center;
  flex-shrink: 0;
}
.checkbox-label input:checked + .checkmark {
  background-color: #c00a00; border-color: #c00a00; color: white;
}
.checkbox-label input:checked + .checkmark::after {
  content: '✓'; font-size: 14px;
}
.checkbox-label strong { color: var(--text-color); }

/* Butonlar ve Linkler */
.register-btn {
  width: 100%; padding: 15px;
  background-color: #d1d5db; /* Varsayılan Pasif Gri */
  color: white; border: none; border-radius: 50px;
  font-size: 1.1rem; font-weight: 700; 
  cursor: not-allowed;
  transition: all 0.3s ease;
  margin-bottom: 20px;
}

.register-btn.active {
  background-color: #c00a00; /* Aktif Kırmızı */
  cursor: pointer;
}

.register-btn.active:hover {
  background-color: #a00800;
}

.login-link { text-align: center; font-size: 0.95rem; color: var(--text-color); opacity: 0.8; }
.login-link a { color: var(--text-color); text-decoration: underline; font-weight: 600; }

/* Alt Bilgi */
.copyright-text {
  text-align: center; font-size: 0.75rem; color: #999; margin-top: 40px;
}

/* --- MOBİL UYUMLULUK --- */
@media (max-width: 1024px) {
  .main-wrapper {
    flex-direction: column;
  }
  .right-side-image {
    display: none;
  }
  .left-side-form {
    padding: 30px 20px;
  }
  .form-center-content {
    max-width: 100%;
  }
  .input-row {
      flex-direction: column;
      gap: 15px; margin-bottom: 15px;
  }
}
</style>