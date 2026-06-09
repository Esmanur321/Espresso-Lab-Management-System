<script setup lang="ts">
import { ref, computed, onMounted } from 'vue';
import { useRouter } from 'vue-router';
import { useAuthStore } from '~/stores/auth';
import { useCartStore } from '~/stores/cart';
import { useProductStore } from '~/stores/products';
import StoreBestSellers from '@/components/organisms/StoreBestSellers.vue';
import type { IProduct, ICartItem } from '~/types';

const store = useAuthStore();
const cartStore = useCartStore();
const productStore = useProductStore();
const router = useRouter();

// Ürünleri yükle
onMounted(() => {
  productStore.fetchProducts();
});

const bestSellers = computed(() => productStore.products);

// --- LIVE DATA ---
const cartItems = computed(() => cartStore.items);

const shippingCost = ref(0.00);

// --- HESAPLAMALAR (YENİ MANTIK: %10 İNDİRİM) ---
const subtotal = computed(() => {
  return cartItems.value.reduce((total: number, item: ICartItem) => {
    return total + (item.price * item.quantity);
  }, 0);
});

const discountAmount = computed(() => {
  return subtotal.value * 0.10; // %10 indirim
});

const total = computed(() => {
  return subtotal.value - discountAmount.value + shippingCost.value;
});

const summaryData = computed(() => ({
  subtotal: subtotal.value,
  discount: discountAmount.value,
  shipping: shippingCost.value,
  total: total.value
}));

import { useNuxtApp } from '#app';
import { useToast } from '~/composables/useToast';
const { $t } = useNuxtApp() as any;
const { showToast } = useToast();

// --- SABİT VERİLER ---

const breadcrumbLinks = computed(() => [
  { text: $t('cart.breadcrumb_home'), href: '/' },
  { text: $t('cart.breadcrumb_store'), href: '/store' },
  { text: $t('cart.breadcrumb_cart'), href: '/cart' }
]);

// --- METOTLAR ---
const updateQuantity = (item: ICartItem, newQuantity: number) => { 
  cartStore.updateQuantity(item.id, newQuantity);
};

const removeItem = (itemToRemove: ICartItem) => { 
  cartStore.removeFromCart(itemToRemove.id);
};

const applyCoupon = (code: string) => { showToast(`"${code}" ${$t('cart.coupon_applied')}`, 'info'); };
const goToCheckout = async () => { 
  if (!store.isAuthenticated) {
    await showToast($t('cart.login_required') || "Siparişi tamamlamak için önce giriş yapmalı veya kayıt olmalısınız.", 'warning');
    router.push('/login?redirect=/checkout');
  } else {
    router.push('/checkout'); 
  }
};
const continueShopping = () => { router.push('/store'); };

const handleAddToCart = (product: IProduct) => { 
  cartStore.addToCart(product);
  showToast(`${product.name} ${$t('cart.added_to_cart')}`, 'success'); 
};

const goToProductDetail = (product: IProduct) => { router.push(`/product/${product.id}`); };

</script>

<template>
  <main class="page-content">
    <div class="content-container">
        
      <Breadcrumbs :links="breadcrumbLinks" />
      
      <h1 class="page-title">{{ $t('cart.title') }}</h1>
      
      <div v-if="cartItems.length > 0" class="cart-layout">
        <section class="cart-items-list">
          <div class="items-wrapper">
            <CartItem 
              v-for="item in cartItems"
              :key="item.id"
              :item="item"
              :quantity="item.quantity" 
              @update:quantity="updateQuantity(item, $event)"
              @remove="removeItem(item)"
            />
          </div>
        </section>
        
        <div class="sidebar-wrapper">
          <CartSidebar 
            :summary="summaryData"

            @checkout="goToCheckout"
            @continueShopping="continueShopping"
          />
        </div>
      </div>

      <div v-else class="empty-cart-container">
        <div class="empty-icon-wrapper">
          <svg width="64" height="64" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
            <path d="M9 20C9 20.5523 8.55228 21 8 21C7.44772 21 7 20.5523 7 20C7 19.4477 7.44772 19 8 19C8.55228 19 9 19.4477 9 20Z" stroke="#C00000" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
            <path d="M20 20C20 20.5523 19.5523 21 19 21C18.4477 21 18 20.5523 18 20C18 19.4477 18.4477 19 19 19C19.5523 19 20 19.4477 20 20Z" stroke="#C00000" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
            <path d="M1 1H4L6.68 14.39C6.77144 14.8504 7.02191 15.264 7.38755 15.5583C7.75318 15.8526 8.2107 16.009 8.68 16H19.4C19.8693 16.009 20.3268 15.8526 20.6925 15.5583C21.0581 15.264 21.3086 14.8504 21.4 14.39L23 6H6" stroke="#C00000" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
          </svg>
        </div>
        
        <p class="empty-text">{{ $t('cart.empty_text') }}</p>
        
        <button class="start-shopping-btn" @click="continueShopping">
          {{ $t('cart.start_shopping') }}
        </button>
      </div>

      <div class="best-sellers-section">
        <StoreBestSellers 
          :products="bestSellers" 
          @handleCartAdd="handleAddToCart"
          @handleProductClick="goToProductDetail"
        />
      </div>

    </div>
  </main>
</template>

<style scoped>
.page-content {
  padding: 40px 0;
  background-color: #fff;
  min-height: 60vh;
}

.content-container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 0 20px;
}

.page-title {
  font-size: 1.8rem;
  font-weight: 800;
  margin-bottom: 30px; 
  font-family: 'Oswald', sans-serif;
  text-transform: uppercase;
  color: #333;
}

/* DOLU SEPET LAYOUTU */
.cart-layout {
  display: grid;
  grid-template-columns: 2fr 1fr;
  gap: 40px;
  align-items: start;
}

.items-wrapper {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

/* --- BOŞ SEPET TASARIMI --- */
.empty-cart-container {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 40px 0;
  width: 100%;
}

.empty-icon-wrapper {
  margin-bottom: 20px;
  /* İkon boyutu SVG içinden ayarlandı (width="64" height="64") */
}

.empty-text {
  font-size: 16px;
  color: #000;
  margin-bottom: 25px;
  font-weight: 500;
  font-family: 'Oswald', sans-serif;
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

.start-shopping-btn {
  padding: 12px 40px;
  background-color: transparent; /* İçi boş */
  color: #c00000; /* Kırmızı yazı */
  border: 1px solid #c00000; /* Kırmızı çerçeve */
  border-radius: 50px;
  cursor: pointer;
  font-weight: 600;
  font-size: 14px;
  transition: all 0.3s ease;
  font-family: 'Oswald', sans-serif;
  text-transform: uppercase;
  letter-spacing: 1px;
}

.start-shopping-btn:hover {
  background-color: #c00000;
  color: #fff;
}

/* ÇOK SATANLAR */
.best-sellers-section {
  margin-top: 60px;
  padding-top: 40px;
}

/* Cart Item Deep Style */
:deep(.cart-item) {
  border: 1px solid #f0f0f0;
  border-radius: 12px;
  padding: 20px;
  background-color: #fff;
  margin-bottom: 0;
}

@media (max-width: 992px) {
  .cart-layout {
    grid-template-columns: 1fr;
  }
}
</style>