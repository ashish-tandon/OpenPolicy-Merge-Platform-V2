'use client';

import { ReactNode, useState, useEffect } from 'react';
import { cn } from '@/lib/utils';
import Link from 'next/link';

// Breadcrumb Component
interface BreadcrumbItem {
  label: string;
  href?: string;
  current?: boolean;
}

interface BreadcrumbProps {
  items: BreadcrumbItem[];
  className?: string;
  separator?: ReactNode;
  showHome?: boolean;
  homeHref?: string;
  homeLabel?: string;
}

export function Breadcrumb({ 
  items, 
  className = "",
  separator = '/',
  showHome = true,
  homeHref = '/',
  homeLabel = 'Home'
}: BreadcrumbProps) {
  const allItems = showHome 
    ? [{ label: homeLabel, href: homeHref }, ...items]
    : items;
  
  return (
    <nav className={cn("flex", className)} aria-label="Breadcrumb">
      <ol className="flex items-center space-x-2">
        {allItems.map((item, index) => (
          <li key={index} className="flex items-center">
            {index > 0 && (
              <span className="mx-2 text-gray-400" aria-hidden="true">
                {separator}
              </span>
            )}
            
            {item.href && !item.current ? (
              <Link
                href={item.href}
                className="text-sm text-gray-500 hover:text-gray-700 transition-colors"
              >
                {item.label}
              </Link>
            ) : (
              <span
                className={cn(
                  "text-sm",
                  item.current 
                    ? "text-gray-900 font-medium" 
                    : "text-gray-500"
                )}
                aria-current={item.current ? 'page' : undefined}
              >
                {item.label}
              </span>
            )}
          </li>
        ))}
      </ol>
    </nav>
  );
}

// Tab Component
interface Tab {
  id: string;
  label: string;
  content: ReactNode;
  disabled?: boolean;
  icon?: ReactNode;
  badge?: string | number;
}

interface TabsProps {
  tabs: Tab[];
  defaultTab?: string;
  className?: string;
  variant?: 'default' | 'pills' | 'underline';
  size?: 'sm' | 'md' | 'lg';
  fullWidth?: boolean;
  onChange?: (tabId: string) => void;
}

export function Tabs({ 
  tabs, 
  defaultTab,
  className = "",
  variant = 'default',
  size = 'md',
  fullWidth = false,
  onChange
}: TabsProps) {
  const [activeTab, setActiveTab] = useState(defaultTab || tabs[0]?.id);
  
  const handleTabChange = (tabId: string) => {
    setActiveTab(tabId);
    onChange?.(tabId);
  };
  
  const variantClasses = {
    default: {
      container: 'border-b border-gray-200',
      tab: 'border-b-2 border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300',
      active: 'border-op-blue text-op-blue'
    },
    pills: {
      container: 'space-x-1',
      tab: 'rounded-md px-3 py-2 text-sm font-medium text-gray-500 hover:text-gray-700 hover:bg-gray-100',
      active: 'bg-op-blue text-white'
    },
    underline: {
      container: 'border-b border-gray-200',
      tab: 'border-b-2 border-transparent text-gray-500 hover:text-gray-700',
      active: 'border-op-blue text-op-blue'
    }
  };
  
  const sizeClasses = {
    sm: 'px-3 py-1.5 text-sm',
    md: 'px-4 py-2 text-sm',
    lg: 'px-6 py-3 text-base'
  };
  
  const activeTabContent = tabs.find(tab => tab.id === activeTab)?.content;
  
  return (
    <div className={className}>
      <div className={cn(
        "flex",
        variant === 'pills' ? variantClasses.pills.container : variantClasses.default.container,
        fullWidth && "w-full"
      )}>
        {tabs.map((tab) => (
          <button
            key={tab.id}
            onClick={() => handleTabChange(tab.id)}
            disabled={tab.disabled}
            className={cn(
              "flex items-center space-x-2 font-medium transition-colors focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-op-blue",
              sizeClasses[size],
              variantClasses[variant].tab,
              activeTab === tab.id && variantClasses[variant].active,
              tab.disabled && "opacity-50 cursor-not-allowed",
              fullWidth && "flex-1 justify-center"
            )}
          >
            {tab.icon && <span className="h-4 w-4">{tab.icon}</span>}
            <span>{tab.label}</span>
            {tab.badge && (
              <span className={cn(
                "inline-flex items-center px-2 py-0.5 rounded-full text-xs font-medium",
                activeTab === tab.id 
                  ? "bg-white text-op-blue" 
                  : "bg-gray-100 text-gray-600"
              )}>
                {tab.badge}
              </span>
            )}
          </button>
        ))}
      </div>
      
      <div className="mt-6">
        {activeTabContent}
      </div>
    </div>
  );
}

