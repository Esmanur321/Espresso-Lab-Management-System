/**
 * ============================================
 * PRODUCTS STORE - Ürün Yönetimi (WEEK 8 - PINIA)
 * ============================================
 *
 * Pinia defineStore ile yeniden yapılandırıldı.
 * Backend API'den ürünleri çeker, bağlantı yoksa Mock Data'ya düşer.
 *
 * WEEK 10'da Firebase entegrasyonu buraya eklenecek.
 */
import { defineStore } from 'pinia';
import type { IProduct } from '~/types';

const BACKEND_URL = 'http://localhost:8000';

// Normalized Category Helper
const normalizeCategory = (cat: string): string => {
  if (!cat) return '';
  const c = cat.toLowerCase().trim();
  if (c === 'coffee' || c === 'kahve') return 'coffee';
  if (c === 'thermos' || c === 'termos') return 'thermos';
  if (c === 'accessories' || c === 'aksesuar') return 'accessories';
  if (c === 'teas' || c === 'çaylar' || c === 'caylar') return 'teas';
  if (c === 'snacks' || c === 'atıştırmalıklar' || c === 'atistirmaliklar') return 'snacks';
  return c;
};

// Mock Data - Backend çalışmıyorsa kullanılır
const MOCK_PRODUCTS: IProduct[] = [
  {
    id: '1',
    name: 'Kırmızı Pipetli Mug Termos 500 ml',
    price: 599.99,
    imageUrl: '/images/KirmiziTermos.png',
    description: 'Hacim: 500 ml | Malzeme: Paslanmaz Çelik | Renk: Kırmızı',
    originalPrice: 750.00,
    categoryId: 'thermos'
  },
  {
    id: '2',
    name: 'Pratik Filtre Kahve - Colombia',
    price: 195.00,
    imageUrl: '/images/FiltreKahve.png',
    description: 'Menşei: Kolombiya | Tür: %100 Arabica | Nota: Fındık, Karamel',
    originalPrice: 220.00,
    categoryId: 'coffee'
  },
  {
    id: '3',
    name: 'Espresso Blend',
    price: 285.00,
    imageUrl: '/images/EspressoBlend.png',
    description: 'Espressolab\'in özel harmanı | Yoğun ve dengeli aroma',
    categoryId: 'coffee'
  },
  {
    id: '4',
    name: 'Siyah Mug',
    price: 349.00,
    imageUrl: '/images/SiyahMug.png',
    description: 'Özel kaplama | Isı yalıtımlı | 350 ml',
    originalPrice: 420.00,
    categoryId: 'accessories'
  },
  {
    id: '5',
    name: 'Kahve Öğütücü',
    price: 899.00,
    imageUrl: '/images/KahveOgutucu.png',
    description: 'Manuel kahve öğütücü | Paslanmaz çelik bıçaklar',
    categoryId: 'accessories'
  },
  {
    id: '6',
    name: 'Earl Grey Çay',
    price: 125.00,
    imageUrl: '/images/EarlGrey.png',
    description: 'Bergamot aromalı Earl Grey | 100g',
    originalPrice: 150.00,
    categoryId: 'teas'
  },
  {
    id: '7',
    name: 'Fındıklı Kurabiye',
    price: 85.00,
    imageUrl: '/images/FindikliKurabiye.png',
    description: 'Günlük taze pişmiş | Glutensiz',
    categoryId: 'snacks'
  },
  {
    id: '8',
    name: 'V60 Dripper',
    price: 450.00,
    imageUrl: '/images/V60Dripper.png',
    description: 'Seramik V60 dripper | Filtre kahve demliği',
    originalPrice: 550.00,
    categoryId: 'accessories'
  }
];

export const useProductStore = defineStore('products', {
  state: () => ({
    products: [] as IProduct[],
    categories: [
      { title: 'Kahve', image: '/images/KatKahve.png' },
      { title: 'Termos', image: '/images/KatTermos.png' },
      { title: 'Aksesuar', image: '/images/KatAksesuar.png' },
      { title: 'Çaylar', image: '/images/KatÇay.png' },
      { title: 'Atıştırmalıklar', image: '/images/KatAtıştır.png' }
    ],
    isLoading: false,
    error: null as string | null
  }),

  getters: {
    getProductById: (state) => (id: string) =>
      state.products.find(p => p.id === String(id)),

    getProductsByCategory: (state) => (category: string) => {
      const normalizedCat = normalizeCategory(category);
      return state.products.filter(p => p.categoryId === normalizedCat);
    }
  },

  actions: {
    async fetchProducts() {
      this.isLoading = true;
      this.error = null;
      try {
        // Backend'den verileri çekmek için Nuxt 3'ün yerleşik $fetch metodunu kullanıyoruz.
        // Bu kod parçası Backend API (http://localhost:8000/products) ile bağlantı kurar.
        const data: any = await $fetch(`${BACKEND_URL}/products`);
        
        // Gelen veriyi Frontend'in beklediği yapıya (IProduct) dönüştürüyoruz
        this.products = data.map((p: any) => ({
          id: String(p.id),
          name: p.name,
          price: p.price,
          originalPrice: p.original_price,
          imageUrl: p.image_url || '/images/kirmizi-termos.jpg',
          description: p.description,
          categoryId: normalizeCategory(p.category)
        }));
        console.log(`✅ ${this.products.length} ürün backend'den başarıyla yüklendi`);
      } catch (error) {
        console.warn('⚠️ Backend bağlantısı başarısız, Mock Data kullanılıyor.', error);
        this.products = MOCK_PRODUCTS;
        this.error = 'Backend bağlantısı kurulamadı';
      } finally {
        this.isLoading = false;
      }
    }
  }
});
