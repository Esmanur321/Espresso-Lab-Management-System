<script setup lang="ts">
import { ref, onMounted, onUnmounted, computed } from 'vue';
import ProductCard from '@/components/molecules/ProductCard.vue';
import type { IProduct } from '~/types';

const props = defineProps<{
  products: IProduct[];
}>();

const emit = defineEmits(['handleCartAdd', 'handleProductClick']);

// --- CAROUSEL MANTIĞI ---
const currentIndex = ref(0);
const itemsPerView = 4; // Ekranda 4 ürün görünsün
let intervalId: ReturnType<typeof setInterval> | null = null;

// Otomatik Kaydırma
const startAutoScroll = () => {
  intervalId = setInterval(() => {
    if (currentIndex.value >= props.products.length - itemsPerView) {
      currentIndex.value = 0;
    } else {
      currentIndex.value++;
    }
  }, 4000); // 4 saniyede bir kayar
};

const stopAutoScroll = () => { if (intervalId) clearInterval(intervalId); };

onMounted(() => { 
  if (props.products.length > itemsPerView) startAutoScroll(); 
});
onUnmounted(() => stopAutoScroll());

// Kaydırma Stili
const trackStyle = computed(() => {
  const step = 100 / itemsPerView;
  return { transform: `translateX(-${currentIndex.value * step}%)` };
});
</script>

<template>
  <section class="store-best-seller">
    
    <header class="section-header">
      <h2>ÇOK SATANLAR</h2>
      
      <router-link to="/store" class="view-all-link">
        Tümünü Görüntüle <span class="arrow">→</span>
      </router-link>
    </header>

    <div 
      class="carousel-window" 
      @mouseenter="stopAutoScroll" 
      @mouseleave="startAutoScroll"
    >
      <div class="carousel-track" :style="trackStyle">
        <div 
          v-for="product in products" 
          :key="product.id"
          class="carousel-item"
        >
          <ProductCard 
            :product="product"
            @addToCart="emit('handleCartAdd', $event)"
            @view="emit('handleProductClick', $event)" 
          />
        </div>
      </div>
    </div>

  </section>
</template>

<style scoped>
.store-best-seller {
  width: 100%;
  margin: 40px 0;
}

/* BAŞLIK ALANI */
.section-header {
  display: flex;
  justify-content: space-between;
  align-items: baseline;
  margin-bottom: 25px;
  text-align: left;
}

.section-header h2 {
  font-size: 20px;       
  font-weight: 700;      
  color: #4D525A;
  font-family: 'Bebas Kai', 'Inter', sans-serif;
  text-transform: uppercase;
  margin: 0;
  letter-spacing: 0.5px;
}

.view-all-link {
  text-decoration: none;
  color: #c00a00;
  font-size: 14px;
  font-weight: 700;
  transition: color 0.2s;
}
.view-all-link:hover { color: #a00a00; }
.arrow { font-size: 1.1em; }

/* --- CAROUSEL STİLLERİ --- */
.carousel-window {
  width: 100%;
  overflow: hidden; /* Dışarı taşanı gizle */
  padding: 10px 0;  /* Gölge payı */
}

.carousel-track {
  display: flex;
  transition: transform 0.6s cubic-bezier(0.25, 1, 0.5, 1);
  width: 100%;
}

.carousel-item {
  /* 4'lü görünüm için %25 genişlik */
  flex: 0 0 25%; 
  max-width: 25%;
  padding: 0 15px; /* Kartlar arası boşluk */
  box-sizing: border-box;
}

/* Mobil uyum */
@media (max-width: 1024px) { .carousel-item { flex: 0 0 33.33%; max-width: 33.33%; } }
@media (max-width: 768px) { .carousel-item { flex: 0 0 50%; max-width: 50%; } }
@media (max-width: 480px) { .carousel-item { flex: 0 0 100%; max-width: 100%; } }
</style>