'use client';

import { ReactNode, useState, useEffect } from 'react';
import { cn } from '@/lib/utils';

// Modal Component
interface ModalProps {
  isOpen: boolean;
  onClose: () => void;
  children: ReactNode;
  title?: string;
  size?: 'sm' | 'md' | 'lg' | 'xl' | 'full';
  closeOnOverlayClick?: boolean;
  closeOnEscape?: boolean;
  showCloseButton?: boolean;
  className?: string;
}

export function Modal({ 
  isOpen, 
  onClose, 
  children, 
  title,
  size = 'md',
  closeOnOverlayClick = true,
  closeOnEscape = true,
  showCloseButton = true,
  className = ""
}: ModalProps) {
  const [isVisible, setIsVisible] = useState(false);
  
  useEffect(() => {
    if (isOpen) {
      setIsVisible(true);
      document.body.style.overflow = 'hidden';
    } else {
      const timer = setTimeout(() => {
        setIsVisible(false);
      }, 150);
      return () => clearTimeout(timer);
    }
    
    return () => {
      document.body.style.overflow = 'unset';
    };
  }, [isOpen]);
  
  useEffect(() => {
    if (!closeOnEscape) return;
    
    const handleEscape = (e: KeyboardEvent) => {
      if (e.key === 'Escape') {
        onClose();
      }
    };
    
    if (isOpen) {
      document.addEventListener('keydown', handleEscape);
      return () => document.removeEventListener('keydown', handleEscape);
    }
  }, [isOpen, onClose, closeOnEscape]);
  
  const sizeClasses = {
    sm: 'max-w-sm',
    md: 'max-w-md',
    lg: 'max-w-lg',
    xl: 'max-w-xl',
    full: 'max-w-full mx-4'
  };
  
  if (!isVisible) return null;
  
  return (
    <div className="fixed inset-0 z-50 overflow-y-auto">
      <div className="flex min-h-full items-center justify-center p-4">
        {/* Backdrop */}
        <div
          className={cn(
            "fixed inset-0 bg-black transition-opacity duration-150",
            isOpen ? "bg-opacity-50" : "bg-opacity-0"
          )}
          onClick={closeOnOverlayClick ? onClose : undefined}
        />
        
        {/* Modal */}
        <div
          className={cn(
            "relative w-full transform rounded-lg bg-white shadow-xl transition-all duration-150",
            sizeClasses[size],
            isOpen ? "scale-100 opacity-100" : "scale-95 opacity-0",
            className
          )}
        >
          {/* Header */}
          {(title || showCloseButton) && (
            <div className="flex items-center justify-between px-6 py-4 border-b border-gray-200">
              {title && (
                <h3 className="text-lg font-medium text-gray-900">
                  {title}
                </h3>
              )}
              
              {showCloseButton && (
                <button
                  type="button"
                  onClick={onClose}
                  className="rounded-md bg-white text-gray-400 hover:text-gray-500 focus:outline-none focus:ring-2 focus:ring-op-blue focus:ring-offset-2"
                >
                  <span className="sr-only">Close</span>
                  <svg className="h-6 w-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
                  </svg>
                </button>
              )}
            </div>
          )}
          
          {/* Content */}
          <div className="px-6 py-4">
            {children}
          </div>
        </div>
      </div>
    </div>
  );
}

// Drawer Component
interface DrawerProps {
  isOpen: boolean;
  onClose: () => void;
  children: ReactNode;
  title?: string;
  position?: 'left' | 'right' | 'top' | 'bottom';
  size?: 'sm' | 'md' | 'lg' | 'xl' | 'full';
  closeOnOverlayClick?: boolean;
  closeOnEscape?: boolean;
  showCloseButton?: boolean;
  className?: string;
}

