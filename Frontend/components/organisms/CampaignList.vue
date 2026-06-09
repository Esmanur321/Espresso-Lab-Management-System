<script setup lang="ts">
import CampaignCard from '@/components/molecules/CampaignCard.vue';

interface Campaign {
  title: string;
  imageUrl: string;
  description?: string;
}

defineProps<{
  campaigns: Campaign[];
}>();

const emit = defineEmits(['handleCampaignClick']);
</script>

<template>
  <section class="campaign-section">
    <h2 class="page-title">{{ $t('campaigns.current_campaigns') }}</h2>

    <div class="campaign-grid">
      <CampaignCard 
        v-for="(campaign, index) in campaigns" 
        :key="index"
        :campaign="campaign"
        @viewCampaign="emit('handleCampaignClick', $event)"
      />
    </div>
  </section>
</template>

<style scoped>
.campaign-section {
  width: 100%;
}

.page-title {
  font-size: 2.5rem; /* Görseldeki gibi büyük */
  font-weight: 800;  /* Kalın */
  color: var(--text-color, #222);       /* Koyu siyah */
  margin-top: 0;
  margin-bottom: 40px;
  font-family: 'Oswald', 'Arial Narrow', sans-serif; /* Dar font */
  text-transform: uppercase;
  text-align: left;
}

.campaign-grid {
  display: grid;
  /* Masaüstünde tam olarak 2 sütun (Görseldeki gibi) */
  grid-template-columns: 1fr 1fr; 
  gap: 30px; /* Kutular arası boşluk */
}

/* Mobil uyum */
@media (max-width: 768px) {
  .campaign-grid {
    grid-template-columns: 1fr; /* Mobilde alt alta */
  }
  .page-title {
    font-size: 2rem;
  }
}
</style>