'use client';

import React, { createContext, useContext, useState, useEffect } from 'react';

type Language = 'en' | 'fr';

interface LanguageContextType {
  language: Language;
  setLanguage: (lang: Language) => void;
  t: (key: string) => string;
}

const translations: Record<Language, Record<string, string>> = {
  en: {
    // Navigation
    'nav.mps': 'MPs',
    'nav.bills': 'Bills',
    'nav.debates': 'Debates',
    'nav.committees': 'Committees',
    'nav.about': 'About',
    'nav.labs': 'Labs',
    'nav.formerMps': 'Former MPs',
    'nav.votingRecords': 'Voting Records',
    
    // Common
    'common.search': 'Search',
    'common.home': 'Home',
    'common.loading': 'Loading...',
    'common.error': 'Error',
    
    // Homepage
    'home.title': 'Keep tabs on Parliament.',
    'home.subtitle': 'Track Canadian MPs, bills, debates, and committees',
    'home.whatWereDoing': "What we're doing",
    'home.whatsNew': "What's new around here",
    
    // Language
    'lang.french': 'Français',
    'lang.english': 'English',
    'lang.switchTo': 'Voir en français',
  },
  fr: {
    // Navigation
    'nav.mps': 'Députés',
    'nav.bills': 'Projets de loi',
    'nav.debates': 'Débats',
    'nav.committees': 'Comités',
    'nav.about': 'À propos',
    'nav.labs': 'Labs',
    'nav.formerMps': 'Anciens députés',
    'nav.votingRecords': 'Votes',
    
    // Common
    'common.search': 'Rechercher',
    'common.home': 'Accueil',
    'common.loading': 'Chargement...',
    'common.error': 'Erreur',
    
    // Homepage
    'home.title': 'Surveillez le Parlement.',
    'home.subtitle': 'Suivez les députés, projets de loi, débats et comités canadiens',
    'home.whatWereDoing': 'Ce que nous faisons',
    'home.whatsNew': 'Quoi de neuf',
    
    // Language
    'lang.french': 'Français',
    'lang.english': 'English',
    'lang.switchTo': 'View in English',
  },
};

const LanguageContext = createContext<LanguageContextType | undefined>(undefined);

export function LanguageProvider({ children }: { children: React.ReactNode }) {
  const [language, setLanguage] = useState<Language>('en');

  useEffect(() => {
    // Check localStorage for saved language preference
    const savedLang = localStorage.getItem('language') as Language;
    if (savedLang && (savedLang === 'en' || savedLang === 'fr')) {
      setLanguage(savedLang);
    }
  }, []);

  const handleSetLanguage = (lang: Language) => {
    setLanguage(lang);
    localStorage.setItem('language', lang);
    
    // Update document language attribute
    document.documentElement.lang = lang;
    
    // In production, this would handle domain switching between
    // openparliament.ca and parlementouvert.ca
  };

  const t = (key: string): string => {
    return translations[language][key] || translations['en'][key] || key;
  };

  return (
    <LanguageContext.Provider value={{ language, setLanguage: handleSetLanguage, t }}>
      {children}
    </LanguageContext.Provider>
  );
}

export function useLanguage() {
  const context = useContext(LanguageContext);
  if (context === undefined) {
    throw new Error('useLanguage must be used within a LanguageProvider');
  }
  return context;
}