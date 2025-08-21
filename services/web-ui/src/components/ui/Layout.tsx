'use client';

import { ReactNode, useState } from 'react';
import { cn } from '@/lib/utils';

// Container Component
interface ContainerProps {
  children: ReactNode;
  className?: string;
  maxWidth?: 'sm' | 'md' | 'lg' | 'xl' | '2xl' | 'full';
  padding?: 'none' | 'sm' | 'md' | 'lg' | 'xl';
}

export function Container({ 
  children, 
  className = "", 
  maxWidth = 'lg',
  padding = 'md'
}: ContainerProps) {
  const maxWidthClasses = {
    sm: 'max-w-sm',
    md: 'max-w-md',
    lg: 'max-w-lg',
    xl: 'max-w-xl',
    '2xl': 'max-w-2xl',
    full: 'max-w-full'
  };
  
  const paddingClasses = {
    none: '',
    sm: 'px-4 py-2',
    md: 'px-6 py-4',
    lg: 'px-8 py-6',
    xl: 'px-12 py-8'
  };
  
  return (
    <div className={cn(
      "mx-auto",
      maxWidthClasses[maxWidth],
      paddingClasses[padding],
      className
    )}>
      {children}
    </div>
  );
}

// Grid Component
interface GridProps {
  children: ReactNode;
  className?: string;
  cols?: 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 | 10 | 11 | 12;
  gap?: 'none' | 'sm' | 'md' | 'lg' | 'xl';
  responsive?: boolean;
}

export function Grid({ 
  children, 
  className = "", 
  cols = 1,
  gap = 'md',
  responsive = true
}: GridProps) {
  const gapClasses = {
    none: '',
    sm: 'gap-2',
    md: 'gap-4',
    lg: 'gap-6',
    xl: 'gap-8'
  };
  
  const gridCols = responsive 
    ? `grid-cols-1 sm:grid-cols-2 lg:grid-cols-${cols}`
    : `grid-cols-${cols}`;
  
  return (
    <div className={cn(
      "grid",
      gridCols,
      gapClasses[gap],
      className
    )}>
      {children}
    </div>
  );
}

// Flex Component
interface FlexProps {
  children: ReactNode;
  className?: string;
  direction?: 'row' | 'col' | 'row-reverse' | 'col-reverse';
  justify?: 'start' | 'end' | 'center' | 'between' | 'around' | 'evenly';
  align?: 'start' | 'end' | 'center' | 'baseline' | 'stretch';
  wrap?: 'wrap' | 'wrap-reverse' | 'nowrap';
  gap?: 'none' | 'sm' | 'md' | 'lg' | 'xl';
}

export function Flex({ 
  children, 
  className = "", 
  direction = 'row',
  justify = 'start',
  align = 'start',
  wrap = 'nowrap',
  gap = 'none'
}: FlexProps) {
  const gapClasses = {
    none: '',
    sm: 'gap-2',
    md: 'gap-4',
    lg: 'gap-6',
    xl: 'gap-8'
  };
  
  return (
    <div className={cn(
      "flex",
      `flex-${direction}`,
      `justify-${justify}`,
      `items-${align}`,
      `flex-${wrap}`,
      gapClasses[gap],
      className
    )}>
      {children}
    </div>
  );
}

// Stack Component
interface StackProps {
  children: ReactNode;
  className?: string;
  direction?: 'vertical' | 'horizontal';
  spacing?: 'none' | 'sm' | 'md' | 'lg' | 'xl';
  align?: 'start' | 'center' | 'end' | 'stretch';
}

export function Stack({ 
  children, 
  className = "", 
  direction = 'vertical',
  spacing = 'md',
  align = 'stretch'
}: StackProps) {
  const spacingClasses = {
    none: '',
    sm: 'space-y-2',
    md: 'space-y-4',
    lg: 'space-y-6',
    xl: 'space-y-8'
  };
  
  const horizontalSpacingClasses = {
    none: '',
    sm: 'space-x-2',
    md: 'space-x-4',
    lg: 'space-x-6',
    xl: 'space-x-8'
  };
  
  return (
    <div className={cn(
      direction === 'vertical' ? spacingClasses[spacing] : horizontalSpacingClasses[spacing],
      `items-${align}`,
      direction === 'horizontal' && 'flex',
      className
    )}>
      {children}
    </div>
  );
}

