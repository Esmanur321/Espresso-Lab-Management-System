<script setup lang="ts">
import BaseButton from '@/components/atoms/BaseButton.vue';

defineProps({
  campaign: {
    type: Object,
    required: true
  }
});

const emit = defineEmits(['viewCampaign']);
</script>

<template>
  <div class="campaign-card">
    <div class="card-image-wrapper">
      <img :src="campaign.imageUrl" :alt="campaign.title" class="card-image" />
    </div>
    
    <div class="card-content">
      <p class="campaign-date" v-if="campaign.date">{{ campaign.date }}</p>

      <h3 class="card-title">{{ campaign.title }}</h3>
      
      <p class="card-description">{{ campaign.description }}</p>
    </div>
  </div>
</template>

<style scoped>
.campaign-card {
  background: transparent;
  border-radius: 16px;
  overflow: hidden;
  display: flex;
  flex-direction: column;
  /* Kartın kendi gölgesi veya çerçevesi yok, görseldeki gibi temiz duruyor */
}

/* --- RESİM ALANI AYARI --- */
.card-image-wrapper {
  width: 100%;
  
  /* GÜNCELLEME: Sabit yükseklik yerine en-boy oranı kullanıyoruz.
     Resminiz 1280x640 olduğu için oran 2/1'dir.
     Bu sayede resim asla kesilmez ve her ekranda orantılı küçülür/büyür.
  */
  aspect-ratio: 2 / 1; 
  
  border-radius: 16px; /* Resmin köşeleri yuvarlak */
  overflow: hidden;
  margin-bottom: 20px;
  background-color: var(--border-color, #f0f0f0); /* Resim yüklenene kadar gri fon */
}

.card-image {
  width: 100%;
  height: 100%;
  /* 'cover' yerine 'contain' veya bu oranda 'cover' aynı sonucu verir 
     ama oran 2/1 olduğu için tam oturacaktır. */
  object-fit: cover; 
  transition: transform 0.5s ease;
  display: block;
}

.campaign-card:hover .card-image {
  transform: scale(1.03); /* Hover efektini biraz yumuşattım */
}

/* --- İÇERİK STİLLERİ (Aynı kaldı) --- */
.card-content {
  text-align: left;
}

.campaign-date {
  color: #c00a00;
  font-weight: 700;
  font-size: 0.9rem;
  margin-bottom: 10px;
}

.card-title {
  font-size: 1.5rem;
  font-weight: 800;
  color: var(--text-color, #222);
  margin: 0 0 15px 0;
  font-family: 'Arial', sans-serif;
}

.card-description {
  font-size: 1rem;
  color: var(--text-color, #555);
  opacity: 0.85;
  line-height: 1.6;
  margin-bottom: 25px;
}

.campaign-btn {
  border-radius: 50px;
  padding: 12px 30px;
  font-size: 14px;
  text-transform: none;
}
</style>