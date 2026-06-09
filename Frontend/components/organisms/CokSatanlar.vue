<script setup lang="ts">
import ProductCard from '../molecules/ProductCard.vue';

interface Product {
  id: number;
  name: string;
  title: string;
  price: number;
  imageUrl: string;
}

// Örnek Veriler (Normalde API'den gelir)
const products: Product[] = [
  { id: 1, name: 'Kırmızı Pipetli Mug Termos 500 ml', title: 'Kırmızı Pipetli Mug Termos 500 ml', price: 599.99, imageUrl: 'https://st4.myideasoft.com/idea/im/88/myassets/products/355/kirmizi-pipetli-mug-termos-500-ml-no-80-6072-jpg.jpeg' },
  { id: 2, name: 'Pratik Filtre Kahve - Colombia', title: 'Pratik Filtre Kahve - Colombia', price: 195.00, imageUrl: 'https://st4.myideasoft.com/idea/im/88/myassets/products/064/pratik-filtre-kahve-colombia-antioquia-10-lu-paket-4404-png.png' },
  { id: 3, name: 'Türk Kahvesi 200 g', title: 'Türk Kahvesi 200 g', price: 299.99, imageUrl: 'https://st4.myideasoft.com/idea/im/88/myassets/products/596/turk-kahvesi-200-g-5975-png.png' },
  { id: 4, name: 'Tutacaklı Kırmızı Termos 350 ml', title: 'Tutacaklı Kırmızı Termos 350 ml', price: 599.99, imageUrl: 'https://st4.myideasoft.com/idea/im/88/myassets/products/359/tutacakli-kirmizi-termos-350-ml-no-81-6084-jpg.jpeg' },
];
</script>

<template>
  <section class="best-sellers">
    <div class="section-header">
      <h2 class="title">ÇOK SATANLAR</h2>
      <a href="#" class="view-all">Tümünü Görüntüle →</a>
    </div>

    <div class="products-grid">
      <ProductCard 
        v-for="product in products" 
        :key="product.id"
        :product="(product as any)"
      />
    </div>
  </section>
</template>

<style scoped>
.best-sellers {
  padding: 20px;
  background-color: white;
}

.section-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
}

.title {
  font-size: 1.5rem;
  font-weight: bold;
  color: #222;
  text-transform: uppercase;
}

.view-all {
  color: #d32f2f;
  text-decoration: none;
  font-weight: 600;
  font-size: 0.9rem;
}

.products-grid {
  display: flex;
  gap: 20px;
  flex-wrap: wrap; /* Mobilde alta geçsin diye */
}
</style>