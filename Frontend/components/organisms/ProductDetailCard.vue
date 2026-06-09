<script setup lang="ts">
import ImageGallery from '@/components/molecules/ImageGallery.vue';
import BaseRating from '@/components/atoms/BaseRating.vue';
import PriceDisplay from '@/components/atoms/PriceDisplay.vue';
import QuantitySpinner from '@/components/atoms/QuantitySpinner.vue';
import BaseButton from '@/components/atoms/BaseButton.vue';

interface ProductImage {
  src: string;
  alt: string;
}

interface ProductDetail {
  id: string;
  title: string;
  name?: string; // IProduct uyumu için
  rating: number;
  price: number;
  originalPrice?: number;
  description?: string;
  body?: string;
  imageUrl?: string; // IProduct uyumu için
  images: ProductImage[];
}

defineProps<{
  product: ProductDetail;
  quantity: number;
  averageRating?: number;
  totalComments?: number;
}>();

const emit = defineEmits(['update:quantity', 'addToCart']);
</script>

<template>
  <div class="product-detail-wrapper">
    <div class="product-detail-card">
      <div class="gallery-container">
        <ImageGallery :images="product.images" :product="(product as any)" />
      </div>

      <div class="info-container">
        <h1 class="product-title" style="display: flex; align-items: center; flex-wrap: wrap; gap: 10px;">
          {{ $t(product.title) }}
          <span v-if="averageRating && averageRating > 0" class="avg-rating-badge">
            ★ {{ averageRating }}
          </span>
        </h1>
        
        <div class="rating-wrapper" style="display: flex; align-items: center; gap: 8px;">
          <BaseRating :rating="averageRating || 0" class="stars" />
          <span class="comments-count" v-if="totalComments && totalComments > 0" style="font-size: 0.85rem; color: #888;">
            ({{ totalComments }} {{ $t('product.reviews_count') || 'yorum' }})
          </span>
        </div>

        <div class="price-wrapper">
          <PriceDisplay 
            :price="product.price" 
            :originalPrice="product.originalPrice" 
          />
        </div>

        <!-- Ürün Açıklaması -->
        <div class="product-description" v-if="product.description || product.body">
          <h3 class="desc-title">{{ $t('product.desc_title') }}</h3>
          <p>{{ $t('product.desc.' + product.id) !== 'product.desc.' + product.id ? $t('product.desc.' + product.id) : (product.description || product.body || $t('product.no_desc')) }}</p>
        </div>
        
        <div class="actions">
          <QuantitySpinner 
            :modelValue="quantity"
            @update:modelValue="emit('update:quantity', $event)"
            class="qty-spinner"
          />
          <BaseButton 
            :label="$t('store.add_to_cart')"
            @click="emit('addToCart')"
            class="add-to-cart-btn"
          />
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
/* Google Font Import (Eğer projende ekli değilse) */
@import url('https://fonts.googleapis.com/css2?family=Oswald:wght@500;700&display=swap');

.product-detail-wrapper {
  max-width: 1200px;
  margin: 0 auto;
  padding: 20px;
  font-family: 'Inter', sans-serif;
}

.product-detail-card {
  display: grid;
  grid-template-columns: 1.2fr 1fr; /* Sol taraf biraz daha geniş */
  gap: 50px;
  align-items: start;
}

/* --- SAĞ TARAFTAKİ DETAYLAR --- */
.info-container {
  padding-top: 10px;
  display: flex;
  flex-direction: column;
  gap: 15px;
}

/* 1. Başlık */
.product-title {
  font-family: 'Oswald', sans-serif; /* Görseldeki condensed font */
  font-size: 28px;
  font-weight: 700;
  text-transform: uppercase;
  color: #000;
  margin: 0;
  line-height: 1.2;
  letter-spacing: 0.5px;
}

.avg-rating-badge {
  font-size: 1.1rem;
  color: #f39c12;
  background-color: var(--border-color, #eee);
  padding: 4px 12px;
  border-radius: 50px;
  font-weight: 700;
  display: inline-flex;
  align-items: center;
}

/* 2. Yıldızlar (Atom bileşenine stil yedirme) */
.rating-wrapper {
  display: flex;
  align-items: center;
}

/* BaseRating içindeki yıldızları kırmızı yapmak için deep selector */
:deep(.base-rating .star-icon) {
  color: #c00000; /* Kırmızı renk */
  font-size: 18px;
}
:deep(.base-rating .rating-text) {
  color: #888;
  font-size: 13px;
  margin-left: 5px;
}

/* 3. Fiyat */
.price-wrapper {
  margin-top: 5px;
  margin-bottom: 5px;
}
/* PriceDisplay içindeki stilleri ezmek/ayarlamak için */
:deep(.price-display) {
  display: flex;
  align-items: baseline; /* Taban çizgisinden hizala */
  gap: 12px;
}
:deep(.price-display .current-price) {
  font-size: 36px; /* Daha büyük */
  font-weight: 700;
  color: #000;
  letter-spacing: -0.5px;
  line-height: 1;
}
:deep(.price-display .original-price) {
  font-size: 20px;
  color: #9daab5; /* Daha açık gri */
  text-decoration: line-through;
  font-weight: 400;
}

/* YENİ: Ürün Açıklaması */
.product-description {
  margin-bottom: 20px;
  line-height: 1.6;
  color: #555;
  font-size: 15px;
  border-top: 1px solid #eee;
  padding-top: 15px;
}

.desc-title {
  font-size: 16px;
  font-weight: 700;
  color: #333;
  margin-bottom: 10px;
  text-transform: uppercase;
}

/* 4. Aksiyonlar (Miktar + Buton) */
.actions {
  display: flex;
  gap: 20px;
  align-items: center;
  margin-top: 10px;
}

/* Miktar Kutusu Özelleştirme */
:deep(.quantity-spinner) {
  height: 50px;
  width: 120px;
  border: 1px solid #e5e5e5;
  border-radius: 4px; /* Hafif yuvarlak köşe */
  display: flex;
  align-items: center;
  justify-content: space-between;
}
:deep(.quantity-spinner button) {
  background: transparent;
  border: none;
  font-size: 18px;
  color: #555;
  cursor: pointer;
  padding: 0 15px;
}
:deep(.quantity-spinner input) {
  border: none;
  text-align: center;
  font-weight: 600;
  width: 40px;
  font-size: 16px;
}

/* Sepete Ekle Butonu Özelleştirme */
.add-to-cart-btn {
  flex-grow: 1;
  height: 50px;
  background-color: #c00000; /* Espressolab Kırmızısı */
  color: white;
  border: none;
  border-radius: 25px; /* Pill shape (Hap şeklinde) */
  font-size: 16px;
  font-weight: 700;
  cursor: pointer;
  transition: background 0.3s;
}

.add-to-cart-btn:hover {
  background-color: #a00000;
}

/* MOBİL UYUMLULUK */
@media (max-width: 768px) {
  .product-detail-card {
    grid-template-columns: 1fr;
    gap: 30px;
  }
  
  .product-title {
    font-size: 24px;
  }
}
</style>