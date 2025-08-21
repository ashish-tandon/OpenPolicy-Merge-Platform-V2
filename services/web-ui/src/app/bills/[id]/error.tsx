'use client';

import { useEffect } from 'react';
import Link from 'next/link';
import { ExclamationTriangleIcon, ArrowLeftIcon } from '@heroicons/react/24/outline';

interface BillDetailErrorProps {
  error: Error & { digest?: string };
  reset: () => void;
}

export default function BillDetailError({ error, reset }: BillDetailErrorProps) {
  useEffect(() => {
    console.error('Bill detail error:', error);
  }, [error]);

  return (
    <div className="content-container py-8">
      <div className="max-w-2xl mx-auto text-center">
        {/* Error Icon */}
        <div className="mx-auto flex items-center justify-center h-16 w-16 rounded-full bg-red-100 mb-6">
          <ExclamationTriangleIcon className="h-8 w-8 text-red-600" />
        </div>

        {/* Error Message */}
        <h1 className="text-2xl font-bold text-gray-900 mb-4">
          Unable to Load Bill Details
        </h1>
        
        <p className="text-gray-600 mb-8">
          We encountered an error while trying to load the bill details. This might be due to:
        </p>

        {/* Error Details */}
        <div className="text-left bg-gray-50 rounded-lg p-6 mb-8">
          <ul className="space-y-2 text-sm text-gray-600">
            <li className="flex items-start">
              <span className="text-red-500 mr-2">•</span>
              The bill ID might be invalid or no longer available
            </li>
            <li className="flex items-start">
              <span className="text-red-500 mr-2">•</span>
              Temporary server issues or network problems
            </li>
            <li className="flex items-start">
              <span className="text-red-500 mr-2">•</span>
              The bill might have been removed or archived
            </li>
          </ul>
        </div>

        {/* Action Buttons */}
        <div className="flex flex-col sm:flex-row gap-4 justify-center">
          <button
            onClick={reset}
            className="inline-flex items-center px-4 py-2 border border-transparent text-sm font-medium rounded-md shadow-sm text-white bg-op-blue hover:bg-op-blue-700 transition-colors"
          >
            Try Again
          </button>
          
          <Link
            href="/bills"
            className="inline-flex items-center px-4 py-2 border border-gray-300 text-sm font-medium rounded-md text-gray-700 bg-white hover:bg-gray-50 transition-colors"
          >
            <ArrowLeftIcon className="h-4 w-4 mr-2" />
            Back to Bills
          </Link>
        </div>

        {/* Technical Details (Development Only) */}
        {process.env.NODE_ENV === 'development' && (
          <details className="mt-8 text-left">
            <summary className="cursor-pointer text-sm text-gray-500 hover:text-gray-700">
              Technical Details
            </summary>
            <div className="mt-2 p-4 bg-gray-100 rounded text-xs font-mono text-gray-700 overflow-auto">
              <p><strong>Error:</strong> {error.message}</p>
              {error.digest && <p><strong>Digest:</strong> {error.digest}</p>}
              <p><strong>Stack:</strong></p>
              <pre className="whitespace-pre-wrap">{error.stack}</pre>
            </div>
          </details>
        )}
      </div>
    </div>
  );
}
