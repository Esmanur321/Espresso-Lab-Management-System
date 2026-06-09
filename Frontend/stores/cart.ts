/**
 * ============================================
 * CART STORE - Sepet Yönetimi (WEEK 8 - PINIA)
 * ============================================
 *
 * Pinia defineStore ile yeniden yapılandırıldı.
 * localStorage persist ile sayfa yenilemelerinde sepet korunur.
 * Backend'e stok kontrolü için istek atılır.
 *
 * WEEK 10'da Firestore senkronizasyonu eklenecek.
 */
import { defineStore } from 'pinia';
import type { ICartItem } from '~/types';

const BACKEND_URL = 'http://localhost:8000';

export const useCartStore = defineStore('cart', {
  state: () => ({
    items: [] as ICartItem[],
    isLoading: false
  }),

  getters: {
    totalItems: (state) =>
      state.items.reduce((acc, item) => acc + item.quantity, 0),

    subtotal: (state) =>
      Math.round(state.items.reduce((acc, item) => acc + item.price * item.quantity, 0) * 100) / 100,

    isEmpty: (state) => state.items.length === 0
  },

  actions: {
    /** Sayfa açılışında localStorage'dan sepeti yükle */
    initialize() {
      if (process.client) {
        const saved = localStorage.getItem('cart');
        if (saved) {
          try {
            this.items = JSON.parse(saved);
          } catch {
            this.items = [];
          }
        }
      }
    },

    /** localStorage'ı güncelle (her değişiklikte çağrılır) */
    _persist() {
      if (process.client) {
        localStorage.setItem('cart', JSON.stringify(this.items));
      }
    },

    async addToCart(product: any, quantity: number = 1) {
      // Backend stok kontrolü
      try {
        const data: any = await $fetch(`${BACKEND_URL}/products/${product.id}`);
        if (data && data.stock <= 0) {
          throw new Error('Ürün stokta yok');
        }
      } catch (e: any) {
        if (e.message === 'Ürün stokta yok') {
          alert('Ürün stokta yok!');
          return;
        }
        // Backend yoksa veya ürün bulunamadıysa devam et (mock mod)
        console.warn('Stok kontrolü yapılamadı (backend kapalı veya hata)', e);
      }

      const existing = this.items.find(i => i.id === product.id);
      if (existing) {
        existing.quantity += quantity;
      } else {
        this.items.push({ ...product, quantity });
      }
      this._persist();
    },

    async updateQuantity(productId: string, quantity: number) {
      const item = this.items.find(i => i.id === productId);
      if (item) {
        item.quantity = quantity;
        this._persist();
      }
    },

    async removeFromCart(productId: string) {
      this.items = this.items.filter(i => i.id !== productId);
      this._persist();
    },

    clearCart() {
      this.items = [];
      if (process.client) localStorage.removeItem('cart');
    },

    // WEEK 10 PLACEHOLDER: Firestore senkronizasyonu
    async loadCart(userId: string) {
      // Week 10'da: Firestore'dan kullanıcının sepetini çek
      // const db = useNuxtApp().$db;
      // const cartDoc = await getDoc(doc(db, 'carts', userId));
      console.log('loadCart: Week 10\'da Firestore ile bağlanacak');
    }
  }
});
