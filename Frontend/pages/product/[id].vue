<script setup lang="ts">
import { ref, onMounted, computed, watch } from 'vue';
import { useAuthStore } from '~/stores/auth';
import { useProductStore } from '~/stores/products'; // EKLENDİ
import { useCartStore } from '~/stores/cart'; // EKLENDİ
import { useRoute, useRouter } from 'vue-router';
import type { IProduct } from '~/types';

// Ürün detay verisi için interface
interface ProductDetailData {
  id: string;
  title: string;
  rating: number;
  price: number;
  originalPrice: number;
  description?: string;
  images: { src: string; alt: string }[];
}

const store = useAuthStore();
const productStore = useProductStore(); // EKLENDİ
const cartStore = useCartStore(); // EKLENDİ
const route = useRoute();
const router = useRouter();


import Breadcrumbs from '@/components/molecules/Breadcrumbs.vue';
import ProductDetailCard from '@/components/organisms/ProductDetailCard.vue';
import ProductDescriptionTabs from '@/components/organisms/ProductDescriptionTabs.vue';
import StoreBestSellers from '@/components/organisms/StoreBestSellers.vue';

const productQuantity = ref(1);

const breadcrumbLinks = ref([
  { text: 'Ana Sayfa', href: '/' },
  { text: 'Online Mağaza', href: '/store' },
  { text: 'Ürün Detay', href: '#' }
]);

const productData = ref<ProductDetailData>({
  id: '', // ID Eklendi
  title: 'Yükleniyor...',
  rating: 0,
  price: 0,
  originalPrice: 0,
  images: []
});

// Ürünü Bulma Fonksiyonu
const loadProduct = async () => {
    const id = route.params.id as string;
    
    // Eğer store boşsa verileri çek
    if (productStore.products.length === 0) {
        await productStore.fetchProducts();
    }

    const found = productStore.products.find(p => p.id === id);
    
    if (found) {
        productData.value = {
            id: found.id, // ID eşlemesi
            title: found.name,
            rating: 5, // Varsayılan puan
            price: found.price,
            originalPrice: found.originalPrice || 0,
            description: found.description, // ✅ Açıklama Eklendi
            images: [
                { src: found.imageUrl, alt: found.name },
                { src: found.imageUrl, alt: found.name } // Detay sayfasında galeri olduğu için aynısını 2 kere ekledim
            ]
        };
        // Breadcrumb güncelle
        breadcrumbLinks.value[2] = { text: found.categoryId || 'Ürün', href: '#' };
        breadcrumbLinks.value[3] = { text: found.name, href: '#' };
    }
};

const comments = ref<any[]>([]);
const newCommentText = ref('');
const newCommentRating = ref(5);
const commentSuccessMessage = ref('');

const fetchComments = async () => {
  const id = route.params.id as string;
  try {
    const data: any = await $fetch(`http://localhost:8000/comments/product/${id}`);
    comments.value = data || [];
  } catch (error) {
    console.error('Failed to fetch product comments:', error);
  }
};

const handleCommentSubmit = async () => {
  if (!store.user) return;
  const id = route.params.id as string;
  try {
    await $fetch('http://localhost:8000/comments/', {
      method: 'POST',
      body: {
        product_id: parseInt(id),
        user_id: parseInt(store.user.uid),
        rating: newCommentRating.value,
        content: newCommentText.value
      }
    });
    newCommentText.value = '';
    newCommentRating.value = 5;
    commentSuccessMessage.value = $t('product.comment_success') || 'Yorumunuz başarıyla gönderildi. Admin onayından sonra yayınlanacaktır.';
    setTimeout(() => {
      commentSuccessMessage.value = '';
    }, 5000);
  } catch (error) {
    console.error('Failed to submit comment:', error);
    alert($t('product.comment_error') || 'Yorum gönderilirken hata oluştu.');
  }
};

const averageRating = computed(() => {
  if (!comments.value || comments.value.length === 0) return 0;
  const sum = comments.value.reduce((acc, c) => acc + c.rating, 0);
  return parseFloat((sum / comments.value.length).toFixed(1));
});

onMounted(() => {
    loadProduct();
    fetchComments();
});

// Route değişince (benzer ürünlere tıklayınca) yeniden yükle
watch(() => route.params.id, () => {
    loadProduct();
    fetchComments();
    window.scrollTo(0,0);
});


import { useNuxtApp } from '#app';
const { $t, $locale } = useNuxtApp() as any;

