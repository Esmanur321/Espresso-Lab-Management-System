<script setup lang="ts">
import { useRouter } from 'vue-router'; // Router ekle
import BaseButton from '@/components/atoms/BaseButton.vue';
import type { IUser } from '~/types';

const router = useRouter();

defineProps<{
  buttonLabel: string;
  user: IUser | null;
}>();

const emit = defineEmits(['logout']);

// Butona tıklanınca Mağazaya git
const goToStore = () => {
  router.push('/store');
};
</script>

<template>
  <div class="user-actions">
    <div @click="goToStore">
      <BaseButton :label="buttonLabel" />
    </div>
    
    <div v-if="user" class="user-profile">
       </div>
    <div v-else class="auth-links">
       </div>
  </div>
</template>