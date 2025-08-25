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
import { ThemeService, Theme, ColorScheme } from '@/services/themeService';

// Utility function for combining class names
const cn = (...classes: (string | undefined | null | false)[]) => {
  return classes.filter(Boolean).join(' ');
};

// Theme Context
interface ThemeContextType {
  theme: Theme;
  colorScheme: ColorScheme;
  setTheme: (theme: Theme) => void;
  setColorScheme: (scheme: ColorScheme) => void;
  isDark: boolean;
  isSystem: boolean;
  highContrast: boolean;
  setHighContrast: (enabled: boolean) => void;
  fontSize: 'small' | 'medium' | 'large';
  setFontSize: (size: 'small' | 'medium' | 'large') => void;
  reducedMotion: boolean;
  setReducedMotion: (enabled: boolean) => void;
}

const ThemeContext = createContext<ThemeContextType | undefined>(undefined);

// Theme Provider Component
interface ThemeProviderProps {
  children: ReactNode;
  className?: string;
}

export function ThemeProvider({
  children,
  className = ""
}: ThemeProviderProps) {
  const [config, setConfig] = useState(() => ThemeService.getConfig());
  const [isDark, setIsDark] = useState(() => ThemeService.isDark());

  useEffect(() => {
    // Initialize theme service
    ThemeService.initialize();
    
    // Update state with current config
    setConfig(ThemeService.getConfig());
    setIsDark(ThemeService.isDark());
    
    // Listen for system theme changes
    const mediaQuery = window.matchMedia('(prefers-color-scheme: dark)');
    const handleChange = () => {
      setIsDark(ThemeService.isDark());
    };
    
    mediaQuery.addEventListener('change', handleChange);
    return () => mediaQuery.removeEventListener('change', handleChange);
  }, []);

  const setTheme = (newTheme: Theme) => {
    ThemeService.setTheme(newTheme);
    setConfig(ThemeService.getConfig());
    setIsDark(ThemeService.isDark());
  };

  const setColorScheme = (newColorScheme: ColorScheme) => {
    ThemeService.setColorScheme(newColorScheme);
    setConfig(ThemeService.getConfig());
  };

  const setHighContrast = (enabled: boolean) => {
    ThemeService.setHighContrast(enabled);
    setConfig(ThemeService.getConfig());
  };

  const setFontSize = (size: 'small' | 'medium' | 'large') => {
    ThemeService.setFontSize(size);
    setConfig(ThemeService.getConfig());
  };

  const setReducedMotion = (enabled: boolean) => {
    ThemeService.setReducedMotion(enabled);
    setConfig(ThemeService.getConfig());
  };

  const value: ThemeContextType = {
    theme: config.theme,
    colorScheme: config.colorScheme,
    setTheme,
    setColorScheme,
    isDark,
    isSystem: config.theme === 'system',
    highContrast: config.highContrast,
    setHighContrast,
    fontSize: config.fontSize,
    setFontSize,
    reducedMotion: config.reducedMotion,
    setReducedMotion
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

// High Contrast Toggle Component
interface HighContrastToggleProps {
  className?: string;
}

export function HighContrastToggle({
  className = ""
}: HighContrastToggleProps) {
  const { highContrast, setHighContrast } = useTheme();

  return (
    <button
      onClick={() => setHighContrast(!highContrast)}
      aria-pressed={highContrast}
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
      {highContrast ? (
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
  className?: string;
}

export function FontSizeToggle({
  className = ""
}: FontSizeToggleProps) {
  const { fontSize, setFontSize } = useTheme();

  return (
    <div className={cn("flex items-center space-x-2", className)}>
      <span className="text-sm font-medium text-gray-700 dark:text-gray-300">Font Size:</span>
      <div className="flex rounded-md shadow-sm">
        {(['small', 'medium', 'large'] as const).map((size) => (
          <button
            key={size}
            onClick={() => setFontSize(size)}
            aria-pressed={fontSize === size}
            className={cn(
              "px-3 py-1 text-sm font-medium border transition-colors",
              "first:rounded-l-md last:rounded-r-md",
              fontSize === size
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
  className?: string;
}

export function ReducedMotionToggle({
  className = ""
}: ReducedMotionToggleProps) {
  const { reducedMotion, setReducedMotion } = useTheme();

  return (
    <button
      onClick={() => setReducedMotion(!reducedMotion)}
      aria-pressed={reducedMotion}
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
      <span>Reduced Motion: {reducedMotion ? 'On' : 'Off'}</span>
    </button>
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

// Export theme CSS variables helper
export { ThemeService } from '@/services/themeService';
