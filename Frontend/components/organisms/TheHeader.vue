<script setup lang="ts">
import { computed } from 'vue';
import { useRouter } from 'vue-router';
import { useNuxtApp } from '#app';
import { useAuthStore } from '~/stores/auth';
import { useCartStore } from '~/stores/cart';
import { useTheme } from '~/composables/useTheme';

import NavMenu from '@/components/molecules/NavMenu.vue';
import SearchBar from '@/components/molecules/SearchBar.vue';
import LangSwitcher from '@/components/molecules/LangSwitcher.vue';

const { $t } = useNuxtApp() as any;
const router = useRouter();
const authStore = useAuthStore();
const cartStore = useCartStore();
const { theme, toggleTheme } = useTheme();

// Internal Navigation Links
const navItems = computed(() => [
  { text: $t('header.coffee_and_us'), href: '/hakkimizda' },
  { text: $t('header.sustainability'), href: '/surdurulebilirlik' },
  { text: $t('header.stores'), href: '/magazalar' },
  { 
    text: $t('header.discover').replace(' ▾', ''), href: '#',
    children: [
      { text: $t('header.campaigns'), href: '/campaigns' }
    ]
  }
]);

const handleUserClick = () => {
  if (authStore.user) {
    router.push('/profile');
  } else {
    router.push('/login');
  }
};

const handleLogout = async () => {
  await authStore.logout();
  router.push('/');
};

const goToCart = () => { router.push('/cart'); };
const goToStore = () => { router.push('/store'); };
const goToHome = () => { router.push('/'); };

const cartCount = computed(() => cartStore.totalItems);
const isAdmin = computed(() => authStore.isAdmin);

const goToAdmin = () => {
  router.push('/admin');
};
</script>

<template>
  <header class="unified-header">
    <div class="header-container">
      
      <!-- Logo -->
      <div class="logo-section" @click="goToHome">
        <img src="/images/EslabHeader.png" alt="Espressolab" class="logo-img" />
      </div>

      <!-- Navigation (Corporate links) -->
      <div class="nav-section">
        <NavMenu :links="navItems" />
      </div>

      <!-- Right Actions (Store features) -->
      <div class="actions-section">
        
        <div class="search-wrapper">
          <SearchBar :placeholder="$t('header.search_placeholder')" />
        </div>

        <button class="store-btn" @click="goToStore">
          {{ $t('header.online_store') }}
        </button>



        <!-- Giriş Yap (Giriş yapmamışsa) -->
        <div v-if="!authStore.isLoggedIn" class="action-item user-link" @click="handleUserClick">
          <svg class="svg-icon" width="24" height="24" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
            <circle cx="12" cy="12" r="9" stroke="currentColor" stroke-width="1.5"></circle>
            <circle cx="12" cy="10" r="3" stroke="currentColor" stroke-width="1.5"></circle>
            <path d="M17.9691 20C17.81 17.1085 15.454 15 12 15C8.54596 15 6.19003 17.1085 6.03097 20" stroke="currentColor" stroke-width="1.5" stroke-linecap="round"></path>
          </svg>
          <span class="action-text">{{ $t('login.title') || 'Giriş Yap' }}</span>
        </div>

        <!-- Kullanıcı Adı ve Çıkış Yap (Giriş yapmışsa) -->
        <template v-else>
          <div class="action-item user-link" @click="handleUserClick">
            <svg class="svg-icon" width="24" height="24" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
              <circle cx="12" cy="12" r="9" stroke="currentColor" stroke-width="1.5"></circle>
              <circle cx="12" cy="10" r="3" stroke="currentColor" stroke-width="1.5"></circle>
              <path d="M17.9691 20C17.81 17.1085 15.454 15 12 15C8.54596 15 6.19003 17.1085 6.03097 20" stroke="currentColor" stroke-width="1.5" stroke-linecap="round"></path>
            </svg>
            <span class="action-text user-name">{{ authStore.user?.name }}</span>
          </div>

          <div class="action-item logout-link" @click="handleLogout" :title="$t('profile.modal_logout_title') || 'Çıkış Yap'">
            <svg class="svg-icon logout-icon" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round" xmlns="http://www.w3.org/2000/svg">
              <path d="M9 21H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h4"></path>
              <polyline points="16 17 21 12 16 7"></polyline>
              <line x1="21" y1="12" x2="9" y2="12"></line>
            </svg>
            <span class="action-text logout-text">{{ $t('profile.modal_logout_title') || 'Çıkış Yap' }}</span>
          </div>
        </template>

        <div class="action-item cart-link" @click="goToCart">
          <svg class="svg-icon" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round" xmlns="http://www.w3.org/2000/svg">
            <circle cx="9" cy="21" r="1"></circle>
            <circle cx="20" cy="21" r="1"></circle>
            <path d="M1 1h4l2.68 13.39a2 2 0 0 0 2 1.61h9.72a2 2 0 0 0 2-1.61L23 6H6"></path>
          </svg>
          <span v-if="cartCount > 0" class="cart-badge">{{ cartCount }}</span>
        </div>

        <div class="lang-theme-container">
          <LangSwitcher />
          
          <div class="action-item theme-toggle" @click="toggleTheme" title="Toggle Theme">
            <svg v-if="theme === 'light'" class="svg-icon" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
              <path d="M21 12.79A9 9 0 1 1 11.21 3 7 7 0 0 0 21 12.79z"></path>
            </svg>
            <svg v-else class="svg-icon" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
              <circle cx="12" cy="12" r="5"></circle>
              <line x1="12" y1="1" x2="12" y2="3"></line>
              <line x1="12" y1="21" x2="12" y2="23"></line>
              <line x1="4.22" y1="4.22" x2="5.64" y2="5.64"></line>
              <line x1="18.36" y1="18.36" x2="19.78" y2="19.78"></line>
              <line x1="1" y1="12" x2="3" y2="12"></line>
              <line x1="21" y1="12" x2="23" y2="12"></line>
              <line x1="4.22" y1="19.78" x2="5.64" y2="18.36"></line>
              <line x1="18.36" y1="5.64" x2="19.78" y2="4.22"></line>
            </svg>
          </div>
        </div>

      </div>
    </div>
  </header>