export function Drawer({ 
  isOpen, 
  onClose, 
  children, 
  title,
  position = 'right',
  size = 'md',
  closeOnOverlayClick = true,
  closeOnEscape = true,
  showCloseButton = true,
  className = ""
}: DrawerProps) {
  const [isVisible, setIsVisible] = useState(false);
  
  useEffect(() => {
    if (isOpen) {
      setIsVisible(true);
      document.body.style.overflow = 'hidden';
    } else {
      const timer = setTimeout(() => {
        setIsVisible(false);
      }, 150);
      return () => clearTimeout(timer);
    }
    
    return () => {
      document.body.style.overflow = 'unset';
    };
  }, [isOpen]);
  
  useEffect(() => {
    if (!closeOnEscape) return;
    
    const handleEscape = (e: KeyboardEvent) => {
      if (e.key === 'Escape') {
        onClose();
      }
    };
    
    if (isOpen) {
      document.addEventListener('keydown', handleEscape);
      return () => document.removeEventListener('keydown', handleEscape);
    }
  }, [isOpen, onClose, closeOnEscape]);
  
  const positionClasses = {
    left: 'left-0 h-full',
    right: 'right-0 h-full',
    top: 'top-0 w-full',
    bottom: 'bottom-0 w-full'
  };
  
  const sizeClasses = {
    sm: position === 'left' || position === 'right' ? 'w-80' : 'h-80',
    md: position === 'left' || position === 'right' ? 'w-96' : 'h-96',
    lg: position === 'left' || position === 'right' ? 'w-[32rem]' : 'h-[32rem]',
    xl: position === 'left' || position === 'right' ? 'w-[40rem]' : 'h-[40rem]',
    full: position === 'left' || position === 'right' ? 'w-full' : 'h-full'
  };
  
  const transformClasses = {
    left: isOpen ? 'translate-x-0' : '-translate-x-full',
    right: isOpen ? 'translate-x-0' : 'translate-x-full',
    top: isOpen ? 'translate-y-0' : '-translate-y-full',
    bottom: isOpen ? 'translate-y-0' : 'translate-y-full'
  };
  
  if (!isVisible) return null;
  
  return (
    <div className="fixed inset-0 z-50 overflow-hidden">
      {/* Backdrop */}
      <div
        className={cn(
          "fixed inset-0 bg-black transition-opacity duration-150",
          isOpen ? "bg-opacity-50" : "bg-opacity-0"
        )}
        onClick={closeOnOverlayClick ? onClose : undefined}
      />
      
      {/* Drawer */}
      <div
        className={cn(
          "fixed bg-white shadow-xl transition-transform duration-150 ease-in-out",
          positionClasses[position],
          sizeClasses[size],
          transformClasses[position],
          className
        )}
      >
        {/* Header */}
        {(title || showCloseButton) && (
          <div className="flex items-center justify-between px-6 py-4 border-b border-gray-200">
            {title && (
              <h3 className="text-lg font-medium text-gray-900">
                {title}
              </h3>
            )}
            
            {showCloseButton && (
              <button
                type="button"
                onClick={onClose}
                className="rounded-md bg-white text-gray-400 hover:text-gray-500 focus:outline-none focus:ring-2 focus:ring-op-blue focus:ring-offset-2"
              >
                <span className="sr-only">Close</span>
                <svg className="h-6 w-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
                </svg>
              </button>
            )}
          </div>
        )}
        
        {/* Content */}
        <div className="h-full overflow-y-auto px-6 py-4">
          {children}
        </div>
      </div>
    </div>
  );
}

// Popover Component
interface PopoverProps {
  trigger: ReactNode;
  children: ReactNode;
  isOpen?: boolean;
  onOpenChange?: (open: boolean) => void;
  placement?: 'top' | 'bottom' | 'left' | 'right';
  align?: 'start' | 'center' | 'end';
  className?: string;
  offset?: number;
}

