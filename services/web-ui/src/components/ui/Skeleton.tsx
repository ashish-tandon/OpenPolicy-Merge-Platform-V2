import { cn } from '@/lib/utils';

interface SkeletonProps {
  className?: string;
  variant?: 'default' | 'circular' | 'text' | 'title' | 'avatar';
  lines?: number;
}

export default function Skeleton({ 
  className, 
  variant = 'default',
  lines = 1 
}: SkeletonProps) {
  const baseClasses = "animate-pulse bg-gray-200 rounded";
  
  const variants = {
    default: baseClasses,
    circular: `${baseClasses} rounded-full`,
    text: `${baseClasses} h-4`,
    title: `${baseClasses} h-6`,
    avatar: `${baseClasses} rounded-full w-12 h-12`
  };

  if (variant === 'text' && lines > 1) {
    return (
      <div className="space-y-2">
        {Array.from({ length: lines }).map((_, index) => (
          <div
            key={index}
            className={cn(
              variants.text,
              index === lines - 1 ? 'w-3/4' : 'w-full',
              className
            )}
          />
        ))}
      </div>
    );
  }

  return (
    <div className={cn(variants[variant], className)} />
  );
}

// Specialized skeleton components
export function BillCardSkeleton() {
  return (
    <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-6 animate-pulse">
      <div className="flex items-start justify-between mb-4">
        <div className="flex-1">
          <Skeleton variant="title" className="w-3/4 mb-2" />
          <Skeleton variant="text" className="w-1/2 mb-3" />
          <Skeleton variant="text" lines={3} />
        </div>
        <div className="ml-4">
          <Skeleton variant="default" className="w-20 h-8" />
        </div>
      </div>
      
      <div className="flex items-center space-x-4">
        <Skeleton variant="default" className="w-16 h-6" />
        <Skeleton variant="default" className="w-24 h-6" />
        <Skeleton variant="default" className="w-20 h-6" />
      </div>
    </div>
  );
}

export function MPCardSkeleton() {
  return (
    <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-6 animate-pulse">
      <div className="flex items-center space-x-4 mb-4">
        <Skeleton variant="avatar" />
        <div className="flex-1">
          <Skeleton variant="title" className="w-1/2 mb-2" />
          <Skeleton variant="text" className="w-1/3" />
        </div>
      </div>
      
      <div className="space-y-3">
        <Skeleton variant="text" className="w-full" />
        <Skeleton variant="text" className="w-3/4" />
        <Skeleton variant="text" className="w-1/2" />
      </div>
      
      <div className="flex items-center justify-between mt-4">
        <div className="flex space-x-2">
          <Skeleton variant="default" className="w-16 h-6" />
          <Skeleton variant="default" className="w-20 h-6" />
        </div>
        <Skeleton variant="default" className="w-24 h-8" />
      </div>
    </div>
  );
}

export function DebateCardSkeleton() {
  return (
    <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-6 animate-pulse">
      <div className="mb-4">
        <Skeleton variant="title" className="w-2/3 mb-2" />
        <Skeleton variant="text" className="w-1/3 mb-3" />
        <Skeleton variant="text" lines={2} />
      </div>
      
      <div className="flex items-center justify-between">
        <div className="flex items-center space-x-4">
          <Skeleton variant="avatar" className="w-8 h-8" />
          <Skeleton variant="text" className="w-24" />
        </div>
        <Skeleton variant="default" className="w-20 h-6" />
      </div>
    </div>
  );
}

export function CommitteeCardSkeleton() {
  return (
    <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-6 animate-pulse">
      <div className="mb-4">
        <Skeleton variant="title" className="w-1/2 mb-2" />
        <Skeleton variant="text" className="w-1/3 mb-3" />
        <Skeleton variant="text" lines={2} />
      </div>
      
      <div className="space-y-2">
        <Skeleton variant="text" className="w-3/4" />
        <Skeleton variant="text" className="w-1/2" />
      </div>
      
      <div className="flex items-center justify-between mt-4">
        <Skeleton variant="default" className="w-16 h-6" />
        <Skeleton variant="default" className="w-20 h-8" />
      </div>
    </div>
  );
}

export function VoteCardSkeleton() {
  return (
    <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-6 animate-pulse">
      <div className="mb-4">
        <Skeleton variant="title" className="w-2/3 mb-2" />
        <Skeleton variant="text" className="w-1/2 mb-3" />
        <Skeleton variant="text" className="w-full" />
      </div>
      
      <div className="grid grid-cols-3 gap-4 mb-4">
        <div className="text-center">
          <Skeleton variant="default" className="w-12 h-8 mx-auto mb-1" />
          <Skeleton variant="text" className="w-16 mx-auto" />
        </div>
        <div className="text-center">
          <Skeleton variant="default" className="w-12 h-8 mx-auto mb-1" />
          <Skeleton variant="text" className="w-16 mx-auto" />
        </div>
        <div className="text-center">
          <Skeleton variant="default" className="w-12 h-8 mx-auto mb-1" />
          <Skeleton variant="text" className="w-16 mx-auto" />
        </div>
      </div>
      
      <div className="flex items-center justify-between">
        <Skeleton variant="default" className="w-24 h-6" />
        <Skeleton variant="default" className="w-20 h-8" />
      </div>
    </div>
  );
}

export function TableSkeleton({ rows = 5, columns = 4 }: { rows?: number; columns?: number }) {
  return (
    <div className="bg-white rounded-lg shadow-sm border border-gray-200 overflow-hidden animate-pulse">
      {/* Header */}
      <div className="px-6 py-4 border-b border-gray-200">
        <div className="grid grid-cols-4 gap-4">
          {Array.from({ length: columns }).map((_, index) => (
            <Skeleton key={index} variant="text" className="w-20" />
          ))}
        </div>
      </div>
      
      {/* Rows */}
      <div className="divide-y divide-gray-200">
        {Array.from({ length: rows }).map((_, rowIndex) => (
          <div key={rowIndex} className="px-6 py-4">
            <div className="grid grid-cols-4 gap-4">
              {Array.from({ length: columns }).map((_, colIndex) => (
                <Skeleton 
                  key={colIndex} 
                  variant="text" 
                  className={colIndex === 0 ? "w-32" : "w-24"} 
                />
              ))}
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}

export function ListSkeleton({ items = 3, variant = 'default' }: { items?: number; variant?: 'default' | 'compact' }) {
  const CardSkeleton = variant === 'compact' ? (
    <div className="flex items-center space-x-3 p-3">
      <Skeleton variant="avatar" className="w-10 h-10" />
      <div className="flex-1">
        <Skeleton variant="text" className="w-32 mb-1" />
        <Skeleton variant="text" className="w-24" />
      </div>
      <Skeleton variant="default" className="w-16 h-6" />
    </div>
  ) : (
    <div className="p-4">
      <Skeleton variant="title" className="w-2/3 mb-2" />
      <Skeleton variant="text" className="w-full mb-2" />
      <Skeleton variant="text" className="w-3/4" />
    </div>
  );

  return (
    <div className="space-y-2">
      {Array.from({ length: items }).map((_, index) => (
        <div key={index} className="bg-white rounded-lg border border-gray-200">
          {CardSkeleton}
        </div>
      ))}
    </div>
  );
}
