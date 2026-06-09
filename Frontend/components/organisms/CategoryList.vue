<script setup lang="ts">
import CategoryItem from '@/components/molecules/CategoryItem.vue';

interface Category {
  title: string;
  image: string;
}

defineProps<{
  categories: Category[];
}>();

defineEmits(['selectCategory']);
</script>

<template>
  <section class="category-section">
    <h2 class="section-title">{{ $t('store.categories') }}</h2>
    
    <div class="category-row">
      <CategoryItem 
        v-for="(cat, index) in categories" 
        :key="index"
        :category="cat"
        @click="$emit('selectCategory', cat)"
      />
    </div>
  </section>
</template>

<style scoped>
.category-section {
  width: 100%;
  margin-top: 40px;
}

.section-title {
  font-size: 30px;
  font-weight: 40rem;
  color: #4D525A;
  font-family: 'Bebas Kai', 'Inter', sans-serif;
  text-transform: uppercase;
  margin-bottom: 30px;
  text-align: left;
  letter-spacing: 0.5px;
}

/* ... */
.category-row {
  display: grid;
  /* 160px'lik kutulara göre otomatik yerleşim */
  grid-template-columns: repeat(auto-fill, 160px);
  
  gap: 45px; /* Kutular arası boşluk */
  justify-content: flex-start; 
}
/* ... */

@media (max-width: 768px) {
  .category-row {
    justify-content: center;
    gap: 20px;
    /* Mobilde sığmazsa otomatik küçülsün diye minmax kullanabiliriz */
    grid-template-columns: repeat(auto-fill, minmax(140px, 1fr));
  }
}
</style>