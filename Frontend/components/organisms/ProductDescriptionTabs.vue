<script setup lang="ts">
import { ref } from 'vue';

interface TabItem {
  title: string;
  content: string;
}

defineProps<{
  tabs: TabItem[]; // Format: [{ title: '...', content: '...' }]
}>();

const activeTabIndex = ref(0);
</script>

<template>
  <div class="tabs-organism">
    <div class="tab-headers">
      <button
        v-for="(tab, index) in tabs"
        :key="index"
        :class="{ active: index === activeTabIndex }"
        @click="activeTabIndex = index"
        class="tab-header"
      >
        {{ tab.title }}
      </button>
    </div>
    <div class="tab-content">
      <div v-html="tabs[activeTabIndex].content"></div>
    </div>
  </div>
</template>

<style scoped>
.tabs-organism { margin-top: 40px; border-top: 1px solid #eee; }
.tab-headers { display: flex; border-bottom: 2px solid #eee; }
.tab-header {
  padding: 15px 20px;
  cursor: pointer;
  background: none;
  border: none;
  font-size: 1rem;
  font-weight: 600;
  color: #777;
  border-bottom: 3px solid transparent;
}
.tab-header.active { color: #c00a00; border-bottom-color: #c00a00; }
.tab-content { padding: 20px; font-size: 0.9rem; color: #555; line-height: 1.6; }
</style>