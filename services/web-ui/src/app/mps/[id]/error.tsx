'use client';
            
import { useEffect } from 'react';
import Link from 'next/link';
import { ExclamationTriangleIcon, ArrowLeftIcon } from '@heroicons/react/24/outline';
            
interface MPProfileErrorProps {
  error: Error & { digest?: string };
  reset: () => void;
}
            
export default function MPProfileError({ error, reset }: MPProfileErrorProps) {
  useEffect(() => {
    console.error('MP profile error:', error);
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
          Unable to Load MP Profile
        </h1>
        <p className="text-gray-600 mb-8">
          We encountered an error while trying to load this Member of Parliament's profile. 
          This could be due to a temporary issue or the MP ID may not exist.
        </p>
            
        {/* Action Buttons */}
        <div className="flex flex-col sm:flex-row gap-4 justify-center">
          <button
            onClick={reset}
            className="inline-flex items-center px-4 py-2 border border-transparent text-sm font-medium rounded-md shadow-sm text-white bg-op-blue hover:bg-op-blue-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-op-blue"
          >
            Try Again
          </button>
          <Link
            href="/mps"
            className="inline-flex items-center px-4 py-2 border border-gray-300 text-sm font-medium rounded-md shadow-sm text-gray-700 bg-white hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-op-blue"
          >
            <ArrowLeftIcon className="-ml-1 mr-2 h-4 w-4" />
            Back to MPs List
          </Link>
        </div>
            
        {/* Technical Details (Development Only) */}
        {process.env.NODE_ENV === 'development' && (
          <details className="mt-8 text-left">
            <summary className="cursor-pointer text-sm text-gray-500 hover:text-gray-700">
              Technical Details
            </summary>
            <div className="mt-2 p-4 bg-gray-50 rounded-md text-xs font-mono text-gray-600 overflow-auto">
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
