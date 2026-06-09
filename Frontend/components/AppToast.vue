<script setup lang="ts">
import { useToast } from '~/composables/useToast';
import { useNuxtApp } from '#app';
import { computed } from 'vue';

const { state, closeToast } = useToast();
const { $t } = useNuxtApp() as any;

const iconMap = {
  success: '✅',
  error: '❌',
  warning: '⚠️',
  info: 'ℹ️',
};

const colorMap = {
  success: '#00a651',
  error: '#c00000',
  warning: '#e67e22',
  info: '#2980b9',
};

const icon = computed(() => iconMap[state.value.type] || 'ℹ️');
const headerColor = computed(() => colorMap[state.value.type] || '#2980b9');
</script>

<template>
  <Teleport to="body">
    <Transition name="toast-fade">
      <div v-if="state.visible" class="toast-overlay" @click.self="closeToast">
        <div class="toast-modal">
          <div class="toast-header" :style="{ background: headerColor }">
            <span class="toast-icon">{{ icon }}</span>
          </div>
          <div class="toast-body">
            <p class="toast-message">{{ state.message }}</p>
          </div>
          <div class="toast-footer">
            <button class="toast-ok-btn" @click="closeToast">
              {{ $t('common.ok') }}
            </button>
          </div>
        </div>
      </div>
    </Transition>
  </Teleport>
</template>

<style scoped>
.toast-overlay {
  position: fixed;
  inset: 0;
  background: rgba(0, 0, 0, 0.45);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 99999;
  backdrop-filter: blur(3px);
}

.toast-modal {
  background: #fff;
  border-radius: 16px;
  min-width: 300px;
  max-width: 420px;
  width: 90%;
  box-shadow: 0 20px 60px rgba(0, 0, 0, 0.25);
  overflow: hidden;
  animation: modal-pop 0.25s cubic-bezier(0.34, 1.56, 0.64, 1);
}

@keyframes modal-pop {
  from { transform: scale(0.85); opacity: 0; }
  to   { transform: scale(1);    opacity: 1; }
}

.toast-header {
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 20px;
}

.toast-icon {
  font-size: 36px;
  line-height: 1;
}

.toast-body {
  padding: 20px 24px 12px;
  text-align: center;
}

.toast-message {
  font-size: 15px;
  color: #333;
  line-height: 1.6;
  margin: 0;
  font-family: 'Inter', 'Outfit', sans-serif;
}

.toast-footer {
  padding: 12px 24px 20px;
  display: flex;
  justify-content: center;
}

.toast-ok-btn {
  background: #c00000;
  color: #fff;
  border: none;
  border-radius: 50px;
  padding: 10px 40px;
  font-size: 14px;
  font-weight: 700;
  font-family: 'Oswald', sans-serif;
  text-transform: uppercase;
  letter-spacing: 1px;
  cursor: pointer;
  transition: background 0.2s, transform 0.15s;
}

.toast-ok-btn:hover {
  background: #a00000;
  transform: scale(1.04);
}

/* Transition */
.toast-fade-enter-active,
.toast-fade-leave-active {
  transition: opacity 0.2s;
}
.toast-fade-enter-from,
.toast-fade-leave-to {
  opacity: 0;
}
</style>
