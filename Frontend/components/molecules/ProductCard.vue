<!--
============================================
PRODUCT CARD - Ürün Kartı Bileşeni (MOLEKÜL)
============================================

Bu bileşen, Atomik Tasarım'da "Molekül" seviyesindedir:
- Atomları (BaseButton) kullanarak daha karmaşık bir yapı oluşturur
- Organizmalarda (StoreBestSellers, CategoryList) kullanılır
- Kendi başına anlam ifade eder ve yeniden kullanılabilir

Proje Gereksinimi:
- "Vue sayfaları önceki atomik komponentlere dayanarak üretilmeli"
- Bu molekül, BaseButton atomunu kullanıyor (import satırına bakınız)
-->

<script setup lang="ts">
/**
 * ========== IMPORT'LAR ==========
 * Vue Composition API ve diğer bileşenler
 */
import { computed } from 'vue';  // Hesaplanmış özellik (computed property)
import BaseButton from '@/components/atoms/BaseButton.vue';  // ATOM: Temel buton bileşeni
import { useFavoritesStore } from '~/stores/favorites';  // Favoriler Pinia store'u
import type { IProduct } from '~/types';

// Favoriler store'una erişim
const favoritesStore = useFavoritesStore();

/**
 * formatCurrency: Para birimini Türk Lirası formatına çevirir
 * Örnek: 599.99 -> "₺599,99"
 */
const formatCurrency = (value: number | undefined): string => {
  if (!value) return '';
  return `₺${value.toFixed(2).replace('.', ',')}`;
};

/**
 * ========== PROPS (Dışarıdan Gelen Veriler) ==========
 * 
 * Props, üst bileşenden (parent) bu bileşene veri aktarır.
 * "Dumb component" prensibi: Veriyi kendi üretmez, dışarıdan alır.
 */
const props = defineProps<{
  product: IProduct;  // Ürün objesi (id, name, price, imageUrl vb.)
  layout?: string;  // Görünüm modu: 'vertical' | 'horizontal'
}>();

const layout = props.layout ?? 'vertical';

/**
 * ========== EVENTS (Dışarıya Gönderilen Olaylar) ==========
 * 
 * emit, bu bileşenden üst bileşene olay gönderir.
 * Örnek: Sepete ekle butonuna tıklandığında 'addToCart' olayı tetiklenir.
 */
const emit = defineEmits(['addToCart', 'view']);

/**
 * handleCardClick: Kart tıklandığında ürün detayına git
 */
const handleCardClick = () => {
    emit('view', props.product);  // 'view' olayını tetikle, ürün verisini gönder
};

/**
 * handleAddToCart: Sepete ekle butonuna tıklandığında
 */
const handleAddToCart = () => {
    emit('addToCart', props.product);  // 'addToCart' olayını tetikle
};

/**
 * handleToggleFavorite: Favori butonuna tıklandığında
 * Favorilere ekler veya çıkarır (toggle)
 */
const handleToggleFavorite = async () => {
  await favoritesStore.toggleFavorite(props.product);
};

/**
 * isFavorited: Bu ürün favorilerde mi?
 * computed: Reaktif olarak güncellenir (favoriler değişince)
 */
const isFavorited = computed(() => favoritesStore.isFavorite(props.product.id));
</script>

