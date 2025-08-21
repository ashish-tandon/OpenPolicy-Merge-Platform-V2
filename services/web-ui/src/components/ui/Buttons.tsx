'use client';

import { ReactNode, forwardRef } from 'react';
import { cn } from '@/lib/utils';
import { useState } from 'react';

// Button Variants
const buttonVariants = {
  primary: "bg-op-blue text-white hover:bg-op-blue-700 focus:ring-op-blue",
  secondary: "bg-gray-100 text-gray-900 hover:bg-gray-200 focus:ring-gray-500",
  success: "bg-green-600 text-white hover:bg-green-700 focus:ring-green-500",
  danger: "bg-red-600 text-white hover:bg-red-700 focus:ring-red-500",
  warning: "bg-yellow-600 text-white hover:bg-yellow-700 focus:ring-yellow-500",
  info: "bg-blue-600 text-white hover:bg-blue-700 focus:ring-blue-500",
  outline: "border border-gray-300 bg-white text-gray-700 hover:bg-gray-50 focus:ring-op-blue",
  ghost: "text-gray-700 hover:bg-gray-100 focus:ring-gray-500",
  link: "text-op-blue hover:text-op-blue-700 underline-offset-4 hover:underline focus:ring-op-blue"
};

// Button Sizes
const buttonSizes = {
  xs: "px-2 py-1 text-xs",
  sm: "px-3 py-1.5 text-sm",
  md: "px-4 py-2 text-sm",
  lg: "px-6 py-3 text-base",
  xl: "px-8 py-4 text-lg"
};

// Base Button Component
interface BaseButtonProps extends React.ButtonHTMLAttributes<HTMLButtonElement> {
  variant?: keyof typeof buttonVariants;
  size?: keyof typeof buttonSizes;
  loading?: boolean;
  leftIcon?: ReactNode;
  rightIcon?: ReactNode;
  fullWidth?: boolean;
  children: ReactNode;
}

export const BaseButton = forwardRef<HTMLButtonElement, BaseButtonProps>(
  ({ 
    variant = 'primary',
    size = 'md',
    loading = false,
    leftIcon,
    rightIcon,
    fullWidth = false,
    className = "",
    disabled,
    children,
    ...props 
  }, ref) => {
    const isDisabled = disabled || loading;
    
    return (
      <button
        ref={ref}
        disabled={isDisabled}
        className={cn(
          "inline-flex items-center justify-center font-medium rounded-md transition-all duration-200 focus:outline-none focus:ring-2 focus:ring-offset-2 disabled:opacity-50 disabled:cursor-not-allowed",
          buttonVariants[variant],
          buttonSizes[size],
          fullWidth && "w-full",
          className
        )}
        {...props}
      >
        {loading && (
          <svg className="animate-spin -ml-1 mr-2 h-4 w-4" fill="none" viewBox="0 0 24 24">
            <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4" />
            <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z" />
          </svg>
        )}
        
        {!loading && leftIcon && (
          <span className={cn("mr-2", size === 'xs' ? "h-3 w-3" : size === 'sm' ? "h-4 w-4" : "h-5 w-5")}>
            {leftIcon}
          </span>
        )}
        
        {children}
        
        {!loading && rightIcon && (
          <span className={cn("ml-2", size === 'xs' ? "h-3 w-3" : size === 'sm' ? "h-4 w-4" : "h-5 w-5")}>
            {rightIcon}
          </span>
        )}
      </button>
    );
  }
);

BaseButton.displayName = 'BaseButton';

// Primary Button
export const Button = forwardRef<HTMLButtonElement, Omit<BaseButtonProps, 'variant'>>(
  (props, ref) => {
    return <BaseButton ref={ref} variant="primary" {...props} />;
  }
);

Button.displayName = 'Button';

// Secondary Button
export const SecondaryButton = forwardRef<HTMLButtonElement, Omit<BaseButtonProps, 'variant'>>(
  (props, ref) => {
    return <BaseButton ref={ref} variant="secondary" {...props} />;
  }
);

SecondaryButton.displayName = 'SecondaryButton';

// Success Button
export const SuccessButton = forwardRef<HTMLButtonElement, Omit<BaseButtonProps, 'variant'>>(
  (props, ref) => {
    return <BaseButton ref={ref} variant="success" {...props} />;
  }
);

