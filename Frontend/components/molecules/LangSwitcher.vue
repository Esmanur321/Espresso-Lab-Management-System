<script setup lang="ts">
import { computed, ref, onMounted, onUnmounted } from 'vue';
import { useI18n } from '~/composables/useI18n';

const { locale, setLocale } = useI18n();

const currentLang = computed(() => locale.value.toUpperCase());
const isDropdownOpen = ref(false);

const toggleDropdown = () => {
  isDropdownOpen.value = !isDropdownOpen.value;
};

const selectLanguage = (lang: string) => {
  setLocale(lang);
  isDropdownOpen.value = false;
};

// Dışarı tıklanınca kapatma mantığı
const dropdownRef = ref<HTMLElement | null>(null);

const handleClickOutside = (event: MouseEvent) => {
  if (dropdownRef.value && !dropdownRef.value.contains(event.target as Node)) {
    isDropdownOpen.value = false;
  }
};

onMounted(() => {
  document.addEventListener('click', handleClickOutside);
});

onUnmounted(() => {
  document.removeEventListener('click', handleClickOutside);
});
</script>

<template>
  <ClientOnly>
    <div class="lang-wrapper" ref="dropdownRef" style="position: relative;">
      <div class="lang-pill" @click="toggleDropdown" style="cursor: pointer;">
        <div class="flag-circle">
          <img v-if="currentLang === 'TR'" src="/images/turkey-flag.png" alt="TR" class="flag-img" />
          <img v-else src="/images/usa-flag.png" alt="EN" class="flag-img" />
        </div>
        <span class="lang-text">{{ currentLang }}</span>
        <span class="arrow-down">▼</span>
      </div>

      <!-- Açılır Menü -->
      <div v-if="isDropdownOpen" class="lang-dropdown">
        <div class="lang-option" @click="selectLanguage('TR')">
          <div class="flag-circle-sm">
            <img src="/images/turkey-flag.png" alt="TR" class="flag-img" />
          </div>
          <span>TR</span>
        </div>
        <div class="lang-option" @click="selectLanguage('EN')">
          <div class="flag-circle-sm">
             <img src="/images/usa-flag.png" alt="EN" class="flag-img" />
          </div>
          <span>EN</span>
        </div>
      </div>
    </div>
  </ClientOnly>
</template>

<style scoped>
.lang-pill { 
  display: flex; 
  align-items: center; 
  gap: 5px; 
  border: 1px solid #e0e0e0; 
  padding: 3px 8px 3px 3px; 
  border-radius: 50px; 
  background-color: #fff;
  cursor: pointer; 
}

.flag-circle { 
  width: 20px; 
  height: 20px; 
  border-radius: 50%; 
  display: flex; 
  align-items: center; 
  justify-content: center; 
  overflow: hidden;
}

.lang-text { 
  font-size: 12px; 
  font-weight: 600; 
  color: #333; 
}

.arrow-down { 
  font-size: 10px; 
  color: #777; 
  margin-top: -1px; 
}

.flag-img {
  width: 100%;
  height: 100%;
  object-fit: cover;
  border-radius: 50%;
}

/* Dropdown Stilleri */
.lang-dropdown {
  position: absolute;
  top: 100%;
  right: 0;
  margin-top: 5px;
  background-color: white;
  border: 1px solid #e0e0e0;
  border-radius: 8px;
  box-shadow: 0 4px 12px rgba(0,0,0,0.1);
  padding: 5px;
  z-index: 100;
  min-width: 80px;
}

.lang-option {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 8px 10px;
  cursor: pointer;
  border-radius: 4px;
  transition: background 0.2s;
}

.lang-option:hover {
  background-color: #f5f5f5;
}

.lang-option span {
  font-size: 13px;
  font-weight: 500;
  color: #333;
}

.flag-circle-sm {
  width: 18px;
  height: 18px;
  border-radius: 50%;
  overflow: hidden;
  border: 1px solid #eee;
}
</style>
