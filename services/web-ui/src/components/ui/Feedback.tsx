'use client';

import { ReactNode, useState, useEffect } from 'react';
import { cn } from '@/lib/utils';

// Alert Component
interface AlertProps {
  children: ReactNode;
  type?: 'info' | 'success' | 'warning' | 'error';
  title?: string;
  className?: string;
  dismissible?: boolean;
  onDismiss?: () => void;
  icon?: ReactNode;
}

export function Alert({ 
  children, 
  type = 'info',
  title,
  className = "",
  dismissible = false,
  onDismiss,
  icon
}: AlertProps) {
  const [isVisible, setIsVisible] = useState(true);
  
  const alertStyles = {
    info: {
      container: 'bg-blue-50 border-blue-200 text-blue-800',
      icon: 'text-blue-400',
      title: 'text-blue-800',
      text: 'text-blue-700'
    },
    success: {
      container: 'bg-green-50 border-green-200 text-green-800',
      icon: 'text-green-400',
      title: 'text-green-800',
      text: 'text-green-700'
    },
    warning: {
      container: 'bg-yellow-50 border-yellow-200 text-yellow-800',
      icon: 'text-yellow-400',
      title: 'text-yellow-800',
      text: 'text-yellow-700'
    },
    error: {
      container: 'bg-red-50 border-red-200 text-red-800',
      icon: 'text-red-400',
      title: 'text-red-800',
      text: 'text-red-700'
    }
  };
  
  const defaultIcons = {
    info: (
      <svg className="h-5 w-5" fill="currentColor" viewBox="0 0 20 20">
        <path fillRule="evenodd" d="M18 10a8 8 0 11-16 0 8 8 0 0116 0zm-7-4a1 1 0 11-2 0 1 1 0 012 0zM9 9a1 1 0 000 2v3a1 1 0 001 1h1a1 1 0 100-2v-3a1 1 0 00-1-1H9z" clipRule="evenodd" />
      </svg>
    ),
    success: (
      <svg className="h-5 w-5" fill="currentColor" viewBox="0 0 20 20">
        <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clipRule="evenodd" />
      </svg>
    ),
    warning: (
      <svg className="h-5 w-5" fill="currentColor" viewBox="0 0 20 20">
        <path fillRule="evenodd" d="M8.257 3.099c.765-1.36 2.722-1.36 3.486 0l5.58 9.92c.75 1.334-.213 2.98-1.742 2.98H4.42c-1.53 0-2.493-1.646-1.743-2.98l5.58-9.92zM11 13a1 1 0 11-2 0 1 1 0 012 0zm-1-8a1 1 0 00-1 1v3a1 1 0 002 0V6a1 1 0 00-1-1z" clipRule="evenodd" />
      </svg>
    ),
    error: (
      <svg className="h-5 w-5" fill="currentColor" viewBox="0 0 20 20">
        <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zM8.707 7.293a1 1 0 00-1.414 1.414L8.586 10l-1.293 1.293a1 1 0 101.414 1.414L10 11.414l1.293 1.293a1 1 0 001.414-1.414L11.414 10l1.293-1.293a1 1 0 00-1.414-1.414L10 8.586 8.707 7.293z" clipRule="evenodd" />
      </svg>
    )
  };
  
  const handleDismiss = () => {
    setIsVisible(false);
    onDismiss?.();
  };
  
  if (!isVisible) return null;
  
  return (
    <div className={cn(
      "rounded-md p-4 border",
      alertStyles[type].container,
      className
    )}>
      <div className="flex">
        <div className="flex-shrink-0">
          {icon || defaultIcons[type]}
        </div>
        
        <div className="ml-3 flex-1">
          {title && (
            <h3 className={cn(
              "text-sm font-medium",
              alertStyles[type].title
            )}>
              {title}
            </h3>
          )}
          
          <div className={cn(
            "text-sm",
            title ? "mt-2" : "",
            alertStyles[type].text
          )}>
            {children}
          </div>
        </div>
        
        {dismissible && (
          <div className="ml-auto pl-3">
            <button
              type="button"
              onClick={handleDismiss}
              className={cn(
                "inline-flex rounded-md p-1.5 focus:outline-none focus:ring-2 focus:ring-offset-2",
                alertStyles[type].container,
                "hover:bg-opacity-75 transition-opacity"
              )}
            >
              <svg className="h-4 w-4" fill="currentColor" viewBox="0 0 20 20">
                <path fillRule="evenodd" d="M4.293 4.293a1 1 0 011.414 0L10 8.586l4.293-4.293a1 1 0 111.414 1.414L11.414 10l4.293 4.293a1 1 0 01-1.414 1.414L10 11.414l-4.293 4.293a1 1 0 01-1.414-1.414L8.586 10 4.293 5.707a1 1 0 010-1.414z" clipRule="evenodd" />
              </svg>
            </button>
          </div>
        )}
      </div>
    </div>
  );
}

