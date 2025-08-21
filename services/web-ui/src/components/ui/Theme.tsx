'use client';

import { ReactNode, createContext, useContext, useState, useEffect } from 'react';
import { 
  SunIcon, 
  MoonIcon, 
  ComputerDesktopIcon,
  SwatchIcon,
  EyeIcon,
  EyeSlashIcon
} from '@heroicons/react/24/outline';

// Utility function for combining class names
const cn = (...classes: (string | undefined | null | false)[]) => {
  return classes.filter(Boolean).join(' ');
};

// Theme Types
export type Theme = 'light' | 'dark' | 'system';
export type ColorScheme = 'blue' | 'green' | 'red' | 'yellow' | 'purple' | 'pink' | 'indigo' | 'teal';

// Theme Context
interface ThemeContextType {
  theme: Theme;
  colorScheme: ColorScheme;
  setTheme: (theme: Theme) => void;
  setColorScheme: (scheme: ColorScheme) => void;
  isDark: boolean;
  isSystem: boolean;
}

const ThemeContext = createContext<ThemeContextType | undefined>(undefined);

// Theme Provider Component
interface ThemeProviderProps {
  children: ReactNode;
  defaultTheme?: Theme;
  defaultColorScheme?: ColorScheme;
  storageKey?: string;
  className?: string;
}

export function ThemeProvider({
  children,
  defaultTheme = 'system',
  defaultColorScheme = 'blue',
  storageKey = 'op-theme',
  className = ""
}: ThemeProviderProps) {
  const [theme, setThemeState] = useState<Theme>(defaultTheme);
  const [colorScheme, setColorSchemeState] = useState<ColorScheme>(defaultColorScheme);
  const [isDark, setIsDark] = useState(false);
  const [isSystem, setIsSystem] = useState(defaultTheme === 'system');

  useEffect(() => {
    // Load theme from localStorage
    const savedTheme = localStorage.getItem(storageKey) as Theme;
    const savedColorScheme = localStorage.getItem(`${storageKey}-color`) as ColorScheme;
    
    if (savedTheme) {
      setThemeState(savedTheme);
      setIsSystem(savedTheme === 'system');
    }
    
    if (savedColorScheme) {
      setColorSchemeState(savedColorScheme);
    }
  }, [storageKey]);

  useEffect(() => {
    // Apply theme to document
    const root = document.documentElement;
    
    // Remove existing theme classes
    root.classList.remove('light', 'dark');
    
    if (theme === 'system') {
      const systemTheme = window.matchMedia('(prefers-color-scheme: dark)').matches ? 'dark' : 'light';
      root.classList.add(systemTheme);
      setIsDark(systemTheme === 'dark');
      setIsSystem(true);
    } else {
      root.classList.add(theme);
      setIsDark(theme === 'dark');
      setIsSystem(false);
    }
    
    // Save to localStorage
    localStorage.setItem(storageKey, theme);
  }, [theme, storageKey]);

  useEffect(() => {
    // Apply color scheme to document
    const root = document.documentElement;
    
    // Remove existing color scheme classes
    root.classList.remove('color-blue', 'color-green', 'color-red', 'color-yellow', 'color-purple', 'color-pink', 'color-indigo', 'color-teal');
    
    // Add new color scheme class
    root.classList.add(`color-${colorScheme}`);
    
    // Save to localStorage
    localStorage.setItem(`${storageKey}-color`, colorScheme);
  }, [colorScheme, storageKey]);

  useEffect(() => {
    // Listen for system theme changes
    if (theme === 'system') {
      const mediaQuery = window.matchMedia('(prefers-color-scheme: dark)');
      
      const handleChange = (e: MediaQueryListEvent) => {
        const root = document.documentElement;
        root.classList.remove('light', 'dark');
        root.classList.add(e.matches ? 'dark' : 'light');
        setIsDark(e.matches);
      };
      
      mediaQuery.addEventListener('change', handleChange);
      return () => mediaQuery.removeEventListener('change', handleChange);
    }
  }, [theme]);

  const setTheme = (newTheme: Theme) => {
    setThemeState(newTheme);
  };

  const setColorScheme = (newColorScheme: ColorScheme) => {
    setColorSchemeState(newColorScheme);
  };

  const value: ThemeContextType = {
    theme,
    colorScheme,
    setTheme,
    setColorScheme,
    isDark,
    isSystem
  };

  return (
    <ThemeContext.Provider value={value}>
      <div className={cn("theme-provider", className)}>
        {children}
      </div>
    </ThemeContext.Provider>
  );
}

// Theme Hook
export function useTheme(): ThemeContextType {
  const context = useContext(ThemeContext);
  if (context === undefined) {
    throw new Error('useTheme must be used within a ThemeProvider');
  }
  return context;
}

