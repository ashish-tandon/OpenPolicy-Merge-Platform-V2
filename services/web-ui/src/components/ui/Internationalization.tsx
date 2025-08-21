'use client';

import { ReactNode, createContext, useContext, useState, useEffect } from 'react';
import { 
  GlobeAltIcon, 
  LanguageIcon,
  TranslateIcon,
  CheckIcon
} from '@heroicons/react/24/outline';

// Utility function for combining class names
const cn = (...classes: (string | undefined | null | false)[]) => {
  return classes.filter(Boolean).join(' ');
};

// Language Types
export interface Language {
  code: string;
  name: string;
  nativeName: string;
  flag?: string;
  direction?: 'ltr' | 'rtl';
}

export interface Locale {
  code: string;
  messages: Record<string, string>;
  dateFormat: string;
  timeFormat: string;
  currency: string;
  numberFormat: Intl.NumberFormatOptions;
}

// Internationalization Context
interface I18nContextType {
  currentLanguage: Language;
  currentLocale: Locale;
  languages: Language[];
  locales: Locale[];
  setLanguage: (languageCode: string) => void;
  setLocale: (localeCode: string) => void;
  t: (key: string, params?: Record<string, any>) => string;
  formatDate: (date: Date, format?: string) => string;
  formatTime: (date: Date, format?: string) => string;
  formatCurrency: (amount: number, currency?: string) => string;
  formatNumber: (number: number, options?: Intl.NumberFormatOptions) => string;
  isRTL: boolean;
}

const I18nContext = createContext<I18nContextType | undefined>(undefined);

// Default Languages
export const defaultLanguages: Language[] = [
  { code: 'en', name: 'English', nativeName: 'English', flag: '🇺🇸', direction: 'ltr' },
  { code: 'fr', name: 'French', nativeName: 'Français', flag: '🇫🇷', direction: 'ltr' },
  { code: 'es', name: 'Spanish', nativeName: 'Español', flag: '🇪🇸', direction: 'ltr' },
  { code: 'de', name: 'German', nativeName: 'Deutsch', flag: '🇩🇪', direction: 'ltr' },
  { code: 'it', name: 'Italian', nativeName: 'Italiano', flag: '🇮🇹', direction: 'ltr' },
  { code: 'pt', name: 'Portuguese', nativeName: 'Português', flag: '🇵🇹', direction: 'ltr' },
  { code: 'ru', name: 'Russian', nativeName: 'Русский', flag: '🇷🇺', direction: 'ltr' },
  { code: 'zh', name: 'Chinese', nativeName: '中文', flag: '🇨🇳', direction: 'ltr' },
  { code: 'ja', name: 'Japanese', nativeName: '日本語', flag: '🇯🇵', direction: 'ltr' },
  { code: 'ko', name: 'Korean', nativeName: '한국어', flag: '🇰🇷', direction: 'ltr' },
  { code: 'ar', name: 'Arabic', nativeName: 'العربية', flag: '🇸🇦', direction: 'rtl' },
  { code: 'he', name: 'Hebrew', nativeName: 'עברית', flag: '🇮🇱', direction: 'rtl' },
  { code: 'hi', name: 'Hindi', nativeName: 'हिन्दी', flag: '🇮🇳', direction: 'ltr' },
  { code: 'tr', name: 'Turkish', nativeName: 'Türkçe', flag: '🇹🇷', direction: 'ltr' },
  { code: 'nl', name: 'Dutch', nativeName: 'Nederlands', flag: '🇳🇱', direction: 'ltr' }
];