// Pagination Component
interface PaginationProps {
  currentPage: number;
  totalPages: number;
  onPageChange: (page: number) => void;
  className?: string;
  showPageNumbers?: boolean;
  showFirstLast?: boolean;
  showPrevNext?: boolean;
  siblingCount?: number;
}

export function Pagination({ 
  currentPage, 
  totalPages, 
  onPageChange,
  className = "",
  showPageNumbers = true,
  showFirstLast = true,
  showPrevNext = true,
  siblingCount = 1
}: PaginationProps) {
  const getPageNumbers = () => {
    const delta = siblingCount + 2;
    const range = [];
    const rangeWithDots = [];
    
    for (let i = Math.max(2, currentPage - delta); i <= Math.min(totalPages - 1, currentPage + delta); i++) {
      range.push(i);
    }
    
    if (currentPage - delta > 2) {
      rangeWithDots.push(1, '...');
    } else {
      rangeWithDots.push(1);
    }
    
    rangeWithDots.push(...range);
    
    if (currentPage + delta < totalPages - 1) {
      rangeWithDots.push('...', totalPages);
    } else {
      rangeWithDots.push(totalPages);
    }
    
    return rangeWithDots;
  };
  
  const pageNumbers = getPageNumbers();
  
  return (
    <nav className={cn("flex items-center justify-center space-x-1", className)} aria-label="Pagination">
      {showFirstLast && currentPage > 1 && (
        <button
          onClick={() => onPageChange(1)}
          className="px-3 py-2 text-sm font-medium text-gray-500 bg-white border border-gray-300 rounded-md hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-op-blue"
        >
          First
        </button>
      )}
      
      {showPrevNext && currentPage > 1 && (
        <button
          onClick={() => onPageChange(currentPage - 1)}
          className="px-3 py-2 text-sm font-medium text-gray-500 bg-white border border-gray-300 rounded-md hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-op-blue"
        >
          Previous
        </button>
      )}
      
      {showPageNumbers && pageNumbers.map((page, index) => (
        <button
          key={index}
          onClick={() => typeof page === 'number' && onPageChange(page)}
          disabled={page === '...'}
          className={cn(
            "px-3 py-2 text-sm font-medium border rounded-md focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-op-blue",
            page === currentPage
              ? "bg-op-blue text-white border-op-blue"
              : page === '...'
              ? "text-gray-400 border-gray-300 cursor-default"
              : "text-gray-500 bg-white border-gray-300 hover:bg-gray-50"
          )}
        >
          {page}
        </button>
      ))}
      
      {showPrevNext && currentPage < totalPages && (
        <button
          onClick={() => onPageChange(currentPage + 1)}
          className="px-3 py-2 text-sm font-medium text-gray-500 bg-white border border-gray-300 rounded-md hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-op-blue"
        >
          Next
        </button>
      )}
      
      {showFirstLast && currentPage < totalPages && (
        <button
          onClick={() => onPageChange(totalPages)}
          className="px-3 py-2 text-sm font-medium text-gray-500 bg-white border border-gray-300 rounded-md hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-op-blue"
        >
          Last
        </button>
      )}
    </nav>
  );
}

// Sidebar Navigation Component
interface SidebarNavItem {
  id: string;
  label: string;
  href?: string;
  icon?: ReactNode;
  badge?: string | number;
  children?: SidebarNavItem[];
  disabled?: boolean;
}

interface SidebarNavProps {
  items: SidebarNavItem[];
  className?: string;
  variant?: 'default' | 'compact';
  activeItem?: string;
  onItemClick?: (item: SidebarNavItem) => void;
}