SuccessButton.displayName = 'SuccessButton';

// Danger Button
export const DangerButton = forwardRef<HTMLButtonElement, Omit<BaseButtonProps, 'variant'>>(
  (props, ref) => {
    return <BaseButton ref={ref} variant="danger" {...props} />;
  }
);

DangerButton.displayName = 'DangerButton';

// Warning Button
export const WarningButton = forwardRef<HTMLButtonElement, Omit<BaseButtonProps, 'variant'>>(
  (props, ref) => {
    return <BaseButton ref={ref} variant="warning" {...props} />;
  }
);

WarningButton.displayName = 'WarningButton';

// Info Button
export const InfoButton = forwardRef<HTMLButtonElement, Omit<BaseButtonProps, 'variant'>>(
  (props, ref) => {
    return <BaseButton ref={ref} variant="info" {...props} />;
  }
);

InfoButton.displayName = 'InfoButton';

// Outline Button
export const OutlineButton = forwardRef<HTMLButtonElement, Omit<BaseButtonProps, 'variant'>>(
  (props, ref) => {
    return <BaseButton ref={ref} variant="outline" {...props} />;
  }
);

OutlineButton.displayName = 'OutlineButton';

// Ghost Button
export const GhostButton = forwardRef<HTMLButtonElement, Omit<BaseButtonProps, 'variant'>>(
  (props, ref) => {
    return <BaseButton ref={ref} variant="ghost" {...props} />;
  }
);

GhostButton.displayName = 'GhostButton';

// Link Button
export const LinkButton = forwardRef<HTMLButtonElement, Omit<BaseButtonProps, 'variant'>>(
  (props, ref) => {
    return <BaseButton ref={ref} variant="link" {...props} />;
  }
);

LinkButton.displayName = 'LinkButton';

// Icon Button Component
interface IconButtonProps extends Omit<BaseButtonProps, 'children' | 'leftIcon' | 'rightIcon'> {
  icon: ReactNode;
  label?: string;
  tooltip?: string;
}

export const IconButton = forwardRef<HTMLButtonElement, IconButtonProps>(
  ({ 
    icon, 
    label, 
    tooltip, 
    size = 'md',
    variant = 'ghost',
    className = "",
    ...props 
  }, ref) => {
    const iconSizes = {
      xs: "h-4 w-4",
      sm: "h-5 w-5",
      md: "h-6 w-6",
      lg: "h-7 w-7",
      xl: "h-8 w-8"
    };
    
    const buttonSizes = {
      xs: "p-1",
      sm: "p-1.5",
      md: "p-2",
      lg: "p-2.5",
      xl: "p-3"
    };
    
    return (
      <button
        ref={ref}
        className={cn(
          "inline-flex items-center justify-center rounded-md transition-all duration-200 focus:outline-none focus:ring-2 focus:ring-offset-2 disabled:opacity-50 disabled:cursor-not-allowed",
          buttonVariants[variant],
          buttonSizes[size],
          className
        )}
        aria-label={label}
        title={tooltip}
        {...props}
      >
        <span className={iconSizes[size]}>
          {icon}
        </span>
      </button>
    );
  }
);

IconButton.displayName = 'IconButton';

// Button Group Component
interface ButtonGroupProps {
  children: ReactNode;
  className?: string;
  vertical?: boolean;
}

export function ButtonGroup({ children, className = "", vertical = false }: ButtonGroupProps) {
  return (
    <div className={cn(
      "inline-flex",
      vertical ? "flex-col" : "flex-row",
      className
    )}>
      {children}
    </div>
  );
}

// Button Group Item Component
interface ButtonGroupItemProps extends BaseButtonProps {
  isFirst?: boolean;
  isLast?: boolean;
  isMiddle?: boolean;
}

export const ButtonGroupItem = forwardRef<HTMLButtonElement, ButtonGroupItemProps>(
  ({ 
    isFirst = false, 
    isLast = false, 
    isMiddle = false,
    className = "",
    ...props 
  }, ref) => {
    return (
      <BaseButton
        ref={ref}
        className={cn(
          "rounded-none",
          isFirst && "rounded-l-md",
          isLast && "rounded-r-md",
          !isFirst && !isLast && !isMiddle && "rounded-none",
          isMiddle && "rounded-none",
          className
        )}
        {...props}
      />
    );
  }
);

