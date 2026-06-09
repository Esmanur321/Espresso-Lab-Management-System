import { defineNuxtPlugin } from '#app';
import { useI18n, initLocaleFromStorage } from '~/composables/useI18n';

export default defineNuxtPlugin(() => {
  initLocaleFromStorage();

  const { locale, setLocale, t } = useI18n();

  return {
    provide: {
      t,
      locale,
      setLocale
    }
  };
});
