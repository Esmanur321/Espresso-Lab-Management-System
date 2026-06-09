<script setup lang="ts">
import { ref, computed } from 'vue';
import { useNuxtApp } from '#app';
import { useToast } from '~/composables/useToast';

const { $t } = useNuxtApp() as any;
const { showToast } = useToast();

useHead({ title: computed(() => `${$t('header.contact')} | Espressolab`) });

const form = ref({ name: '', email: '', topic: '', message: '' });
const errors = ref<Record<string, string>>({});
const loading = ref(false);
const submitted = ref(false);

const validate = () => {
  const e: Record<string, string> = {};
  if (!form.value.name.trim()) e.name = $t('form.required');
  if (!form.value.email.trim()) {
    e.email = $t('form.required');
  } else if (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(form.value.email)) {
    e.email = $t('form.invalid_email');
  }
  if (!form.value.topic) e.topic = $t('form.required');
  if (!form.value.message.trim()) e.message = $t('form.required');
  errors.value = e;
  return Object.keys(e).length === 0;
};

const handleSubmit = async () => {
  if (!validate()) {
    showToast($t('form.fix_errors'), 'error');
    return;
  }
  loading.value = true;
  // Simulate async send (replace with real API if backend email endpoint added)
  await new Promise(r => setTimeout(r, 1200));
  loading.value = false;
  submitted.value = true;
  form.value = { name: '', email: '', topic: '', message: '' };
  errors.value = {};
  showToast($t('form.contact_success'), 'success');
};
</script>

<template>
  <main class="contact-page">
    <div class="page-hero">
      <h1>{{ $t('header.contact') }}</h1>
      <p>{{ $t('contact.hero_subtitle') }}</p>
    </div>

    <div class="content-container">
      <div class="contact-grid">
        <!-- LEFT: Info -->
        <div class="contact-info">
          <h2>{{ $t('contact.reach_title') }}</h2>
          
          <div class="info-block">
            <div class="info-icon">📍</div>
            <div>
              <h4>{{ $t('footer.address_label') }}</h4>
              <p>Espressolab Genel Müdürlük<br>Levent Mah. Büyükdere Cad. No: 193<br>Şişli / İstanbul</p>
            </div>
          </div>

          <div class="info-block">
            <div class="info-icon">📞</div>
            <div>
              <h4>{{ $t('footer.phone_label') }}</h4>
              <p><a href="tel:+902125551234">+90 212 555 12 34</a></p>
              <p><small>{{ $t('contact.hours') }}</small></p>
            </div>
          </div>

          <div class="info-block">
            <div class="info-icon">✉️</div>
            <div>
              <h4>{{ $t('footer.email_label') }}</h4>
              <p><a href="mailto:info@espressolab.com.tr">info@espressolab.com.tr</a></p>
            </div>
          </div>

          <div class="social-links">
            <h4>{{ $t('contact.social') }}</h4>
            <div class="social-icons">
              <a href="https://instagram.com/espressolab" target="_blank" class="social-icon">📷 Instagram</a>
              <a href="https://twitter.com/espressolab" target="_blank" class="social-icon">🐦 Twitter / X</a>
              <a href="https://facebook.com/espressolab" target="_blank" class="social-icon">📘 Facebook</a>
            </div>
          </div>
        </div>

        <!-- RIGHT: Form -->
        <div class="contact-form-section">
          <h2>{{ $t('contact.form_title') }}</h2>

          <!-- Success state -->
          <div v-if="submitted" class="success-banner">
            <div class="success-icon">✅</div>
            <div>
              <strong>{{ $t('form.contact_success_title') }}</strong>
              <p>{{ $t('form.contact_success_desc') }}</p>
            </div>
            <button class="reset-btn" @click="submitted = false">{{ $t('form.send_another') }}</button>
          </div>

          <form v-else class="contact-form" @submit.prevent="handleSubmit" novalidate>
            <div class="form-group">
              <label for="c-name">{{ $t('franchise.field_name') }} <span class="req">*</span></label>
              <input
                id="c-name"
                v-model="form.name"
                type="text"
                :placeholder="$t('franchise.field_name_ph')"
                class="form-input"
                :class="{ 'has-error': errors.name }"
              />
              <span v-if="errors.name" class="error-msg">{{ errors.name }}</span>
            </div>

            <div class="form-group">
              <label for="c-email">{{ $t('franchise.field_email') }} <span class="req">*</span></label>
              <input
                id="c-email"
                v-model="form.email"
                type="email"
                placeholder="ornek@email.com"
                class="form-input"
                :class="{ 'has-error': errors.email }"
              />
              <span v-if="errors.email" class="error-msg">{{ errors.email }}</span>
            </div>

            <div class="form-group">
              <label for="c-topic">{{ $t('contact.topic') }} <span class="req">*</span></label>
              <select
                id="c-topic"
                v-model="form.topic"
                class="form-input"
                :class="{ 'has-error': errors.topic }"
              >
                <option value="">—</option>
                <option value="product">{{ $t('contact.topic_product') }}</option>
                <option value="order">{{ $t('contact.topic_order') }}</option>
                <option value="complaint">{{ $t('contact.topic_complaint') }}</option>
                <option value="suggestion">{{ $t('contact.topic_suggestion') }}</option>
                <option value="other">{{ $t('contact.topic_other') }}</option>
              </select>
              <span v-if="errors.topic" class="error-msg">{{ errors.topic }}</span>
            </div>

            <div class="form-group">
              <label for="c-message">{{ $t('contact.field_message') }} <span class="req">*</span></label>
              <textarea
                id="c-message"
                v-model="form.message"
                rows="5"
                :placeholder="$t('contact.field_message_ph')"
                class="form-input form-textarea"
                :class="{ 'has-error': errors.message }"
              ></textarea>
              <span v-if="errors.message" class="error-msg">{{ errors.message }}</span>
            </div>

            <button type="submit" class="submit-btn" :disabled="loading">
              <span v-if="loading" class="spinner"></span>
              {{ loading ? $t('form.sending') : $t('contact.submit') }}
            </button>
          </form>
        </div>
      </div>
    </div>
  </main>
