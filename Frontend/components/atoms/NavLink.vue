<script setup lang="ts">
defineProps({
  text: { type: String, required: true },
  hasDropdown: { type: Boolean, default: false },
  to: { type: String, default: '#' }
});
</script>

<template>
  <NuxtLink :to="to" class="nav-link">
    {{ text }}
    <span v-if="hasDropdown" class="dropdown-arrow">▼</span>
  </NuxtLink>
</template>

<style scoped>
.nav-link {
  display: flex;
  align-items: center;
  padding: 10px 15px;
  text-decoration: none;
  color: #333; /* Siyahımsı gri */
  font-weight: 700; /* Fontu biraz kalınlaştırdım resimdeki gibi */
  font-size: 0.85rem; /* Fontu biraz küçülttüm */
  transition: color 0.3s ease;
  white-space: nowrap;
  letter-spacing: 0.5px;
}

.nav-link:hover {
  color: #c00a00;
}

.dropdown-arrow {
  margin-left: 6px;
  font-size: 0.6rem;
  color: #777;
}
</style>