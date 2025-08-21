'use client';

import { ReactNode, useState, useRef, useEffect } from 'react';
import { 
  EyeIcon, 
  EyeSlashIcon,
  SpeakerWaveIcon,
  SpeakerXMarkIcon,
  MagnifyingGlassIcon,
  AdjustmentsHorizontalIcon
} from '@heroicons/react/24/outline';

// Utility function for combining class names
const cn = (...classes: (string | undefined | null | false)[]) => {
  return classes.filter(Boolean).join(' ');
};

// Skip Link Component
interface SkipLinkProps {
  href: string;
  children: ReactNode;
  className?: string;
}

export function SkipLink({
  href,
  children,
  className = ""
}: SkipLinkProps) {
  return (
    <a
      href={href}
      className={cn(
        "sr-only focus:not-sr-only focus:absolute focus:top-4 focus:left-4",
        "z-50 px-4 py-2 bg-op-blue text-white rounded-md",
        "focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-op-blue",
        className
      )}
    >
      {children}
    </a>
  );
}

// Screen Reader Only Component
interface ScreenReaderOnlyProps {
  children: ReactNode;
  className?: string;
}

export function ScreenReaderOnly({
  children,
  className = ""
}: ScreenReaderOnlyProps) {
  return (
    <span className={cn("sr-only", className)}>
      {children}
    </span>
  );
}

// High Contrast Toggle Component
interface HighContrastToggleProps {
  onToggle?: (enabled: boolean) => void;
  className?: string;
}

export function HighContrastToggle({
  onToggle,
  className = ""
}: HighContrastToggleProps) {
  const [isEnabled, setIsEnabled] = useState(false);

  const toggleHighContrast = () => {
    const newState = !isEnabled;
    setIsEnabled(newState);
    
    if (newState) {
      document.documentElement.classList.add('high-contrast');
    } else {
      document.documentElement.classList.remove('high-contrast');
    }
    
    onToggle?.(newState);
  };

  return (
    <button
      onClick={toggleHighContrast}
      aria-pressed={isEnabled}
      aria-label="Toggle high contrast mode"
      className={cn(
        "flex items-center space-x-2 px-3 py-2 text-sm font-medium",
        "bg-gray-100 text-gray-700 rounded-md hover:bg-gray-200",
        "focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-op-blue",
        "transition-colors",
        className
      )}
    >
      {isEnabled ? (
        <>
          <EyeIcon className="h-4 w-4" />
          <span>High Contrast: On</span>
        </>
      ) : (
        <>
          <EyeSlashIcon className="h-4 w-4" />
          <span>High Contrast: Off</span>
        </>
      )}
    </button>
  );
}

// Font Size Toggle Component
interface FontSizeToggleProps {
  onSizeChange?: (size: 'small' | 'medium' | 'large') => void;
  className?: string;
}

export function FontSizeToggle({
  onSizeChange,
  className = ""
}: FontSizeToggleProps) {
  const [currentSize, setCurrentSize] = useState<'small' | 'medium' | 'large'>('medium');

  const changeFontSize = (size: 'small' | 'medium' | 'large') => {
    setCurrentSize(size);
    
    // Remove existing font size classes
    document.documentElement.classList.remove('text-sm', 'text-base', 'text-lg');
    
    // Add new font size class
    if (size === 'small') {
      document.documentElement.classList.add('text-sm');
    } else if (size === 'large') {
      document.documentElement.classList.add('text-lg');
    }
    
    onSizeChange?.(size);
  };

  return (
    <div className={cn("flex items-center space-x-2", className)}>
      <span className="text-sm font-medium text-gray-700">Font Size:</span>
      <div className="flex rounded-md shadow-sm">
        {(['small', 'medium', 'large'] as const).map((size) => (
          <button
            key={size}
            onClick={() => changeFontSize(size)}
            aria-pressed={currentSize === size}
            className={cn(
              "px-3 py-1 text-sm font-medium border transition-colors",
              "first:rounded-l-md last:rounded-r-md",
              currentSize === size
                ? "bg-op-blue text-white border-op-blue"
                : "bg-white text-gray-700 border-gray-300 hover:bg-gray-50",
              "focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-op-blue",
              "focus:z-10"
            )}
          >
            {size.charAt(0).toUpperCase() + size.slice(1)}
          </button>
        ))}
      </div>
    </div>
  );
}

// Reduced Motion Toggle Component
interface ReducedMotionToggleProps {
  onToggle?: (enabled: boolean) => void;
  className?: string;
}