// Default Locales
export const defaultLocales: Locale[] = [
  {
    code: 'en',
    messages: {
      'common.welcome': 'Welcome',
      'common.hello': 'Hello',
      'common.goodbye': 'Goodbye',
      'common.yes': 'Yes',
      'common.no': 'No',
      'common.cancel': 'Cancel',
      'common.save': 'Save',
      'common.delete': 'Delete',
      'common.edit': 'Edit',
      'common.view': 'View',
      'common.search': 'Search',
      'common.loading': 'Loading...',
      'common.error': 'Error',
      'common.success': 'Success',
      'common.info': 'Information'
    },
    dateFormat: 'MM/dd/yyyy',
    timeFormat: 'HH:mm',
    currency: 'USD',
    numberFormat: { style: 'decimal', minimumFractionDigits: 0, maximumFractionDigits: 2 }
  },
  {
    code: 'fr',
    messages: {
      'common.welcome': 'Bienvenue',
      'common.hello': 'Bonjour',
      'common.goodbye': 'Au revoir',
      'common.yes': 'Oui',
      'common.no': 'Non',
      'common.cancel': 'Annuler',
      'common.save': 'Enregistrer',
      'common.delete': 'Supprimer',
      'common.edit': 'Modifier',
      'common.view': 'Voir',
      'common.search': 'Rechercher',
      'common.loading': 'Chargement...',
      'common.error': 'Erreur',
      'common.success': 'Succès',
      'common.info': 'Information'
    },
    dateFormat: 'dd/MM/yyyy',
    timeFormat: 'HH:mm',
    currency: 'EUR',
    numberFormat: { style: 'decimal', minimumFractionDigits: 0, maximumFractionDigits: 2 }
  },
  {
    code: 'es',
    messages: {
      'common.welcome': 'Bienvenido',
      'common.hello': 'Hola',
      'common.goodbye': 'Adiós',
      'common.yes': 'Sí',
      'common.no': 'No',
      'common.cancel': 'Cancelar',
      'common.save': 'Guardar',
      'common.delete': 'Eliminar',
      'common.edit': 'Editar',
      'common.view': 'Ver',
      'common.search': 'Buscar',
      'common.loading': 'Cargando...',
      'common.error': 'Error',
      'common.success': 'Éxito',
      'common.info': 'Información'
    },
    dateFormat: 'dd/MM/yyyy',
    timeFormat: 'HH:mm',
    currency: 'EUR',
    numberFormat: { style: 'decimal', minimumFractionDigits: 0, maximumFractionDigits: 2 }
  }
];

// Internationalization Provider Component
interface I18nProviderProps {
  children: ReactNode;
  defaultLanguage?: string;
  languages?: Language[];
  locales?: Locale[];
  storageKey?: string;
  className?: string;
}

export function I18nProvider({
  children,
  defaultLanguage = 'en',
  languages = defaultLanguages,
  locales = defaultLocales,
  storageKey = 'op-language',
  className = ""
}: I18nProviderProps) {
  const [currentLanguage, setCurrentLanguageState] = useState<Language>(
    languages.find(lang => lang.code === defaultLanguage) || languages[0]
  );
  const [currentLocale, setCurrentLocaleState] = useState<Locale>(
    locales.find(locale => locale.code === defaultLanguage) || locales[0]
  );

  useEffect(() => {
    // Load language from localStorage
    const savedLanguage = localStorage.getItem(storageKey);
    if (savedLanguage) {
      const language = languages.find(lang => lang.code === savedLanguage);
      const locale = locales.find(loc => loc.code === savedLanguage);
      
      if (language && locale) {
        setCurrentLanguageState(language);
        setCurrentLocaleState(locale);
      }
    }
  }, [storageKey, languages, locales]);

  useEffect(() => {
    // Apply language to document
    const root = document.documentElement;
    
    // Remove existing language classes
    root.classList.remove('ltr', 'rtl');
    
    // Add direction class
    root.classList.add(currentLanguage.direction || 'ltr');
    
    // Set lang attribute
    root.lang = currentLanguage.code;
    
    // Save to localStorage
    localStorage.setItem(storageKey, currentLanguage.code);
  }, [currentLanguage, storageKey]);

  const setLanguage = (languageCode: string) => {
    const language = languages.find(lang => lang.code === languageCode);
    const locale = locales.find(loc => loc.code === languageCode);
    
    if (language && locale) {
      setCurrentLanguageState(language);
      setCurrentLocaleState(locale);
    }
  };

  const setLocale = (localeCode: string) => {
    const locale = locales.find(loc => loc.code === localeCode);
    if (locale) {
      setCurrentLocaleState(locale);
    }
  };

  const t = (key: string, params?: Record<string, any>): string => {
    let message = currentLocale.messages[key] || key;
    
    if (params) {
      Object.entries(params).forEach(([param, value]) => {
        message = message.replace(new RegExp(`{${param}}`, 'g'), String(value));
      });
    }
    
    return message;
  };

  const formatDate = (date: Date, format?: string): string => {
    const options: Intl.DateTimeFormatOptions = {
      year: 'numeric',
      month: 'long',
      day: 'numeric'
    };
    
    return new Intl.DateTimeFormat(currentLanguage.code, options).format(date);
  };

  const formatTime = (date: Date, format?: string): string => {
    const options: Intl.DateTimeFormatOptions = {
      hour: '2-digit',
      minute: '2-digit'
    };
    
    return new Intl.DateTimeFormat(currentLanguage.code, options).format(date);
  };

  const formatCurrency = (amount: number, currency?: string): string => {
    return new Intl.NumberFormat(currentLanguage.code, {
      style: 'currency',
      currency: currency || currentLocale.currency
    }).format(amount);
  };

  const formatNumber = (number: number, options?: Intl.NumberFormatOptions): string => {
    const formatOptions = { ...currentLocale.numberFormat, ...options };
    return new Intl.NumberFormat(currentLanguage.code, formatOptions).format(number);
  };

  const value: I18nContextType = {
    currentLanguage,
    currentLocale,
    languages,
    locales,
    setLanguage,
    setLocale,
    t,
    formatDate,
    formatTime,
    formatCurrency,
    formatNumber,
    isRTL: currentLanguage.direction === 'rtl'
  };

  return (
    <I18nContext.Provider value={value}>
      <div className={cn("i18n-provider", className)}>
        {children}
      </div>
    </I18nContext.Provider>
  );
}

