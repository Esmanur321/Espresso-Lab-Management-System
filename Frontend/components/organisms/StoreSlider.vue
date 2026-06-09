<script setup lang="ts">
import { ref, onMounted, onUnmounted, computed } from 'vue';
import SliderArrow from '@/components/atoms/SliderArrow.vue';
import SliderDotsGroup from '@/components/molecules/SliderDotsGroup.vue';

interface SlideItem {
  tr_image?: string;
  en_image?: string;
  imgUrl?: string;
  alt: string;
}

const props = defineProps<{
  slides: SlideItem[];
  interval?: number;
}>();

import { useI18n } from '~/composables/useI18n';
const { locale } = useI18n();
const currentLang = computed(() => locale.value);

const activeIndex = ref(0);
const currentSlide = computed(() => props.slides[activeIndex.value] || { alt: '' });
const currentImage = computed(() => {
  const banner = currentSlide.value;
  if (!banner) return '';
  return currentLang.value === 'en' ? (banner.en_image || banner.imgUrl || '') : (banner.tr_image || banner.imgUrl || '');
});
let slideInterval: ReturnType<typeof setInterval> | null = null;

const nextSlide = () => { activeIndex.value = (activeIndex.value + 1) % props.slides.length; };
const prevSlide = () => { activeIndex.value = (activeIndex.value - 1 + props.slides.length) % props.slides.length; };
const goToSlide = (index: number) => { activeIndex.value = index; resetTimer(); };

const interval = props.interval ?? 5000;
const startTimer = () => { if (slideInterval) return; slideInterval = setInterval(nextSlide, interval); };
const stopTimer = () => { if (slideInterval) { clearInterval(slideInterval); slideInterval = null; } };
const resetTimer = () => { stopTimer(); startTimer(); };

onMounted(() => { startTimer(); });
onUnmounted(() => { stopTimer(); });
</script>

<template>
  <div class="store-slider" @mouseenter="stopTimer" @mouseleave="startTimer">
    <div class="arrow-wrapper left"><SliderArrow direction="left" @click="prevSlide" /></div>

    <div class="slider-image-wrapper">
      <img :src="currentImage" :alt="currentSlide.alt" class="store-banner-image" />
    </div>

    <div class="arrow-wrapper right"><SliderArrow direction="right" @click="nextSlide" /></div>

    <div class="dots-navigation">
      <SliderDotsGroup :count="slides.length" :activeIndex="activeIndex" @dotClick="goToSlide" />
    </div>
  </div>
</template>

<style scoped>
.store-slider {
  position: relative;
  width: 100%;
  height: 450px; /* Mağaza için sabit yükseklik */
  overflow: hidden;
  background-color: #f9f9f9;
  border-radius: 24px; /* Yuvarlak Köşeler BURADA */
}

.slider-image-wrapper { width: 100%; height: 100%; }

.store-banner-image {
  width: 100%;
  height: 100%;
  object-fit: cover; /* Mağazada resimler bozulmasın, gerekirse kessin */
  display: block;
}

.arrow-wrapper { position: absolute; top: 50%; transform: translateY(-50%); z-index: 10; }
.left { left: 20px; }
.right { right: 20px; }
.dots-navigation { position: absolute; bottom: 15px; left: 50%; transform: translateX(-50%); z-index: 10; }

@media (max-width: 768px) {
  .store-slider { height: 250px; border-radius: 16px; }
}
</style>