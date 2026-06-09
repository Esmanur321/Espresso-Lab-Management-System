<script setup lang="ts">
import { computed } from 'vue';
import { useNuxtApp } from '#app';
const { $t } = useNuxtApp() as any;
useHead({ title: computed(() => `${$t('legal.kvkk_title')} | Espressolab`) });
</script>

<template>
  <main class="legal-page">
    <div class="page-hero">
      <h1>{{ $t('legal.kvkk_title') }}</h1>
    </div>
    <div class="legal-container">
      <div class="legal-card">
        <p class="last-update">{{ $t('legal.last_update') }}: 01.01.2024</p>

        <h2>{{ $t('legal.kvkk_s1') }}</h2>
        <p>{{ $t('legal.kvkk_s1_text') }}</p>

        <h2>{{ $t('legal.kvkk_s2') }}</h2>
        <p>{{ $t('legal.kvkk_s2_text') }}</p>

        <h2>{{ $t('legal.kvkk_s3') }}</h2>
        <p>{{ $t('legal.kvkk_s3_text') }}</p>

        <h2>{{ $t('legal.kvkk_s4') }}</h2>
        <p>{{ $t('legal.kvkk_s4_text') }}</p>

        <h2>{{ $t('legal.kvkk_s5') }}</h2>
        <p>{{ $t('legal.kvkk_s5_text') }}</p>

        <div class="contact-box">
          <strong>{{ $t('legal.contact_title') }}</strong>
          <p>Espressolab Gıda A.Ş.<br>
          Levent Mah. Büyükdere Cad. No:193 Şişli / İstanbul<br>
          kvkk@espressolab.com.tr</p>
        </div>
      </div>
    </div>
  </main>
</template>

<style scoped>
.legal-page { background: var(--bg-color, #fff); min-height: 80vh; }

.page-hero {
  background: linear-gradient(135deg, #1a1a1a 0%, #c00000 100%);
  color: #fff;
  text-align: center;
  padding: 60px 20px;
}

.page-hero h1 {
  font-size: 2.2rem;
  font-family: 'Oswald', sans-serif;
  text-transform: uppercase;
  letter-spacing: 2px;
  margin: 0;
}

.legal-container { max-width: 860px; margin: 0 auto; padding: 60px 20px; }

.legal-card {
  background: var(--card-bg, #fff);
  border: 1px solid var(--border-color, #eee);
  border-radius: 16px;
  padding: 48px;
}

.last-update {
  font-size: 13px;
  color: #999;
  margin-bottom: 32px;
}

h2 {
  font-family: 'Oswald', sans-serif;
  font-size: 1.1rem;
  color: #c00000;
  text-transform: uppercase;
  margin: 32px 0 10px;
  letter-spacing: 0.5px;
}

p {
  font-size: 14px;
  color: var(--text-color, #555);
  line-height: 1.8;
  margin: 0;
}

.contact-box {
  margin-top: 40px;
  padding: 24px;
  background: #fff8f8;
  border-radius: 12px;
  border-left: 4px solid #c00000;
}

.contact-box strong {
  display: block;
  font-size: 14px;
  font-weight: 700;
  margin-bottom: 8px;
  color: #c00000;
  text-transform: uppercase;
}

.contact-box p { color: #555; }
</style>