// Internationalization Hook
export function useI18n(): I18nContextType {
  const context = useContext(I18nContext);
  if (context === undefined) {
    throw new Error('useI18n must be used within an I18nProvider');
  }
  return context;
}

// Language Selector Component
interface LanguageSelectorProps {
  className?: string;
  showFlags?: boolean;
  showNativeNames?: boolean;
  size?: 'sm' | 'md' | 'lg';
}

export function LanguageSelector({
  className = "",
  showFlags = true,
  showNativeNames = false,
  size = 'md'
}: LanguageSelectorProps) {
  const { currentLanguage, languages, setLanguage } = useI18n();
  const [isOpen, setIsOpen] = useState(false);

  const sizeClasses = {
    sm: 'px-2 py-1 text-sm',
    md: 'px-3 py-2 text-sm',
    lg: 'px-4 py-3 text-base'
  };

  const handleLanguageChange = (languageCode: string) => {
    setLanguage(languageCode);
    setIsOpen(false);
  };

  return (
    <div className={cn("relative", className)}>
      <button
        onClick={() => setIsOpen(!isOpen)}
        aria-expanded={isOpen}
        aria-label="Select language"
        className={cn(
          "flex items-center space-x-2 bg-white dark:bg-gray-800 border border-gray-300 dark:border-gray-600 rounded-md",
          "hover:bg-gray-50 dark:hover:bg-gray-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-op-blue",
          "transition-colors",
          sizeClasses[size]
        )}
      >
        <GlobeAltIcon className="h-4 w-4 text-gray-500" />
        {showFlags && currentLanguage.flag && (
          <span className="text-lg">{currentLanguage.flag}</span>
        )}
        <span className="font-medium text-gray-700 dark:text-gray-200">
          {showNativeNames ? currentLanguage.nativeName : currentLanguage.name}
        </span>
        <LanguageIcon className="h-4 w-4 text-gray-400" />
      </button>

      {isOpen && (
        <div className="absolute right-0 mt-2 w-56 bg-white dark:bg-gray-800 rounded-md shadow-lg border border-gray-200 dark:border-gray-600 z-50">
          <div className="py-1">
            {languages.map((language) => (
              <button
                key={language.code}
                onClick={() => handleLanguageChange(language.code)}
                className={cn(
                  "w-full flex items-center space-x-3 px-4 py-2 text-sm text-left",
                  "hover:bg-gray-100 dark:hover:bg-gray-700 transition-colors",
                  currentLanguage.code === language.code && "bg-op-blue-50 dark:bg-op-blue-900/20"
                )}
              >
                {showFlags && language.flag && (
                  <span className="text-lg">{language.flag}</span>
                )}
                <div className="flex-1">
                  <div className="font-medium text-gray-900 dark:text-gray-100">
                    {language.name}
                  </div>
                  {showNativeNames && (
                    <div className="text-xs text-gray-500 dark:text-gray-400">
                      {language.nativeName}
                    </div>
                  )}
                </div>
                {currentLanguage.code === language.code && (
                  <CheckIcon className="h-4 w-4 text-op-blue" />
                )}
              </button>
            ))}
          </div>
        </div>
      )}
    </div>
  );
}

// Translation Component
interface TranslationProps {
  messageKey: string;
  params?: Record<string, any>;
  fallback?: string;
  className?: string;
}

export function Translation({
  messageKey,
  params,
  fallback,
  className = ""
}: TranslationProps) {
  const { t } = useI18n();
  const message = t(messageKey, params);

  if (message === messageKey && fallback) {
    return <span className={className}>{fallback}</span>;
  }

  return <span className={className}>{message}</span>;
}

// Date Formatter Component
interface DateFormatterProps {
  date: Date | string;
  format?: string;
  className?: string;
}

export function DateFormatter({
  date,
  format,
  className = ""
}: DateFormatterProps) {
  const { formatDate } = useI18n();
  const dateObj = typeof date === 'string' ? new Date(date) : date;

  return (
    <time dateTime={dateObj.toISOString()} className={className}>
      {formatDate(dateObj, format)}
    </time>
  );
}

// Time Formatter Component
interface TimeFormatterProps {
  date: Date | string;
  format?: string;
  className?: string;
}