const productTabs = computed(() => {
  const _lang = $locale.value; // Reaktiviteyi zorlamak için
  return [
    { title: $t('product.desc_title'), content: `<ul><li>${$t('product.quality_material')}</li><li>${$t('product.espressolab_guarantee')}</li></ul>` }
  ];
});

// ÇOK SATANLAR (Canlı Veri) w/ computed
const bestSellers = computed(() => productStore.products);

const handleAddToCart = (product?: IProduct) => { 
    // Eğer fonksiyona bir ürün geldiyse (Best Sellers'dan), onu ekle
    // Yoksa (Detay kartından), şu anki sayfadaki ürünü ekle
    const targetProduct = product && product.id ? product : null;
    const qty = product && product.id ? 1 : productQuantity.value; // Best sellers'dan ise 1 adet, değilse seçilen miktar

    const itemToAdd = {
        id: targetProduct?.id || productData.value.id,
        name: targetProduct?.name || productData.value.title,
        price: targetProduct?.price || productData.value.price,
        imageUrl: targetProduct?.imageUrl || (productData.value.images[0]?.src) || '',
    };
    cartStore.addToCart(itemToAdd, qty);
    alert(`${qty} ${$t('product.added_piece', { name: itemToAdd.name }) || 'adet ' + itemToAdd.name + ' sepete eklendi!'}`); 
};
const goToProductDetail = (product: IProduct) => { 
    router.push(`/product/${product.id}`); 
    window.scrollTo(0, 0);
};

</script>