// Toast Component
interface ToastProps {
  children: ReactNode;
  type?: 'info' | 'success' | 'warning' | 'error';
  title?: string;
  className?: string;
  duration?: number;
  onClose?: () => void;
  position?: 'top-right' | 'top-left' | 'bottom-right' | 'bottom-left' | 'top-center' | 'bottom-center';
}

export function Toast({ 
  children, 
  type = 'info',
  title,
  className = "",
  duration = 5000,
  onClose,
  position = 'top-right'
}: ToastProps) {
  const [isVisible, setIsVisible] = useState(true);
  
  useEffect(() => {
    if (duration > 0) {
      const timer = setTimeout(() => {
        setIsVisible(false);
        onClose?.();
      }, duration);
      
      return () => clearTimeout(timer);
    }
  }, [duration, onClose]);
  
  const positionClasses = {
    'top-right': 'top-4 right-4',
    'top-left': 'top-4 left-4',
    'bottom-right': 'bottom-4 right-4',
    'bottom-left': 'bottom-4 left-4',
    'top-center': 'top-4 left-1/2 transform -translate-x-1/2',
    'bottom-center': 'bottom-4 left-1/2 transform -translate-x-1/2'
  };
  
  const toastStyles = {
    info: 'bg-blue-600 text-white',
    success: 'bg-green-600 text-white',
    warning: 'bg-yellow-600 text-white',
    error: 'bg-red-600 text-white'
  };
  
  const handleClose = () => {
    setIsVisible(false);
    onClose?.();
  };
  
  if (!isVisible) return null;
  
  return (
    <div className={cn(
      "fixed z-50 max-w-sm w-full shadow-lg rounded-lg pointer-events-auto",
      positionClasses[position],
      toastStyles[type],
      className
    )}>
      <div className="p-4">
        <div className="flex items-start">
          <div className="flex-1">
            {title && (
              <p className="text-sm font-medium mb-1">
                {title}
              </p>
            )}
            <p className="text-sm opacity-90">
              {children}
            </p>
          </div>
          
          <button
            type="button"
            onClick={handleClose}
            className="ml-4 flex-shrink-0 rounded-md inline-flex text-white hover:text-white focus:outline-none focus:ring-2 focus:ring-white"
          >
            <svg className="h-4 w-4" fill="currentColor" viewBox="0 0 20 20">
              <path fillRule="evenodd" d="M4.293 4.293a1 1 0 011.414 0L10 8.586l4.293-4.293a1 1 0 111.414 1.414L11.414 10l4.293 4.293a1 1 0 01-1.414 1.414L10 11.414l-4.293 4.293a1 1 0 01-1.414-1.414L8.586 10 4.293 5.707a1 1 0 010-1.414z" clipRule="evenodd" />
            </svg>
          </button>
        </div>
      </div>
    </div>
  );
}

// Toast Container Component
interface ToastContainerProps {
  children: ReactNode;
  position?: 'top-right' | 'top-left' | 'bottom-right' | 'bottom-left' | 'top-center' | 'bottom-center';
  className?: string;
}

export function ToastContainer({ 
  children, 
  position = 'top-right',
  className = "" 
}: ToastContainerProps) {
  const positionClasses = {
    'top-right': 'top-0 right-0',
    'top-left': 'top-0 left-0',
    'bottom-right': 'bottom-0 right-0',
    'bottom-left': 'bottom-0 left-0',
    'top-center': 'top-0 left-1/2 transform -translate-x-1/2',
    'bottom-center': 'bottom-0 left-1/2 transform -translate-x-1/2'
  };
  
  return (
    <div className={cn(
      "fixed z-50 p-4 space-y-4 pointer-events-none",
      positionClasses[position],
      className
    )}>
      {children}
    </div>
  );
}