// Section Component
interface SectionProps {
  children: ReactNode;
  className?: string;
  padding?: 'none' | 'sm' | 'md' | 'lg' | 'xl';
  background?: 'none' | 'white' | 'gray' | 'op-blue';
  border?: 'none' | 'top' | 'bottom' | 'both';
}

export function Section({ 
  children, 
  className = "", 
  padding = 'md',
  background = 'none',
  border = 'none'
}: SectionProps) {
  const paddingClasses = {
    none: '',
    sm: 'py-4',
    md: 'py-8',
    lg: 'py-12',
    xl: 'py-16'
  };
  
  const backgroundClasses = {
    none: '',
    white: 'bg-white',
    gray: 'bg-gray-50',
    'op-blue': 'bg-op-blue-50'
  };
  
  const borderClasses = {
    none: '',
    top: 'border-t border-gray-200',
    bottom: 'border-b border-gray-200',
    both: 'border-y border-gray-200'
  };
  
  return (
    <section className={cn(
      paddingClasses[padding],
      backgroundClasses[background],
      borderClasses[border],
      className
    )}>
      {children}
    </section>
  );
}

// Card Component
interface CardProps {
  children: ReactNode;
  className?: string;
  padding?: 'none' | 'sm' | 'md' | 'lg' | 'xl';
  shadow?: 'none' | 'sm' | 'md' | 'lg' | 'xl';
  border?: boolean;
  hover?: boolean;
}

export function Card({ 
  children, 
  className = "", 
  padding = 'md',
  shadow = 'sm',
  border = true,
  hover = false
}: CardProps) {
  const paddingClasses = {
    none: '',
    sm: 'p-3',
    md: 'p-6',
    lg: 'p-8',
    xl: 'p-10'
  };
  
  const shadowClasses = {
    none: '',
    sm: 'shadow-sm',
    md: 'shadow',
    lg: 'shadow-lg',
    xl: 'shadow-xl'
  };
  
  return (
    <div className={cn(
      "bg-white rounded-lg",
      paddingClasses[padding],
      shadowClasses[shadow],
      border && "border border-gray-200",
      hover && "hover:shadow-md transition-shadow duration-200",
      className
    )}>
      {children}
    </div>
  );
}

// Header Component
interface HeaderProps {
  children: ReactNode;
  className?: string;
  level?: 1 | 2 | 3 | 4 | 5 | 6;
  size?: 'sm' | 'md' | 'lg' | 'xl' | '2xl' | '3xl';
  color?: 'default' | 'muted' | 'primary';
}

export function Header({ 
  children, 
  className = "", 
  level = 1,
  size = 'lg',
  color = 'default'
}: HeaderProps) {
  const sizeClasses = {
    sm: 'text-sm',
    md: 'text-base',
    lg: 'text-lg',
    xl: 'text-xl',
    '2xl': 'text-2xl',
    '3xl': 'text-3xl'
  };
  
  const colorClasses = {
    default: 'text-gray-900',
    muted: 'text-gray-600',
    primary: 'text-op-blue'
  };
  
  const Component = `h${level}` as keyof JSX.IntrinsicElements;
  
  return (
    <Component className={cn(
      "font-semibold leading-tight",
      sizeClasses[size],
      colorClasses[color],
      className
    )}>
      {children}
    </Component>
  );
}

// Divider Component
interface DividerProps {
  className?: string;
  orientation?: 'horizontal' | 'vertical';
  size?: 'sm' | 'md' | 'lg';
  color?: 'default' | 'light' | 'dark';
}

export function Divider({ 
  className = "", 
  orientation = 'horizontal',
  size = 'md',
  color = 'default'
}: DividerProps) {
  const sizeClasses = {
    sm: orientation === 'horizontal' ? 'h-px' : 'w-px',
    md: orientation === 'horizontal' ? 'h-0.5' : 'w-0.5',
    lg: orientation === 'horizontal' ? 'h-1' : 'w-1'
  };
  
  const colorClasses = {
    default: 'bg-gray-200',
    light: 'bg-gray-100',
    dark: 'bg-gray-300'
  };
  
  return (
    <div className={cn(
      sizeClasses[size],
      colorClasses[color],
      orientation === 'vertical' ? 'mx-2' : 'my-2',
      className
    )} />
  );
}

