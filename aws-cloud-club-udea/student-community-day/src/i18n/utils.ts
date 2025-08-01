import en from './en.json';
import es from './es.json';

const translations = {
  en,
  es
};

export type Language = keyof typeof translations;

export function getTranslations(lang: Language) {
  return translations[lang] || translations.en;
}

export function t(lang: Language, key: string): string {
  const keys = key.split('.');
  let value: any = getTranslations(lang);
  
  for (const k of keys) {
    value = value?.[k];
  }
  
  return value || key;
}

export function getCurrentLanguage(url: URL): Language {
  const pathname = url.pathname;
  if (pathname.startsWith('/es')) return 'es';
  return 'en';
}

export function getLocalizedPath(path: string, lang: Language): string {
  if (lang === 'en') return path;
  return `/es${path}`;
}

export function getAlternateLanguage(currentLang: Language): Language {
  return currentLang === 'en' ? 'es' : 'en';
}

export function getLanguageName(lang: Language): string {
  return lang === 'en' ? 'English' : 'Español';
}