</template>

<style scoped>
.unified-header {
  background-color: var(--header-bg, #ffffff);
  border-bottom: 1px solid var(--border-color, #eaeaea); 
  padding: 15px 0;
  transition: background-color 0.3s, border-color 0.3s;
  position: relative;
  z-index: 1000;
  width: 100%;
}

.header-container {
  max-width: 1400px;
  margin: 0 auto;
  padding: 0 10px;
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 10px;
}

.logo-section { cursor: pointer; width: 140px; flex-shrink: 0; }
.logo-img { width: 100%; display: block; filter: var(--logo-filter, none); }

.nav-section {
  flex-grow: 1;
  display: flex;
  justify-content: center;
}

:deep(.nav-link), :deep(.nav-item a) {
  font-family: 'Inter', sans-serif !important;
  font-size: 13px !important;
  font-weight: 600 !important;
  color: var(--text-color, #000) !important; 
  letter-spacing: 0.5px;
  text-transform: uppercase;
  white-space: nowrap;
}

.actions-section { 
  display: flex; 
  align-items: center; 
  gap: 10px; 
  color: var(--text-color, #000); 
  flex-shrink: 0; 
  flex-wrap: nowrap;
}

.search-wrapper {
  max-width: 160px;
}

.store-btn {
  background-color: #C00A00;
  color: white;
  border: none;
  border-radius: 50px;
  padding: 8px 12px;
  font-size: 11px;
  font-weight: 700;
  cursor: pointer;
  white-space: nowrap;
  transition: background-color 0.2s;
}
.store-btn:hover { background-color: #a00800; }

.admin-btn {
  background-color: #1a1a1a;
  color: #fff;
  border: none;
  border-radius: 50px;
  padding: 8px 14px;
  font-size: 11px;
  font-weight: 700;
  cursor: pointer;
  white-space: nowrap;
  transition: background-color 0.2s;
}
.admin-btn:hover {
  background-color: #c00a00;
}

.action-item { display: flex; align-items: center; gap: 4px; cursor: pointer; transition: color 0.2s; }
.action-item:hover { color: #c00a00; }
.action-text { 
  font-size: 13px; 
  font-weight: 600; 
  color: var(--text-color, #000); 
  white-space: nowrap; 
  overflow: hidden; 
  text-overflow: ellipsis; 
  max-width: 80px; 
}
.user-name { font-weight: 700; }
.logout-link {
  display: flex;
  align-items: center;
  gap: 4px;
  cursor: pointer;
  transition: color 0.2s;
}
.logout-link:hover {
  color: #c00a00;
}
.logout-text {
  font-weight: 600;
  font-size: 13px;
  color: var(--text-color, #000);
}
.svg-icon { color: var(--text-color, #000); width: 20px; height: 20px; }

.action-item.cart-link { position: relative; }

.cart-badge {
  position: absolute;
  top: -5px;
  right: -8px;
  background-color: #c00a00;
  color: white;
  border-radius: 50%;
  width: 18px;
  height: 18px;
  font-size: 10px;
  font-weight: 700;
  display: flex;
  align-items: center;
  justify-content: center;
  border: 1px solid #fff;
}

.lang-theme-container {
  display: flex;
  align-items: center;
  gap: 10px;
  flex-shrink: 0;
}

@media (min-width: 1101px) and (max-width: 1350px) {
  .header-container {
    gap: 8px;
    padding: 0 10px;
  }
  .logo-section {
    width: 110px;
  }
  :deep(.nav-link), :deep(.nav-item a) {
    font-size: 11px !important;
  }
  .actions-section {
    gap: 6px;
  }
  .search-wrapper {
    max-width: 120px;
  }
  .store-btn, .admin-btn {
    padding: 6px 10px;
    font-size: 10px;
  }
  .action-text {
    max-width: 55px;
    font-size: 11px;
  }
}

@media (min-width: 1101px) and (max-width: 1220px) {
  .logout-text {
    display: none;
  }
  .user-link .action-text {
    display: none;
  }
}

/* MOBİL UYUM */
@media (max-width: 1100px) {
  .nav-section { display: none; }
  .header-container { flex-wrap: wrap; justify-content: center; gap: 15px; }
  .search-wrapper { order: 3; width: 100%; max-width: 100%; }
  .actions-section { order: 2; width: 100%; justify-content: space-between; }
  .logo-section { order: 1; }
  .action-text { display: none; }
  .store-btn { display: none; } /* Hide store button on mobile to save space */
}
</style>