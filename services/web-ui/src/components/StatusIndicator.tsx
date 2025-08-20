/**
 * Status indicator component for various states
 * Based on legacy status patterns from bills and debates
 */

interface StatusIndicatorProps {
  status: string;
  type?: 'dot' | 'badge' | 'banner';
  size?: 'sm' | 'md' | 'lg';
  className?: string;
}

export default function StatusIndicator({ 
  status, 
  type = 'badge',
  size = 'md',
  className = '' 
}: StatusIndicatorProps) {
  // Status color mappings based on legacy patterns
  const getStatusColor = (status: string) => {
    const lowerStatus = status.toLowerCase();
    
    // Success states
    if (['passed', 'royal assent', 'active', 'sitting', 'online', 'available'].includes(lowerStatus)) {
      return {
        bg: 'bg-green-100',
        text: 'text-green-800',
        dot: 'bg-green-500'
      };
    }
    
    // Error/Failed states
    if (['defeated', 'failed', 'offline', 'error', 'unavailable'].includes(lowerStatus)) {
      return {
        bg: 'bg-red-100',
        text: 'text-red-800',
        dot: 'bg-red-500'
      };
    }
    
    // In Progress states
    if (['in committee', 'in progress', 'pending', 'processing'].includes(lowerStatus)) {
      return {
        bg: 'bg-blue-100',
        text: 'text-blue-800',
        dot: 'bg-blue-500'
      };
    }
    
    // Warning states
    if (['adjourned', 'delayed', 'warning'].includes(lowerStatus)) {
      return {
        bg: 'bg-yellow-100',
        text: 'text-yellow-800',
        dot: 'bg-yellow-500'
      };
    }
    
    // Default/Neutral
    return {
      bg: 'bg-gray-100',
      text: 'text-gray-800',
      dot: 'bg-gray-500'
    };
  };
  
  const colors = getStatusColor(status);
  const sizeClasses = {
    sm: {
      badge: 'px-2 py-0.5 text-xs',
      dot: 'h-2 w-2',
      banner: 'px-3 py-1 text-sm'
    },
    md: {
      badge: 'px-3 py-1 text-sm',
      dot: 'h-3 w-3',
      banner: 'px-4 py-2 text-base'
    },
    lg: {
      badge: 'px-4 py-2 text-base',
      dot: 'h-4 w-4',
      banner: 'px-6 py-3 text-lg'
    }
  };
  
  if (type === 'dot') {
    return (
      <span 
        className={`inline-flex items-center ${className}`}
        role="status"
        aria-label={`Status: ${status}`}
      >
        <span className={`${sizeClasses[size].dot} ${colors.dot} rounded-full`} />
        <span className="sr-only">{status}</span>
      </span>
    );
  }
  
  if (type === 'banner') {
    return (
      <div 
        className={`${colors.bg} ${colors.text} ${sizeClasses[size].banner} rounded-md border border-current border-opacity-20 ${className}`}
        role="status"
        aria-live="polite"
      >
        <div className="flex items-center">
          <span className={`${sizeClasses[size].dot} ${colors.dot} rounded-full mr-3`} />
          <span className="font-medium">{status}</span>
        </div>
      </div>
    );
  }
  
  // Default badge type
  return (
    <span 
      className={`inline-flex items-center ${colors.bg} ${colors.text} ${sizeClasses[size].badge} rounded-md font-medium ${className}`}
      role="status"
    >
      {status}
    </span>
  );
}

// Live status component for real-time updates
export function LiveStatusIndicator({ 
  isLive,
  label = 'Live'
}: { 
  isLive: boolean;
  label?: string;
}) {
  if (!isLive) return null;
  
  return (
    <span 
      className="inline-flex items-center px-3 py-1 rounded-full text-xs font-medium bg-red-100 text-red-800"
      role="status"
      aria-live="polite"
      aria-atomic="true"
    >
      <span className="relative flex h-2 w-2 mr-2">
        <span className="animate-ping absolute inline-flex h-full w-full rounded-full bg-red-400 opacity-75" />
        <span className="relative inline-flex rounded-full h-2 w-2 bg-red-500" />
      </span>
      {label}
    </span>
  );
}
