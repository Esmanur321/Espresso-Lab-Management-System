<script setup lang="ts">
import { ref, computed, onMounted } from 'vue';
import { useRouter, useRoute } from 'vue-router'; 
import { useAuthStore } from '~/stores/auth';
import { useNuxtApp } from '#app';
import { useToast } from '~/composables/useToast';
import { parseJwtPayload } from '~/utils/jwtClient';

import { useI18n } from '~/composables/useI18n';

definePageMeta({
  layout: 'auth'
});
const store = useAuthStore();
const router = useRouter(); 
const route = useRoute();

const { t, locale } = useI18n();
const $t = (key: string): string => {
  void locale.value;
  return t(key);
};
const { showToast } = useToast();

const email = ref('');
const password = ref('');
const isLoading = ref(false);
const showPassword = ref(false);

const pageContent = computed(() => ({
  title: $t('login.title') || 'Giriş Yap',
  instruction: $t('login.instruction') || 'Lütfen bilgilerinizi giriniz.',
  buttonText: $t('login.button') || 'Giriş Yap',
  copyright: $t('footer.copyright')
}));

const isButtonDisabled = computed(() => {
  return email.value.length < 5 || password.value.length < 3 || isLoading.value;
});

const API_BASE = 'http://localhost:8000';

const handleLogin = async () => {
  if (isButtonDisabled.value) return;
  isLoading.value = true;
  
  try {
    await store.login({ 
      email: email.value,
      password: password.value
    });
    
    await showToast($t('login.success') || 'Giriş başarılı!', 'success');
    await store.syncProfileFromServer();
    const redirectPath = route.query.redirect
      ? String(route.query.redirect)
      : (store.isAdmin ? '/admin' : '/');
    router.push(redirectPath);
  } catch (error: any) {
    console.error('Login error:', error);
    await showToast(($t('login.error') || 'Bir hata oluştu: ') + ' ' + error.message, 'error');
  } finally {
    isLoading.value = false;
  }
};

const handleSocialLogin = () => {
  window.location.href = `${API_BASE}/auth/google/login`;
};

onMounted(async () => {
  if (!process.client) return;

  const params = new URLSearchParams(window.location.search);

  // Google sometimes returns ?code=... to /login when redirect URI was misconfigured.
  // Forward the authorization code to the backend callback so it can exchange for JWT.
  const oauthCode = params.get('code');
  if (oauthCode && !params.get('auth_success')) {
    window.location.replace(`${API_BASE}/auth/google/callback?${params.toString()}`);
    return;
  }

  let authSuccess = params.get('auth_success') || '';
  let token = params.get('token') || '';
  let id = params.get('id') || '';
  let email = params.get('email') || '';
  let name = params.get('name') || '';
  let surname = params.get('surname') || '';
  let phone = params.get('phone') || '';
  let isAdmin = params.get('is_admin') || '';
  let redirect = params.get('redirect') || '';

  // Fallback to route query if search params are empty
  if (!authSuccess && route.query.auth_success) {
    authSuccess = String(route.query.auth_success);
    token = String(route.query.token || '');
    id = String(route.query.id || '');
    email = String(route.query.email || '');
    name = String(route.query.name || '');
    surname = String(route.query.surname || '');
    phone = String(route.query.phone || '');
    isAdmin = String(route.query.is_admin || '');
    redirect = String(route.query.redirect || '');
  }

  if (authSuccess === 'true' && token) {
    try {
      let user: {
        uid: string;
        name: string;
        surname: string;
        email: string;
        phone: string;
        birthDate: string;
        role: 'admin' | 'user';
      };

      const isJwt = token.split('.').length === 3;
      if (isJwt) {
        const claims = parseJwtPayload(token);
        if (!claims || typeof claims.sub !== 'string') {
          throw new Error('Invalid session token from server');
        }
        user = {
          uid: String(claims.sub),
          name: String(claims.name ?? ''),
          surname: String(claims.surname ?? ''),
          email: String(claims.email ?? ''),
          phone: String(claims.phone ?? ''),
          birthDate: '',
          role: claims.is_admin === true ? 'admin' : 'user'
        };
      } else {
        user = {
          uid: String(id),
          name: String(name),
          surname: String(surname),
          email: String(email),
          phone: String(phone),
          birthDate: '',
          role: (isAdmin === 'true' || isAdmin === 'admin') ? 'admin' : 'user' as any
        };
      }

      store.setSession(user);
      localStorage.setItem('auth_token', token);
      await store.syncProfileFromServer();

      await showToast($t('login.google_success') || 'Google ile giriş başarılı!', 'success');

      window.history.replaceState({}, document.title, window.location.pathname);
      router.replace({ query: {} });

      const redirectPath = redirect
        ? String(redirect)
        : (store.isAdmin ? '/admin' : '/');
      router.push(redirectPath);
    } catch (e: any) {
      console.error('Failed to log in after oauth:', e);
      await showToast($t('login.google_error') || 'Sosyal medya girişi başarısız oldu.', 'error');
    }
  } else {
    const authError = route.query.auth_error || params.get('auth_error');
    if (authError) {
      console.error('OAuth error redirect code:', authError);
      await showToast($t('login.google_error') || 'Sosyal medya girişi başarısız oldu.', 'error');
    }
  }
});
</script>

