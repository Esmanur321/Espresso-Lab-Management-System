<script setup lang="ts">
import { computed } from 'vue';
import { useNuxtApp } from '#app';
const { $t } = useNuxtApp() as any;

useHead({
  title: computed(() => `${$t('header.coffee_and_us')} | Espressolab`),
  meta: [{ name: 'description', content: 'Espressolab\'in kahveye olan tutkusu, hikayesi ve değerleri.' }]
});
</script>

<template>
  <main class="info-page">
    <div class="hero-section">
      <div class="hero-overlay">
        <h1 class="hero-title">{{ $t('header.coffee_and_us') }}</h1>
        <p class="hero-subtitle">{{ $t('about.hero_subtitle') }}</p>
      </div>
    </div>

    <div class="content-container">
      <section class="story-section">
        <div class="section-grid">
          <div class="text-block">
            <h2>{{ $t('about.story_title') }}</h2>
            <p>{{ $t('about.story_p1') }}</p>
            <p>{{ $t('about.story_p2') }}</p>
          </div>
          <div class="image-block">
            <img src="https://images.unsplash.com/photo-1497935586351-b67a49e012bf?q=80&w=800&auto=format&fit=crop" alt="Kahve ve Biz" class="section-image" />
          </div>
        </div>
      </section>

      <section class="values-section">
        <h2 class="values-title">{{ $t('about.values_title') }}</h2>
        <div class="values-grid">
          <div class="value-card">
            <div class="value-icon">☕</div>
            <h3>{{ $t('about.val1_title') }}</h3>
            <p>{{ $t('about.val1_desc') }}</p>
          </div>
          <div class="value-card">
            <div class="value-icon">🌱</div>
            <h3>{{ $t('about.val2_title') }}</h3>
            <p>{{ $t('about.val2_desc') }}</p>
          </div>
          <div class="value-card">
            <div class="value-icon">🤝</div>
            <h3>{{ $t('about.val3_title') }}</h3>
            <p>{{ $t('about.val3_desc') }}</p>
          </div>
          <div class="value-card">
            <div class="value-icon">🔬</div>
            <h3>{{ $t('about.val4_title') }}</h3>
            <p>{{ $t('about.val4_desc') }}</p>
          </div>
        </div>
      </section>
    </div>
  </main>
</template>

<style scoped>
.info-page { background: var(--bg-color, #fff); }

.hero-section {
  height: 50vh;
  background: url('https://images.unsplash.com/photo-1447933601403-0c6688de566e?q=80&w=1600&auto=format&fit=crop') center/cover no-repeat;
  position: relative;
  display: flex;
  align-items: center;
  justify-content: center;
}

.hero-overlay {
  background: rgba(0,0,0,0.5);
  inset: 0;
  position: absolute;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  gap: 12px;
  padding: 20px;
}

.hero-title {
  color: #fff;
  font-size: 3rem;
  font-family: 'Oswald', sans-serif;
  text-transform: uppercase;
  letter-spacing: 3px;
  text-align: center;
  margin: 0;
}

.hero-subtitle {
  color: rgba(255,255,255,0.85);
  font-size: 1.2rem;
  margin: 0;
  text-align: center;
}

.content-container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 60px 20px;
}

.story-section { margin-bottom: 80px; }

.section-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 60px;
  align-items: center;
}

.text-block h2 {
  font-size: 2rem;
  font-family: 'Oswald', sans-serif;
  color: #c00000;
  margin-bottom: 20px;
  text-transform: uppercase;
}

.text-block p {
  color: var(--text-color, #555);
  line-height: 1.8;
  margin-bottom: 16px;
  font-size: 16px;
}

.section-image {
  width: 100%;
  border-radius: 16px;
  object-fit: cover;
  height: 400px;
  box-shadow: 0 20px 60px rgba(0,0,0,0.12);
}

.values-title {
  font-size: 2.2rem;
  font-family: 'Oswald', sans-serif;
  text-transform: uppercase;
  text-align: center;
  margin-bottom: 50px;
  color: var(--text-color, #222);
}

.values-grid {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 30px;
}

.value-card {
  background: var(--card-bg, #f9f9f9);
  border-radius: 16px;
  padding: 30px 24px;
  text-align: center;
  border: 1px solid var(--border-color, #eee);
  transition: transform 0.3s, box-shadow 0.3s;
}

.value-card:hover {
  transform: translateY(-8px);
  box-shadow: 0 20px 40px rgba(0,0,0,0.08);
}

.value-icon { font-size: 40px; margin-bottom: 16px; }

.value-card h3 {
  font-size: 1.1rem;
  font-weight: 700;
  margin-bottom: 10px;
  color: var(--text-color, #222);
}

.value-card p {
  font-size: 14px;
  color: #777;
  line-height: 1.6;
}

@media (max-width: 768px) {
  .hero-title { font-size: 2rem; }
  .section-grid { grid-template-columns: 1fr; }
  .values-grid { grid-template-columns: repeat(2, 1fr); }
}
</style>