<template>
  <main class="page-content">
    <div class="content-container">
      <Breadcrumbs :links="breadcrumbLinks" />
      
      <ProductDetailCard 
        :product="productData"
        :averageRating="averageRating"
        :totalComments="comments.length"
        v-model:quantity="productQuantity"
        @addToCart="handleAddToCart"
      />
      
      <ProductDescriptionTabs :tabs="productTabs" />

      <!-- Reviews Section -->
      <div class="reviews-section">
        <h2 class="reviews-title">{{ $t('product.reviews_heading') || 'Müşteri Değerlendirmeleri' }} ({{ comments.length }})</h2>
        
        <div class="reviews-layout">
          <!-- Left: Reviews List -->
          <div class="reviews-list">
            <div v-if="comments.length === 0" class="no-reviews">
              <p>{{ $t('product.no_reviews_yet') || 'Bu ürün için henüz yorum yapılmamış. İlk yorum yapan siz olun!' }}</p>
            </div>
            <div v-else class="review-items">
              <div v-for="c in comments" :key="c.id" class="review-card">
                <div class="review-header">
                  <span class="review-author">{{ c.user_name }}</span>
                  <span class="review-rating">
                    <span v-for="star in 5" :key="star" class="review-star">
                      {{ star <= c.rating ? '★' : '☆' }}
                    </span>
                  </span>
                </div>
                <p class="review-text">{{ c.content }}</p>
                <span class="review-date">{{ new Date(c.created_at).toLocaleDateString() }}</span>
              </div>
            </div>
          </div>
          
          <!-- Right: Add Review Form -->
          <div class="add-review-panel">
            <div v-if="store.user" class="review-form-card">
              <h3>{{ $t('product.write_review') || 'Değerlendirme Yaz' }}</h3>
              <form @submit.prevent="handleCommentSubmit" class="comment-form">
                
                <div class="form-group">
                  <label class="form-label">{{ $t('product.your_rating') || 'Puanınız:' }}</label>
                  <div class="star-selector-container">
                    <span v-for="star in 5" :key="star" @click="newCommentRating = star" class="star-selector">
                      {{ star <= newCommentRating ? '★' : '☆' }}
                    </span>
                  </div>
                </div>

                <div class="form-group">
                  <label class="form-label">{{ $t('product.your_comment') || 'Yorumunuz:' }}</label>
                  <textarea v-model="newCommentText" :placeholder="$t('product.comment_placeholder') || 'Düşüncelerinizi paylaşın...'" required class="comment-textarea"></textarea>
                </div>

                <button type="submit" class="submit-comment-btn">{{ $t('product.submit') || 'Gönder' }}</button>
                
                <p v-if="commentSuccessMessage" class="success-message">{{ commentSuccessMessage }}</p>
              </form>
            </div>
            <div v-else class="login-prompt-card">
              <p>{{ $t('product.login_to_review') || 'Yorum yapabilmek için lütfen giriş yapın.' }}</p>
              <NuxtLink :to="`/login?redirect=${route.path}`" class="login-link-btn">{{ $t('auth.login') }}</NuxtLink>
            </div>
          </div>
        </div>
      </div>

      <div class="related-products">
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
  background-color: var(--bg-color, #fff);
  color: var(--text-color, #333);
}

.content-container {
  max-width: 1200px; 
  margin: 0 auto; 
  padding: 0 20px; 
}

.reviews-section {
  margin-top: 50px;
  border-top: 1px solid var(--border-color, #eee);
  padding-top: 40px;
  color: var(--text-color);
  text-align: left;
}
.reviews-title {
  font-family: 'Oswald', sans-serif;
  text-transform: uppercase;
  font-size: 1.8rem;
  margin-bottom: 30px;
  color: var(--text-color);
}
.reviews-layout {
  display: grid;
  grid-template-columns: 1.2fr 1fr;
  gap: 50px;
}
@media (max-width: 768px) {
  .reviews-layout {
    grid-template-columns: 1fr;
    gap: 30px;
  }
}
.no-reviews {
  padding: 30px;
  background-color: var(--card-bg, #fafafa);
  border-radius: 12px;
  border: 1px solid var(--border-color, #eee);
  color: #888;
  text-align: center;
}
.review-items {
  display: flex;
  flex-direction: column;
  gap: 20px;
}
.review-card {
  padding: 20px;
  background-color: var(--card-bg, #fafafa);
  border-radius: 12px;
  border: 1px solid var(--border-color, #eee);
  display: flex;
  flex-direction: column;
  gap: 10px;
}
.review-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}
.review-author {
  font-weight: 700;
  font-size: 1.05rem;
  color: var(--text-color);
}
.review-star {
  color: #f39c12;
  font-size: 1.1rem;
}
.review-text {
  margin: 0;
  line-height: 1.6;
  font-size: 0.95rem;
  opacity: 0.9;
  color: var(--text-color);
}
.review-date {
  font-size: 0.8rem;
  color: #999;
  align-self: flex-end;
}
.review-form-card, .login-prompt-card {
  padding: 25px;
  border: 1px solid var(--border-color, #eee);
  border-radius: 12px;
  background-color: var(--card-bg, #fff);
  box-shadow: 0 4px 12px rgba(0,0,0,0.03);
}
.review-form-card h3 {
  margin-top: 0;
  margin-bottom: 20px;
  font-family: 'Oswald', sans-serif;
  text-transform: uppercase;
  font-size: 1.3rem;
  color: var(--text-color);
}
.form-group {
  display: flex;
  flex-direction: column;
  gap: 8px;
  margin-bottom: 15px;
}
.form-label {
  font-weight: 600;
  font-size: 0.9rem;
  color: var(--text-color);
}
.star-selector-container {
  display: flex;
  gap: 6px;
}
.star-selector {
  font-size: 1.8rem;
  color: #f39c12;
  cursor: pointer;
  transition: transform 0.2s;
  user-select: none;
}
.star-selector:hover {
  transform: scale(1.15);
}
.comment-textarea {
  width: 100%;
  height: 100px;
  padding: 12px;
  border: 1px solid var(--border-color, #ccc);
  border-radius: 8px;
  font-size: 0.95rem;
  background-color: transparent;
  color: inherit;
  resize: vertical;
  box-sizing: border-box;
}
.comment-textarea:focus {
  outline: none;
  border-color: #c00000;
}
.submit-comment-btn {
  width: 100%;
  height: 45px;
  background-color: #c00000;
  color: white;
  border: none;
  border-radius: 50px;
  font-weight: 700;
  font-size: 0.95rem;
  cursor: pointer;
  transition: background-color 0.2s;
}
.submit-comment-btn:hover {
  background-color: #a00000;
}
.success-message {
  margin-top: 10px;
  color: #249743;
  font-size: 0.85rem;
  text-align: center;
}
.login-prompt-card {
  text-align: center;
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 15px;
}
.login-prompt-card p {
  margin: 0;
  color: var(--text-color);
  opacity: 0.8;
}
.login-link-btn {
  display: inline-block;
  background-color: #111;
  color: white;
  padding: 10px 24px;
  border-radius: 50px;
  text-decoration: none;
  font-weight: 700;
  transition: background-color 0.2s;
}
.login-link-btn:hover {
  background-color: #333;
}

.related-products {
    margin-top: 60px; /* Ürün detayından biraz uzaklaştır */
    border-top: 1px solid var(--border-color, #eee);
    padding-top: 40px;
}
</style>