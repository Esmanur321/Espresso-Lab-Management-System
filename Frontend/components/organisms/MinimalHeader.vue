<script setup lang="ts">
// Basit bir header, sadece logo içerir
</script>

<template>
  <header class="minimal-header">
    <div class="logo-container">
      <router-link to="/">
        <img src="/images/EslabHeader.png" alt="Espressolab" class="logo-img" />
      </router-link>
    </div>
  </header>
</template>

<style scoped>
.minimal-header {
  width: 100%;
  padding: 40px 0 20px 60px; /* Sol taraftan boşluk (Görseldeki gibi) */
  background-color: #fff;
}

.logo-img {
  height: 35px; /* Logo boyutu */
  width: auto;
  display: block;
}

@media (max-width: 768px) {
  .minimal-header {
    padding: 20px;
    display: flex;
    justify-content: center;
  }
}
</style>