export function ReducedMotionToggle({
  onToggle,
  className = ""
}: ReducedMotionToggleProps) {
  const [isEnabled, setIsEnabled] = useState(false);

  const toggleReducedMotion = () => {
    const newState = !isEnabled;
    setIsEnabled(newState);
    
    if (newState) {
      document.documentElement.classList.add('reduce-motion');
    } else {
      document.documentElement.classList.remove('reduce-motion');
    }
    
    onToggle?.(newState);
  };

  return (
    <button
      onClick={toggleReducedMotion}
      aria-pressed={isEnabled}
      aria-label="Toggle reduced motion"
      className={cn(
        "flex items-center space-x-2 px-3 py-2 text-sm font-medium",
        "bg-gray-100 text-gray-700 rounded-md hover:bg-gray-200",
        "focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-op-blue",
        "transition-colors",
        className
      )}
    >
      {isEnabled ? (
        <>
          <AdjustmentsHorizontalIcon className="h-4 w-4" />
          <span>Reduced Motion: On</span>
        </>
      ) : (
        <>
          <AdjustmentsHorizontalIcon className="h-4 w-4" />
          <span>Reduced Motion: Off</span>
        </>
      )}
    </button>
  );
}

// Focus Trap Component
interface FocusTrapProps {
  children: ReactNode;
  isActive?: boolean;
  className?: string;
}

export function FocusTrap({
  children,
  isActive = true,
  className = ""
}: FocusTrapProps) {
  const containerRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    if (!isActive) return;

    const container = containerRef.current;
    if (!container) return;

    const focusableElements = container.querySelectorAll(
      'button, [href], input, select, textarea, [tabindex]:not([tabindex="-1"])'
    );

    if (focusableElements.length === 0) return;

    const firstElement = focusableElements[0] as HTMLElement;
    const lastElement = focusableElements[focusableElements.length - 1] as HTMLElement;

    const handleKeyDown = (event: KeyboardEvent) => {
      if (event.key === 'Tab') {
        if (event.shiftKey) {
          if (document.activeElement === firstElement) {
            event.preventDefault();
            lastElement.focus();
          }
        } else {
          if (document.activeElement === lastElement) {
            event.preventDefault();
            firstElement.focus();
          }
        }
      }
    };

    container.addEventListener('keydown', handleKeyDown);
    return () => container.removeEventListener('keydown', handleKeyDown);
  }, [isActive]);

  return (
    <div ref={containerRef} className={className}>
      {children}
    </div>
  );
}

// Live Region Component
interface LiveRegionProps {
  children: ReactNode;
  type?: 'polite' | 'assertive' | 'off';
  className?: string;
}

export function LiveRegion({
  children,
  type = 'polite',
  className = ""
}: LiveRegionProps) {
  return (
    <div
      aria-live={type}
      aria-atomic="true"
      className={cn("sr-only", className)}
    >
      {children}
    </div>
  );
}

// Skip to Content Component
interface SkipToContentProps {
  mainContentId?: string;
  className?: string;
}

export function SkipToContent({
  mainContentId = 'main-content',
  className = ""
}: SkipToContentProps) {
  return (
    <SkipLink
      href={`#${mainContentId}`}
      className={className}
    >
      Skip to main content
    </SkipLink>
  );
}

// Accessibility Menu Component
interface AccessibilityMenuProps {
  className?: string;
}

export function AccessibilityMenu({
  className = ""
}: AccessibilityMenuProps) {
  const [isOpen, setIsOpen] = useState(false);

  return (
    <div className={cn("relative", className)}>
      <button
        onClick={() => setIsOpen(!isOpen)}
        aria-expanded={isOpen}
        aria-label="Accessibility options"
        className={cn(
          "flex items-center space-x-2 px-3 py-2 text-sm font-medium",
          "bg-gray-100 text-gray-700 rounded-md hover:bg-gray-200",
          "focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-op-blue",
          "transition-colors"
        )}
      >
        <AdjustmentsHorizontalIcon className="h-4 w-4" />
        <span>Accessibility</span>
      </button>

      {isOpen && (
        <div className="absolute right-0 mt-2 w-64 bg-white rounded-md shadow-lg border border-gray-200 z-50">
          <div className="p-4 space-y-4">
            <h3 className="text-sm font-medium text-gray-900">Accessibility Options</h3>
            
            <div className="space-y-3">
              <HighContrastToggle />
              <FontSizeToggle />
              <ReducedMotionToggle />
            </div>
          </div>
        </div>
      )}
    </div>
  );
}

// ARIA Label Component
interface AriaLabelProps {
  children: ReactNode;
  label: string;
  className?: string;
}

export function AriaLabel({
  children,
  label,
  className = ""
}: AriaLabelProps) {
  return (
    <div aria-label={label} className={className}>
      {children}
    </div>
  );
}

// ARIA Described By Component
interface AriaDescribedByProps {
  children: ReactNode;
  description: string;
  className?: string;
}

