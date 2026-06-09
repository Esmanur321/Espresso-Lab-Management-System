<script setup lang="ts">
defineProps<{
  address?: string;
  phone?: string;
  email?: string;
}>();
</script>

<template>
  <div class="contact-info">
    <div v-if="address" class="contact-line">
      <span class="icon">📍</span>
      <span>{{ address }}</span>
    </div>

    <div v-if="phone" class="contact-line">
      <span class="icon">📞</span>
      <span>{{ phone }}</span>
    </div>

    <div v-if="email" class="contact-line">
      <span class="icon">✉️</span>
      <span>{{ email }}</span>
    </div>
  </div>
</template>

<style scoped>
.contact-info {
  font-size: 0.9rem;
  color: #555;
}
.contact-line {
  display: flex;
  align-items: flex-start;
  margin-bottom: 15px;
}
.contact-line .icon {
  margin-right: 12px;
  font-size: 1.1rem;
  color: #333;
}
</style>