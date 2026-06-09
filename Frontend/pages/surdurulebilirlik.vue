<script setup lang="ts">
import { computed } from 'vue';
import { useNuxtApp } from '#app';
const { $t } = useNuxtApp() as any;

useHead({
  title: computed(() => `${$t('header.sustainability')} | Espressolab`),
});

const commitments = computed(() => [
  { icon: '🌿', titleKey: 'sustain.c1_title', descKey: 'sustain.c1_desc' },
  { icon: '☕', titleKey: 'sustain.c2_title', descKey: 'sustain.c2_desc' },
  { icon: '💧', titleKey: 'sustain.c3_title', descKey: 'sustain.c3_desc' },
  { icon: '♻️', titleKey: 'sustain.c4_title', descKey: 'sustain.c4_desc' },
  { icon: '🌍', titleKey: 'sustain.c5_title', descKey: 'sustain.c5_desc' },
  { icon: '👩‍🌾', titleKey: 'sustain.c6_title', descKey: 'sustain.c6_desc' },
]);
</script>

<template>
  <main class="sustainability-page">
    <div class="page-hero">
      <div class="hero-content">
        <div class="hero-badge">{{ $t('sustain.hero_badge') }}</div>
        <h1>{{ $t('sustain.hero_title') }}</h1>
        <p>{{ $t('sustain.hero_desc') }}</p>
      </div>
    </div>

    <div class="content-container">
      <section class="mission-section">
        <div class="mission-text">
          <h2>{{ $t('sustain.mission_title') }}</h2>
          <p>{{ $t('sustain.mission_p1') }}</p>
          <p>{{ $t('sustain.mission_p2') }}</p>
        </div>
        <div class="mission-stats">
          <div class="stat-item">
            <span class="stat-number">80%</span>
            <span class="stat-label">{{ $t('sustain.c4_title') }}</span>
          </div>
          <div class="stat-item">
            <span class="stat-number">30%</span>
            <span class="stat-label">{{ $t('sustain.c3_title') }}</span>
          </div>
          <div class="stat-item">
            <span class="stat-number">100%</span>
            <span class="stat-label">{{ $t('sustain.c2_title') }}</span>
          </div>
        </div>
      </section>

      <section class="commitments-section">
        <h2 class="section-title">{{ $t('sustain.commit_title') }}</h2>
        <div class="commitments-grid">
          <div v-for="item in commitments" :key="item.titleKey" class="commitment-card">
            <div class="commitment-icon">{{ item.icon }}</div>
            <h3>{{ $t(item.titleKey) }}</h3>
            <p>{{ $t(item.descKey) }}</p>
          </div>
        </div>
      </section>
    </div>
  </main>
</template>

<style scoped>
.sustainability-page { background: var(--bg-color, #fff); }

.page-hero {
  background: linear-gradient(135deg, #1a5c2a 0%, #2d8a44 50%, #1a5c2a 100%);
  color: #fff;
  text-align: center;
  padding: 100px 20px;
  position: relative;
  overflow: hidden;
}

.page-hero::before {
  content: '';
  position: absolute;
  inset: 0;
  background: url('/images/slider3.jpg') center/cover no-repeat;
  opacity: 0.15;
}

.hero-content { position: relative; z-index: 1; }

.hero-badge {
  display: inline-block;
  background: rgba(255,255,255,0.2);
  border: 1px solid rgba(255,255,255,0.4);
  border-radius: 50px;
  padding: 6px 20px;
  font-size: 14px;
  margin-bottom: 20px;
}

.page-hero h1 {
  font-size: 3.5rem;
  font-family: 'Oswald', sans-serif;
  margin: 0 0 16px;
}

.page-hero p {
  font-size: 1.2rem;
  opacity: 0.9;
  max-width: 600px;
  margin: 0 auto;
  line-height: 1.6;
}

.content-container { max-width: 1200px; margin: 0 auto; padding: 80px 20px; }

.mission-section {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 60px;
  align-items: center;
  margin-bottom: 80px;
}

.mission-text h2 {
  font-size: 2rem;
  font-family: 'Oswald', sans-serif;
  color: #2d8a44;
  margin-bottom: 20px;
  text-transform: uppercase;
}

.mission-text p {
  color: var(--text-color, #555);
  line-height: 1.8;
  margin-bottom: 16px;
  font-size: 16px;
}

.mission-stats { display: flex; flex-direction: column; gap: 24px; }

.stat-item {
  display: flex;
  flex-direction: column;
  background: linear-gradient(135deg, #f0fff4, #dcfce7);
  border-radius: 16px;
  padding: 24px;
  border-left: 4px solid #2d8a44;
}

.stat-number {
  font-size: 2.5rem;
  font-weight: 900;
  color: #2d8a44;
  font-family: 'Oswald', sans-serif;
}

.stat-label { font-size: 14px; color: #555; font-weight: 600; }

.section-title {
  font-size: 2.2rem;
  font-family: 'Oswald', sans-serif;
  text-transform: uppercase;
  text-align: center;
  margin-bottom: 50px;
  color: var(--text-color, #222);
}

.commitments-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 24px;
}

.commitment-card {
  background: var(--card-bg, #f9f9f9);
  border-radius: 16px;
  padding: 32px 24px;
  border: 1px solid var(--border-color, #eee);
  transition: transform 0.3s, box-shadow 0.3s;
}

.commitment-card:hover {
  transform: translateY(-6px);
  box-shadow: 0 16px 40px rgba(0,0,0,0.08);
}

.commitment-icon { font-size: 36px; margin-bottom: 16px; }
.commitment-card h3 { font-size: 1.05rem; font-weight: 700; margin-bottom: 10px; color: var(--text-color, #222); }
.commitment-card p { font-size: 14px; color: #777; line-height: 1.7; }

@media (max-width: 768px) {
  .mission-section { grid-template-columns: 1fr; }
  .commitments-grid { grid-template-columns: repeat(2, 1fr); }
}
@media (max-width: 500px) { .commitments-grid { grid-template-columns: 1fr; } }
</style>
