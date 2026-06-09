<script setup lang="ts">
defineProps({
  category: {
    type: Object,
    required: true
  }
});

defineEmits(['click']);
</script>

<template>
  <div class="category-item" @click="$emit('click', category)">
    <div class="image-wrapper">
      <img :src="category.image" :alt="category.title" class="cat-img" />
    </div>
    <span class="cat-title">{{ category.title }}</span>
  </div>
</template>

<style scoped>
/* --- KUTU STİLİ (İstediğiniz Özelliklerle) --- */
.category-item {
  /* Genişlik ve Yükseklik (Görseldeki orana uygun) */
  width: 150px;
  height: 158px;
  
  /* GÖRSELDEN ALINAN ÖZELLİKLER: */
  background-color: #F7F7F7; /* Arka plan Beyaz */
  
  /* Çerçeve: #B3B9C4 rengine yakın gri, hafif görünür */
  border: 1px solid rgba(179, 185, 196, 0.5); 
  
  /* Köşe Yuvarlaklığı: 16px */
  border-radius: 16px; 
  
  /* İçerik Düzeni */
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  gap: 15px;
  padding: 16px;
  
  cursor: pointer;
  transition: all 0.3s ease;
}

/* Hover Efekti */
.category-item:hover {
  /* Üzerine gelince gölge ve çerçeve rengi değişimi */
  box-shadow: 0 10px 30px rgba(0,0,0,0.08);
  border-color: rgba(179, 185, 196, 1); /* Çerçeve koyulaşsın */
  transform: translateY(-5px);
}

/* --- RESİM ALANI --- */
.image-wrapper {
  width: 100%;
  height: 100px; /* Resim alanı */
  display: flex;
  align-items: center;
  justify-content: center;
}

.cat-img {
  max-width: 90%;
  max-height: 100%;
  object-fit: contain;
  mix-blend-mode: multiply; /* Beyaz fonu temizler */
}

/* --- BAŞLIK STİLİ --- */
.cat-title {
  font-size: 16px;
  font-weight: 700;
  color: #374151; /* Koyu gri yazı */
  text-align: center;
  line-height: 1.2;
}
</style>