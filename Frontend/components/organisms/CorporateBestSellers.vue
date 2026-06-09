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
const itemsPerView = 4; 
let intervalId: ReturnType<typeof setInterval> | null = null;

const startAutoScroll = () => {
  intervalId = setInterval(() => {
    if (currentIndex.value >= props.products.length - itemsPerView) {
      currentIndex.value = 0;
    } else {
      currentIndex.value++;
    }
  }, 4000);
};

const stopAutoScroll = () => { if (intervalId) clearInterval(intervalId); };

onMounted(() => { if (props.products.length > itemsPerView) startAutoScroll(); });
onUnmounted(() => stopAutoScroll());

const trackStyle = computed(() => {
  const step = 100 / itemsPerView;
  return { transform: `translateX(-${currentIndex.value * step}%)` };
});
</script>

<template>
  <section class="corp-best-seller">
    
    <header class="section-header">
      <h2>{{ $t('home.best_sellers') }}</h2>
      
      <router-link to="/store" class="view-all-link">
        {{ $t('home.view_all') }} <span class="arrow">→</span>
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
.corp-best-seller {
  width: 100%;
  margin: 40px 0;
}

.section-header {
  display: flex;
  justify-content: space-between;
  align-items: baseline;
  margin-bottom: 25px;
  text-align: left; /* SOLA YASLI */
}

.section-header h2 {
  /* KATEGORİLER İLE AYNI STİL */
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
}
.arrow { font-size: 1.1em; }

/* --- CAROUSEL --- */
.carousel-window { width: 100%; overflow: hidden; padding: 10px 0; }
.carousel-track { display: flex; transition: transform 0.6s cubic-bezier(0.25, 1, 0.5, 1); width: 100%; }
.carousel-item { flex: 0 0 25%; max-width: 25%; padding: 0 15px; box-sizing: border-box; }

@media (max-width: 1024px) { .carousel-item { flex: 0 0 33.33%; max-width: 33.33%; } }
@media (max-width: 768px) { .carousel-item { flex: 0 0 50%; max-width: 50%; } }
</style>