ButtonGroupItem.displayName = 'ButtonGroupItem';

// Loading Button Component
interface LoadingButtonProps extends Omit<BaseButtonProps, 'loading'> {
  loadingText?: string;
  children: ReactNode;
}

export const LoadingButton = forwardRef<HTMLButtonElement, LoadingButtonProps>(
  ({ 
    loadingText, 
    children, 
    ...props 
  }, ref) => {
    const [isLoading, setIsLoading] = useState(false);
    
    const handleClick = async (e: React.MouseEvent<HTMLButtonElement>) => {
      if (props.onClick) {
        setIsLoading(true);
        try {
          await props.onClick(e);
        } finally {
          setIsLoading(false);
        }
      }
    };
    
    return (
      <BaseButton
        ref={ref}
        loading={isLoading}
        onClick={handleClick}
        {...props}
      >
        {isLoading ? (loadingText || children) : children}
      </BaseButton>
    );
  }
);

LoadingButton.displayName = 'LoadingButton';

// Toggle Button Component
interface ToggleButtonProps extends Omit<BaseButtonProps, 'variant'> {
  pressed?: boolean;
  onPressedChange?: (pressed: boolean) => void;
  children: ReactNode;
}

export const ToggleButton = forwardRef<HTMLButtonElement, ToggleButtonProps>(
  ({ 
    pressed = false, 
    onPressedChange, 
    children, 
    className = "",
    ...props 
  }, ref) => {
    const handleClick = () => {
      onPressedChange?.(!pressed);
    };
    
    return (
      <BaseButton
        ref={ref}
        variant={pressed ? 'primary' : 'outline'}
        onClick={handleClick}
        className={cn(
          pressed && "ring-2 ring-op-blue ring-offset-2",
          className
        )}
        {...props}
      >
        {children}
      </BaseButton>
    );
  }
);

ToggleButton.displayName = 'ToggleButton';

// Social Button Components
interface SocialButtonProps extends Omit<BaseButtonProps, 'variant' | 'leftIcon'> {
  provider: 'google' | 'github' | 'facebook' | 'twitter' | 'linkedin';
  children?: ReactNode;
}