export function SidebarNav({ 
  items, 
  className = "",
  variant = 'default',
  activeItem,
  onItemClick
}: SidebarNavProps) {
  const [expandedItems, setExpandedItems] = useState<Set<string>>(new Set());
  
  const toggleExpanded = (itemId: string) => {
    const newExpanded = new Set(expandedItems);
    if (newExpanded.has(itemId)) {
      newExpanded.delete(itemId);
    } else {
      newExpanded.add(itemId);
    }
    setExpandedItems(newExpanded);
  };
  
  const renderNavItem = (item: SidebarNavItem, level = 0) => {
    const isActive = activeItem === item.id;
    const isExpanded = expandedItems.has(item.id);
    const hasChildren = item.children && item.children.length > 0;
    
    return (
      <div key={item.id}>
        <div
          className={cn(
            "flex items-center px-3 py-2 text-sm font-medium rounded-md transition-colors cursor-pointer",
            level > 0 && "ml-4",
            variant === 'compact' ? "py-1.5" : "py-2",
            isActive
              ? "bg-op-blue text-white"
              : "text-gray-600 hover:bg-gray-100 hover:text-gray-900",
            item.disabled && "opacity-50 cursor-not-allowed"
          )}
          onClick={() => {
            if (hasChildren) {
              toggleExpanded(item.id);
            } else if (item.href) {
              onItemClick?.(item);
            }
          }}
        >
          {item.icon && (
            <span className={cn("mr-3", variant === 'compact' ? "h-4 w-4" : "h-5 w-5")}>
              {item.icon}
            </span>
          )}
          
          <span className="flex-1">{item.label}</span>
          
          {item.badge && (
            <span className={cn(
              "inline-flex items-center px-2 py-0.5 rounded-full text-xs font-medium",
              isActive 
                ? "bg-white text-op-blue" 
                : "bg-gray-100 text-gray-600"
            )}>
              {item.badge}
            </span>
          )}
          
          {hasChildren && (
            <svg
              className={cn(
                "ml-2 h-4 w-4 transition-transform",
                isExpanded && "rotate-180"
              )}
              fill="none"
              stroke="currentColor"
              viewBox="0 0 24 24"
            >
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 9l-7 7-7-7" />
            </svg>
          )}
        </div>
        
        {hasChildren && isExpanded && (
          <div className="mt-1">
            {item.children!.map(child => renderNavItem(child, level + 1))}
          </div>
        )}
      </div>
    );
  };
  
  return (
    <nav className={cn("space-y-1", className)}>
      {items.map(item => renderNavItem(item))}
    </nav>
  );
}

// Dropdown Menu Component
interface DropdownMenuItem {
  id: string;
  label: string;
  href?: string;
  icon?: ReactNode;
  disabled?: boolean;
  divider?: boolean;
  onClick?: () => void;
}

interface DropdownMenuProps {
  trigger: ReactNode;
  items: DropdownMenuItem[];
  className?: string;
  placement?: 'top' | 'bottom' | 'left' | 'right';
  align?: 'start' | 'center' | 'end';
}

export function DropdownMenu({ 
  trigger, 
  items, 
  className = "",
  placement = 'bottom',
  align = 'start'
}: DropdownMenuProps) {
  const [isOpen, setIsOpen] = useState(false);
  
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
  
  useEffect(() => {
    const handleClickOutside = (event: MouseEvent) => {
      if (isOpen && !(event.target as Element).closest('.dropdown-menu')) {
        setIsOpen(false);
      }
    };
    
    document.addEventListener('mousedown', handleClickOutside);
    return () => document.removeEventListener('mousedown', handleClickOutside);
  }, [isOpen]);
  
  return (
    <div className={cn("relative dropdown-menu", className)}>
      <div onClick={() => setIsOpen(!isOpen)}>
        {trigger}
      </div>
      
      {isOpen && (
        <div className={cn(
          "absolute z-50 min-w-48 bg-white rounded-md shadow-lg border border-gray-200 py-1",
          placementClasses[placement],
          alignClasses[align]
        )}>
          {items.map((item, index) => (
            <div key={item.id}>
              {item.divider ? (
                <div className="border-t border-gray-100 my-1" />
              ) : item.href ? (
                <Link
                  href={item.href}
                  className="flex items-center px-4 py-2 text-sm text-gray-700 hover:bg-gray-100 transition-colors"
                  onClick={() => setIsOpen(false)}
                >
                  {item.icon && <span className="mr-3 h-4 w-4">{item.icon}</span>}
                  {item.label}
                </Link>
              ) : (
                <button
                  onClick={() => {
                    item.onClick?.();
                    setIsOpen(false);
                  }}
                  disabled={item.disabled}
                  className={cn(
                    "w-full flex items-center px-4 py-2 text-sm text-left transition-colors",
                    item.disabled
                      ? "text-gray-400 cursor-not-allowed"
                      : "text-gray-700 hover:bg-gray-100"
                  )}
                >
                  {item.icon && <span className="mr-3 h-4 w-4">{item.icon}</span>}
                  {item.label}
                </button>
              )}
            </div>
          ))}
        </div>
      )}
    </div>
  );
}