export function TimeFormatter({
  date,
  format,
  className = ""
}: TimeFormatterProps) {
  const { formatTime } = useI18n();
  const dateObj = typeof date === 'string' ? new Date(date) : date;

  return (
    <time dateTime={dateObj.toISOString()} className={className}>
      {formatTime(dateObj, format)}
    </time>
  );
}

// Currency Formatter Component
interface CurrencyFormatterProps {
  amount: number;
  currency?: string;
  className?: string;
}

export function CurrencyFormatter({
  amount,
  currency,
  className = ""
}: CurrencyFormatterProps) {
  const { formatCurrency } = useI18n();

  return (
    <span className={className}>
      {formatCurrency(amount, currency)}
    </span>
  );
}

// Number Formatter Component
interface NumberFormatterProps {
  number: number;
  options?: Intl.NumberFormatOptions;
  className?: string;
}

export function NumberFormatter({
  number,
  options,
  className = ""
}: NumberFormatterProps) {
  const { formatNumber } = useI18n();

  return (
    <span className={className}>
      {formatNumber(number, options)}
    </span>
  );
}

// RTL Aware Component
interface RTLAwareProps {
  children: ReactNode;
  ltrClassName?: string;
  rtlClassName?: string;
  className?: string;
}

export function RTLAware({
  children,
  ltrClassName = "",
  rtlClassName = "",
  className = ""
}: RTLAwareProps) {
  const { isRTL } = useI18n();

  return (
    <div className={cn(
      isRTL ? rtlClassName : ltrClassName,
      className
    )}>
      {children}
    </div>
  );
}

// Language Switcher Component
interface LanguageSwitcherProps {
  className?: string;
  showCurrentLanguage?: boolean;
}

export function LanguageSwitcher({
  className = "",
  showCurrentLanguage = true
}: LanguageSwitcherProps) {
  const { currentLanguage, languages, setLanguage } = useI18n();

  return (
    <div className={cn("flex items-center space-x-2", className)}>
      {showCurrentLanguage && (
        <span className="text-sm text-gray-600 dark:text-gray-400">
          {currentLanguage.name}
        </span>
      )}
      <LanguageSelector />
    </div>
  );
}

// Internationalization Settings Panel Component
interface I18nSettingsPanelProps {
  isOpen: boolean;
  onClose: () => void;
  className?: string;
}

export function I18nSettingsPanel({
  isOpen,
  onClose,
  className = ""
}: I18nSettingsPanelProps) {
  if (!isOpen) return null;

  return (
    <div className={cn("fixed inset-0 z-50 overflow-y-auto", className)}>
      <div className="flex min-h-full items-end justify-center p-4 text-center sm:items-center sm:p-0">
        <div className="fixed inset-0 bg-gray-500 bg-opacity-75 transition-opacity" onClick={onClose} />
        
        <div className="relative transform overflow-hidden rounded-lg bg-white dark:bg-gray-800 px-4 pb-4 pt-5 text-left shadow-xl transition-all sm:my-8 sm:w-full sm:max-w-lg sm:p-6">
          <div className="absolute right-0 top-0 pr-4 pt-4">
            <button
              onClick={onClose}
              className="rounded-md bg-white dark:bg-gray-800 text-gray-400 hover:text-gray-500 focus:outline-none focus:ring-2 focus:ring-op-blue focus:ring-offset-2"
            >
              <span className="sr-only">Close</span>
              <svg className="h-6 w-6" fill="none" viewBox="0 0 24 24" strokeWidth="1.5" stroke="currentColor">
                <path strokeLinecap="round" strokeLinejoin="round" d="M6 18L18 6M6 6l12 12" />
              </svg>
            </button>
          </div>
          
          <div className="sm:flex sm:items-start">
            <div className="mt-3 text-center sm:ml-4 sm:mt-0 sm:text-left w-full">
              <h3 className="text-lg font-medium leading-6 text-gray-900 dark:text-gray-100 mb-4">
                Language & Regional Settings
              </h3>
              
              <div className="space-y-6">
                <div>
                  <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
                    Language
                  </label>
                  <LanguageSelector showFlags showNativeNames />
                </div>
                
                <div>
                  <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
                    Date Format
                  </label>
                  <div className="text-sm text-gray-600 dark:text-gray-400">
                    Current: {new Date().toLocaleDateString()}
                  </div>
                </div>
                
                <div>
                  <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
                    Time Format
                  </label>
                  <div className="text-sm text-gray-600 dark:text-gray-400">
                    Current: {new Date().toLocaleTimeString()}
                  </div>
                </div>
                
                <div>
                  <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
                    Currency
                  </label>
                  <div className="text-sm text-gray-600 dark:text-gray-400">
                    Current: $1,234.56
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
