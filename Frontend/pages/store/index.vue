<script setup lang="ts">
import { ref, onMounted, computed, watch } from 'vue';
import { useProductStore } from '~/stores/products';
import { useCartStore } from '~/stores/cart';
import { useRouter, useRoute } from 'vue-router';
import type { IProduct } from '~/types';

const productStore = useProductStore();
const cartStore = useCartStore();
const router = useRouter();
const route = useRoute();

// Verileri çek
onMounted(() => {
  productStore.fetchProducts();
});

import { useNuxtApp } from '#app';
import { useToast } from '~/composables/useToast';
const { $t, $locale } = useNuxtApp() as any;
const { showToast } = useToast();

// --- SLIDER ---
const sliderData = computed(() => {
  return [
    { imgUrl: '/images/1tıkla-kapında.jpg', alt: $t('slider.campaign1') },
    { imgUrl: '/images/atıştırmalık.jpg', alt: $t('slider.campaign2') },
    { imgUrl: '/images/costa-rica-la-lia.jpg', alt: $t('slider.campaign3') },
    { imgUrl: '/images/kapsül-kahve.jpg', alt: $t('slider.campaign4') },
    { imgUrl: '/images/termos.jpg', alt: $t('slider.campaign5') }
  ];
});

// --- KATEGORİLER ---
const categoryData = computed(() => [
  { id: 'coffee', title: $t('cat.coffee'), image: '/images/KatKahve.png' },
  { id: 'thermos', title: $t('cat.thermos'), image: '/images/KatTermos.png' },
  { id: 'accessories', title: $t('cat.accessories'), image: '/images/KatAksesuar.png' },
  { id: 'teas', title: $t('cat.teas'), image: '/images/KatÇay.png' },
  { id: 'snacks', title: $t('cat.snacks'), image: '/images/KatAtıştır.png' }
]);

const searchQuery = ref((route.query.search as string) || '');

// Watch for URL search param changes
watch(() => route.query.search, (val) => {
  searchQuery.value = (val as string) || '';
});

const selectedCategory = ref('');

// --- ÇOK SATANLAR (Canlı Veri + Arama) ---
const bestSellers = computed(() => {
  let products = productStore.products;
  if (selectedCategory.value) {
    products = productStore.getProductsByCategory(selectedCategory.value);
  }
  if (searchQuery.value.trim()) {
    const q = searchQuery.value.toLowerCase();
    products = products.filter(p => 
      p.name.toLowerCase().includes(q) || 
      (p.categoryId && p.categoryId.toLowerCase().includes(q))
    );
  }
  return products;
});

const handleCategorySelect = (cat: any) => {
  selectedCategory.value = cat.id;
};

const handleViewAll = () => {
  selectedCategory.value = '';
};

// --- METOTLAR ---
const handleAddToCart = (product: IProduct) => { 
  cartStore.addToCart(product);
  showToast(`${product.name} ${$t('cart.added_to_cart')}`, 'success'); 
};
const goToProductDetail = (product: IProduct) => { router.push(`/product/${product.id}`); };
</script>

<template>
  <div style="background-color: var(--bg-color); color: var(--text-color); width: 100%; transition: background-color 0.3s, color 0.3s;">
    <main class="main-content-container">
      
      <div class="store-slider-wrapper">
        <StoreSlider :slides="sliderData" />
      </div>

      <div class="categories-wrapper">
        <CategoryList :categories="categoryData" @selectCategory="handleCategorySelect" />
      </div>
      
      <StoreBestSellers 
        :products="bestSellers" 
        @handleCartAdd="handleAddToCart"
        @handleProductClick="goToProductDetail"
        @viewAll="handleViewAll"
      />
      
    </main>
  </div>


</template>

<style scoped>
.main-content-container {
  max-width: 1200px; 
  margin: 0 auto;    
  padding: 0 20px;   
  padding-bottom: 60px;
}

.store-slider-wrapper {
  margin-top: 20px;
  margin-bottom: 50px;
}

.categories-wrapper {
  margin-bottom: 50px;
}
</style>