// Spacer Component
interface SpacerProps {
  size?: 'xs' | 'sm' | 'md' | 'lg' | 'xl' | '2xl';
  axis?: 'horizontal' | 'vertical';
  className?: string;
}

export function Spacer({ 
  size = 'md', 
  axis = 'vertical',
  className = "" 
}: SpacerProps) {
  const sizeClasses = {
    xs: '4',
    sm: '8',
    md: '16',
    lg: '24',
    xl: '32',
    '2xl': '48'
  };
  
  const spacing = sizeClasses[size];
  
  return (
    <div className={cn(
      axis === 'vertical' ? `h-${spacing}` : `w-${spacing}`,
      className
    )} />
  );
}

// Aspect Ratio Component
interface AspectRatioProps {
  children: ReactNode;
  ratio?: 'square' | 'video' | 'wide' | 'ultrawide' | 'custom';
  customRatio?: number; // width / height
  className?: string;
}

export function AspectRatio({ 
  children, 
  ratio = 'video',
  customRatio,
  className = "" 
}: AspectRatioProps) {
  const ratioClasses = {
    square: 'aspect-square',
    video: 'aspect-video',
    wide: 'aspect-[21/9]',
    ultrawide: 'aspect-[32/9]',
    custom: customRatio ? `aspect-[${customRatio}/1]` : 'aspect-video'
  };
  
  return (
    <div className={cn(
      "relative overflow-hidden",
      ratioClasses[ratio],
      className
    )}>
      {children}
    </div>
  );
}

// Responsive Container Component
interface ResponsiveContainerProps {
  children: ReactNode;
  className?: string;
  breakpoints?: {
    sm?: string;
    md?: string;
    lg?: string;
    xl?: string;
    '2xl'?: string;
  };
}

export function ResponsiveContainer({ 
  children, 
  className = "",
  breakpoints = {}
}: ResponsiveContainerProps) {
  const defaultBreakpoints = {
    sm: 'max-w-sm',
    md: 'max-w-md',
    lg: 'max-w-lg',
    xl: 'max-w-xl',
    '2xl': 'max-w-2xl'
  };
  
  const responsiveClasses = Object.entries({ ...defaultBreakpoints, ...breakpoints })
    .map(([breakpoint, maxWidth]) => `${breakpoint}:${maxWidth}`)
    .join(' ');
  
  return (
    <div className={cn(
      "mx-auto px-4 sm:px-6 lg:px-8",
      responsiveClasses,
      className
    )}>
      {children}
    </div>
  );
}

// Sidebar Layout Component
interface SidebarLayoutProps {
  sidebar: ReactNode;
  main: ReactNode;
  className?: string;
  sidebarWidth?: 'sm' | 'md' | 'lg' | 'xl';
  sidebarPosition?: 'left' | 'right';
  collapsible?: boolean;
  defaultCollapsed?: boolean;
}

export function SidebarLayout({ 
  sidebar, 
  main, 
  className = "",
  sidebarWidth = 'lg',
  sidebarPosition = 'left',
  collapsible = false,
  defaultCollapsed = false
}: SidebarLayoutProps) {
  const [isCollapsed, setIsCollapsed] = useState(defaultCollapsed);
  
  const widthClasses = {
    sm: 'w-64',
    md: 'w-72',
    lg: 'w-80',
    xl: 'w-96'
  };
  
  const collapsedWidth = 'w-16';
  
  return (
    <div className={cn(
      "flex min-h-screen",
      sidebarPosition === 'right' && "flex-row-reverse",
      className
    )}>
      {/* Sidebar */}
      <aside className={cn(
        "flex-shrink-0 bg-white border-r border-gray-200 transition-all duration-300",
        isCollapsed ? collapsedWidth : widthClasses[sidebarWidth],
        sidebarPosition === 'right' && "border-l border-r-0"
      )}>
        {collapsible && (
          <button
            onClick={() => setIsCollapsed(!isCollapsed)}
            className="absolute top-4 right-2 p-1 rounded-md hover:bg-gray-100 transition-colors"
          >
            <svg className="h-4 w-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M15 19l-7-7 7-7" />
            </svg>
          </button>
        )}
        
        <div className={cn(
          "h-full overflow-y-auto",
          isCollapsed ? "px-2" : "px-4"
        )}>
          {sidebar}
        </div>
      </aside>
      
      {/* Main Content */}
      <main className="flex-1 overflow-y-auto">
        {main}
      </main>
    </div>
  );
}