<template>
  <div class="split-screen-layout">
    
    <div class="left-panel">
      
      <div class="auth-logo">
        <router-link to="/">
          <img src="/images/EslabHeader.png" alt="Espressolab" />
        </router-link>
      </div>

      <div class="form-container">
        <h2 class="form-title">{{ pageContent.title }}</h2>
        <p class="form-subtitle">{{ pageContent.instruction }}</p>

        <form @submit.prevent="handleLogin" class="login-form">
          <div class="input-group">
            <span class="input-icon">✉️</span>
            <input type="email" v-model="email" :placeholder="$t('login.email_placeholder') || 'E-posta Adresi'" required />
          </div>

          <div class="input-group">
            <span class="input-icon">🔑</span>
            <input :type="showPassword ? 'text' : 'password'" v-model="password" :placeholder="$t('login.password_placeholder') || 'Şifre'" required />
            <span class="password-eye" @click="showPassword = !showPassword">
              {{ showPassword ? '🙈' : '👁️' }}
            </span>
          </div>

          <button type="submit" class="register-btn" :class="{ 'active': !isButtonDisabled }" :disabled="isButtonDisabled">
            {{ isLoading ? 'İşleniyor...' : pageContent.buttonText }}
          </button>
        </form>
        
        <div class="divider">
          <span>{{ $t('login.or') || 'VEYA' }}</span>
        </div>

        <button class="social-btn google-btn" @click.prevent="handleSocialLogin" :disabled="isLoading">
          <svg viewBox="0 0 24 24" width="20" height="20" xmlns="http://www.w3.org/2000/svg"><path d="M22.56 12.25c0-.78-.07-1.53-.2-2.25H12v4.26h5.92c-.26 1.37-1.04 2.53-2.21 3.31v2.77h3.57c2.08-1.92 3.28-4.74 3.28-8.09z" fill="#4285F4"/><path d="M12 23c2.97 0 5.46-.98 7.28-2.66l-3.57-2.77c-.98.66-2.23 1.06-3.71 1.06-2.86 0-5.29-1.93-6.16-4.53H2.18v2.84C3.99 20.53 7.7 23 12 23z" fill="#34A853"/><path d="M5.84 14.09c-.22-.66-.35-1.36-.35-2.09s.13-1.43.35-2.09V7.07H2.18C1.43 8.55 1 10.22 1 12s.43 3.45 1.18 4.93l2.85-2.22.81-.62z" fill="#FBBC05"/><path d="M12 5.38c1.62 0 3.06.56 4.21 1.64l3.15-3.15C17.45 2.09 14.97 1 12 1 7.7 1 3.99 3.47 2.18 7.07l3.66 2.84c.87-2.6 3.3-4.53 6.16-4.53z" fill="#EA4335"/><path d="M1 1h22v22H1z" fill="none"/></svg>
          {{ $t('login.google_btn') }}
        </button>

        <p class="login-link">
          {{ $t('login.no_account') }} <NuxtLink :to="`/register${route.query.redirect ? '?redirect=' + route.query.redirect : ''}`">{{ $t('login.register') }}</NuxtLink>
        </p>
      </div>

      <div class="auth-footer">
        <p>{{ pageContent.copyright }}</p>
      </div>
    </div>

    <div class="right-panel">
      <img src="/images/GirişYapResmi.jpg" alt="Espressolab Moment" class="cover-image" />
    </div>

  </div>
