<script setup lang="ts">
import { computed } from 'vue';
import { useNuxtApp } from '#app';
const { $t } = useNuxtApp() as any;

useHead({ title: computed(() => `${$t('header.stores')} | Espressolab`) });

const stores = [
  { city: 'İstanbul', name: 'Espressolab Nişantaşı', address: 'Teşvikiye Mah. Vali Konağı Cad. No:45', phone: '+90 212 555 01 01', hours: '07:00 - 23:00' },
  { city: 'İstanbul', name: 'Espressolab Kadıköy', address: 'Moda Cad. No:22, Kadıköy', phone: '+90 216 555 02 02', hours: '07:00 - 22:00' },
  { city: 'İstanbul', name: 'Espressolab Beşiktaş', address: 'Barbaros Bulvarı No:66, Beşiktaş', phone: '+90 212 555 03 03', hours: '08:00 - 22:00' },
  { city: 'Ankara', name: 'Espressolab Çankaya', address: 'Tunalı Hilmi Cad. No:55, Çankaya', phone: '+90 312 555 04 04', hours: '07:30 - 21:30' },
  { city: 'Ankara', name: 'Espressolab Kızılay', address: 'Atatürk Bulvarı No:112, Kızılay', phone: '+90 312 555 05 05', hours: '08:00 - 22:00' },
  { city: 'İzmir', name: 'Espressolab Alsancak', address: 'Kıbrıs Şehitleri Cad. No:88, Alsancak', phone: '+90 232 555 06 06', hours: '07:00 - 23:00' },
];
</script>

<template>
  <main class="stores-page">
    <div class="page-hero">
      <h1>{{ $t('header.stores') }}</h1>
      <p>{{ $t('stores.hero_subtitle') }}</p>
    </div>

    <div class="content-container">
      <div class="stores-grid">
        <div v-for="store in stores" :key="store.name" class="store-card">
          <div class="store-city-badge">{{ store.city }}</div>
          <h3 class="store-name">{{ store.name }}</h3>
          <div class="store-detail">
            <span class="detail-icon">📍</span>
            <span>{{ store.address }}</span>
          </div>
          <div class="store-detail">
            <span class="detail-icon">📞</span>
            <span>{{ store.phone }}</span>
          </div>
          <div class="store-detail">
            <span class="detail-icon">🕐</span>
            <span>{{ store.hours }}</span>
          </div>
          <a :href="`https://maps.google.com/?q=${encodeURIComponent(store.address)}`" target="_blank" class="map-btn">
            {{ $t('stores.map_btn') }}
          </a>
        </div>
      </div>
    </div>
  </main>
</template>

<style scoped>
.stores-page { background: var(--bg-color, #fff); }

.page-hero {
  background: linear-gradient(135deg, #1a1a1a 0%, #c00000 100%);
  color: #fff;
  text-align: center;
  padding: 80px 20px;
}

.page-hero h1 {
  font-size: 3rem;
  font-family: 'Oswald', sans-serif;
  text-transform: uppercase;
  letter-spacing: 3px;
  margin: 0 0 10px;
}

.page-hero p { font-size: 1.1rem; opacity: 0.85; margin: 0; }

.content-container { max-width: 1200px; margin: 0 auto; padding: 60px 20px; }

.stores-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 24px;
}

.store-card {
  background: var(--card-bg, #fff);
  border: 1px solid var(--border-color, #eee);
  border-radius: 16px;
  padding: 28px;
  transition: transform 0.3s, box-shadow 0.3s;
}

.store-card:hover {
  transform: translateY(-6px);
  box-shadow: 0 16px 40px rgba(0,0,0,0.1);
}

.store-city-badge {
  display: inline-block;
  background: #fff0f0;
  color: #c00000;
  border: 1px solid #fcc;
  border-radius: 20px;
  padding: 3px 12px;
  font-size: 12px;
  font-weight: 700;
  margin-bottom: 12px;
}

.store-name {
  font-size: 1.1rem;
  font-weight: 800;
  color: var(--text-color, #222);
  margin: 0 0 16px;
  font-family: 'Oswald', sans-serif;
}

.store-detail {
  display: flex;
  align-items: flex-start;
  gap: 10px;
  margin-bottom: 10px;
  font-size: 14px;
  color: #666;
  line-height: 1.5;
}

.detail-icon { flex-shrink: 0; }

.map-btn {
  display: inline-block;
  margin-top: 16px;
  color: #c00000;
  font-weight: 700;
  font-size: 13px;
  text-decoration: none;
  border: 1px solid #c00000;
  border-radius: 50px;
  padding: 6px 18px;
  transition: all 0.2s;
}

.map-btn:hover { background: #c00000; color: #fff; }

@media (max-width: 900px) { .stores-grid { grid-template-columns: repeat(2, 1fr); } }
@media (max-width: 600px) { .stores-grid { grid-template-columns: 1fr; } }
</style>