</template>

<style scoped>
.contact-page { background: var(--bg-color, #fff); }

.page-hero {
  background: linear-gradient(135deg, #1a1a1a 0%, #c00000 100%);
  color: #fff; text-align: center; padding: 80px 20px;
}
.page-hero h1 {
  font-size: 3rem; font-family: 'Oswald', sans-serif;
  text-transform: uppercase; letter-spacing: 3px; margin: 0 0 10px;
}
.page-hero p { font-size: 1.1rem; opacity: 0.85; margin: 0; }

.content-container { max-width: 1200px; margin: 0 auto; padding: 80px 20px; }

.contact-grid {
  display: grid; grid-template-columns: 1fr 1.4fr; gap: 60px;
}

.contact-info h2, .contact-form-section h2 {
  font-size: 1.8rem; font-family: 'Oswald', sans-serif;
  text-transform: uppercase; margin-bottom: 30px; color: var(--text-color, #222);
}

.info-block { display: flex; gap: 16px; margin-bottom: 28px; align-items: flex-start; }
.info-icon { font-size: 24px; flex-shrink: 0; }

.info-block h4 {
  font-weight: 700; margin: 0 0 6px; font-size: 14px;
  text-transform: uppercase; color: #c00000;
}
.info-block p { margin: 0 0 4px; font-size: 14px; color: var(--text-color, #555); line-height: 1.6; }
.info-block a { color: var(--text-color, #555); text-decoration: none; }
.info-block a:hover { color: #c00000; }

.social-links { margin-top: 32px; }
.social-links h4 {
  font-weight: 700; font-size: 14px; text-transform: uppercase;
  color: #c00000; margin-bottom: 12px;
}
.social-icons { display: flex; flex-direction: column; gap: 10px; }
.social-icon {
  text-decoration: none; color: var(--text-color, #555);
  font-size: 14px; display: flex; align-items: center; gap: 8px; transition: color 0.2s;
}
.social-icon:hover { color: #c00000; }

/* Form */
.contact-form { display: flex; flex-direction: column; gap: 20px; }

.form-group { display: flex; flex-direction: column; gap: 6px; }
.form-group label { font-size: 14px; font-weight: 600; color: var(--text-color, #333); }

.req { color: #c00000; }

.form-input {
  border: 1.5px solid var(--border-color, #ddd);
  border-radius: 8px; padding: 12px 16px; font-size: 14px;
  background: var(--card-bg, #fff); color: var(--text-color, #333);
  transition: border-color 0.2s; width: 100%; box-sizing: border-box;
}
.form-input:focus { outline: none; border-color: #c00000; }
.form-input.has-error { border-color: #e53e3e; background: #fff5f5; }
.form-textarea { resize: vertical; }

.error-msg { font-size: 12px; color: #e53e3e; font-weight: 500; }

.submit-btn {
  background: #c00000; color: #fff; border: none; border-radius: 50px;
  padding: 14px 48px; font-size: 15px; font-weight: 700; cursor: pointer;
  font-family: 'Oswald', sans-serif; text-transform: uppercase; letter-spacing: 1px;
  transition: background 0.2s, transform 0.15s; align-self: flex-start;
  display: flex; align-items: center; gap: 10px;
}
.submit-btn:hover:not(:disabled) { background: #a00000; transform: scale(1.03); }
.submit-btn:disabled { opacity: 0.65; cursor: not-allowed; transform: none; }

.spinner {
  width: 16px; height: 16px; border: 2px solid rgba(255,255,255,0.4);
  border-top-color: #fff; border-radius: 50%;
  animation: spin 0.7s linear infinite; display: inline-block;
}
@keyframes spin { to { transform: rotate(360deg); } }

/* Success */
.success-banner {
  display: flex; flex-direction: column; align-items: center;
  text-align: center; gap: 16px;
  background: linear-gradient(135deg, #f0fff4, #dcfce7);
  border: 1px solid #86efac; border-radius: 16px; padding: 48px 32px;
}
.success-icon { font-size: 56px; }
.success-banner strong { display: block; font-size: 1.2rem; font-weight: 700; color: #166534; margin-bottom: 6px; }
.success-banner p { color: #4a7c59; font-size: 14px; margin: 0; }
.reset-btn {
  margin-top: 8px; border: 1.5px solid #166534; background: transparent;
  color: #166534; border-radius: 50px; padding: 10px 28px;
  font-size: 14px; font-weight: 600; cursor: pointer; transition: all 0.2s;
}
.reset-btn:hover { background: #166534; color: #fff; }

@media (max-width: 768px) {
  .contact-grid { grid-template-columns: 1fr; gap: 40px; }
}
</style>
