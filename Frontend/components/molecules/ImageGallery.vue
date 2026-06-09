<script setup lang="ts">
import { ref, computed } from 'vue';
// IconButton'ı favori butonu için yeniden kullanıyoruz
import IconButton from '@/components/atoms/IconButton.vue';
import { useFavoritesStore } from '~/stores/favorites';
import type { IProduct } from '~/types';

interface ImageItem {
  src: string;
  alt: string;
}

const favoritesStore = useFavoritesStore();

const props = defineProps<{
  images: ImageItem[]; // Format: [{ src: '...', alt: '...' }]
  product?: IProduct; // Ürün bilgisi favoriler için
}>();

const selectedImageIndex = ref(0);

const selectImage = (index: number) => {
  selectedImageIndex.value = index;
};

const handleToggleFavorite = async () => {
  if (props.product) {
    await favoritesStore.toggleFavorite(props.product);
  }
};

const isFav = computed(() => props.product ? favoritesStore.isFavorite(props.product.id) : false);

</script>

<template>
  <div class="image-gallery">
    <div class="main-image-wrapper">
      <IconButton class="wishlist-btn" :class="{ 'is-favorite': isFav }" @click="handleToggleFavorite">
        <svg width="24" height="24" viewBox="0 0 24 24" :fill="isFav ? '#c00a00' : 'none'" xmlns="http://www.w3.org/2000/svg">
          <path d="M12.1 21.35L10.55 20.03C5.4 15.36 2 12.28 2 8.5C2 5.42 4.42 3 7.5 3C9.24 3 10.91 3.81 12 5.09C13.09 3.81 14.76 3 16.5 3C19.58 3 22 5.42 22 8.5C22 12.28 18.6 15.36 13.45 20.04L12 21.35H12.1Z" :stroke="isFav ? '#c00a00' : '#333'" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
        </svg>
      </IconButton> 

      <img 
        v-if="images.length > 0"
        :src="images[selectedImageIndex].src" 
        :alt="images[selectedImageIndex].alt" 
        class="main-image"
      >
      <div v-else class="no-image">Görsel Yok</div>
      </div>

    <div class="thumbnail-list">
      <img
        v-for="(image, index) in images"
        :key="index"
        :src="image.src"
        :alt="image.alt"
        :class="{ active: index === selectedImageIndex }"
        @click="selectImage(index)"
        class="thumbnail-image"
      />
    </div>
  </div>
</template>

<style scoped>
.image-gallery { width: 80%; }
.main-image-wrapper {
  position: relative;
  border: 1px solid #f0f0f0;
  border-radius: 8px;
  overflow: hidden;
  margin-bottom: 10px;
}
.main-image { width: 100%; display: block; }
.wishlist-btn {
  position: absolute;
  top: 15px;
  right: 15px;
  z-index: 10;
  background-color: rgba(255, 255, 255, 0.9);
  color: #333;
  transition: all 0.3s ease;
}

.wishlist-btn.is-favorite {
  background-color: #fff5f5;
}
.thumbnail-list { display: flex; gap: 10px; }
.thumbnail-image {
  width: 70px;
  height: 70px;
  border: 1px solid #ddd;
  border-radius: 4px;
  cursor: pointer;
  object-fit: cover;
}
.thumbnail-image.active { border: 2px solid #c00a00; }
</style>