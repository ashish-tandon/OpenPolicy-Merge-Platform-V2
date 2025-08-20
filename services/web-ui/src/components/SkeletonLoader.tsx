/**
 * Skeleton loading states based on legacy .loading patterns
 * Provides accessible loading indicators
 */

interface SkeletonLoaderProps {
  type?: 'text' | 'title' | 'paragraph' | 'card' | 'table' | 'image';
  lines?: number;
  className?: string;
}

export default function SkeletonLoader({ 
  type = 'text', 
  lines = 1,
  className = '' 
}: SkeletonLoaderProps) {
  const baseClass = "animate-pulse bg-gray-200 rounded";
  
  // Based on legacy loading patterns from haiku.html
  if (type === 'text') {
    return (
      <div className={`space-y-2 ${className}`} aria-busy="true" aria-label="Loading content">
        {Array.from({ length: lines }).map((_, i) => (
          <div key={i} className={`${baseClass} h-4 w-full`} />
        ))}
      </div>
    );
  }
  
  if (type === 'title') {
    return (
      <div className={`${baseClass} h-8 w-3/4 ${className}`} aria-busy="true" aria-label="Loading title" />
    );
  }
  
  if (type === 'paragraph') {
    return (
      <div className={`space-y-2 ${className}`} aria-busy="true" aria-label="Loading paragraph">
        <div className={`${baseClass} h-4 w-full`} />
        <div className={`${baseClass} h-4 w-full`} />
        <div className={`${baseClass} h-4 w-3/4`} />
      </div>
    );
  }
  
  if (type === 'card') {
    return (
      <div className={`${baseClass} ${className}`} aria-busy="true" aria-label="Loading card">
        <div className="p-6 space-y-4">
          <div className={`${baseClass} h-6 w-1/2 bg-gray-300`} />
          <div className="space-y-2">
            <div className={`${baseClass} h-4 w-full bg-gray-300`} />
            <div className={`${baseClass} h-4 w-3/4 bg-gray-300`} />
          </div>
          <div className="flex space-x-4">
            <div className={`${baseClass} h-8 w-20 bg-gray-300`} />
            <div className={`${baseClass} h-8 w-20 bg-gray-300`} />
          </div>
        </div>
      </div>
    );
  }
  
  if (type === 'table') {
    return (
      <div className={`w-full ${className}`} aria-busy="true" aria-label="Loading table">
        <div className={`${baseClass} h-10 w-full mb-2`} />
        {Array.from({ length: 5 }).map((_, i) => (
          <div key={i} className={`${baseClass} h-12 w-full mb-1`} />
        ))}
      </div>
    );
  }
  
  if (type === 'image') {
    return (
      <div 
        className={`${baseClass} aspect-square ${className}`} 
        aria-busy="true" 
        aria-label="Loading image"
      />
    );
  }
  
  return null;
}

// Spinner component for inline loading states
export function LoadingSpinner({ 
  size = 'md',
  className = '' 
}: { 
  size?: 'sm' | 'md' | 'lg';
  className?: string;
}) {
  const sizeClasses = {
    sm: 'h-4 w-4',
    md: 'h-6 w-6',
    lg: 'h-8 w-8'
  };
  
  return (
    <div 
      className={`inline-block ${className}`}
      role="status"
      aria-label="Loading"
    >
      <svg 
        className={`animate-spin ${sizeClasses[size]} text-gray-400`}
        xmlns="http://www.w3.org/2000/svg" 
        fill="none" 
        viewBox="0 0 24 24"
      >
        <circle 
          className="opacity-25" 
          cx="12" 
          cy="12" 
          r="10" 
          stroke="currentColor" 
          strokeWidth="4"
        />
        <path 
          className="opacity-75" 
          fill="currentColor" 
          d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"
        />
      </svg>
      <span className="sr-only">Loading...</span>
    </div>
  );
}
