<script setup lang="ts">
import { ref, computed } from 'vue';
import { useAuthStore } from '~/stores/auth';
import { useRouter } from 'vue-router';
import { useNuxtApp } from '#app';

const store = useAuthStore();
const router = useRouter();
const { $t } = useNuxtApp() as any;

const breadcrumbLinks = computed(() => [
  { text: $t('cart.breadcrumb_home') || 'Ana Sayfa', href: '/' },
  { text: $t('header.campaigns') || 'Kampanyalar', href: '/campaigns' }
]);

const allCampaigns = computed(() => [
  {
    date: $t('campaigns.c1_date'),
    title: $t('campaigns.c1_title'),
    description: $t('campaigns.c1_desc'),
    imageUrl: '/images/campaign1.jpg',
    buttonText: $t('campaigns.review_campaign')
  },
  {
    date: $t('campaigns.c2_date'),
    title: $t('campaigns.c2_title'),
    description: $t('campaigns.c2_desc'),
    imageUrl: '/images/campaign2.jpg',
    buttonText: $t('campaigns.review_campaign')
  },
  {
    date: $t('campaigns.c3_date'),
    title: $t('campaigns.c3_title'),
    description: $t('campaigns.c3_desc'),
    imageUrl: '/images/campaign3.jpg',
    buttonText: $t('campaigns.review_campaign')
  },
  {
    date: $t('campaigns.c4_date'),
    title: $t('campaigns.c4_title'),
    description: $t('campaigns.c4_desc'),
    imageUrl: '/images/campaign4.jpg',
    buttonText: $t('campaigns.review_campaign')
  }
]);

const handleViewCampaign = () => {
  router.push('/store');
};
</script>

<template>
  <main class="page-content">
    <div class="content-container">
      
      <div class="breadcrumbs-wrapper">
        <Breadcrumbs :links="breadcrumbLinks" />
      </div>
      
      <h1 class="page-title">{{ $t('campaigns.current_campaigns') }}</h1>
      
      <div class="campaign-list-wrapper">
        <CampaignList 
          :campaigns="allCampaigns" 
          @handleCampaignClick="handleViewCampaign"
        />
      </div>

    </div>
  </main>
</template>

<style scoped>
.page-content {
  padding-top: 20px; 
  padding-bottom: 60px;
  background-color: var(--bg-color, #fff);
  color: var(--text-color, #222);
  transition: background-color 0.3s, color 0.3s;
}

.content-container {
  max-width: 1200px; 
  margin: 0 auto;
  padding: 0 20px;
}

.breadcrumbs-wrapper {
  margin-bottom: 15px;
  font-size: 14px;
  color: #777;
}

.page-title {
  font-size: 1.8rem; 
  font-weight: 600; 
  color: var(--text-color, #222);
  margin-top: 0;
  margin-bottom: 30px;
  font-family: 'Oswald', 'Arial Narrow', sans-serif;
  text-transform: uppercase;
  text-align: left;
}

:deep(.campaign-section .page-title) {
  display: none;
}
</style>