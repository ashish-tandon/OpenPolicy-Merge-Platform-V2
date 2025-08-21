'use client';

import { ReactNode, useState, useEffect, useRef } from 'react';
import { motion, AnimatePresence, Variants } from 'framer-motion';

// Utility function for combining class names
const cn = (...classes: (string | undefined | null | false)[]) => {
  return classes.filter(Boolean).join(' ');
};

// Fade In Component
interface FadeInProps {
  children: ReactNode;
  delay?: number;
  duration?: number;
  direction?: 'up' | 'down' | 'left' | 'right' | 'none';
  className?: string;
  once?: boolean;
}

export function FadeIn({
  children,
  delay = 0,
  duration = 0.5,
  direction = 'none',
  className = "",
  once = true
}: FadeInProps) {
  const getVariants = (): Variants => {
    const baseVariants: Variants = {
      hidden: { opacity: 0 },
      visible: { opacity: 1 }
    };

    if (direction === 'up') {
      return {
        hidden: { opacity: 0, y: 20 },
        visible: { opacity: 1, y: 0 }
      };
    } else if (direction === 'down') {
      return {
        hidden: { opacity: 0, y: -20 },
        visible: { opacity: 1, y: 0 }
      };
    } else if (direction === 'left') {
      return {
        hidden: { opacity: 0, x: 20 },
        visible: { opacity: 1, x: 0 }
      };
    } else if (direction === 'right') {
      return {
        hidden: { opacity: 0, x: -20 },
        visible: { opacity: 1, x: 0 }
      };
    }

    return baseVariants;
  };

  return (
    <motion.div
      initial="hidden"
      whileInView="visible"
      viewport={{ once }}
      variants={getVariants()}
      transition={{ duration, delay }}
      className={className}
    >
      {children}
    </motion.div>
  );
}

// Slide In Component
interface SlideInProps {
  children: ReactNode;
  direction?: 'up' | 'down' | 'left' | 'right';
  distance?: number;
  delay?: number;
  duration?: number;
  className?: string;
  once?: boolean;
}

export function SlideIn({
  children,
  direction = 'up',
  distance = 50,
  delay = 0,
  duration = 0.5,
  className = "",
  once = true
}: SlideInProps) {
  const getVariants = (): Variants => {
    const variants: Variants = {
      hidden: { opacity: 0 },
      visible: { opacity: 1 }
    };

    if (direction === 'up') {
      variants.hidden.y = distance;
      variants.visible.y = 0;
    } else if (direction === 'down') {
      variants.hidden.y = -distance;
      variants.visible.y = 0;
    } else if (direction === 'left') {
      variants.hidden.x = distance;
      variants.visible.x = 0;
    } else if (direction === 'right') {
      variants.hidden.x = -distance;
      variants.visible.x = 0;
    }

    return variants;
  };

  return (
    <motion.div
      initial="hidden"
      whileInView="visible"
      viewport={{ once }}
      variants={getVariants()}
      transition={{ duration, delay, ease: "easeOut" }}
      className={className}
    >
      {children}
    </motion.div>
  );
}

// Scale In Component
interface ScaleInProps {
  children: ReactNode;
  scale?: number;
  delay?: number;
  duration?: number;
  className?: string;
  once?: boolean;
}

export function ScaleIn({
  children,
  scale = 0.8,
  delay = 0,
  duration = 0.5,
  className = "",
  once = true
}: ScaleInProps) {
  return (
    <motion.div
      initial={{ opacity: 0, scale }}
      whileInView={{ opacity: 1, scale: 1 }}
      viewport={{ once }}
      transition={{ duration, delay, ease: "easeOut" }}
      className={className}
    >
      {children}
    </motion.div>
  );
}

// Rotate In Component
interface RotateInProps {
  children: ReactNode;
  angle?: number;
  delay?: number;
  duration?: number;
  className?: string;
  once?: boolean;
}

