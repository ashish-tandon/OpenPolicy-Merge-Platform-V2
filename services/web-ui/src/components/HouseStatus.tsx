'use client';

import { useEffect, useState } from 'react';

export default function HouseStatus() {
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
      <div className="bg-yellow-50 border border-yellow-200 rounded-lg p-4 mb-6">
        <div className="flex items-center">
          <svg className="w-5 h-5 text-yellow-600 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z" />
          </svg>
          <span className="text-yellow-800">{status.message}</span>
        </div>
      </div>
    );
  }

  return (
    <div className="bg-green-50 border border-green-200 rounded-lg p-4 mb-6">
      <div className="flex items-center">
        <div className="w-3 h-3 bg-green-500 rounded-full mr-2 animate-pulse"></div>
        <span className="text-green-800">The House is currently sitting</span>
      </div>
    </div>
  );
}