// Theme Toggle Component
interface ThemeToggleProps {
  className?: string;
  showLabels?: boolean;
}

export function ThemeToggle({
  className = "",
  showLabels = true
}: ThemeToggleProps) {
  const { theme, setTheme } = useTheme();

  const toggleTheme = () => {
    const themes: Theme[] = ['light', 'dark', 'system'];
    const currentIndex = themes.indexOf(theme);
    const nextIndex = (currentIndex + 1) % themes.length;
    setTheme(themes[nextIndex]);
  };

  const getThemeIcon = () => {
    switch (theme) {
      case 'light':
        return <SunIcon className="h-5 w-5" />;
      case 'dark':
        return <MoonIcon className="h-5 w-5" />;
      case 'system':
        return <ComputerDesktopIcon className="h-5 w-5" />;
      default:
        return <SunIcon className="h-5 w-5" />;
    }
  };

  const getThemeLabel = () => {
    switch (theme) {
      case 'light':
        return 'Light';
      case 'dark':
        return 'Dark';
      case 'system':
        return 'System';
      default:
        return 'Light';
    }
  };

  return (
    <button
      onClick={toggleTheme}
      aria-label={`Switch to ${theme === 'light' ? 'dark' : theme === 'dark' ? 'system' : 'light'} theme`}
      className={cn(
        "flex items-center space-x-2 px-3 py-2 text-sm font-medium",
        "bg-gray-100 text-gray-700 rounded-md hover:bg-gray-200",
        "dark:bg-gray-800 dark:text-gray-200 dark:hover:bg-gray-700",
        "focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-op-blue",
        "transition-colors",
        className
      )}
    >
      {getThemeIcon()}
      {showLabels && <span>{getThemeLabel()}</span>}
    </button>
  );
}

// Color Scheme Picker Component
interface ColorSchemePickerProps {
  className?: string;
  showLabels?: boolean;
}

export function ColorSchemePicker({
  className = "",
  showLabels = true
}: ColorSchemePickerProps) {
  const { colorScheme, setColorScheme } = useTheme();

  const colorSchemes: { scheme: ColorScheme; name: string; bgClass: string; textClass: string }[] = [
    { scheme: 'blue', name: 'Blue', bgClass: 'bg-blue-500', textClass: 'text-blue-500' },
    { scheme: 'green', name: 'Green', bgClass: 'bg-green-500', textClass: 'text-green-500' },
    { scheme: 'red', name: 'Red', bgClass: 'bg-red-500', textClass: 'text-red-500' },
    { scheme: 'yellow', name: 'Yellow', bgClass: 'bg-yellow-500', textClass: 'text-yellow-500' },
    { scheme: 'purple', name: 'Purple', bgClass: 'bg-purple-500', textClass: 'text-purple-500' },
    { scheme: 'pink', name: 'Pink', bgClass: 'bg-pink-500', textClass: 'text-pink-500' },
    { scheme: 'indigo', name: 'Indigo', bgClass: 'bg-indigo-500', textClass: 'text-indigo-500' },
    { scheme: 'teal', name: 'Teal', bgClass: 'bg-teal-500', textClass: 'text-teal-500' }
  ];

  return (
    <div className={cn("space-y-3", className)}>
      {showLabels && (
        <div className="flex items-center space-x-2">
          <SwatchIcon className="h-4 w-4 text-gray-500" />
          <span className="text-sm font-medium text-gray-700 dark:text-gray-300">Color Scheme</span>
        </div>
      )}
      
      <div className="grid grid-cols-4 gap-2">
        {colorSchemes.map(({ scheme, name, bgClass, textClass }) => (
          <button
            key={scheme}
            onClick={() => setColorScheme(scheme)}
            aria-label={`Switch to ${name} color scheme`}
            aria-pressed={colorScheme === scheme}
            className={cn(
              "w-8 h-8 rounded-full border-2 transition-all",
              "focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-op-blue",
              colorScheme === scheme
                ? `${bgClass} border-white ring-2 ring-op-blue ring-offset-2`
                : `${bgClass} border-gray-200 hover:border-gray-300 hover:scale-110`
            )}
          />
        ))}
      </div>
    </div>
  );
}

// Theme Switcher Component
interface ThemeSwitcherProps {
  className?: string;
  showColorPicker?: boolean;
}

export function ThemeSwitcher({
  className = "",
  showColorPicker = true
}: ThemeSwitcherProps) {
  return (
    <div className={cn("space-y-4", className)}>
      <ThemeToggle />
      {showColorPicker && <ColorSchemePicker />}
    </div>
  );
}

// Theme Aware Component
interface ThemeAwareProps {
  children: ReactNode;
  lightClassName?: string;
  darkClassName?: string;
  className?: string;
}

