/**
 * Theme Service
 * 
 * Centralized service for managing application themes.
 * Consolidates all theme-related functionality to ensure consistency.
 */

export type Theme = 'light' | 'dark' | 'system';
export type ColorScheme = 'blue' | 'green' | 'red' | 'yellow' | 'purple' | 'pink' | 'indigo' | 'teal';

interface ThemeConfig {
  theme: Theme;
  colorScheme: ColorScheme;
  highContrast: boolean;
  fontSize: 'small' | 'medium' | 'large';
  reducedMotion: boolean;
}

export class ThemeService {
  private static readonly STORAGE_KEY = 'op-theme-config';
  private static config: ThemeConfig = {
    theme: 'system',
    colorScheme: 'blue',
    highContrast: false,
    fontSize: 'medium',
    reducedMotion: false
  };

  /**
   * Initialize theme service and apply saved preferences
   */
  static initialize(): void {
    // Load saved config
    const saved = this.loadConfig();
    if (saved) {
      this.config = saved;
    }

    // Apply initial theme
    this.applyTheme();
    
    // Listen for system theme changes
    if (this.config.theme === 'system') {
      this.setupSystemThemeListener();
    }
  }

  /**
   * Get current theme configuration
   */
  static getConfig(): Readonly<ThemeConfig> {
    return { ...this.config };
  }

  /**
   * Set theme (light, dark, or system)
   */
  static setTheme(theme: Theme): void {
    this.config.theme = theme;
    this.applyTheme();
    this.saveConfig();
    
    // Setup or remove system theme listener
    if (theme === 'system') {
      this.setupSystemThemeListener();
    } else {
      this.removeSystemThemeListener();
    }
  }

  /**
   * Set color scheme
   */
  static setColorScheme(colorScheme: ColorScheme): void {
    this.config.colorScheme = colorScheme;
    this.applyColorScheme();
    this.saveConfig();
  }

  /**
   * Toggle high contrast mode
   */
  static setHighContrast(enabled: boolean): void {
    this.config.highContrast = enabled;
    this.applyHighContrast();
    this.saveConfig();
  }

  /**
   * Set font size
   */
  static setFontSize(size: 'small' | 'medium' | 'large'): void {
    this.config.fontSize = size;
    this.applyFontSize();
    this.saveConfig();
  }

  /**
   * Toggle reduced motion
   */
  static setReducedMotion(enabled: boolean): void {
    this.config.reducedMotion = enabled;
    this.applyReducedMotion();
    this.saveConfig();
  }

  /**
   * Check if current theme is dark
   */
  static isDark(): boolean {
    if (this.config.theme === 'dark') return true;
    if (this.config.theme === 'light') return false;
    
    // For system theme, check actual preference
    return window.matchMedia('(prefers-color-scheme: dark)').matches;
  }

  /**
   * Get CSS variables for current color scheme
   */
  static getColorSchemeVariables(): Record<string, string> {
    const schemes: Record<ColorScheme, Record<string, string>> = {
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

    return schemes[this.config.colorScheme];
  }

  // Private methods

  private static applyTheme(): void {
    const root = document.documentElement;
    
    // Remove existing theme classes
    root.classList.remove('light', 'dark');
    
    if (this.config.theme === 'system') {
      const systemTheme = window.matchMedia('(prefers-color-scheme: dark)').matches ? 'dark' : 'light';
      root.classList.add(systemTheme);
    } else {
      root.classList.add(this.config.theme);
    }
  }

  private static applyColorScheme(): void {
    const root = document.documentElement;
    
    // Remove existing color scheme classes
    root.classList.remove('color-blue', 'color-green', 'color-red', 'color-yellow', 
                         'color-purple', 'color-pink', 'color-indigo', 'color-teal');
    
    // Add new color scheme class
    root.classList.add(`color-${this.config.colorScheme}`);
    
    // Apply CSS variables
    const variables = this.getColorSchemeVariables();
    Object.entries(variables).forEach(([key, value]) => {
      root.style.setProperty(key, value);
    });
  }

  private static applyHighContrast(): void {
    const root = document.documentElement;
    
    if (this.config.highContrast) {
      root.classList.add('high-contrast');
    } else {
      root.classList.remove('high-contrast');
    }
  }

  private static applyFontSize(): void {
    const root = document.documentElement;
    
    // Remove existing font size classes
    root.classList.remove('text-sm', 'text-base', 'text-lg');
    
    // Add new font size class
    if (this.config.fontSize === 'small') {
      root.classList.add('text-sm');
    } else if (this.config.fontSize === 'large') {
      root.classList.add('text-lg');
    }
  }

  private static applyReducedMotion(): void {
    const root = document.documentElement;
    
    if (this.config.reducedMotion) {
      root.classList.add('reduce-motion');
    } else {
      root.classList.remove('reduce-motion');
    }
  }

  private static setupSystemThemeListener(): void {
    const mediaQuery = window.matchMedia('(prefers-color-scheme: dark)');
    
    const handleChange = (e: MediaQueryListEvent) => {
      if (this.config.theme === 'system') {
        this.applyTheme();
      }
    };
    
    // Store listener reference for cleanup
    (window as any).__themeListener = handleChange;
    mediaQuery.addEventListener('change', handleChange);
  }

  private static removeSystemThemeListener(): void {
    const mediaQuery = window.matchMedia('(prefers-color-scheme: dark)');
    const listener = (window as any).__themeListener;
    
    if (listener) {
      mediaQuery.removeEventListener('change', listener);
      delete (window as any).__themeListener;
    }
  }

  private static loadConfig(): ThemeConfig | null {
    try {
      const saved = localStorage.getItem(this.STORAGE_KEY);
      if (saved) {
        return JSON.parse(saved);
      }
    } catch (error) {
      console.error('Failed to load theme config:', error);
    }
    return null;
  }

  private static saveConfig(): void {
    try {
      localStorage.setItem(this.STORAGE_KEY, JSON.stringify(this.config));
    } catch (error) {
      console.error('Failed to save theme config:', error);
    }
  }
}