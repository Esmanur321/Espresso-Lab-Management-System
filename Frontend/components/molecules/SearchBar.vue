<script setup lang="ts">
import { ref } from 'vue';
import { useRouter } from 'vue-router';

defineProps({
  placeholder: {
    type: String,
    default: 'Ürün adı arayın'
  }
});

const query = ref('');
const router = useRouter();

const doSearch = () => {
  const q = query.value.trim();
  if (q) {
    router.push(`/store?search=${encodeURIComponent(q)}`);
    query.value = '';
  }
};
</script>

<template>
  <div class="search-bar-wrapper">
    <span class="search-icon" @click="doSearch" style="cursor:pointer">
      <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="#999" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="11" cy="11" r="8"></circle><line x1="21" y1="21" x2="16.65" y2="16.65"></line></svg>
    </span>
    <input
      type="text"
      v-model="query"
      :placeholder="placeholder"
      class="search-input"
      @keyup.enter="doSearch"
    />
  </div>
</template>

<style scoped>
.search-bar-wrapper {
  display: flex;
  align-items: center;
  background-color: #fff;
  
  /* GÖRSELDEKİ GİBİ: İnce gri çerçeve */
  border: 1px solid #e5e5e5; 
  
  /* GÖRSELDEKİ GİBİ: Hafif yuvarlak köşeler (Tam yuvarlak değil) */
  border-radius: 12px; 
  
  padding: 10px 15px;
  width: 100%;
  height: 48px; /* Yükseklik sabitlendi */
  box-sizing: border-box;
  transition: all 0.3s ease;
}

.search-bar-wrapper:focus-within {
  border-color: #333; /* Tıklanınca koyulaşsın */
}

.search-icon {
  display: flex;
  align-items: center;
  margin-right: 12px;
}

.search-input {
  border: none;
  outline: none;
  width: 100%;
  font-size: 14px;
  color: #333;
  background: transparent;
}

.search-input::placeholder {
  color: #999;
}
</style>