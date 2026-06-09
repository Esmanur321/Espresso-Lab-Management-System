<script setup lang="ts">
interface BreadcrumbLink {
  text: string;
  href: string;
}

defineProps<{
  links: BreadcrumbLink[]; // Format: [{ text: '...', href: '...' }]
}>();
</script>

<template>
  <nav class="breadcrumbs">
    <span v-for="(link, index) in links" :key="link.text">
      <router-link v-if="index < links.length - 1" :to="link.href" class="crumb-link">
        {{ link.text }}
      </router-link>
      <span v-else class="crumb-active">{{ link.text }}</span>

      <span v-if="index < links.length - 1" class="separator"> > </span>
    </span>
  </nav>
</template>

<style scoped>
.breadcrumbs { font-size: 0.9rem; color: #777; margin-bottom: 20px; }
.crumb-link { text-decoration: none; color: #555; }
.crumb-link:hover { text-decoration: underline; }
.crumb-active { font-weight: 600; color: #333; }
.separator { margin: 0 8px; }
</style>