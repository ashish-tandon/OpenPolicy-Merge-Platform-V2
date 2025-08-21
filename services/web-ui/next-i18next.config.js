module.exports = {
  i18n: {
    defaultLocale: 'en',
    locales: ['en', 'fr'],
  },
  fallbackLng: 'en',
  supportedLngs: ['en', 'fr'],
  ns: ['common', 'home', 'bills', 'mps', 'debates', 'committees', 'search', 'labs'],
  defaultNS: 'common',
  interpolation: {
    escapeValue: false,
  },
  react: {
    useSuspense: false,
  },
}