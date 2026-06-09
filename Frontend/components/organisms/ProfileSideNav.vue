<script setup lang="ts">
import ProfileNavLink from '@/components/atoms/ProfileNavLink.vue';

interface NavItem {
  label: string;
  slug: string;
}

// Sayfadan (ProfilePage) prop olarak al
defineProps<{
  navItems: NavItem[]; // [{ label: '...', slug: '...' }]
  activeSlug: string; // 'siparislerim'
}>();

const emit = defineEmits(['navigate']);
</script>

<template>
  <aside class="profile-nav-menu">
    <ProfileNavLink 
      v-for="item in navItems"
      :key="item.slug"
      :label="item.label"
      :isActive="item.slug === activeSlug"
      @click.prevent="emit('navigate', item.slug)"
    />
  </aside>
</template>

<style scoped>
.profile-nav-menu {
  background-color: var(--card-bg, #ffffff);
  border: 1px solid var(--border-color, #f0f0f0);
  border-radius: 12px;
  overflow: hidden; /* Köşelerin yuvarlak kalması için */
}
</style>