'use client';

import Link from 'next/link';
import { useState } from 'react';
import { useRouter } from 'next/navigation';
import SearchBar from './SearchBar';
import { useLanguage } from '@/contexts/LanguageContext';

export default function Navbar() {
  const [mobileMenuOpen, setMobileMenuOpen] = useState(false);
  const { language, setLanguage, t } = useLanguage();
  const router = useRouter();

  const handleLanguageToggle = () => {
    const newLang = language === 'en' ? 'fr' : 'en';
    setLanguage(newLang);
  };

  const navItems = [
    { href: '/mps', label: t('nav.mps') },
    { href: '/bills', label: t('nav.bills') },
    { href: '/debates', label: t('nav.debates') },
    { href: '/committees', label: t('nav.committees') },
    { href: '/about', label: t('nav.about') },
    { href: '/labs', label: t('nav.labs') },
  ];

  return (
    <nav className="bg-white shadow-md sticky top-0 z-50">
      <div className="content-container">
        <div className="flex justify-between items-center py-4">
          {/* Logo */}
          <Link href="/" className="flex items-center space-x-2">
            <span className="text-xl font-bold text-op-blue">
              {language === 'en' ? 'openparliament.ca' : 'parlementouvert.ca'}
            </span>
          </Link>

          {/* Desktop Navigation */}
          <div className="hidden md:flex items-center space-x-6">
            {navItems.map((item) => (
              <Link
                key={item.href}
                href={item.href}
                className="text-gray-700 hover:text-op-blue transition-colors"
              >
                {item.label}
              </Link>
            ))}
          </div>

          {/* Search Bar */}
          <div className="hidden md:block flex-1 max-w-md mx-6">
            <SearchBar />
          </div>

          {/* Language Toggle */}
          <div className="hidden md:flex items-center space-x-4">
            <button 
              onClick={handleLanguageToggle}
              className="text-sm text-gray-600 hover:text-op-blue transition-colors"
              title={language === 'en' ? 'Voir en français' : 'View in English'}
            >
              {language === 'en' ? 'Français' : 'English'}
            </button>
          </div>

          {/* Mobile Menu Button */}
          <button
            className="md:hidden"
            onClick={() => setMobileMenuOpen(!mobileMenuOpen)}
          >
            <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              {mobileMenuOpen ? (
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
              ) : (
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 6h16M4 12h16M4 18h16" />
              )}
            </svg>
          </button>
        </div>

        {/* Mobile Menu */}
        {mobileMenuOpen && (
          <div className="md:hidden py-4 border-t">
            <div className="mb-4">
              <SearchBar />
            </div>
            {navItems.map((item) => (
              <Link
                key={item.href}
                href={item.href}
                className="block py-2 text-gray-700 hover:text-op-blue"
                onClick={() => setMobileMenuOpen(false)}
              >
                {item.label}
              </Link>
            ))}
            <button 
              onClick={handleLanguageToggle}
              className="block py-2 text-gray-600 hover:text-op-blue"
            >
              {language === 'en' ? 'Français' : 'English'}
            </button>
          </div>
        )}
      </div>
    </nav>
  );
}