// Two Column Layout Component
interface TwoColumnLayoutProps {
  left: ReactNode;
  right: ReactNode;
  className?: string;
  leftWidth?: '1/3' | '1/2' | '2/3' | '3/4';
  gap?: 'none' | 'sm' | 'md' | 'lg' | 'xl';
  responsive?: boolean;
}

export function TwoColumnLayout({ 
  left, 
  right, 
  className = "",
  leftWidth = '1/2',
  gap = 'lg',
  responsive = true
}: TwoColumnLayoutProps) {
  const gapClasses = {
    none: '',
    sm: 'gap-4',
    md: 'gap-6',
    lg: 'gap-8',
    xl: 'gap-12'
  };
  
  const responsiveClasses = responsive 
    ? 'flex-col lg:flex-row'
    : 'flex-row';
  
  return (
    <div className={cn(
      "flex",
      responsiveClasses,
      gapClasses[gap],
      className
    )}>
      <div className={cn(
        responsive ? 'w-full lg:w-1/2' : `w-${leftWidth}`,
        leftWidth === '1/3' && 'lg:w-1/3',
        leftWidth === '1/2' && 'lg:w-1/2',
        leftWidth === '2/3' && 'lg:w-2/3',
        leftWidth === '3/4' && 'lg:w-3/4'
      )}>
        {left}
      </div>
      
      <div className={cn(
        responsive ? 'w-full lg:w-1/2' : 'flex-1',
        leftWidth === '1/3' && 'lg:w-2/3',
        leftWidth === '1/2' && 'lg:w-1/2',
        leftWidth === '2/3' && 'lg:w-1/3',
        leftWidth === '3/4' && 'lg:w-1/4'
      )}>
        {right}
      </div>
    </div>
  );
}

// Page Header Component
interface PageHeaderProps {
  title: string;
  subtitle?: string;
  actions?: ReactNode;
  breadcrumbs?: ReactNode;
  className?: string;
}

export function PageHeader({ 
  title, 
  subtitle, 
  actions, 
  breadcrumbs,
  className = "" 
}: PageHeaderProps) {
  return (
    <div className={cn("mb-8", className)}>
      {breadcrumbs && (
        <nav className="mb-4">
          {breadcrumbs}
        </nav>
      )}
      
      <div className="flex items-start justify-between">
        <div className="flex-1">
          <Header level={1} size="3xl" className="mb-2">
            {title}
          </Header>
          
          {subtitle && (
            <p className="text-lg text-gray-600 max-w-3xl">
              {subtitle}
            </p>
          )}
        </div>
        
        {actions && (
          <div className="flex items-center space-x-3">
            {actions}
          </div>
        )}
      </div>
    </div>
  );
}

// Content Container Component
interface ContentContainerProps {
  children: ReactNode;
  className?: string;
  maxWidth?: 'sm' | 'md' | 'lg' | 'xl' | '2xl' | 'full';
  padding?: 'none' | 'sm' | 'md' | 'lg' | 'xl';
  centered?: boolean;
}

export function ContentContainer({ 
  children, 
  className = "", 
  maxWidth = 'lg',
  padding = 'md',
  centered = true
}: ContentContainerProps) {
  const maxWidthClasses = {
    sm: 'max-w-sm',
    md: 'max-w-md',
    lg: 'max-w-lg',
    xl: 'max-w-xl',
    '2xl': 'max-w-2xl',
    full: 'max-w-full'
  };
  
  const paddingClasses = {
    none: '',
    sm: 'px-4 py-2',
    md: 'px-6 py-4',
    lg: 'px-8 py-6',
    xl: 'px-12 py-8'
  };
  
  return (
    <div className={cn(
      centered && "mx-auto",
      maxWidthClasses[maxWidth],
      paddingClasses[padding],
      className
    )}>
      {children}
    </div>
  );
}
