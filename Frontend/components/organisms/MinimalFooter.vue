<script setup lang="ts">
defineProps({
  copyrightText: String
});
</script>

<template>
  <footer class="minimal-footer">
    <p>{{ copyrightText }}</p>
  </footer>
</template>

<style scoped>
.minimal-footer {
  text-align: center;
  padding: 20px;
}
.minimal-footer p {
  font-size: 0.8rem;
  color: #777;
  margin: 0;
}
</style>