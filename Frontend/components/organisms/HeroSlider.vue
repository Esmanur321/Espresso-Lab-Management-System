<script setup lang="ts">
import { ref, onMounted, onUnmounted, computed } from 'vue';
import SliderArrow from '@/components/atoms/SliderArrow.vue';
import SliderDotsGroup from '@/components/molecules/SliderDotsGroup.vue';

interface SlideItem {
  tr_image?: string;
  en_image?: string;
  imgUrl?: string;
  alt?: string;
}

const props = withDefaults(defineProps<{
  slides: SlideItem[];
  interval?: number;
  height?: string;
  borderRadius?: string;
}>(), {
  interval: 5000,
  height: '500px',
  borderRadius: '0px'
});

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

const startTimer = () => { if (slideInterval) return; slideInterval = setInterval(nextSlide, props.interval); };
const stopTimer = () => { if (slideInterval) { clearInterval(slideInterval); slideInterval = null; } };
const resetTimer = () => { stopTimer(); startTimer(); };

onMounted(() => { startTimer(); });
onUnmounted(() => { stopTimer(); });
</script>

<template>
  <div 
    class="hero-slider-container" 
    :style="{ height: height, borderRadius: borderRadius }"
    @mouseenter="stopTimer"
    @mouseleave="startTimer"
  >
    <div class="arrow-wrapper left">
      <SliderArrow direction="left" @click="prevSlide" />
    </div>

    <div class="slider-image-wrapper">
      <img 
        :src="currentImage" 
        :alt="currentSlide.alt || 'Banner'" 
        class="full-banner-image"
      />
    </div>

    <div class="arrow-wrapper right">
      <SliderArrow direction="right" @click="nextSlide" />
    </div>

    <div class="dots-navigation">
      <SliderDotsGroup 
        :count="slides.length" 
        :activeIndex="activeIndex"
        @dotClick="goToSlide"
      />
    </div>
  </div>
</template>

<style scoped>
.hero-slider-container {
  position: relative;
  width: 100%;
  /* height ve border-radius artık inline-style olarak geliyor */
  margin: 0 auto;
  overflow: hidden; /* Yuvarlatılan köşelerden resmin taşmaması için şart */
  background-color: #fff;
}

.slider-image-wrapper { width: 100%; height: 100%; }

.full-banner-image {
  width: 100%;
  height: 100%;
  object-fit: fill; 
  display: block;
}

.arrow-wrapper { position: absolute; top: 50%; transform: translateY(-50%); z-index: 10; }
.left { left: 20px; }
.right { right: 20px; }

.dots-navigation { position: absolute; bottom: 20px; left: 50%; transform: translateX(-50%); z-index: 10; }

@media (max-width: 768px) {
  /* Mobilde yüksekliği biraz kısalım */
  .hero-slider-container { height: 250px !important; } 
}
</style>