<template>
  <div class="auth-layout">
    <div class="auth-lang-bar">
      <LangSwitcher />
    </div>
    <slot />
  </div>
</template>

<script setup lang="ts">
import LangSwitcher from '~/components/molecules/LangSwitcher.vue';
</script>

<style scoped>
.auth-layout {
  min-height: 100vh;
  display: flex;
  flex-direction: column;
  background-color: var(--bg-color);
  color: var(--text-color);
  transition: background-color 0.3s, color 0.3s;
  position: relative;
}

.auth-lang-bar {
  position: absolute;
  top: 16px;
  right: 20px;
  z-index: 100;
}
</style>
