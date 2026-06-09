<script setup lang="ts">
import { computed } from 'vue';
import type { ICartItem } from '~/types';

// Para formatlama
const formatCurrency = (value: number | undefined): string => {
  if (typeof value !== 'number') return '₺0,00';
  return `₺${value.toFixed(2).replace('.', ',')}`;
};

// v-model ve item prop'u
const props = defineProps<{
  item: ICartItem;
  quantity: number;
}>();

const emit = defineEmits(['update:quantity', 'remove']);

// %10 indirim hesaplama
const unitPrice = computed(() => props.item.price);
const discountedPrice = computed(() => props.item.price * 0.9); // %10 indirim

// Miktar Artırma
const increment = () => {
  emit('update:quantity', props.quantity + 1);
};

// Miktar Azaltma veya Silme
const decrementOrRemove = () => {
  if (props.quantity > 1) {
    emit('update:quantity', props.quantity - 1);
  } else {
    emit('remove', props.item);
  }
};
</script>

<template>
  <div class="cart-item-wrapper">
    <div class="item-main-content">
      <div class="left-section">
        <div class="image-container">
          <img :src="item.imageUrl" :alt="item.name" class="item-image" />
        </div>
        
        <div class="info-container">
          <div class="main-price">{{ formatCurrency(discountedPrice) }}</div>
          <h3 class="item-name">{{ $t(item.name) }}</h3>
        </div>
      </div>

      <div class="right-section">
        <div class="quantity-controls">
          <button class="qty-btn left" @click="decrementOrRemove">
            <svg v-if="quantity === 1" class="icon-trash" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
              <path d="M3 6H5H21" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
              <path d="M8 6V4C8 3.46957 8.21071 2.96086 8.58579 2.58579C8.96086 2.21071 9.46957 2 10 2H14C14.5304 2 15.0391 2.21071 15.4142 2.58579C15.7893 2.96086 16 3.46957 16 4V6M19 6V20C19 20.5304 18.7893 21.0391 18.4142 21.4142C18.0391 21.7893 17.5304 22 17 22H7C6.46957 22 5.96086 21.7893 5.58579 21.4142C5.21071 21.0391 5 20.5304 5 20V6H19Z" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
            </svg>
            <span v-else class="icon-minus">-</span>
          </button>
          <span class="qty-value">{{ quantity }}</span>
          <button class="qty-btn right" @click="increment">
            <span class="icon-plus">+</span>
          </button>
        </div>
      </div>
    </div>

    <div class="item-footer">
      <div class="unit-price-label">{{ $t('cart.unit_price') }}:<span class="strikethrough">{{ formatCurrency(unitPrice) }}</span></div>
      <div class="discount-price-label">{{ $t('cart.discounted_price') }}: <span class="green-text">{{ formatCurrency(discountedPrice) }}</span></div>
    </div>
  </div>
</template>

<style scoped>
/* Genel Kapsayıcı */
.cart-item-wrapper {
  display: flex;
  flex-direction: column;
  width: 100%;
  padding-bottom: 20px;
  border-bottom: 1px solid #eee;
  margin-bottom: 20px;
}

/* Üst Alan (Resim + Bilgi + Miktar) */
.item-main-content {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  margin-bottom: 15px;
}

.left-section {
  display: flex;
  gap: 15px;
}

/* Resim Alanı */
.image-container {
  width: 80px;
  height: 80px;
  border: 1px solid #f0f0f0;
  border-radius: 8px;
  padding: 5px;
  display: flex;
  align-items: center;
  justify-content: center;
}

.item-image {
  max-width: 100%;
  max-height: 100%;
  object-fit: contain;
}

/* Bilgi Alanı */
.info-container {
  display: flex;
  flex-direction: column;
  gap: 4px;
}

.main-price {
  font-size: 16px;
  font-weight: 700;
  color: #000;
}

.item-name {
  font-size: 14px;
  font-weight: 400;
  color: #333;
  margin: 0;
  line-height: 1.4;
  max-width: 250px;
}

/* Sağ Bölüm (Miktar + Öğütme Tipi) */
.right-section {
    display: flex;
    flex-direction: column;
    align-items: flex-end;
    gap: 8px;
}

/* Miktar Butonları */
.quantity-controls {
  display: flex;
  align-items: center;
  border: 1px solid #e5e7eb;
  border-radius: 4px;
  height: 32px;
}

.qty-btn {
  width: 30px;
  height: 100%;
  border: none;
  background: #fff;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  color: #666;
}

.qty-btn:hover {
  background-color: #f9fafb;
}

.qty-btn.left { border-right: 1px solid #e5e7eb; }
.qty-btn.right { border-left: 1px solid #e5e7eb; }

.qty-value {
  width: 30px;
  text-align: center;
  font-size: 14px;
  font-weight: 500;
}

.icon-trash { width: 16px; height: 16px; color: #999; }
.qty-btn:hover .icon-trash { color: #c00000; }
.icon-minus, .icon-plus { font-size: 16px; }

/* Öğütme Bilgisi */
.grind-info {
    text-align: right;
    font-size: 11px;
    line-height: 1.2;
}
.grind-label { color: #999; display: block; }
.grind-value { color: #000; font-weight: 700; }

/* Alt Alan (Fiyatlar) */
.item-footer {
  display: flex;
  justify-content: space-between;
  align-items: center;
  font-size: 12px;
  padding-top: 5px;
}

.unit-price-label {
  color: #999;
}

.strikethrough {
  text-decoration: line-through;
  margin-left: 4px;
}

.discount-price-label {
    color: #00a651; /* Yeşil Metin */
    font-weight: 500;
}

.green-text {
  font-weight: 700;
  margin-left: 4px;
}
</style>