export function Popover({ 
  trigger, 
  children, 
  isOpen: controlledIsOpen,
  onOpenChange,
  placement = 'bottom',
  align = 'center',
  className = "",
  offset = 8
}: PopoverProps) {
  const [isOpen, setIsOpen] = useState(false);
  const [triggerRef, setTriggerRef] = useState<HTMLDivElement | null>(null);
  const [popoverRef, setPopoverRef] = useState<HTMLDivElement | null>(null);
  
  const isControlled = controlledIsOpen !== undefined;
  const open = isControlled ? controlledIsOpen : isOpen;
  
  const handleToggle = () => {
    if (isControlled) {
      onOpenChange?.(!open);
    } else {
      setIsOpen(!open);
    }
  };
  
  useEffect(() => {
    const handleClickOutside = (event: MouseEvent) => {
      if (
        open &&
        triggerRef &&
        popoverRef &&
        !triggerRef.contains(event.target as Node) &&
        !popoverRef.contains(event.target as Node)
      ) {
        if (isControlled) {
          onOpenChange?.(false);
        } else {
          setIsOpen(false);
        }
      }
    };
    
    document.addEventListener('mousedown', handleClickOutside);
    return () => document.removeEventListener('mousedown', handleClickOutside);
  }, [open, triggerRef, popoverRef, isControlled, onOpenChange]);
  
  const placementClasses = {
    top: 'bottom-full mb-2',
    bottom: 'top-full mt-2',
    left: 'right-full mr-2',
    right: 'left-full ml-2'
  };
  
  const alignClasses = {
    start: 'left-0',
    center: 'left-1/2 transform -translate-x-1/2',
    end: 'right-0'
  };
  
  return (
    <div className="relative">
      <div ref={setTriggerRef} onClick={handleToggle}>
        {trigger}
      </div>
      
      {open && (
        <div
          ref={setPopoverRef}
          className={cn(
            "absolute z-50 min-w-48 bg-white rounded-md shadow-lg border border-gray-200 py-1",
            placementClasses[placement],
            alignClasses[align],
            className
          )}
        >
          {children}
        </div>
      )}
    </div>
  );
}

// Tooltip Component
interface TooltipProps {
  children: ReactNode;
  content: string;
  placement?: 'top' | 'bottom' | 'left' | 'right';
  className?: string;
  delay?: number;
  showArrow?: boolean;
}

export function Tooltip({ 
  children, 
  content, 
  placement = 'top',
  className = "",
  delay = 200,
  showArrow = true
}: TooltipProps) {
  const [isVisible, setIsVisible] = useState(false);
  const [timeoutId, setTimeoutId] = useState<NodeJS.Timeout | null>(null);
  
  const handleMouseEnter = () => {
    if (timeoutId) {
      clearTimeout(timeoutId);
    }
    setTimeoutId(setTimeout(() => setIsVisible(true), delay));
  };
  
  const handleMouseLeave = () => {
    if (timeoutId) {
      clearTimeout(timeoutId);
    }
    setIsVisible(false);
  };
  
  const placementClasses = {
    top: 'bottom-full mb-2',
    bottom: 'top-full mt-2',
    left: 'right-full mr-2',
    right: 'left-full ml-2'
  };
  
  const arrowClasses = {
    top: 'top-full left-1/2 transform -translate-x-1/2 border-t border-gray-200',
    bottom: 'bottom-full left-1/2 transform -translate-x-1/2 border-b border-gray-200',
    left: 'left-full top-1/2 transform -translate-y-1/2 border-l border-gray-200',
    right: 'right-full top-1/2 transform -translate-y-1/2 border-r border-gray-200'
  };
  
  return (
    <div
      className="relative inline-block"
      onMouseEnter={handleMouseEnter}
      onMouseLeave={handleMouseLeave}
    >
      {children}
      
      {isVisible && (
        <div
          className={cn(
            "absolute z-50 px-2 py-1 text-sm text-white bg-gray-900 rounded shadow-lg whitespace-nowrap",
            placementClasses[placement],
            "left-1/2 transform -translate-x-1/2",
            className
          )}
        >
          {content}
          
          {showArrow && (
            <div
              className={cn(
                "absolute w-0 h-0",
                arrowClasses[placement]
              )}
              style={{
                [placement === 'top' || placement === 'bottom' ? 'borderLeft' : 'borderTop']: '4px solid transparent',
                [placement === 'top' || placement === 'bottom' ? 'borderRight' : 'borderBottom']: '4px solid transparent',
                [placement === 'top' ? 'borderTop' : placement === 'bottom' ? 'borderBottom' : placement === 'left' ? 'borderLeft' : 'borderRight']: '4px solid #111827'
              }}
            />
          )}
        </div>
      )}
    </div>
  );
}

