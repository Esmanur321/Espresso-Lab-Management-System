import { useState } from '#app';
import { watchEffect } from 'vue';

export const useTheme = () => {
  const theme = useState<'light' | 'dark'>('theme', () => 'light');

  const toggleTheme = () => {
    theme.value = theme.value === 'light' ? 'dark' : 'light';
  };

  const initTheme = () => {
    if (typeof window !== 'undefined') {
      const savedTheme = localStorage.getItem('theme') as 'light' | 'dark';
      if (savedTheme) {
        theme.value = savedTheme;
      }
      
      watchEffect(() => {
        localStorage.setItem('theme', theme.value);
        if (theme.value === 'dark') {
          document.documentElement.classList.add('dark-theme');
        } else {
          document.documentElement.classList.remove('dark-theme');
        }
      });
    }
  };

  return { theme, toggleTheme, initTheme };
};