// Progress Bar Component
interface ProgressBarProps {
  value: number;
  max?: number;
  className?: string;
  size?: 'sm' | 'md' | 'lg';
  color?: 'default' | 'success' | 'warning' | 'error';
  showLabel?: boolean;
  animated?: boolean;
}

export function ProgressBar({ 
  value, 
  max = 100,
  className = "",
  size = 'md',
  color = 'default',
  showLabel = false,
  animated = false
}: ProgressBarProps) {
  const percentage = Math.min(Math.max((value / max) * 100, 0), 100);
  
  const sizeClasses = {
    sm: 'h-2',
    md: 'h-3',
    lg: 'h-4'
  };
  
  const colorClasses = {
    default: 'bg-op-blue',
    success: 'bg-green-500',
    warning: 'bg-yellow-500',
    error: 'bg-red-500'
  };
  
  return (
    <div className={cn("w-full", className)}>
      {showLabel && (
        <div className="flex justify-between text-sm text-gray-600 mb-1">
          <span>Progress</span>
          <span>{Math.round(percentage)}%</span>
        </div>
      )}
      
      <div className={cn(
        "w-full bg-gray-200 rounded-full overflow-hidden",
        sizeClasses[size]
      )}>
        <div
          className={cn(
            "h-full rounded-full transition-all duration-300 ease-out",
            colorClasses[color],
            animated && "animate-pulse"
          )}
          style={{ width: `${percentage}%` }}
        />
      </div>
    </div>
  );
}

// Spinner Component
interface SpinnerProps {
  size?: 'sm' | 'md' | 'lg' | 'xl';
  color?: 'default' | 'white' | 'gray';
  className?: string;
  label?: string;
}

export function Spinner({ 
  size = 'md',
  color = 'default',
  className = "",
  label = 'Loading...'
}: SpinnerProps) {
  const sizeClasses = {
    sm: 'h-4 w-4',
    md: 'h-6 w-6',
    lg: 'h-8 w-8',
    xl: 'h-12 w-12'
  };
  
  const colorClasses = {
    default: 'text-op-blue',
    white: 'text-white',
    gray: 'text-gray-400'
  };
  
  return (
    <div className={cn("flex items-center", className)}>
      <svg
        className={cn(
          "animate-spin",
          sizeClasses[size],
          colorClasses[color]
        )}
        fill="none"
        viewBox="0 0 24 24"
        role="status"
        aria-label={label}
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
      
      {label && (
        <span className="ml-2 text-sm text-gray-600 sr-only">
          {label}
        </span>
      )}
    </div>
  );
}

// Loading Skeleton Component
interface SkeletonProps {
  className?: string;
  width?: string | number;
  height?: string | number;
  rounded?: boolean;
  animated?: boolean;
}

export function Skeleton({ 
  className = "",
  width,
  height,
  rounded = true,
  animated = true
}: SkeletonProps) {
  const style: React.CSSProperties = {};
  
  if (width) {
    style.width = typeof width === 'number' ? `${width}px` : width;
  }
  
  if (height) {
    style.height = typeof height === 'number' ? `${height}px` : height;
  }
  
  return (
    <div
      className={cn(
        "bg-gray-200",
        rounded && "rounded",
        animated && "animate-pulse",
        className
      )}
      style={style}
    />
  );
}

// Skeleton Text Component
interface SkeletonTextProps {
  lines?: number;
  className?: string;
  lineHeight?: 'sm' | 'md' | 'lg';
}

export function SkeletonText({ 
  lines = 3,
  className = "",
  lineHeight = 'md'
}: SkeletonTextProps) {
  const heightClasses = {
    sm: 'h-3',
    md: 'h-4',
    lg: 'h-5'
  };
  
  return (
    <div className={cn("space-y-2", className)}>
      {Array.from({ length: lines }).map((_, index) => (
        <Skeleton
          key={index}
          className={cn(
            heightClasses[lineHeight],
            index === lines - 1 ? "w-3/4" : "w-full"
          )}
        />
      ))}
    </div>
  );
}