// Loading Overlay Component
interface LoadingOverlayProps {
  isVisible: boolean;
  children?: ReactNode;
  text?: string;
  spinner?: ReactNode;
  className?: string;
}

export function LoadingOverlay({ 
  isVisible, 
  children, 
  text = "Loading...",
  spinner,
  className = ""
}: LoadingOverlayProps) {
  if (!isVisible) return <>{children}</>;
  
  const defaultSpinner = (
    <svg className="animate-spin h-8 w-8 text-white" fill="none" viewBox="0 0 24 24">
      <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4" />
      <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z" />
    </svg>
  );
  
  return (
    <div className={cn("relative", className)}>
      {children}
      
      <div className="absolute inset-0 bg-black bg-opacity-50 flex items-center justify-center z-10">
        <div className="bg-white rounded-lg p-6 shadow-xl">
          <div className="flex flex-col items-center space-y-4">
            {spinner || defaultSpinner}
            <p className="text-gray-700 font-medium">{text}</p>
          </div>
        </div>
      </div>
    </div>
  );
}

// Notification Component
interface NotificationProps {
  isVisible: boolean;
  onClose: () => void;
  children: ReactNode;
  type?: 'info' | 'success' | 'warning' | 'error';
  title?: string;
  duration?: number;
  position?: 'top-right' | 'top-left' | 'bottom-right' | 'bottom-left' | 'top-center' | 'bottom-center';
  className?: string;
}

export function Notification({ 
  isVisible, 
  onClose, 
  children, 
  type = 'info',
  title,
  duration = 5000,
  position = 'top-right',
  className = ""
}: NotificationProps) {
  const [isVisibleState, setIsVisibleState] = useState(false);
  
  useEffect(() => {
    if (isVisible) {
      setIsVisibleState(true);
      
      if (duration > 0) {
        const timer = setTimeout(() => {
          onClose();
        }, duration);
        
        return () => clearTimeout(timer);
      }
    } else {
      const timer = setTimeout(() => {
        setIsVisibleState(false);
      }, 150);
      
      return () => clearTimeout(timer);
    }
  }, [isVisible, onClose, duration]);
  
  const positionClasses = {
    'top-right': 'top-4 right-4',
    'top-left': 'top-4 left-4',
    'bottom-right': 'bottom-4 right-4',
    'bottom-left': 'bottom-4 left-4',
    'top-center': 'top-4 left-1/2 transform -translate-x-1/2',
    'bottom-center': 'bottom-4 left-1/2 transform -translate-x-1/2'
  };
  
  const typeClasses = {
    info: 'bg-blue-600 text-white',
    success: 'bg-green-600 text-white',
    warning: 'bg-yellow-600 text-white',
    error: 'bg-red-600 text-white'
  };
  
  if (!isVisibleState) return null;
  
  return (
    <div
      className={cn(
        "fixed z-50 max-w-sm w-full shadow-lg rounded-lg pointer-events-auto transition-all duration-150",
        positionClasses[position],
        typeClasses[type],
        isVisible ? "opacity-100 scale-100" : "opacity-0 scale-95",
        className
      )}
    >
      <div className="p-4">
        <div className="flex items-start">
          <div className="flex-1">
            {title && (
              <p className="text-sm font-medium mb-1">
                {title}
              </p>
            )}
            <div className="text-sm opacity-90">
              {children}
            </div>
          </div>
          
          <button
            type="button"
            onClick={onClose}
            className="ml-4 flex-shrink-0 rounded-md inline-flex text-white hover:text-white focus:outline-none focus:ring-2 focus:ring-white"
          >
            <svg className="h-4 w-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
            </svg>
          </button>
        </div>
      </div>
    </div>
  );
}

// Notification Container Component
interface NotificationContainerProps {
  children: ReactNode;
  position?: 'top-right' | 'top-left' | 'bottom-right' | 'bottom-left' | 'top-center' | 'bottom-center';
  className?: string;
}

export function NotificationContainer({ 
  children, 
  position = 'top-right',
  className = "" 
}: NotificationContainerProps) {
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