<template>
  <div class="product-card" :class="layout" @click="handleCardClick">
    
    <div class="card-top-actions">
      <!-- Yatay modda badge resmi kaplamasın diye farklı konumlandırılabilir ama şimdilik aynı kalsın -->
      <span v-if="product.id === '1' || product.id === '5'" class="badge new">{{ $t('store.new') }}</span>
      <span v-else></span> 
      <button class="wishlist-btn" :class="{ 'is-favorite': isFavorited }" @click.stop="handleToggleFavorite">
        <svg width="22" height="22" viewBox="0 0 24 24" :fill="isFavorited ? '#c00a00' : 'none'" :stroke="isFavorited ? '#c00a00' : '#9CA3AF'" stroke-width="2">
          <path d="M20.84 4.61a5.5 5.5 0 0 0-7.78 0L12 5.67l-1.06-1.06a5.5 5.5 0 0 0-7.78 7.78l1.06 1.06L12 21.23l7.78-7.78 1.06-1.06a5.5 5.5 0 0 0 0-7.78z"></path>
        </svg>
      </button>
    </div>

    <div class="card-inner-wrapper">
      <div class="card-image-wrapper">
        <img :src="product.imageUrl" :alt="product.name" class="card-image" />
      </div>
      
      <div class="card-content">
        <h3 class="card-title">
          {{ $t(product.name) }}
        </h3>
        
        <div class="price-container">
          <span v-if="product.originalPrice" class="old-price">
            {{ formatCurrency(product.originalPrice) }}
          </span>
          <span class="current-price">{{ formatCurrency(product.price) }}</span>
        </div>
        
        <div class="button-wrapper">
          <BaseButton 
            :label="$t('store.add_to_cart')" 
            variant="outline" 
            @click.stop="handleAddToCart"
            class="add-btn"
          />
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
.product-card {
  background: var(--card-bg, #FFFFFF);
  border: 1px solid var(--border-color, #e5e7eb); 
  border-radius: 12px; 
  padding: 12px;
  overflow: hidden;
  transition: all 0.3s ease;
  box-sizing: border-box;
  position: relative;
  cursor: pointer; /* TÜM KART TIKLANABİLİR */
}


.product-card:hover {
  box-shadow: 0 4px 20px rgba(0,0,0,0.08); 
}

/* --- VERTICAL (Default) --- */
.product-card.vertical {
  width: 100%; 
  height: 100%;
  text-align: center;
  display: flex;
  flex-direction: column;
}

.product-card.vertical .card-inner-wrapper {
  display: flex;
  flex-direction: column;
  height: 100%;
}

.product-card.vertical .card-image-wrapper {
  height: 200px;
  margin-bottom: 12px;
}

/* --- HORIZONTAL (SLIMMER) --- */
.product-card.horizontal {
  width: 100%;
  height: auto; 
  min-height: 110px; /* Daha ince yükseklik */
  display: flex;
  flex-direction: column; 
  padding: 8px; /* Daha az padding */
}

.product-card.horizontal .card-inner-wrapper {
  display: flex;
  flex-direction: row;
  align-items: center;
  gap: 10px;
  height: 100%;
}

.product-card.horizontal .card-image-wrapper {
  flex: 0 0 30%; /* Resim daha dar */
  height: 80px; /* Resim daha kısa */
  display: flex;
  align-items: center;
  justify-content: center;
}

.product-card.horizontal .card-content {
  flex: 1;
  text-align: left; /* Sola hizalı */
  align-items: flex-start; /* İçerik sola */
  justify-content: center;
}

.product-card.horizontal .card-title {
  font-size: 14px;
  margin-bottom: 8px;
  height: auto;
  display: -webkit-box;
  -webkit-line-clamp: 2; /* 2 satıra düşürüldü */
  line-clamp: 2; /* Standart property for compatibility */
  -webkit-box-orient: vertical;
  overflow: hidden;
  text-overflow: ellipsis;
}

.product-card.horizontal .price-container {
  align-items: flex-start;
  margin-bottom: 12px;
}

.product-card.horizontal .button-wrapper {
  width: 100%;
}

/* --- ORTAK --- */

.card-top-actions {
  width: 100%;
  display: flex;
  justify-content: space-between;
  position: absolute;
  top: 10px;
  left: 0;
  padding: 0 10px;
  z-index: 2;
}

.badge.new {
  background-color: #00a651;
  color: white;
  font-size: 10px;
  font-weight: 700;
  padding: 2px 6px;
  border-radius: 4px;
}

.wishlist-btn {
  background: var(--card-bg, white);
  border: 1px solid var(--border-color, #eee);
  border-radius: 50%;
  width: 30px; height: 30px;
  display: flex; align-items: center; justify-content: center;
  cursor: pointer;
  margin-left: auto; /* Sağa yasla */
  transition: all 0.3s ease;
}

.wishlist-btn:hover {
  background: #fff5f5;
  border-color: #c00a00;
}

.wishlist-btn.is-favorite {
  background: #fff5f5;
  border-color: #c00a00;
}

.card-image-wrapper {
  display: flex;
  justify-content: center;
}

.card-image {
  max-width: 100%;
  max-height: 100%;
  object-fit: contain;
}

.card-content {
  display: flex;
  flex-direction: column;
}

.card-title {
  font-weight: 600;
  color: var(--text-color, #111);
  line-height: 1.3;
  cursor: pointer;
  transition: color 0.2s;
}


.price-container {
  display: flex;
  flex-direction: column;
}

.old-price {
  font-size: 12px;
  color: #999;
  text-decoration: line-through;
}

.current-price {
  font-size: 16px;
  font-weight: 700;
  color: var(--text-color, #000);
}

:deep(.add-btn) {
  width: 100%;
  border-radius: 50px;
  padding: 8px 15px;
  font-size: 12px;
  font-weight: 700;
  border: 1px solid #c00a00; 
  color: #c00a00;
  background-color: transparent;
  transition: all 0.3s;
  text-transform: uppercase;
}

:deep(.add-btn:hover) {
  background-color: #c00a00;
  color: #fff;
}
</style>