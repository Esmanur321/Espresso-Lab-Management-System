/**
 * useToast - Global bildirim sistemi
 * Tarayıcının native alert() yerine kullanılır.
 * Dile bağımsız "OK/Tamam" butonu için özel modal kullanır.
 */
import { ref } from 'vue';

interface ToastState {
  visible: boolean;
  message: string;
  type: 'success' | 'error' | 'info' | 'warning';
  resolve?: () => void;
}

const state = ref<ToastState>({
  visible: false,
  message: '',
  type: 'info',
});

export const useToast = () => {
  const showToast = (message: string, type: ToastState['type'] = 'info'): Promise<void> => {
    return new Promise((resolve) => {
      state.value = { visible: true, message, type, resolve };
    });
  };

  const closeToast = () => {
    if (state.value.resolve) state.value.resolve();
    state.value = { visible: false, message: '', type: 'info' };
  };

  return { state, showToast, closeToast };
};