export function RotateIn({
  children,
  angle = 180,
  delay = 0,
  duration = 0.5,
  className = "",
  once = true
}: RotateInProps) {
  return (
    <motion.div
      initial={{ opacity: 0, rotate: angle }}
      whileInView={{ opacity: 1, rotate: 0 }}
      viewport={{ once }}
      transition={{ duration, delay, ease: "easeOut" }}
      className={className}
    >
      {children}
    </motion.div>
  );
}

// Stagger Container Component
interface StaggerContainerProps {
  children: ReactNode;
  staggerDelay?: number;
  className?: string;
  once?: boolean;
}

export function StaggerContainer({
  children,
  staggerDelay = 0.1,
  className = "",
  once = true
}: StaggerContainerProps) {
  const containerVariants: Variants = {
    hidden: { opacity: 0 },
    visible: {
      opacity: 1,
      transition: {
        staggerChildren: staggerDelay
      }
    }
  };

  const itemVariants: Variants = {
    hidden: { opacity: 0, y: 20 },
    visible: { opacity: 1, y: 0 }
  };

  return (
    <motion.div
      initial="hidden"
      whileInView="visible"
      viewport={{ once }}
      variants={containerVariants}
      className={className}
    >
      {Array.isArray(children) ? (
        children.map((child, index) => (
          <motion.div key={index} variants={itemVariants}>
            {child}
          </motion.div>
        ))
      ) : (
        <motion.div variants={itemVariants}>
          {children}
        </motion.div>
      )}
    </motion.div>
  );
}

// Parallax Component
interface ParallaxProps {
  children: ReactNode;
  speed?: number;
  className?: string;
}

export function Parallax({
  children,
  speed = 0.5,
  className = ""
}: ParallaxProps) {
  const [offset, setOffset] = useState(0);
  const ref = useRef<HTMLDivElement>(null);

  useEffect(() => {
    const handleScroll = () => {
      if (ref.current) {
        const rect = ref.current.getBoundingClientRect();
        const scrolled = window.pageYOffset;
        const rate = scrolled * -speed;
        setOffset(rate);
      }
    };

    window.addEventListener('scroll', handleScroll);
    return () => window.removeEventListener('scroll', handleScroll);
  }, [speed]);

  return (
    <div ref={ref} className={cn("relative overflow-hidden", className)}>
      <motion.div
        style={{ y: offset }}
        className="relative"
      >
        {children}
      </motion.div>
    </div>
  );
}

// Hover Lift Component
interface HoverLiftProps {
  children: ReactNode;
  lift?: number;
  scale?: number;
  className?: string;
}

export function HoverLift({
  children,
  lift = -8,
  scale = 1.02,
  className = ""
}: HoverLiftProps) {
  return (
    <motion.div
      whileHover={{ y: lift, scale }}
      transition={{ duration: 0.2, ease: "easeOut" }}
      className={className}
    >
      {children}
    </motion.div>
  );
}

// Pulse Component
interface PulseProps {
  children: ReactNode;
  duration?: number;
  className?: string;
}

export function Pulse({
  children,
  duration = 2,
  className = ""
}: PulseProps) {
  return (
    <motion.div
      animate={{ scale: [1, 1.05, 1] }}
      transition={{ duration, repeat: Infinity, ease: "easeInOut" }}
      className={className}
    >
      {children}
    </motion.div>
  );
}

// Bounce Component
interface BounceProps {
  children: ReactNode;
  duration?: number;
  className?: string;
}

export function Bounce({
  children,
  duration = 1,
  className = ""
}: BounceProps) {
  return (
    <motion.div
      animate={{ y: [0, -10, 0] }}
      transition={{ duration, repeat: Infinity, ease: "easeInOut" }}
      className={className}
    >
      {children}
    </motion.div>
  );
}

// Shake Component
interface ShakeProps {
  children: ReactNode;
  duration?: number;
  className?: string;
}

export function Shake({
  children,
  duration = 0.5,
  className = ""
}: ShakeProps) {
  return (
    <motion.div
      animate={{ x: [0, -5, 5, -5, 5, 0] }}
      transition={{ duration, repeat: Infinity, ease: "easeInOut" }}
      className={className}
    >
      {children}
    </motion.div>
  );
}

