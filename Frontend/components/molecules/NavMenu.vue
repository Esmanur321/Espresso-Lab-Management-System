<script setup lang="ts">
import { useRoute } from 'vue-router'; // Mevcut sayfayı öğrenmek için
import NavLink from '@/components/atoms/NavLink.vue';

interface NavLinkChild {
  text: string;
  href: string;
}

interface NavLinkItem {
  text: string;
  href?: string;
  children?: NavLinkChild[];
}

defineProps<{
  links: NavLinkItem[];
}>();

const route = useRoute();

// FONKSİYON: Bir menü öğesi aktif mi?
// Eğer kendisi veya çocuklarından biri şu anki sayfadaysa TRUE döner.
const isActiveItem = (link: NavLinkItem): boolean => {
  // 1. Kendi linki eşleşiyor mu? (Örn: /magazalar)
  if (link.href === route.path) return true;
  
  // 2. Çocuklarından biri eşleşiyor mu? (Örn: /campaigns, KEŞFET'in çocuğudur)
  if (link.children) {
    return link.children.some(child => child.href === route.path);
  }
  
  return false;
};
</script>

<template>
  <nav class="main-nav">
    <ul class="nav-list">
      
      <li 
        v-for="link in links" 
        :key="link.text" 
        class="nav-item"
        :class="{ 'is-active': isActiveItem(link) }" 
      >
        <div class="link-wrapper">
          <NavLink 
            :text="link.text" 
            :hasDropdown="!!link.children" 
            :to="link.href"
          />
        </div>

        <div v-if="link.children" class="dropdown-menu">
          <ul>
            <li v-for="child in link.children" :key="child.text">
              <router-link :to="child.href">{{ child.text }}</router-link>
            </li>
          </ul>
        </div>

      </li>

    </ul>
  </nav>
</template>

<style scoped>
.main-nav {
  height: 100%;
}

.nav-list {
  display: flex;
  list-style: none;
  margin: 0;
  padding: 0;
  gap: 10px; 
}

.nav-item {
  position: relative;
  padding: 15px 0;
  cursor: pointer;
}

/* --- RENK AYARLARI --- */

/* 1. HOVER DURUMU: Fare üzerine gelince Kırmızı olsun */
.nav-item:hover :deep(.nav-link) {
  color: #c00a00 !important;
  transition: color 0.3s ease;
}

/* 2. AKTİF DURUMU: Eğer o sayfadaysak Kırmızı kalsın */
.nav-item.is-active :deep(.nav-link) {
  color: #c00a00 !important;
}

/* --- DROPDOWN STİLLERİ --- */
.dropdown-menu {
  opacity: 0;
  visibility: hidden;
  transform: translateY(10px);
  transition: all 0.2s ease-in-out;
  position: absolute;
  top: 100%; 
  left: -20px; 
  background-color: white;
  min-width: 200px;
  box-shadow: 0 10px 30px rgba(0,0,0,0.1);
  border-radius: 12px;
  padding: 10px 0;
  z-index: 100;
  border-top: 3px solid #c00a00;
}

/* Köprü (Menü kapanmasın diye) */
.dropdown-menu::before {
  content: "";
  position: absolute;
  top: -20px; 
  left: 0;
  width: 100%;
  height: 20px;
  background: transparent;
}

.nav-item:hover .dropdown-menu {
  opacity: 1;
  visibility: visible;
  transform: translateY(0);
}

.dropdown-menu ul {
  list-style: none;
  padding: 0;
  margin: 0;
}

.dropdown-menu li a {
  display: block;
  padding: 12px 25px;
  text-decoration: none;
  color: #333;
  font-size: 14px;
  font-weight: 600;
  transition: all 0.2s;
  font-family: 'Inter', sans-serif; /* Font uyumu */
}

.dropdown-menu li a:hover {
  background-color: #f9f9f9;
  color: #c00a00;
  padding-left: 30px; 
}
</style>