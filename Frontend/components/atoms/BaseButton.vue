<script setup lang="ts">
defineProps({
  label: {
    type: String,
    required: true
  },
  variant: {
    type: String,
    default: 'solid' // 'solid' (dolu) veya 'outline' (çerçeve)
  }
});
</script>

<template>
  <button :class="['base-button', variant]">
    {{ label }}
  </button>
</template>

<style scoped>
.base-button {
  border: 1px solid #c00a00; /* Ortak kırmızı çerçeve */
  border-radius: 50px;
  padding: 10px 20px;
  font-weight: 600;
  font-size: 0.9rem;
  cursor: pointer;
  transition: all 0.3s ease;
  text-transform: uppercase;
}

/* Dolu (Solid) Stil - Varsayılan */
.base-button.solid {
  background-color: #c00a00;
  color: white;
}
.base-button.solid:hover {
  background-color: #a00a00;
  border-color: #a00a00;
}

/* Çerçeve (Outline) Stil - Yeni */
.base-button.outline {
  background-color: #ffffff;
  color: #c00a00;
}
.base-button.outline:hover {
  background-color: #fef7f2; /* Çok açık pembe */
}

/* Pasif (Disabled) durumunu da yönetelim */
.base-button:disabled {
  background-color: #e0e0e0;
  color: #999;
  border-color: #e0e0e0;
  cursor: not-allowed;
}
</style>