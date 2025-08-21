'use client';

import { useEffect, useState } from 'react';
import { useTranslation } from '@/hooks/useTranslation';
import { ClockIcon } from '@heroicons/react/24/outline';

export default function HouseStatus() {
  const { t } = useTranslation();
  const [status, setStatus] = useState({
    sitting: false,
    message: 'The House is on summer break, scheduled to return Sept. 15',
    nextSitting: '2025-09-15',
  });

  // In production, this would fetch real-time status from the API
  useEffect(() => {
    // Placeholder for real-time status updates
  }, []);

  if (!status.sitting) {
    return (
      <div className="bg-amber-500/10 dark:bg-amber-500/20 border border-amber-500/30 rounded-lg p-4 mb-6 animate-fade-in">
        <div className="flex items-center">
          <ClockIcon className="w-5 h-5 text-amber-600 dark:text-amber-400 mr-2" />
          <span className="text-amber-900 dark:text-amber-100">{status.message}</span>
        </div>
      </div>
    );
  }

  return (
    <div className="bg-green-500/10 dark:bg-green-500/20 border border-green-500/30 rounded-lg p-4 mb-6 animate-fade-in">
      <div className="flex items-center">
        <div className="w-3 h-3 bg-green-500 rounded-full mr-2 animate-pulse-slow"></div>
        <span className="text-green-900 dark:text-green-100">{t('home.houseStatus.sitting')}</span>
      </div>
    </div>
  );
}