// Mobile Menu Component
interface MobileMenuProps {
  isOpen: boolean;
  onClose: () => void;
  children: ReactNode;
  className?: string;
}

export function MobileMenu({ 
  isOpen, 
  onClose, 
  children, 
  className = "" 
}: MobileMenuProps) {
  useEffect(() => {
    if (isOpen) {
      document.body.style.overflow = 'hidden';
    } else {
      document.body.style.overflow = 'unset';
    }
    
    return () => {
      document.body.style.overflow = 'unset';
    };
  }, [isOpen]);
  
  if (!isOpen) return null;
  
  return (
    <>
      {/* Backdrop */}
      <div
        className="fixed inset-0 bg-black bg-opacity-50 z-40 lg:hidden"
        onClick={onClose}
      />
      
      {/* Menu */}
      <div className={cn(
        "fixed inset-y-0 left-0 z-50 w-64 bg-white shadow-xl transform transition-transform duration-300 ease-in-out lg:hidden",
        isOpen ? "translate-x-0" : "-translate-x-full",
        className
      )}>
        <div className="flex items-center justify-between p-4 border-b border-gray-200">
          <h2 className="text-lg font-semibold text-gray-900">Menu</h2>
          <button
            onClick={onClose}
            className="p-2 rounded-md text-gray-400 hover:text-gray-600 hover:bg-gray-100 transition-colors"
          >
            <svg className="h-6 w-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
            </svg>
          </button>
        </div>
        
        <div className="p-4">
          {children}
        </div>
      </div>
    </>
  );
}

// Search Bar Component
interface SearchBarProps {
  placeholder?: string;
  value?: string;
  onChange?: (value: string) => void;
  onSearch?: (query: string) => void;
  className?: string;
  size?: 'sm' | 'md' | 'lg';
  showClearButton?: boolean;
  loading?: boolean;
}

export function SearchBar({ 
  placeholder = "Search...",
  value = "",
  onChange,
  onSearch,
  className = "",
  size = 'md',
  showClearButton = true,
  loading = false
}: SearchBarProps) {
  const [searchValue, setSearchValue] = useState(value);
  
  const sizeClasses = {
    sm: 'px-3 py-1.5 text-sm',
    md: 'px-4 py-2 text-sm',
    lg: 'px-6 py-3 text-base'
  };
  
  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const newValue = e.target.value;
    setSearchValue(newValue);
    onChange?.(newValue);
  };
  
  const handleClear = () => {
    setSearchValue('');
    onChange?.('');
  };
  
  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    onSearch?.(searchValue);
  };
  
  return (
    <form onSubmit={handleSubmit} className={cn("relative", className)}>
      <div className="relative">
        <div className="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
          {loading ? (
            <svg className="animate-spin h-5 w-5 text-gray-400" fill="none" viewBox="0 0 24 24">
              <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4" />
              <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z" />
            </svg>
          ) : (
            <svg className="h-5 w-5 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" />
            </svg>
          )}
        </div>
        
        <input
          type="text"
          value={searchValue}
          onChange={handleChange}
          placeholder={placeholder}
          className={cn(
            "block w-full pl-10 pr-10 border border-gray-300 rounded-md shadow-sm focus:ring-op-blue focus:border-op-blue transition-colors",
            sizeClasses[size]
          )}
        />
        
        {showClearButton && searchValue && (
          <button
            type="button"
            onClick={handleClear}
            className="absolute inset-y-0 right-0 pr-3 flex items-center"
          >
            <svg className="h-5 w-5 text-gray-400 hover:text-gray-600 transition-colors" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
            </svg>
          </button>
        )}
      </div>
    </form>
  );
}
