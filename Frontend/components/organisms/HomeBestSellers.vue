<script setup lang="ts">
import ProductCard from '@/components/molecules/ProductCard.vue';
import type { IProduct } from '~/types';

defineProps<{
  products: IProduct[];
}>();

const emit = defineEmits(['handleCartAdd', 'handleProductClick']);
</script>

<template>
  <section class="home-best-seller">
    
    <header class="section-header">
      <h2>EN ÇOK SATAN ÜRÜNLERİMİZ</h2>
    </header>

    <div class="product-grid">
      <ProductCard 
        v-for="product in products" 
        :key="product.id"
        :product="product"
        @addToCart="emit('handleCartAdd', $event)"
        @view="emit('handleProductClick', $event)" 
      />
    </div>

    <div class="view-all-container">
      <router-link to="/store" class="view-all-btn">
        Tümünü Görüntüle
      </router-link>
    </div>

  </section>
</template>

<style scoped>
.home-best-seller { width: 100%; margin: 60px 0; }

/* ORTALI BAŞLIK STİLİ */
.section-header { text-align: center; margin-bottom: 40px; }
.section-header h2 {
  font-size: 32px;
  font-weight: 700;
  color: #000;
  text-transform: uppercase;
  margin: 0;
  font-family: 'Oswald', sans-serif;
}

.product-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(350px, 1fr));
  gap: 30px;
}

.view-all-container { display: flex; justify-content: center; margin-top: 30px; }

.view-all-btn {
  text-decoration: none; color: #333; border: 1px solid #ccc;
  padding: 12px 40px; border-radius: 50px; font-size: 14px; font-weight: 600;
  transition: all 0.3s ease;
}
.view-all-btn:hover { background-color: #f9f9f9; border-color: #000; }
</style>