<script setup lang="ts">
import { ref, computed, watch } from 'vue';
import { useRoute } from 'vue-router';
import ProductCard from '@/components/molecules/ProductCard.vue';
import type { IProduct } from '~/types';

const props = defineProps<{
  products: IProduct[];
}>();

const emit = defineEmits(['handleCartAdd', 'handleProductClick', 'viewAll']);

const route = useRoute();

// Grid view state
const isGridView = ref(false);

const handleViewAllClick = (event: Event) => {
  event.preventDefault();
  isGridView.value = !isGridView.value;
  if (!isGridView.value) {
    currentIndex.value = 0;
  }
  emit('viewAll');
};

// Carousel state
const currentIndex = ref(0); // ✅ Tek tek kaymak için index
const itemsToShow = 4; // Ekranda gösterilecek ürün sayısı
const scrollBy = 1; // ✅ Her seferinde 1 ürün kay

// Gösterilecek 4 ürün (currentIndex'ten başlayarak)
const visibleProducts = computed(() => {
  const start = currentIndex.value;
  const end = start + itemsToShow;
  return props.products.slice(start, end);
});

// Maksimum index (son ürüne ulaşınca başa dön)
const maxIndex = computed(() => Math.max(0, props.products.length - itemsToShow));

const nextSlide = () => {
  if (currentIndex.value < maxIndex.value) {
    currentIndex.value += scrollBy; // ✅ 1 ürün kaydır
  }
};

const prevSlide = () => {
  if (currentIndex.value > 0) {
    currentIndex.value -= scrollBy;
  }
};

// Ürünler değiştiğinde de kontrol et
watch(() => props.products.length, (newLength: number) => {
  console.log('📦 Products changed. New length:', newLength);
  currentIndex.value = 0; // ✅ Listeyi sıfırla ki boş görünmesin
});
</script>

<template>
  <section class="store-best-seller">
    
    <header class="section-header">
      <h2 class="section-title">{{ $t('home.best_sellers') }}</h2>
      <div class="header-actions" style="display: flex; align-items: center; gap: 20px;">
        <!-- Slider Controls -->
        <div v-if="!isGridView && products.length > itemsToShow" class="slider-controls" style="display: flex; gap: 8px;">
          <button @click="prevSlide" class="control-btn" :disabled="currentIndex === 0" aria-label="Previous">
            ←
          </button>
          <button @click="nextSlide" class="control-btn" :disabled="currentIndex >= maxIndex" aria-label="Next">
            →
          </button>
        </div>
        <a href="#" class="view-all-link" @click="handleViewAllClick">
          {{ isGridView ? ($t('home.view_less') || 'Daha Az Göster') : $t('home.view_all') }} <span class="arrow">→</span>
        </a>
      </div>
    </header>

    <div class="product-grid" :class="{ 'grid-view': isGridView }">
      <div v-if="isGridView" class="grid-wrapper grid-layout">
        <ProductCard 
          v-for="product in products" 
          :key="product.id"
          :product="product"
          layout="vertical"
          @addToCart="emit('handleCartAdd', $event)"
          @view="emit('handleProductClick', $event)" 
        />
      </div>
      <transition-group v-else name="slide" tag="div" class="grid-wrapper">
        <ProductCard 
          v-for="product in visibleProducts" 
          :key="product.id"
          :product="product"
          layout="horizontal"
          @addToCart="emit('handleCartAdd', $event)"
          @view="emit('handleProductClick', $event)" 
        />
      </transition-group>
    </div>

  </section>
</template>

<style scoped>
.store-best-seller {
  width: 100%;
  margin: 40px 0;
  padding: 0 10px;
}

.section-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
  padding-bottom: 10px;
}

.section-title {
  font-size: 24px;
  font-weight: 700;
  color: var(--text-color, #000);
  text-transform: uppercase;
  margin: 0;
  font-family: 'Oswald', sans-serif;
  letter-spacing: 0.5px;
}

.view-all-link {
  text-decoration: none;
  font-size: 14px;
  font-weight: 700;
  color: #c00a00;
  display: flex;
  align-items: center;
  gap: 5px;
  transition: opacity 0.3s;
}

.view-all-link:hover {
  opacity: 0.8;
}

.arrow {
  font-size: 18px;
  line-height: 1;
  margin-bottom: 2px;
}

.product-grid {
  position: relative;
  overflow: hidden;
  min-height: 400px;
}

.grid-wrapper {
  display: grid;
  grid-template-columns: repeat(4, 1fr); 
  gap: 20px;
}

.grid-layout {
  display: grid !important;
  grid-template-columns: repeat(4, 1fr) !important;
  gap: 20px !important;
  position: static !important;
}

.control-btn {
  background: transparent;
  border: 1px solid var(--border-color, #ccc);
  color: var(--text-color, #333);
  width: 36px;
  height: 36px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  font-size: 16px;
  font-weight: 700;
  transition: all 0.2s ease;
}
.control-btn:hover:not(:disabled) {
  background-color: var(--border-color, #eee);
  border-color: var(--text-color, #333);
}
.control-btn:disabled {
  opacity: 0.3;
  cursor: not-allowed;
}

/* Slide Transition (Sağdan Sola - Daha Akıcı) */
/* --- "ŞERİT GİBİ" GEÇİŞ ANİMASYONU --- */
.slide-enter-active,
.slide-leave-active,
.slide-move {
  transition: all 1.0s ease; /* Daha yavaş ve "normal" akış */
}

/* Giden eleman (Sola kayar ve kaybolur) */
.slide-leave-active {
  position: absolute; /* ÖNEMLİ: Diğerlerinin kaymasını tetikler */
  top: 0;
  left: 0;
  width: calc(25% - 15px);
  z-index: 0;
}

.slide-leave-to {
  opacity: 0;
  transform: translateX(-10000%); /* Daha az mesafe (-120% yerine -100%) */
}

/* Gelen eleman (Sağdan girer) */
.slide-enter-from {
  opacity: 0;
  transform: translateX(100%); /* Simetrik giriş */
}

.slide-enter-to,
.slide-leave-from {
  opacity: 1;
  transform: translateX(0);
}

/* Diğer elemanların sıralanması */
.grid-wrapper {
  position: relative; /* Absolute eleman için referans */
}

/* MOBİL UYUM */
@media (max-width: 1024px) {
  .grid-wrapper { grid-template-columns: repeat(2, 1fr); }
  .grid-layout { grid-template-columns: repeat(2, 1fr) !important; }
  
  /* Tablette giden eleman genişliği */
  .slide-leave-active {
    width: calc(50% - 10px); /* (100% - 20px) / 2 */
  }
}

@media (max-width: 600px) {
  .grid-wrapper { grid-template-columns: 1fr; }
  .grid-layout { grid-template-columns: 1fr !important; }
  .section-header { flex-direction: row; align-items: center; }
  .section-title { font-size: 20px; }
  
  /* Mobilde giden eleman genişliği */
  .slide-leave-active {
    width: 100%;
  }
}
</style>