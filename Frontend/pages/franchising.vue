<script setup lang="ts">
import { computed } from 'vue';
import { useNuxtApp } from '#app';
const { $t } = useNuxtApp() as any;

useHead({ title: computed(() => `${$t('header.franchising')} | Espressolab`) });

const benefits = [
  { icon: '🏆', titleKey: 'franchise.b1_title', descKey: 'franchise.b1_desc' },
  { icon: '📚', titleKey: 'franchise.b2_title', descKey: 'franchise.b2_desc' },
  { icon: '📈', titleKey: 'franchise.b3_title', descKey: 'franchise.b3_desc' },
  { icon: '💼', titleKey: 'franchise.b4_title', descKey: 'franchise.b4_desc' },
];
</script>

<template>
  <main class="franchise-page">
    <div class="page-hero">
      <h1>{{ $t('header.franchising') }}</h1>
      <p>{{ $t('franchise.hero_subtitle') }}</p>
    </div>

    <div class="content-container">
      <div class="intro-section">
        <h2>{{ $t('franchise.why_title') }}</h2>
        <div class="benefits-grid">
          <div v-for="b in benefits" :key="b.titleKey" class="benefit-item">
            <div class="benefit-icon">{{ b.icon }}</div>
            <h3>{{ $t(b.titleKey) }}</h3>
            <p>{{ $t(b.descKey) }}</p>
          </div>
        </div>
      </div>

      <div class="contact-section">
        <h2>{{ $t('franchise.form_title') }}</h2>
        <p class="contact-desc">{{ $t('franchise.form_desc') }}</p>
        <form class="franchise-form" @submit.prevent>
          <div class="form-row">
            <div class="form-group">
              <label>{{ $t('franchise.field_name') }}</label>
              <input type="text" :placeholder="$t('franchise.field_name_ph')" class="form-input" />
            </div>
            <div class="form-group">
              <label>{{ $t('franchise.field_email') }}</label>
              <input type="email" placeholder="ornek@email.com" class="form-input" />
            </div>
          </div>
          <div class="form-row">
            <div class="form-group">
              <label>{{ $t('franchise.field_phone') }}</label>
              <input type="tel" placeholder="+90 5xx xxx xx xx" class="form-input" />
            </div>
            <div class="form-group">
              <label>{{ $t('franchise.field_city') }}</label>
              <input type="text" :placeholder="$t('franchise.field_city_ph')" class="form-input" />
            </div>
          </div>
          <div class="form-group">
            <label>{{ $t('franchise.field_message') }}</label>
            <textarea rows="4" :placeholder="$t('franchise.field_message_ph')" class="form-input form-textarea"></textarea>
          </div>
          <button type="submit" class="submit-btn">{{ $t('franchise.submit') }}</button>
        </form>
      </div>
    </div>
  </main>
</template>

<style scoped>
.franchise-page { background: var(--bg-color, #fff); }

.page-hero {
  background: linear-gradient(135deg, #c00000 0%, #800000 100%);
  color: #fff;
  text-align: center;
  padding: 100px 20px;
}

.page-hero h1 {
  font-size: 3.5rem;
  font-family: 'Oswald', sans-serif;
  text-transform: uppercase;
  margin: 0 0 16px;
  letter-spacing: 3px;
}

.page-hero p { font-size: 1.2rem; opacity: 0.9; margin: 0; }

.content-container { max-width: 1200px; margin: 0 auto; padding: 80px 20px; }

.intro-section { margin-bottom: 80px; }

.intro-section h2 {
  font-size: 2.2rem;
  font-family: 'Oswald', sans-serif;
  text-transform: uppercase;
  text-align: center;
  margin-bottom: 50px;
  color: var(--text-color, #222);
}

.benefits-grid {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 24px;
}

.benefit-item {
  background: var(--card-bg, #f9f9f9);
  border-radius: 16px;
  padding: 32px 24px;
  text-align: center;
  border: 1px solid var(--border-color, #eee);
  transition: transform 0.3s, box-shadow 0.3s;
}

.benefit-item:hover {
  transform: translateY(-6px);
  box-shadow: 0 16px 40px rgba(0,0,0,0.08);
}

.benefit-icon { font-size: 40px; margin-bottom: 16px; }

.benefit-item h3 { font-weight: 700; font-size: 1.05rem; margin-bottom: 10px; color: var(--text-color, #222); }
.benefit-item p { font-size: 14px; color: #777; line-height: 1.6; }

.contact-section h2 {
  font-size: 2rem;
  font-family: 'Oswald', sans-serif;
  text-transform: uppercase;
  margin-bottom: 10px;
  color: var(--text-color, #222);
}

.contact-desc { color: #777; margin-bottom: 40px; font-size: 16px; }

.franchise-form { max-width: 800px; }

.form-row { display: grid; grid-template-columns: 1fr 1fr; gap: 20px; margin-bottom: 20px; }

.form-group { display: flex; flex-direction: column; gap: 6px; margin-bottom: 20px; }
.form-group label { font-size: 14px; font-weight: 600; color: var(--text-color, #333); }

.form-input {
  border: 1px solid var(--border-color, #ddd);
  border-radius: 8px;
  padding: 12px 16px;
  font-size: 14px;
  background: var(--card-bg, #fff);
  color: var(--text-color, #333);
  transition: border-color 0.2s;
  width: 100%;
  box-sizing: border-box;
}

.form-input:focus { outline: none; border-color: #c00000; }
.form-textarea { resize: vertical; }

.submit-btn {
  background: #c00000;
  color: #fff;
  border: none;
  border-radius: 50px;
  padding: 14px 48px;
  font-size: 15px;
  font-weight: 700;
  cursor: pointer;
  font-family: 'Oswald', sans-serif;
  text-transform: uppercase;
  letter-spacing: 1px;
  transition: background 0.2s, transform 0.15s;
}

.submit-btn:hover { background: #a00000; transform: scale(1.03); }

@media (max-width: 768px) {
  .benefits-grid { grid-template-columns: repeat(2, 1fr); }
  .form-row { grid-template-columns: 1fr; }
}
</style>
