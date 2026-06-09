<script setup lang="ts">
import { onMounted } from 'vue';
import { useCartStore } from '~/stores/cart';
import { useTheme } from '~/composables/useTheme';

// Uygulama başladığında store'u başlat
const cartStore = useCartStore();
const { initTheme } = useTheme();

onMounted(() => {
  initTheme();
  cartStore.initialize();
});
</script>

<template>
  <NuxtLayout>
    <NuxtPage />
  </NuxtLayout>
  <AppToast />
</template>

<style>
/* Basit Dark Theme Değişkenleri */
:root {
  --bg-color: #ffffff;
  --text-color: #333333;
  --header-bg: #ffffff;
  --border-color: #eeeeee;
  --card-bg: #ffffff;
}
:root.dark-theme {
  --bg-color: #111827;
  --text-color: #f3f4f6;
  --header-bg: #1f2937;
  --border-color: #374151;
  --card-bg: #1f2937;
}
body {
  background-color: var(--bg-color);
  color: var(--text-color);
  transition: background-color 0.3s, color 0.3s;
}

/* Global Dark Mode Overrides */
.dark-theme .page-content,
.dark-theme main.page-content,
.dark-theme .main-content-container,
.dark-theme .page-content-wrapper,
.dark-theme .profile-layout,
.dark-theme .profile-content-area {
  background-color: var(--bg-color) !important;
  color: var(--text-color) !important;
}

.dark-theme .content-panel,
.dark-theme .order-card,
.dark-theme .ordered-product,
.dark-theme .address-item,
.dark-theme .card,
.dark-theme .unauthorized-card,
.dark-theme .confirm-modal-content,
.dark-theme .address-modal,
.dark-theme .modal-content,
.dark-theme .cart-item,
.dark-theme .cart-sidebar-card,
.dark-theme .coupon-card,
.dark-theme .order-summary-card,
.dark-theme .payment-method-card,
.dark-theme .payment-form-card,
.dark-theme .profile-nav-menu,
.dark-theme .side-nav-item,
.dark-theme .profile-nav-link {
  background-color: var(--card-bg) !important;
  color: var(--text-color) !important;
  border-color: var(--border-color) !important;
}

.dark-theme .side-nav-item:hover,
.dark-theme .profile-nav-link:not(.active):hover {
  background-color: var(--border-color) !important;
}

.dark-theme .side-nav-item.active,
.dark-theme .profile-nav-link.active,
.dark-theme .profile-nav-link.active {
  background-color: #c00a00 !important;
  color: #ffffff !important;
}

.dark-theme input,
.dark-theme textarea,
.dark-theme select,
.dark-theme .custom-input-group,
.dark-theme .modal-input,
.dark-theme .modal-textarea,
.dark-theme .modal-select,
.dark-theme .phone-input-row,
.dark-theme .admin-input,
.dark-theme .comment-textarea {
  background-color: var(--bg-color) !important;
  color: var(--text-color) !important;
  border-color: var(--border-color) !important;
}

.dark-theme .disabled-input,
.dark-theme .phone-prefix,
.dark-theme .phone-group.disabled-input .phone-prefix {
  background-color: var(--border-color) !important;
  color: var(--text-color) !important;
  border-color: var(--border-color) !important;
  opacity: 0.8;
}

.dark-theme .panel-header,
.dark-theme .modal-header,
.dark-theme .order-header,
.dark-theme .card-title,
.dark-theme .section-header {
  border-bottom-color: var(--border-color) !important;
  color: var(--text-color) !important;
}

.dark-theme .panel-title,
.dark-theme .section-title,
.dark-theme .page-title,
.dark-theme h1,
.dark-theme h2,
.dark-theme h3,
.dark-theme h4,
.dark-theme h5,
.dark-theme h6,
.dark-theme .confirm-title,
.dark-theme .feedback-label,
.dark-theme .address-title,
.dark-theme .font-bold {
  color: var(--text-color) !important;
}

.dark-theme .address-detail,
.dark-theme .address-contact,
.dark-theme .order-date,
.dark-theme .order-status,
.dark-theme .ordered-product-qty,
.dark-theme .char-counter,
.dark-theme .feedback-bottom-text,
.dark-theme .confirm-desc,
.dark-theme .empty-favorites-text,
.dark-theme .empty-text,
.dark-theme .desc,
.dark-theme .warning-note {
  color: var(--text-color) !important;
  opacity: 0.8 !important;
}

.dark-theme .orders-table th {
  background-color: var(--bg-color) !important;
  color: var(--text-color) !important;
  border-bottom-color: var(--border-color) !important;
}

.dark-theme .orders-table td {
  border-bottom-color: var(--border-color) !important;
}
</style>