// Skeleton Avatar Component
interface SkeletonAvatarProps {
  size?: 'sm' | 'md' | 'lg' | 'xl';
  className?: string;
}

export function SkeletonAvatar({ 
  size = 'md',
  className = "" 
}: SkeletonAvatarProps) {
  const sizeClasses = {
    sm: 'h-8 w-8',
    md: 'h-10 w-10',
    lg: 'h-12 w-12',
    xl: 'h-16 w-16'
  };
  
  return (
    <Skeleton
      className={cn(
        sizeClasses[size],
        "rounded-full",
        className
      )}
    />
  );
}

// Skeleton Card Component
interface SkeletonCardProps {
  className?: string;
  showAvatar?: boolean;
  showImage?: boolean;
  lines?: number;
}

export function SkeletonCard({ 
  className = "",
  showAvatar = false,
  showImage = false,
  lines = 3
}: SkeletonCardProps) {
  return (
    <div className={cn(
      "bg-white rounded-lg border border-gray-200 p-6",
      className
    )}>
      <div className="flex items-start space-x-4">
        {showAvatar && (
          <SkeletonAvatar size="md" />
        )}
        
        <div className="flex-1 space-y-3">
          {showImage && (
            <Skeleton className="w-full h-32 rounded" />
          )}
          
          <Skeleton className="h-4 w-3/4" />
          <SkeletonText lines={lines} />
        </div>
      </div>
    </div>
  );
}

// Badge Component
interface BadgeProps {
  children: ReactNode;
  variant?: 'default' | 'success' | 'warning' | 'error' | 'info';
  size?: 'sm' | 'md' | 'lg';
  className?: string;
  dot?: boolean;
}

export function Badge({ 
  children, 
  variant = 'default',
  size = 'md',
  className = "",
  dot = false
}: BadgeProps) {
  const variantClasses = {
    default: 'bg-gray-100 text-gray-800',
    success: 'bg-green-100 text-green-800',
    warning: 'bg-yellow-100 text-yellow-800',
    error: 'bg-red-100 text-red-800',
    info: 'bg-blue-100 text-blue-800'
  };
  
  const sizeClasses = {
    sm: 'px-2 py-0.5 text-xs',
    md: 'px-2.5 py-0.5 text-sm',
    lg: 'px-3 py-1 text-base'
  };
  
  const dotColors = {
    default: 'bg-gray-400',
    success: 'bg-green-400',
    warning: 'bg-yellow-400',
    error: 'bg-red-400',
    info: 'bg-blue-400'
  };
  
  return (
    <span className={cn(
      "inline-flex items-center font-medium rounded-full",
      variantClasses[variant],
      sizeClasses[size],
      className
    )}>
      {dot && (
        <span className={cn(
          "w-1.5 h-1.5 rounded-full mr-1.5",
          dotColors[variant]
        )} />
      )}
      {children}
    </span>
  );
}

// Status Indicator Component
interface StatusIndicatorProps {
  status: 'online' | 'offline' | 'away' | 'busy';
  size?: 'sm' | 'md' | 'lg';
  className?: string;
  showLabel?: boolean;
}

export function StatusIndicator({ 
  status, 
  size = 'md',
  className = "",
  showLabel = false
}: StatusIndicatorProps) {
  const statusConfig = {
    online: {
      color: 'bg-green-400',
      label: 'Online'
    },
    offline: {
      color: 'bg-gray-400',
      label: 'Offline'
    },
    away: {
      color: 'bg-yellow-400',
      label: 'Away'
    },
    busy: {
      color: 'bg-red-400',
      label: 'Busy'
    }
  };
  
  const sizeClasses = {
    sm: 'w-2 h-2',
    md: 'w-3 h-3',
    lg: 'w-4 h-4'
  };
  
  const config = statusConfig[status];
  
  return (
    <div className={cn("flex items-center", className)}>
      <span className={cn(
        "rounded-full",
        sizeClasses[size],
        config.color
      )} />
      
      {showLabel && (
        <span className="ml-2 text-sm text-gray-600">
          {config.label}
        </span>
      )}
    </div>
  );
}
