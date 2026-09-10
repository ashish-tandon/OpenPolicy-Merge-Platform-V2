'use client';

import { useLanguage } from '@/contexts/LanguageContext';

export default function LanguageNotification() {
  const { language } = useLanguage();

  if (language !== 'fr') {
    return null;
  }

  return (
    <div className="bg-yellow-50 border-b border-yellow-200">
      <div className="content-container py-3">
        <p className="text-sm text-yellow-800">
          Ceci est un site <strong>expérimental</strong> et <strong>incomplet</strong>. 
          Voir{' '}
          <a 
            href="https://openparliament.ca/" 
            className="underline hover:text-yellow-900"
          >
            openparliament.ca
          </a>, en anglais, pour un site plus fiable.
        </p>
      </div>
    </div>
  );
}