<script setup lang="ts">
interface FooterLink {
  text: string;
  href: string;
}

defineProps<{
  title: string;
  links: FooterLink[]; // Format: [{ text: '...', href: '...' }]
}>();
</script>

<template>
  <div class="link-list-group">
    <h4 class="list-title">{{ title }}</h4>

    <ul class="link-list">
      <li v-for="link in links" :key="link.text">
        <a :href="link.href" class="footer-link">{{ link.text }}</a>
      </li>
    </ul>
  </div>
</template>

<style scoped>
.link-list-group {
  margin: 10px 0;
}
.list-title {
  font-size: 1rem;
  font-weight: 700;
  color: #333;
  margin-bottom: 15px;
  text-transform: uppercase;
}
.link-list {
  list-style: none;
  padding: 0;
  margin: 0;
}
.link-list li {
  margin-bottom: 10px;
}
.footer-link {
  text-decoration: none;
  color: #555;
  font-size: 0.9rem;
  transition: color 0.3s ease;
}
.footer-link:hover {
  color: #c00a00;
}
</style>