// Flip Component
interface FlipProps {
  children: ReactNode;
  isFlipped?: boolean;
  duration?: number;
  className?: string;
}

export function Flip({
  children,
  isFlipped = false,
  duration = 0.6,
  className = ""
}: FlipProps) {
  return (
    <motion.div
      animate={{ rotateY: isFlipped ? 180 : 0 }}
      transition={{ duration, ease: "easeInOut" }}
      className={cn("transform-style-preserve-3d", className)}
    >
      {children}
    </motion.div>
  );
}

// Typewriter Component
interface TypewriterProps {
  text: string;
  speed?: number;
  delay?: number;
  className?: string;
  onComplete?: () => void;
}

export function Typewriter({
  text,
  speed = 50,
  delay = 0,
  className = "",
  onComplete
}: TypewriterProps) {
  const [displayText, setDisplayText] = useState('');
  const [currentIndex, setCurrentIndex] = useState(0);

  useEffect(() => {
    if (delay > 0) {
      const timer = setTimeout(() => {
        setCurrentIndex(0);
      }, delay);
      return () => clearTimeout(timer);
    } else {
      setCurrentIndex(0);
    }
  }, [delay, text]);

  useEffect(() => {
    if (currentIndex < text.length) {
      const timer = setTimeout(() => {
        setDisplayText(text.slice(0, currentIndex + 1));
        setCurrentIndex(currentIndex + 1);
      }, speed);

      return () => clearTimeout(timer);
    } else if (onComplete) {
      onComplete();
    }
  }, [currentIndex, text, speed, onComplete]);

  return (
    <span className={className}>
      {displayText}
      <motion.span
        animate={{ opacity: [1, 0] }}
        transition={{ duration: 0.5, repeat: Infinity }}
        className="inline-block w-0.5 h-4 bg-current ml-1"
      />
    </span>
  );
}

// Counter Component
interface CounterProps {
  end: number;
  start?: number;
  duration?: number;
  delay?: number;
  className?: string;
  prefix?: string;
  suffix?: string;
  onComplete?: () => void;
}

export function Counter({
  end,
  start = 0,
  duration = 2,
  delay = 0,
  className = "",
  prefix = "",
  suffix = "",
  onComplete
}: CounterProps) {
  const [count, setCount] = useState(start);

  useEffect(() => {
    const timer = setTimeout(() => {
      const increment = (end - start) / (duration * 60); // 60fps
      let current = start;

      const counter = setInterval(() => {
        current += increment;
        if (current >= end) {
          setCount(end);
          clearInterval(counter);
          onComplete?.();
        } else {
          setCount(Math.floor(current));
        }
      }, 1000 / 60);

      return () => clearInterval(counter);
    }, delay * 1000);

    return () => clearTimeout(timer);
  }, [end, start, duration, delay, onComplete]);

  return (
    <span className={className}>
      {prefix}{count}{suffix}
    </span>
  );
}

// Loading Spinner Component
interface LoadingSpinnerProps {
  size?: 'sm' | 'md' | 'lg';
  color?: 'blue' | 'green' | 'red' | 'yellow' | 'purple' | 'gray';
  className?: string;
}

export function LoadingSpinner({
  size = 'md',
  color = 'blue',
  className = ""
}: LoadingSpinnerProps) {
  const sizeClasses = {
    sm: 'h-4 w-4',
    md: 'h-8 w-8',
    lg: 'h-12 w-12'
  };

  const colorClasses = {
    blue: 'border-op-blue',
    green: 'border-green-500',
    red: 'border-red-500',
    yellow: 'border-yellow-500',
    purple: 'border-purple-500',
    gray: 'border-gray-500'
  };

  return (
    <motion.div
      animate={{ rotate: 360 }}
      transition={{ duration: 1, repeat: Infinity, ease: "linear" }}
      className={cn(
        "border-2 border-t-transparent rounded-full",
        sizeClasses[size],
        colorClasses[color],
        className
      )}
    />
  );
}

