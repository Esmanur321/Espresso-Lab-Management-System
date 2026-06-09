<script setup lang="ts">
import { ref } from 'vue';
// Daha önce oluşturduğumuz BaseInput atomunu kullanıyoruz
import BaseInput from '@/components/atoms/BaseInput.vue';

const props = defineProps({
  modelValue: String,
  placeholder: String,
  icon: String, // Emoji yer tutucu
  type: {
    type: String,
    default: 'text'
  }
});

const emit = defineEmits(['update:modelValue']);

// Şifre gösterme/gizleme mantığı
const inputType = ref(props.type);
const isPassword = props.type === 'password';

const toggleVisibility = () => {
  inputType.value = inputType.value === 'password' ? 'text' : 'password';
};
</script>

<template>
  <div class="input-wrapper">
    <span class="icon">{{ icon }}</span>
    <BaseInput 
      :type="inputType"
      :modelValue="modelValue"
      :placeholder="placeholder"
      @update:modelValue="emit('update:modelValue', $event)"
      class="icon-input"
    />
    <button 
      v-if="isPassword" 
      type="button" 
      @click="toggleVisibility" 
      class="toggle-visibility"
    >
      👁
    </button>
  </div>
</template>

<style scoped>
.input-wrapper {
  position: relative;
  width: 100%;
}
.icon {
  position: absolute;
  left: 15px;
  top: 50%;
  transform: translateY(-50%);
  color: #999;
  z-index: 1;
}
/* :deep() ile BaseInput'un içindeki style'ı eziyoruz */
.icon-input :deep(.base-input) {
  padding-left: 40px !important; /* İkon için boşluk */
}
.toggle-visibility {
  position: absolute;
  right: 15px;
  top: 50%;
  transform: translateY(-50%);
  background: none;
  border: none;
  cursor: pointer;
  font-size: 1.2rem;
  color: #999;
}
</style>