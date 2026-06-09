import { defineStore } from 'pinia';
import { ref } from 'vue';

export const useUiStore = defineStore('ui', () => {
  // Global UI State
  const isLoading = ref(false);
  const isSidebarOpen = ref(false);
  const activeModal = ref<string | null>(null);
  const toastMessage = ref<string | null>(null);

  // Actions
  const showLoading = () => { isLoading.value = true; };
  const hideLoading = () => { isLoading.value = false; };

  const toggleSidebar = () => { isSidebarOpen.value = !isSidebarOpen.value; };
  const closeSidebar = () => { isSidebarOpen.value = false; };

  const openModal = (modalId: string) => { activeModal.value = modalId; };
  const closeModal = () => { activeModal.value = null; };

  const showToast = (message: string) => {
    toastMessage.value = message;
    setTimeout(() => { toastMessage.value = null; }, 3000);
  };

  return {
    isLoading,
    isSidebarOpen,
    activeModal,
    toastMessage,
    showLoading,
    hideLoading,
    toggleSidebar,
    closeSidebar,
    openModal,
    closeModal,
    showToast
  };
});
