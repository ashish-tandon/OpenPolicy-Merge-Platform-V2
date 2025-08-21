'use client';

import { ReactNode } from 'react';

interface EmptyStateProps {
  icon?: ReactNode;
  title: string;
  description?: string;
  action?: ReactNode;
  className?: string;
}

export default function EmptyState({
  icon,
  title,
  description,
  action,
  className = ''
}: EmptyStateProps) {
  return (
    <div className={`text-center py-12 animate-fade-in ${className}`}>
      {/* Icon */}
      {icon && (
        <div className="mx-auto mb-6 w-20 h-20 bg-muted rounded-full flex items-center justify-center">
          <div className="w-10 h-10 text-muted-foreground">
            {icon}
          </div>
        </div>
      )}
      
      {/* Title */}
      <h3 className="text-xl font-semibold mb-2">{title}</h3>
      
      {/* Description */}
      {description && (
        <p className="text-muted-foreground max-w-md mx-auto mb-6">
          {description}
        </p>
      )}
      
      {/* Action */}
      {action && (
        <div className="mt-6">
          {action}
        </div>
      )}
    </div>
  );
}

// Common empty states
export function NoResultsEmptyState({ searchTerm }: { searchTerm?: string }) {
  return (
    <EmptyState
      icon={
        <svg fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" />
        </svg>
      }
      title="No results found"
      description={searchTerm ? `We couldn't find anything matching "${searchTerm}"` : "Try adjusting your search or filters"}
    />
  );
}

export function ErrorEmptyState({ onRetry }: { onRetry?: () => void }) {
  return (
    <EmptyState
      icon={
        <svg fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 8v4m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
        </svg>
      }
      title="Something went wrong"
      description="We encountered an error while loading this content"
      action={
        onRetry && (
          <button onClick={onRetry} className="btn-primary">
            Try again
          </button>
        )
      }
    />
  );
}