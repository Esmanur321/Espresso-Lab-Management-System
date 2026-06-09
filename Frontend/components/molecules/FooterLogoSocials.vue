<script setup lang="ts">
interface SocialLink {
  platform: string;
  url: string;
  icon?: string;
}

defineProps<{
  socials: SocialLink[];
}>();
</script>

<template>
  <div class="logo-socials-wrapper">
    <div class="footer-logo">
      <a href="/">
        <img src="/images/SonFooter.png" alt="Espressolab" class="f-logo-img" />
      </a>
    </div>
  </div>
</template>

<style scoped>
.logo-socials-wrapper {
  display: flex;
  flex-direction: column;
  align-items: flex-start;
  gap: 15px; /* Logo ve ikonlar arası mesafe */
}

.f-logo-img {
  height: 150px;
  display: block;
}

</style>