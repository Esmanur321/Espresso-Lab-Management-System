/**
 * ============================================
 * FAVORITES STORE - Favoriler (WEEK 8 - PINIA)
 * ============================================
 *
 * Pinia defineStore ile yeniden yapılandırıldı.
 * Favoriler oturum boyunca bellekte tutulur.
 *
 * WEEK 10'da Firestore senkronizasyonu eklenecek.
 */
import { defineStore } from 'pinia';
import type { IProduct } from '~/types';

export const useFavoritesStore = defineStore('favorites', {
  state: () => ({
    items: [] as IProduct[]
  }),

  getters: {
    totalFavorites: (state) => state.items.length,

    isFavorite: (state) => (productId: string) =>
      state.items.some(i => i.id === productId)
  },

  actions: {
    async addToFavorites(product: IProduct) {
      if (!this.isFavorite(product.id)) {
        this.items.push(product);
      }
    },

    async removeFromFavorites(productId: string) {
      this.items = this.items.filter(i => i.id !== productId);
    },

    async toggleFavorite(product: IProduct) {
      if (this.isFavorite(product.id)) {
        await this.removeFromFavorites(product.id);
      } else {
        await this.addToFavorites(product);
      }
    },

    clearFavorites() {
      this.items = [];
    },

    // WEEK 10 PLACEHOLDER: Firestore senkronizasyonu
    async loadFavorites(userId: string) {
      // Week 10'da: Firestore'dan kullanıcının favorilerini çek
      console.log('loadFavorites: Week 10\'da Firestore ile bağlanacak');
    }
  }
});