export function ThemeAware({
  children,
  lightClassName = "",
  darkClassName = "",
  className = ""
}: ThemeAwareProps) {
  const { isDark } = useTheme();

  return (
    <div className={cn(
      isDark ? darkClassName : lightClassName,
      className
    )}>
      {children}
    </div>
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
        "dark:bg-gray-800 dark:text-gray-200 dark:hover:bg-gray-700",
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
      <span className="text-sm font-medium text-gray-700 dark:text-gray-300">Font Size:</span>
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
                : "bg-white text-gray-700 border-gray-300 hover:bg-gray-50 dark:bg-gray-800 dark:text-gray-200 dark:border-gray-600 dark:hover:bg-gray-700",
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
        "dark:bg-gray-800 dark:text-gray-200 dark:hover:bg-gray-700",
        "focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-op-blue",
        "transition-colors",
        className
      )}
    >
      <SwatchIcon className="h-4 w-4" />
      <span>Reduced Motion: {isEnabled ? 'On' : 'Off'}</span>
    </button>
  );
}

// Theme Settings Panel Component
interface ThemeSettingsPanelProps {
  isOpen: boolean;
  onClose: () => void;
  className?: string;
}

export function ThemeSettingsPanel({
  isOpen,
  onClose,
  className = ""
}: ThemeSettingsPanelProps) {
  if (!isOpen) return null;

  return (
    <div className={cn("fixed inset-0 z-50 overflow-y-auto", className)}>
      <div className="flex min-h-full items-end justify-center p-4 text-center sm:items-center sm:p-0">
        <div className="fixed inset-0 bg-gray-500 bg-opacity-75 transition-opacity" onClick={onClose} />
        
        <div className="relative transform overflow-hidden rounded-lg bg-white dark:bg-gray-800 px-4 pb-4 pt-5 text-left shadow-xl transition-all sm:my-8 sm:w-full sm:max-w-lg sm:p-6">
          <div className="absolute right-0 top-0 pr-4 pt-4">
            <button
              onClick={onClose}
              className="rounded-md bg-white dark:bg-gray-800 text-gray-400 hover:text-gray-500 focus:outline-none focus:ring-2 focus:ring-op-blue focus:ring-offset-2"
            >
              <span className="sr-only">Close</span>
              <svg className="h-6 w-6" fill="none" viewBox="0 0 24 24" strokeWidth="1.5" stroke="currentColor">
                <path strokeLinecap="round" strokeLinejoin="round" d="M6 18L18 6M6 6l12 12" />
              </svg>
            </button>
          </div>
          
          <div className="sm:flex sm:items-start">
            <div className="mt-3 text-center sm:ml-4 sm:mt-0 sm:text-left w-full">
              <h3 className="text-lg font-medium leading-6 text-gray-900 dark:text-gray-100 mb-4">
                Theme Settings
              </h3>
              
              <div className="space-y-6">
                <ThemeSwitcher />
                <HighContrastToggle />
                <FontSizeToggle />
                <ReducedMotionToggle />
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}

// CSS Variables for Theme Colors
export const themeCSSVariables = {
  blue: {
    '--op-primary': '#3B82F6',
    '--op-primary-hover': '#2563EB',
    '--op-primary-light': '#DBEAFE',
    '--op-primary-dark': '#1E40AF'
  },
  green: {
    '--op-primary': '#10B981',
    '--op-primary-hover': '#059669',
    '--op-primary-light': '#D1FAE5',
    '--op-primary-dark': '#047857'
  },
  red: {
    '--op-primary': '#EF4444',
    '--op-primary-hover': '#DC2626',
    '--op-primary-light': '#FEE2E2',
    '--op-primary-dark': '#B91C1C'
  },
  yellow: {
    '--op-primary': '#F59E0B',
    '--op-primary-hover': '#D97706',
    '--op-primary-light': '#FEF3C7',
    '--op-primary-dark': '#B45309'
  },
  purple: {
    '--op-primary': '#8B5CF6',
    '--op-primary-hover': '#7C3AED',
    '--op-primary-light': '#EDE9FE',
    '--op-primary-dark': '#6D28D9'
  },
  pink: {
    '--op-primary': '#EC4899',
    '--op-primary-hover': '#DB2777',
    '--op-primary-light': '#FCE7F3',
    '--op-primary-dark': '#BE185D'
  },
  indigo: {
    '--op-primary': '#6366F1',
    '--op-primary-hover': '#4F46E5',
    '--op-primary-light': '#E0E7FF',
    '--op-primary-dark': '#4338CA'
  },
  teal: {
    '--op-primary': '#14B8A6',
    '--op-primary-hover': '#0D9488',
    '--op-primary-light': '#CCFBF1',
    '--op-primary-dark': '#0F766E'
  }
};