</template>

<style scoped>
/* --- ANA DÜZEN (FLEXBOX) --- */
.split-screen-layout {
  display: flex;
  min-height: 100vh;
  width: 100%;
  background-color: var(--bg-color);
  color: var(--text-color);
  transition: background-color 0.3s, color 0.3s;
}

/* --- SOL PANEL (FORM) --- */
.left-panel {
  flex: 1; /* Ekranın %50'si (Geniş ekranda) */
  display: flex;
  flex-direction: column;
  justify-content: space-between; /* Logo üstte, Form ortada, Footer altta */
  padding: 40px 60px;
  max-width: 50%; 
}

.auth-logo img {
  height: 70px;
  width: auto;
}

.form-container {
  width: 100%;
  max-width: 450px;
  margin: 0 auto; /* Yatayda ortala */
}

.auth-footer p {
  font-size: 0.7rem;
  color: #999;
  text-align: center;
}

/* PhoneEntryForm stillerini ezerek sadeleştirelim (Gölgesiz) */
:deep(.phone-form-card) {
  box-shadow: none !important;
  padding: 0 !important;
  text-align: center !important;
  border: none !important;
}
:deep(.form-title) {
  font-size: 1.5rem;
  margin-bottom: 15px;
}

.divider {
  display: flex;
  align-items: center;
  text-align: center;
  margin: 20px 0;
}
.divider::before, .divider::after {
  content: '';
  flex: 1;
  border-bottom: 1px solid var(--border-color);
}
.divider span {
  padding: 0 10px;
  color: var(--text-color);
  opacity: 0.8;
  font-size: 0.85rem;
}

.social-btn {
  width: 100%;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 10px;
  padding: 12px;
  border-radius: 8px;
  border: 1px solid var(--border-color);
  background-color: var(--card-bg);
  color: var(--text-color);
  font-weight: 600;
  cursor: pointer;
  transition: background-color 0.2s, color 0.2s, border-color 0.2s;
}
.social-btn:hover:not(:disabled) {
  background-color: var(--border-color);
}
.social-btn:disabled {
  opacity: 0.7;
  cursor: not-allowed;
}

/* --- SAĞ PANEL (RESİM) --- */
.right-panel {
  flex: 1; /* Diğer %50 */
  background-color: #f4f4f4;
  overflow: hidden;
}

.cover-image {
  width: 100%;
  height: 100%;
  object-fit: cover; 
  display: block;
}

/* --- MOBİL UYUM --- */
@media (max-width: 1024px) {
  .split-screen-layout {
    flex-direction: column; 
  }
  .right-panel {
    display: none; 
  }
  .left-panel {
    max-width: 100%;
    padding: 20px;
  }
}

/* NEW LOGIN FORM STYLES */
.form-subtitle { text-align: center; color: var(--text-color); opacity: 0.8; margin-bottom: 20px; }
.login-form { display: flex; flex-direction: column; gap: 15px; }
.input-group {
  position: relative;
  border: 1px solid var(--border-color); border-radius: 8px;
  padding: 12px 15px; background-color: var(--card-bg);
  display: flex; align-items: center;
  transition: border-color 0.2s, background-color 0.2s;
}
.input-group input {
  border: none; outline: none; width: 100%;
  font-size: 1rem; color: var(--text-color); background: transparent;
  padding-left: 10px;
}
.input-icon { color: #aaa; font-size: 1.1rem; }
.password-eye { color: #aaa; cursor: pointer; margin-left: 10px; user-select: none; }
.password-eye:hover { color: #666; }

.register-btn {
  width: 100%; padding: 15px;
  background-color: #d1d5db; color: white; border: none; border-radius: 50px;
  font-size: 1.1rem; font-weight: 700; 
  cursor: not-allowed; transition: all 0.3s ease; margin-top: 10px;
}
.register-btn.active { background-color: #c00a00; cursor: pointer; }
.register-btn.active:hover { background-color: #a00800; }
.login-link { text-align: center; font-size: 0.95rem; color: var(--text-color); opacity: 0.8; margin-top: 15px; }
.login-link a { color: var(--text-color); text-decoration: underline; font-weight: 600; }
</style>