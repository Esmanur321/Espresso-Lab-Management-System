<script setup lang="ts">
import { ref, onMounted, computed } from 'vue';
import { useRouter } from 'vue-router';
import { useAuthStore } from '~/stores/auth';
import { useProductStore } from '~/stores/products'; // EKLENDİ
import { useCartStore } from '~/stores/cart'; // EKLENDİ
import type { IProduct } from '~/types';

const store = useAuthStore();
const productStore = useProductStore(); // EKLENDİ
const cartStore = useCartStore(); // EKLENDİ

// Verileri çek
onMounted(() => {
  productStore.fetchProducts();
});


import CorporateSlider from '@/components/organisms/CorporateSlider.vue'; 
import CorporateBestSellers from '@/components/organisms/CorporateBestSellers.vue'; 


const router = useRouter();

import { useNuxtApp } from '#app';
import { useToast } from '~/composables/useToast';
const { $t, $locale } = useNuxtApp() as any;
const { showToast } = useToast();

const corporateSlides = computed(() => {
  return [
    { imgUrl: '/images/Slider.jpg', alt: $t('slider.corporate') },
    { imgUrl: '/images/slider2.jpg', alt: $t('slider.coffee_passion') },
    { imgUrl: '/images/slider3.jpg', alt: $t('slider.coffee_passion') },
    { imgUrl: '/images/slider4.jpg', alt: $t('slider.coffee_passion') },
    { imgUrl: '/images/slider5.jpg', alt: $t('slider.coffee_passion') }
  ];
});

// --- ÇOK SATANLAR (Canlı Veri) ---
const bestSellers = computed(() => productStore.products);



const handleAddToCart = (product: IProduct) => { 
  cartStore.addToCart(product);
  showToast(`${product.name} ${$t('cart.added_to_cart')}`, 'success'); 
};
const goToProductDetail = (product: IProduct) => { router.push(`/product/${product.id}`); };
</script>

<template>
  <div class="corporate-page">

    <div class="fullscreen-slider">
      <CorporateSlider :slides="corporateSlides" />
    </div>

    <div class="products-section">
      <CorporateBestSellers 
        :products="bestSellers" 
        @handleCartAdd="handleAddToCart"
        @handleProductClick="goToProductDetail" 
      />
    </div>
  </div>
</template>

<style scoped>
.corporate-page {
  min-height: 100vh;
  display: flex;
  flex-direction: column;
  padding-top: 0;
}

.fullscreen-slider {
  height: 85vh; 
  width: 100%;
}

.products-section {
  background-color: #fff;
  /* İçeriği ortalayıp sınırla (1200px) */
  width: 100%;
  max-width: 1200px;
  margin: 0 auto;
  padding: 60px 20px;
}
</style>