export const SocialButton = forwardRef<HTMLButtonElement, SocialButtonProps>(
  ({ 
    provider, 
    children, 
    className = "",
    ...props 
  }, ref) => {
    const socialConfig = {
      google: {
        icon: (
          <svg className="h-5 w-5" viewBox="0 0 24 24">
            <path fill="#4285F4" d="M22.56 12.25c0-.78-.07-1.53-.2-2.25H12v4.26h5.92c-.26 1.37-1.04 2.53-2.21 3.31v2.77h3.57c2.08-1.92 3.28-4.74 3.28-8.09z"/>
            <path fill="#34A853" d="M12 23c2.97 0 5.46-.98 7.28-2.66l-3.57-2.77c-.98.66-2.23 1.06-3.71 1.06-2.86 0-5.29-1.93-6.16-4.53H2.18v2.84C3.99 20.53 7.7 23 12 23z"/>
            <path fill="#FBBC05" d="M5.84 14.09c-.22-.66-.35-1.36-.35-2.09s.13-1.43.35-2.09V7.07H2.18C1.43 8.55 1 10.22 1 12s.43 3.45 1.18 4.93l2.85-2.22.81-.62z"/>
            <path fill="#EA4335" d="M12 5.38c1.62 0 3.06.56 4.21 1.64l3.15-3.15C17.45 2.09 14.97 1 12 1 7.7 1 3.99 3.47 2.18 7.07l3.66 2.84c.87-2.6 3.3-4.53 6.16-4.53z"/>
          </svg>
        ),
        variant: 'outline' as const,
        text: 'Continue with Google'
      },
      github: {
        icon: (
          <svg className="h-5 w-5" fill="currentColor" viewBox="0 0 24 24">
            <path d="M12 0c-6.626 0-12 5.373-12 12 0 5.302 3.438 9.8 8.207 11.387.599.111.793-.261.793-.577v-2.234c-3.338.726-4.033-1.416-4.033-1.416-.546-1.387-1.333-1.756-1.333-1.756-1.089-.745.083-.729.083-.729 1.205.084 1.839 1.237 1.839 1.237 1.07 1.834 2.807 1.304 3.492.997.107-.775.418-1.305.762-1.604-2.665-.305-5.467-1.334-5.467-5.931 0-1.311.469-2.381 1.236-3.221-.124-.303-.535-1.524.117-3.176 0 0 1.008-.322 3.301 1.23.957-.266 1.983-.399 3.003-.404 1.02.005 2.047.138 3.006.404 2.291-1.552 3.297-1.23 3.297-1.23.653 1.653.242 2.874.118 3.176.77.84 1.235 1.911 1.235 3.221 0 4.609-2.807 5.624-5.479 5.921.43.372.823 1.102.823 2.222v3.293c0 .319.192.694.801.576 4.765-1.589 8.199-6.086 8.199-11.386 0-6.627-5.373-12-12-12z"/>
          </svg>
        ),
        variant: 'primary' as const,
        text: 'Continue with GitHub'
      },
      facebook: {
        icon: (
          <svg className="h-5 w-5" fill="currentColor" viewBox="0 0 24 24">
            <path d="M24 12.073c0-6.627-5.373-12-12-12s-12 5.373-12 12c0 5.99 4.388 10.954 10.125 11.854v-8.385H7.078v-3.47h3.047V9.43c0-3.007 1.792-4.669 4.533-4.669 1.312 0 2.686.235 2.686.235v2.953H15.83c-1.491 0-1.956.925-1.956 1.874v2.25h3.328l-.532 3.47h-2.796v8.385C19.612 23.027 24 18.062 24 12.073z"/>
          </svg>
        ),
        variant: 'primary' as const,
        text: 'Continue with Facebook'
      },
      twitter: {
        icon: (
          <svg className="h-5 w-5" fill="currentColor" viewBox="0 0 24 24">
            <path d="M23.953 4.57a10 10 0 01-2.825.775 4.958 4.958 0 002.163-2.723c-.951.555-2.005.959-3.127 1.184a4.92 4.92 0 00-8.384 4.482C7.69 8.095 4.067 6.13 1.64 3.162a4.822 4.822 0 00-.665 2.475c0 1.71.87 3.213 2.188 4.096a4.904 4.904 0 01-2.228-.616v.06a4.923 4.923 0 003.946 4.827 4.996 4.996 0 01-2.212.085 4.936 4.936 0 004.604 3.417 9.867 9.867 0 01-6.102 2.105c-.39 0-.779-.023-1.17-.067a13.995 13.995 0 007.557 2.209c9.053 0 13.998-7.496 13.998-13.985 0-.21 0-.42-.015-.63A9.935 9.935 0 0024 4.59z"/>
          </svg>
        ),
        variant: 'primary' as const,
        text: 'Continue with Twitter'
      },
      linkedin: {
        icon: (
          <svg className="h-5 w-5" fill="currentColor" viewBox="0 0 24 24">
            <path d="M20.447 20.452h-3.554v-5.569c0-1.328-.027-3.037-1.852-3.037-1.853 0-2.136 1.445-2.136 2.939v5.667H9.351V9h3.414v1.561h.046c.477-.9 1.637-1.85 3.37-1.85 3.601 0 4.267 2.37 4.267 5.455v6.286zM5.337 7.433c-1.144 0-2.063-.926-2.063-2.065 0-1.138.92-2.063 2.063-2.063 1.14 0 2.064.925 2.064 2.063 0 1.139-.925 2.065-2.064 2.065zm1.782 13.019H3.555V9h3.564v11.452zM22.225 0H1.771C.792 0 0 .774 0 1.729v20.542C0 23.227.792 24 1.771 24h20.451C23.2 24 24 23.227 24 22.271V1.729C24 .774 23.2 0 22.222 0h.003z"/>
          </svg>
        ),
        variant: 'primary' as const,
        text: 'Continue with LinkedIn'
      }
    };
    
    const config = socialConfig[provider];
    
    return (
      <BaseButton
        ref={ref}
        variant={config.variant}
        leftIcon={config.icon}
        className={cn("w-full", className)}
        {...props}
      >
        {children || config.text}
      </BaseButton>
    );
  }
);

SocialButton.displayName = 'SocialButton';
