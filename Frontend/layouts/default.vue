<template>
  <div id="app-layout">
    <TheHeader />
    <slot />
    
    <TheFooter 
      v-if="!hideFooter"
      :helpLinks="helpMenu" 
      :categoryLinks="categoryMenu" 
      :contactInfo="contactData" 
      :socialLinks="socialLinks" 
      :copyrightText="footerCopyright" 
    />
  </div>
</template>

<script setup lang="ts">
import { ref, computed } from 'vue';
import { useRoute } from 'vue-router';
import TheHeader from '~/components/organisms/TheHeader.vue';
import TheFooter from '~/components/organisms/TheFooter.vue';

import { useNuxtApp } from '#app';
import { useAuthStore } from '~/stores/auth';

const { $t } = useNuxtApp() as any;
const authStore = useAuthStore();

const route = useRoute();

// Hide footer on Auth pages if they use this layout (though they should use 'auth' layout ideally)
const hideFooter = computed(() => {
  return route.path === '/login' || route.path === '/register';
});

// Footer Data
const helpMenu = computed(() => {
  const links = [
    { text: $t('footer.user_agreement'), href: '/kvkk' },
    { text: $t('footer.distance_sales'), href: '/iptal-iade' },
    { text: $t('footer.pre_info'), href: '/iptal-iade' },
    { text: $t('footer.cancellation'), href: '/iptal-iade' },
    { text: $t('footer.privacy_notice'), href: '/kvkk' }
  ];
  if (authStore.isAdmin) {
    links.push({ text: $t('admin.title'), href: '/admin' });
  }
  return links;
});

const categoryMenu = computed(() => [
  { text: $t('footer.all_products'), href: '/store' },
  { text: $t('footer.coffees'), href: '/store' },
  { text: $t('footer.teas'), href: '/store' },
  { text: $t('footer.accessories'), href: '/store' },
  { text: $t('footer.thermoses'), href: '/store' },
  { text: $t('footer.deals'), href: '/campaigns' }
]);

const contactData = ref({
  address: 'Tozkoparan, General Ali Rıza Gürcan Cd. Çırpıcı Çıkmazı Sok. No: 2 34173 Güngören / İstanbul',
  phone: '444 8 464',
  email: 'info@espressolab.com'
});

const socialLinks = ref([
  { platform: 'Instagram', url: 'https://instagram.com/espressolab', icon: 'Ig' },
  { platform: 'X', url: 'https://twitter.com/espressolab', icon: 'X' },
  { platform: 'YouTube', url: 'https://youtube.com/@espressolab', icon: 'Yt' },
  { platform: 'Facebook', url: 'https://facebook.com/espressolab', icon: 'Fb' },
  { platform: 'LinkedIn', url: 'https://linkedin.com/company/espressolab', icon: 'In' }
]);

const footerCopyright = computed(() => $t('footer.copyright'));
</script>

<style>
/* Global Styles transferred from App.vue */
body {
  font-family: 'Inter', sans-serif;
  margin: 0;
  background-color: #ffffff;
}
#app-layout {
  min-height: 100vh;
  display: flex;
  flex-direction: column;
}
</style>
