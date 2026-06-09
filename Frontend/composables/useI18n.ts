import { messages } from '~/utils/locales';

const LOCALE_STATE_KEY = 'app-locale';

export function useI18n() {
  const locale = useState<string>(LOCALE_STATE_KEY, () => 'tr');

  const setLocale = (lang: string) => {
    const normalized = lang.toLowerCase();
    if (!messages[normalized]) return;
    locale.value = normalized;
    if (import.meta.client) {
      localStorage.setItem('lang', normalized);
    }
  };

  const t = (key: string): string => {
    const dict = messages[locale.value] || messages.tr;
    return dict[key] || key;
  };

  return { locale, setLocale, t };
}

/** Call once on client to restore language from localStorage */
export function initLocaleFromStorage() {
  if (!import.meta.client) return;
  const locale = useState<string>(LOCALE_STATE_KEY, () => 'tr');
  const saved = localStorage.getItem('lang');
  if (saved && messages[saved]) {
    locale.value = saved;
  }
}
