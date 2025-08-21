'use client';

import { ReactNode, useState, useEffect, useRef } from 'react';
import { cn } from '@/lib/utils';

// Click Outside Hook Component
interface ClickOutsideProps {
  children: ReactNode;
  onClickOutside: () => void;
  className?: string;
}

export function ClickOutside({ 
  children, 
  onClickOutside, 
  className = "" 
}: ClickOutsideProps) {
  const ref = useRef<HTMLDivElement>(null);
  
  useEffect(() => {
    const handleClickOutside = (event: MouseEvent) => {
      if (ref.current && !ref.current.contains(event.target as Node)) {
        onClickOutside();
      }
    };
    
    document.addEventListener('mousedown', handleClickOutside);
    return () => document.removeEventListener('mousedown', handleClickOutside);
  }, [onClickOutside]);
  
  return (
    <div ref={ref} className={className}>
      {children}
    </div>
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

// Portal Component
interface PortalProps {
  children: ReactNode;
  container?: HTMLElement;
  className?: string;
}

export function Portal({ 
  children, 
  container = document.body,
  className = "" 
}: PortalProps) {
  const [mounted, setMounted] = useState(false);
  
  useEffect(() => {
    setMounted(true);
  }, []);
  
  if (!mounted) return null;
  
  return (
    <div className={className}>
      {children}
    </div>
  );
}

// Lazy Load Component
interface LazyLoadProps {
  children: ReactNode;
  threshold?: number;
  className?: string;
  placeholder?: ReactNode;
}

export function LazyLoad({ 
  children, 
  threshold = 0.1,
  className = "",
  placeholder
}: LazyLoadProps) {
  const [isVisible, setIsVisible] = useState(false);
  const [isLoaded, setIsLoaded] = useState(false);
  const ref = useRef<HTMLDivElement>(null);
  
  useEffect(() => {
    const observer = new IntersectionObserver(
      ([entry]) => {
        if (entry.isIntersecting) {
          setIsVisible(true);
          observer.disconnect();
        }
      },
      { threshold }
    );
    
    if (ref.current) {
      observer.observe(ref.current);
    }
    
    return () => observer.disconnect();
  }, [threshold]);
  
  const handleLoad = () => {
    setIsLoaded(true);
  };
  
  return (
    <div ref={ref} className={className}>
      {!isVisible && placeholder}
      {isVisible && (
        <div onLoad={handleLoad}>
          {children}
        </div>
      )}
    </div>
  );
}

// Error Boundary Component
interface ErrorBoundaryState {
  hasError: boolean;
  error?: Error;
}

interface ErrorBoundaryProps {
  children: ReactNode;
  fallback?: ReactNode | ((error: Error) => ReactNode);
  onError?: (error: Error, errorInfo: any) => void;
  className?: string;
}

export class ErrorBoundary extends React.Component<ErrorBoundaryProps, ErrorBoundaryState> {
  constructor(props: ErrorBoundaryProps) {
    super(props);
    this.state = { hasError: false };
  }
  
  static getDerivedStateFromError(error: Error): ErrorBoundaryState {
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
        <div className={cn("p-4 bg-red-50 border border-red-200 rounded-md", this.props.className)}>
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

// Suspense Boundary Component
interface SuspenseBoundaryProps {
  children: ReactNode;
  fallback?: ReactNode;
  className?: string;
}

export function SuspenseBoundary({ 
  children, 
  fallback,
  className = "" 
}: SuspenseBoundaryProps) {
  return (
    <React.Suspense
      fallback={
        fallback || (
          <div className={cn("p-4 text-center", className)}>
            <div className="animate-spin h-8 w-8 border-4 border-op-blue border-t-transparent rounded-full mx-auto"></div>
            <p className="mt-2 text-sm text-gray-600">Loading...</p>
          </div>
        )
      }
    >
      {children}
    </React.Suspense>
  );
}

// Debounce Hook Component
interface DebounceProps {
  children: (debouncedValue: any) => ReactNode;
  value: any;
  delay?: number;
}

export function Debounce({ 
  children, 
  value, 
  delay = 300 
}: DebounceProps) {
  const [debouncedValue, setDebouncedValue] = useState(value);
  
  useEffect(() => {
    const timer = setTimeout(() => {
      setDebouncedValue(value);
    }, delay);
    
    return () => clearTimeout(timer);
  }, [value, delay]);
  
  return <>{children(debouncedValue)}</>;
}

// Throttle Hook Component
interface ThrottleProps {
  children: (throttledValue: any) => ReactNode;
  value: any;
  delay?: number;
}

export function Throttle({ 
  children, 
  value, 
  delay = 300 
}: ThrottleProps) {
  const [throttledValue, setThrottledValue] = useState(value);
  const lastRun = useRef(Date.now());
  
  useEffect(() => {
    const now = Date.now();
    if (now - lastRun.current >= delay) {
      setThrottledValue(value);
      lastRun.current = now;
    }
  }, [value, delay]);
  
  return <>{children(throttledValue)}</>;
}

// Local Storage Hook Component
interface LocalStorageProps {
  children: (value: any, setValue: (value: any) => void) => ReactNode;
  key: string;
  defaultValue?: any;
}

export function LocalStorage({ 
  children, 
  key, 
  defaultValue 
}: LocalStorageProps) {
  const [value, setValue] = useState(() => {
    if (typeof window === 'undefined') return defaultValue;
    
    try {
      const item = window.localStorage.getItem(key);
      return item ? JSON.parse(item) : defaultValue;
    } catch {
      return defaultValue;
    }
  });
  
  const setStoredValue = (newValue: any) => {
    try {
      setValue(newValue);
      if (typeof window !== 'undefined') {
        window.localStorage.setItem(key, JSON.stringify(newValue));
      }
    } catch {
      // Handle error
    }
  };
  
  return <>{children(value, setStoredValue)}</>;
}

// Session Storage Hook Component
interface SessionStorageProps {
  children: (value: any, setValue: (value: any) => void) => ReactNode;
  key: string;
  defaultValue?: any;
}

export function SessionStorage({ 
  children, 
  key, 
  defaultValue 
}: SessionStorageProps) {
  const [value, setValue] = useState(() => {
    if (typeof window === 'undefined') return defaultValue;
    
    try {
      const item = window.sessionStorage.getItem(key);
      return item ? JSON.parse(item) : defaultValue;
    } catch {
      return defaultValue;
    }
  });
  
  const setStoredValue = (newValue: any) => {
    try {
      setValue(newValue);
      if (typeof window !== 'undefined') {
        window.sessionStorage.setItem(key, JSON.stringify(newValue));
      }
    } catch {
      // Handle error
    }
  };
  
  return <>{children(value, setStoredValue)}</>;
}

// Media Query Hook Component
interface MediaQueryProps {
  children: (matches: boolean) => ReactNode;
  query: string;
}

export function MediaQuery({ 
  children, 
  query 
}: MediaQueryProps) {
  const [matches, setMatches] = useState(false);
  
  useEffect(() => {
    if (typeof window === 'undefined') return;
    
    const mediaQuery = window.matchMedia(query);
    setMatches(mediaQuery.matches);
    
    const handler = (event: MediaQueryListEvent) => {
      setMatches(event.matches);
    };
    
    mediaQuery.addEventListener('change', handler);
    return () => mediaQuery.removeEventListener('change', handler);
  }, [query]);
  
  return <>{children(matches)}</>;
}

// Intersection Observer Hook Component
interface IntersectionObserverProps {
  children: (isIntersecting: boolean, entry: IntersectionObserverEntry | null) => ReactNode;
  threshold?: number;
  rootMargin?: string;
  root?: Element | null;
}

export function IntersectionObserver({ 
  children, 
  threshold = 0,
  rootMargin = '0px',
  root = null
}: IntersectionObserverProps) {
  const [isIntersecting, setIsIntersecting] = useState(false);
  const [entry, setEntry] = useState<IntersectionObserverEntry | null>(null);
  const ref = useRef<HTMLDivElement>(null);
  
  useEffect(() => {
    if (typeof window === 'undefined') return;
    
    const observer = new IntersectionObserver(
      ([entry]) => {
        setIsIntersecting(entry.isIntersecting);
        setEntry(entry);
      },
      { threshold, rootMargin, root }
    );
    
    if (ref.current) {
      observer.observe(ref.current);
    }
    
    return () => observer.disconnect();
  }, [threshold, rootMargin, root]);
  
  return (
    <div ref={ref}>
      {children(isIntersecting, entry)}
    </div>
  );
}

// Resize Observer Hook Component
interface ResizeObserverProps {
  children: (size: { width: number; height: number }) => ReactNode;
  className?: string;
}

export function ResizeObserver({ 
  children, 
  className = "" 
}: ResizeObserverProps) {
  const [size, setSize] = useState({ width: 0, height: 0 });
  const ref = useRef<HTMLDivElement>(null);
  
  useEffect(() => {
    if (typeof window === 'undefined') return;
    
    const observer = new ResizeObserver((entries) => {
      for (const entry of entries) {
        const { width, height } = entry.contentRect;
        setSize({ width, height });
      }
    });
    
    if (ref.current) {
      observer.observe(ref.current);
    }
    
    return () => observer.disconnect();
  }, []);
  
  return (
    <div ref={ref} className={className}>
      {children(size)}
    </div>
  );
}

// Keyboard Shortcut Component
interface KeyboardShortcutProps {
  children: ReactNode;
  shortcut: string;
  onTrigger: () => void;
  className?: string;
}

export function KeyboardShortcut({ 
  children, 
  shortcut, 
  onTrigger, 
  className = "" 
}: KeyboardShortcutProps) {
  useEffect(() => {
    const handleKeyDown = (event: KeyboardEvent) => {
      const keys = shortcut.toLowerCase().split('+');
      const pressedKeys = [];
      
      if (event.ctrlKey) pressedKeys.push('ctrl');
      if (event.metaKey) pressedKeys.push('cmd');
      if (event.shiftKey) pressedKeys.push('shift');
      if (event.altKey) pressedKeys.push('alt');
      
      const key = event.key.toLowerCase();
      if (key !== 'control' && key !== 'meta' && key !== 'shift' && key !== 'alt') {
        pressedKeys.push(key);
      }
      
      const isMatch = keys.length === pressedKeys.length && 
        keys.every(key => pressedKeys.includes(key));
      
      if (isMatch) {
        event.preventDefault();
        onTrigger();
      }
    };
    
    document.addEventListener('keydown', handleKeyDown);
    return () => document.removeEventListener('keydown', handleKeyDown);
  }, [shortcut, onTrigger]);
  
  return (
    <div className={className}>
      {children}
    </div>
  );
}

// Copy to Clipboard Component
interface CopyToClipboardProps {
  children: ReactNode;
  text: string;
  onCopy?: () => void;
  onError?: (error: Error) => void;
  className?: string;
}

export function CopyToClipboard({ 
  children, 
  text, 
  onCopy, 
  onError, 
  className = "" 
}: CopyToClipboardProps) {
  const handleCopy = async () => {
    try {
      await navigator.clipboard.writeText(text);
      onCopy?.();
    } catch (_error) {
      onError?.(error as Error);
    }
  };
  
  return (
    <div onClick={handleCopy} className={cn("cursor-pointer", className)}>
      {children}
    </div>
  );
}

// Download Component
interface DownloadProps {
  children: ReactNode;
  data: string | Blob;
  filename: string;
  mimeType?: string;
  className?: string;
}

export function Download({ 
  children, 
  data, 
  filename, 
  mimeType = 'text/plain',
  className = "" 
}: DownloadProps) {
  const handleDownload = () => {
    const blob = new Blob([data], { type: mimeType });
    const url = URL.createObjectURL(blob);
    
    const link = document.createElement('a');
    link.href = url;
    link.download = filename;
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
    
    URL.revokeObjectURL(url);
  };
  
  return (
    <div onClick={handleDownload} className={cn("cursor-pointer", className)}>
      {children}
    </div>
  );
}

// Print Component
interface PrintProps {
  children: ReactNode;
  className?: string;
}

export function Print({ 
  children, 
  className = "" 
}: PrintProps) {
  const handlePrint = () => {
    window.print();
  };
  
  return (
    <div onClick={handlePrint} className={cn("cursor-pointer", className)}>
      {children}
    </div>
  );
}

// Scroll to Top Component
interface ScrollToTopProps {
  children: ReactNode;
  className?: string;
  smooth?: boolean;
}

export function ScrollToTop({ 
  children, 
  className = "",
  smooth = true
}: ScrollToTopProps) {
  const handleScrollToTop = () => {
    window.scrollTo({
      top: 0,
      behavior: smooth ? 'smooth' : 'auto'
    });
  };
  
  return (
    <div onClick={handleScrollToTop} className={cn("cursor-pointer", className)}>
      {children}
    </div>
  );
}

// Scroll to Element Component
interface ScrollToElementProps {
  children: ReactNode;
  targetId: string;
  className?: string;
  smooth?: boolean;
  offset?: number;
}

export function ScrollToElement({ 
  children, 
  targetId, 
  className = "",
  smooth = true,
  offset = 0
}: ScrollToElementProps) {
  const handleScrollToElement = () => {
    const element = document.getElementById(targetId);
    if (element) {
      const elementPosition = element.offsetTop - offset;
      window.scrollTo({
        top: elementPosition,
        behavior: smooth ? 'smooth' : 'auto'
      });
    }
  };
  
  return (
    <div onClick={handleScrollToElement} className={cn("cursor-pointer", className)}>
      {children}
    </div>
  );
}