// Progress Ring Component
interface ProgressRingProps {
  progress: number;
  size?: number;
  strokeWidth?: number;
  color?: 'blue' | 'green' | 'red' | 'yellow' | 'purple';
  className?: string;
}

export function ProgressRing({
  progress,
  size = 120,
  strokeWidth = 8,
  color = 'blue',
  className = ""
}: ProgressRingProps) {
  const radius = (size - strokeWidth) / 2;
  const circumference = radius * 2 * Math.PI;
  const strokeDasharray = circumference;
  const strokeDashoffset = circumference - (progress / 100) * circumference;

  const colorClasses = {
    blue: 'stroke-op-blue',
    green: 'stroke-green-500',
    red: 'stroke-red-500',
    yellow: 'stroke-yellow-500',
    purple: 'stroke-purple-500'
  };

  return (
    <div className={cn("relative inline-flex items-center justify-center", className)}>
      <svg
        width={size}
        height={size}
        className="transform -rotate-90"
      >
        <circle
          cx={size / 2}
          cy={size / 2}
          r={radius}
          stroke="currentColor"
          strokeWidth={strokeWidth}
          fill="transparent"
          className="text-gray-200"
        />
        <motion.circle
          cx={size / 2}
          cy={size / 2}
          r={radius}
          stroke="currentColor"
          strokeWidth={strokeWidth}
          fill="transparent"
          className={colorClasses[color]}
          strokeDasharray={strokeDasharray}
          initial={{ strokeDashoffset: circumference }}
          animate={{ strokeDashoffset }}
          transition={{ duration: 1, ease: "easeInOut" }}
        />
      </svg>
      <div className="absolute text-center">
        <span className="text-2xl font-bold text-gray-900">{Math.round(progress)}%</span>
      </div>
    </div>
  );
}

// Animated List Component
interface AnimatedListProps {
  items: ReactNode[];
  staggerDelay?: number;
  className?: string;
  itemClassName?: string;
}

export function AnimatedList({
  items,
  staggerDelay = 0.1,
  className = "",
  itemClassName = ""
}: AnimatedListProps) {
  const containerVariants: Variants = {
    hidden: { opacity: 0 },
    visible: {
      opacity: 1,
      transition: {
        staggerChildren: staggerDelay
      }
    }
  };

  const itemVariants: Variants = {
    hidden: { opacity: 0, x: -20 },
    visible: { opacity: 1, x: 0 }
  };

  return (
    <motion.div
      initial="hidden"
      animate="visible"
      variants={containerVariants}
      className={className}
    >
      {items.map((item, index) => (
        <motion.div
          key={index}
          variants={itemVariants}
          className={itemClassName}
        >
          {item}
        </motion.div>
      ))}
    </motion.div>
  );
}

// Animated Tabs Component
interface AnimatedTabsProps {
  tabs: { id: string; label: string; content: ReactNode }[];
  activeTab: string;
  onTabChange: (tabId: string) => void;
  className?: string;
}

export function AnimatedTabs({
  tabs,
  activeTab,
  onTabChange,
  className = ""
}: AnimatedTabsProps) {
  return (
    <div className={className}>
      {/* Tab Headers */}
      <div className="flex border-b border-gray-200">
        {tabs.map((tab) => (
          <button
            key={tab.id}
            onClick={() => onTabChange(tab.id)}
            className={cn(
              "px-4 py-2 text-sm font-medium border-b-2 transition-colors",
              activeTab === tab.id
                ? "border-op-blue text-op-blue"
                : "border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300"
            )}
          >
            {tab.label}
          </button>
        ))}
      </div>

      {/* Tab Content */}
      <div className="mt-4">
        <AnimatePresence mode="wait">
          {tabs.map((tab) => (
            activeTab === tab.id && (
              <motion.div
                key={tab.id}
                initial={{ opacity: 0, y: 10 }}
                animate={{ opacity: 1, y: 0 }}
                exit={{ opacity: 0, y: -10 }}
                transition={{ duration: 0.2 }}
              >
                {tab.content}
              </motion.div>
            )
          ))}
        </AnimatePresence>
      </div>
    </div>
  );
}