export function AriaDescribedBy({
  children,
  description,
  className = ""
}: AriaDescribedByProps) {
  const descriptionId = `description-${Math.random().toString(36).substr(2, 9)}`;

  return (
    <>
      <div aria-describedby={descriptionId} className={className}>
        {children}
      </div>
      <div id={descriptionId} className="sr-only">
        {description}
      </div>
    </>
  );
}

// Keyboard Navigation Component
interface KeyboardNavigationProps {
  children: ReactNode;
  onKeyDown?: (event: KeyboardEvent) => void;
  className?: string;
}

export function KeyboardNavigation({
  children,
  onKeyDown,
  className = ""
}: KeyboardNavigationProps) {
  const handleKeyDown = (event: React.KeyboardEvent) => {
    onKeyDown?.(event.nativeEvent);
  };

  return (
    <div
      onKeyDown={handleKeyDown}
      tabIndex={0}
      className={cn("outline-none focus:ring-2 focus:ring-op-blue focus:ring-offset-2", className)}
    >
      {children}
    </div>
  );
}

// Announcement Component
interface AnnouncementProps {
  message: string;
  type?: 'polite' | 'assertive';
  className?: string;
}

export function Announcement({
  message,
  type = 'polite',
  className = ""
}: AnnouncementProps) {
  return (
    <LiveRegion type={type} className={className}>
      {message}
    </LiveRegion>
  );
}

// Error Boundary with Accessibility
interface AccessibleErrorBoundaryProps {
  children: ReactNode;
  fallback?: ReactNode | ((error: Error) => ReactNode);
  onError?: (error: Error, errorInfo: any) => void;
  className?: string;
}

export class AccessibleErrorBoundary extends React.Component<AccessibleErrorBoundaryProps, { hasError: boolean; error?: Error }> {
  constructor(props: AccessibleErrorBoundaryProps) {
    super(props);
    this.state = { hasError: false };
  }

  static getDerivedStateFromError(error: Error) {
    return { hasError: true, error };
  }

  componentDidCatch(error: Error, errorInfo: any) {
    this.props.onError?.(error, errorInfo);
  }

  render() {
    if (this.state.hasError) {
      const fallback = this.props.fallback;

      if (typeof fallback === 'function') {
        return fallback(this.state.error!);
      }

      return fallback || (
        <div
          role="alert"
          aria-live="assertive"
          className={cn("p-4 bg-red-50 border border-red-200 rounded-md", this.props.className)}
        >
          <h3 className="text-sm font-medium text-red-800">Something went wrong</h3>
          <p className="mt-2 text-sm text-red-700">
            {this.state.error?.message || 'An unexpected error occurred'}
          </p>
        </div>
      );
    }

    return this.props.children;
  }
}

// Loading State with Accessibility
interface AccessibleLoadingProps {
  isLoading: boolean;
  loadingText?: string;
  children: ReactNode;
  className?: string;
}

export function AccessibleLoading({
  isLoading,
  loadingText = "Loading...",
  children,
  className = ""
}: AccessibleLoadingProps) {
  if (isLoading) {
    return (
      <div
        role="status"
        aria-live="polite"
        className={cn("flex items-center justify-center p-4", className)}
      >
        <div className="animate-spin h-8 w-8 border-4 border-op-blue border-t-transparent rounded-full mr-3"></div>
        <span className="text-sm text-gray-600">{loadingText}</span>
      </div>
    );
  }

  return <>{children}</>;
}

// Progress Bar with Accessibility
interface AccessibleProgressProps {
  value: number;
  max?: number;
  label?: string;
  ariaLabel?: string;
  className?: string;
}

export function AccessibleProgress({
  value,
  max = 100,
  label,
  ariaLabel,
  className = ""
}: AccessibleProgressProps) {
  const percentage = Math.min(Math.max((value / max) * 100, 0), 100);
  const progressId = `progress-${Math.random().toString(36).substr(2, 9)}`;

  return (
    <div className={cn("space-y-2", className)}>
      {(label || ariaLabel) && (
        <div className="flex justify-between items-center">
          {label && <span className="text-sm font-medium text-gray-700">{label}</span>}
          <span className="text-sm text-gray-500">{Math.round(percentage)}%</span>
        </div>
      )}
      
      <div
        role="progressbar"
        aria-valuenow={value}
        aria-valuemin={0}
        aria-valuemax={max}
        aria-labelledby={label ? progressId : undefined}
        aria-label={ariaLabel}
        className="w-full bg-gray-200 rounded-full h-2"
      >
        <div
          id={progressId}
          className="bg-op-blue h-2 rounded-full transition-all duration-300 ease-out"
          style={{ width: `${percentage}%` }}
        />
      </div>
    </div>
  );
}
