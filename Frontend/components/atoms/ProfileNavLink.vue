<script setup lang="ts">
defineProps({
  label: String,
  isActive: { // Tıklanan linki (kırmızı) göstermek için
    type: Boolean,
    default: false
  }
});
</script>

<template>
  <a href="#" :class="['profile-nav-link', { active: isActive }]">
    {{ label }}
  </a>
</template>

<style scoped>
.profile-nav-link {
  display: block;
  padding: 20px 25px;
  text-decoration: none;
  color: var(--text-color, #333);
  font-size: 1rem;
  font-weight: 600;
  border-bottom: 1px solid var(--border-color, #f0f0f0);
  transition: all 0.3s ease;
}

/* Aktif (seçili) link stili */
.profile-nav-link.active {
  color: #c00a00; /* Kırmızı metin */
  background-color: var(--border-color, #fef7f2); /* Tema uyumlu arka plan */
}

/* Son elemanın alt çizgisini kaldıralım */
.profile-nav-link:last-child {
  border-bottom: none;
}

.profile-nav-link:not(.active):hover {
  background-color: var(--border-color, #f9f9f9);
}
</style>