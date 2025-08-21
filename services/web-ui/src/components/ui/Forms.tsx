'use client';

import { ReactNode, useState, useEffect, useRef, forwardRef } from 'react';
import { 
  EyeIcon,
  EyeSlashIcon,
  CheckIcon,
  ExclamationTriangleIcon,
  InformationCircleIcon,
  XMarkIcon,
  ChevronDownIcon,
  CalendarIcon,
  ClockIcon,
  MapPinIcon,
  PhoneIcon,
  EnvelopeIcon,
  UserIcon,
  LockClosedIcon,
  DocumentTextIcon,
  TagIcon,
  CurrencyDollarIcon,
  GlobeAltIcon
} from '@heroicons/react/24/outline';

// Utility function for combining class names
const cn = (...classes: (string | undefined | null | false)[]) => {
  return classes.filter(Boolean).join(' ');
};

// Form Field Types
export interface FormField {
  name: string;
  label: string;
  type: 'text' | 'email' | 'password' | 'number' | 'tel' | 'url' | 'textarea' | 'select' | 'checkbox' | 'radio' | 'date' | 'time' | 'datetime-local' | 'file' | 'search';
  placeholder?: string;
  required?: boolean;
  disabled?: boolean;
  readOnly?: boolean;
  autoComplete?: string;
  autoFocus?: boolean;
  min?: number;
  max?: number;
  step?: number;
  minLength?: number;
  maxLength?: number;
  pattern?: string;
  options?: { value: string; label: string; disabled?: boolean }[];
  validation?: {
    required?: boolean;
    minLength?: number;
    maxLength?: number;
    pattern?: RegExp;
    custom?: (value: any) => string | null;
  };
  helpText?: string;
  errorText?: string;
}

export interface FormSection {
  title: string;
  description?: string;
  fields: FormField[];
  collapsible?: boolean;
  collapsed?: boolean;
}

export interface FormConfig {
  title?: string;
  subtitle?: string;
  sections: FormSection[];
  submitText?: string;
  cancelText?: string;
  showCancel?: boolean;
  onSubmit?: (data: Record<string, any>) => void;
  onCancel?: () => void;
  onReset?: () => void;
  loading?: boolean;
  disabled?: boolean;
}

// Base Input Component
interface BaseInputProps {
  id: string;
  name: string;
  type: string;
  value: string | number;
  onChange: (value: string | number) => void;
  onBlur?: () => void;
  onFocus?: () => void;
  placeholder?: string;
  required?: boolean;
  disabled?: boolean;
  readOnly?: boolean;
  autoComplete?: string;
  autoFocus?: boolean;
  min?: number;
  max?: number;
  step?: number;
  minLength?: number;
  maxLength?: number;
  pattern?: string;
  className?: string;
  error?: string;
  helpText?: string;
  leftIcon?: ReactNode;
  rightIcon?: ReactNode;
  size?: 'sm' | 'md' | 'lg';
}

const BaseInput = forwardRef<HTMLInputElement, BaseInputProps>(({
  id,
  name,
  type,
  value,
  onChange,
  onBlur,
  onFocus,
  placeholder,
  required,
  disabled,
  readOnly,
  autoComplete,
  autoFocus,
  min,
  max,
  step,
  minLength,
  maxLength,
  pattern,
  className = "",
  error,
  helpText,
  leftIcon,
  rightIcon,
  size = 'md'
}, ref) => {
  const [isFocused, setIsFocused] = useState(false);
  const [showPassword, setShowPassword] = useState(false);

  const sizeClasses = {
    sm: 'px-3 py-2 text-sm',
    md: 'px-4 py-2.5 text-sm',
    lg: 'px-4 py-3 text-base'
  };

  const inputType = type === 'password' && showPassword ? 'text' : type;

  return (
    <div className="w-full">
      <div className="relative">
        {/* Left Icon */}
        {leftIcon && (
          <div className="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
            <div className="h-5 w-5 text-gray-400">
              {leftIcon}
            </div>
          </div>
        )}

        {/* Input */}
        <input
          ref={ref}
          id={id}
          name={name}
          type={inputType}
          value={value}
          onChange={(e) => onChange(e.target.value)}
          onBlur={() => {
            setIsFocused(false);
            onBlur?.();
          }}
          onFocus={() => {
            setIsFocused(true);
            onFocus?.();
          }}
          placeholder={placeholder}
          required={required}
          disabled={disabled}
          readOnly={readOnly}
          autoComplete={autoComplete}
          autoFocus={autoFocus}
          min={min}
          max={max}
          step={step}
          minLength={minLength}
          maxLength={maxLength}
          pattern={pattern}
          className={cn(
            "w-full border rounded-md transition-all duration-200 focus:outline-none focus:ring-2 focus:ring-opacity-50",
            sizeClasses[size],
            leftIcon ? "pl-10" : "",
            rightIcon ? "pr-10" : "",
            error
              ? "border-red-300 focus:border-red-500 focus:ring-red-500"
              : isFocused
              ? "border-op-blue focus:border-op-blue focus:ring-op-blue"
              : "border-gray-300 hover:border-gray-400",
            disabled ? "bg-gray-50 text-gray-500 cursor-not-allowed" : "",
            readOnly ? "bg-gray-50 text-gray-700" : ""
          )}
        />

        {/* Right Icon */}
        {rightIcon && (
          <div className="absolute inset-y-0 right-0 pr-3 flex items-center">
            {type === 'password' ? (
              <button
                type="button"
                onClick={() => setShowPassword(!showPassword)}
                className="h-5 w-5 text-gray-400 hover:text-gray-600 transition-colors"
              >
                {showPassword ? <EyeSlashIcon /> : <EyeIcon />}
              </button>
            ) : (
              <div className="h-5 w-5 text-gray-400">
                {rightIcon}
              </div>
            )}
          </div>
        )}
      </div>

      {/* Error Message */}
      {error && (
        <div className="mt-1 flex items-center space-x-1 text-sm text-red-600">
          <ExclamationTriangleIcon className="h-4 w-4 flex-shrink-0" />
          <span>{error}</span>
        </div>
      )}

      {/* Help Text */}
      {helpText && !error && (
        <div className="mt-1 flex items-center space-x-1 text-sm text-gray-500">
          <InformationCircleIcon className="h-4 w-4 flex-shrink-0" />
          <span>{helpText}</span>
        </div>
      )}
    </div>
  );
});

BaseInput.displayName = 'BaseInput';

// Text Input Component
interface TextInputProps extends Omit<BaseInputProps, 'type'> {
  type?: 'text' | 'email' | 'url' | 'tel' | 'search';
  icon?: ReactNode;
}

export function TextInput({
  type = 'text',
  icon,
  ...props
}: TextInputProps) {
  const getIcon = () => {
    if (icon) return icon;
    
    switch (type) {
      case 'email':
        return <EnvelopeIcon />;
      case 'tel':
        return <PhoneIcon />;
      case 'url':
        return <GlobeAltIcon />;
      case 'search':
        return <DocumentTextIcon />;
      default:
        return <UserIcon />;
    }
  };

  return (
    <BaseInput
      {...props}
      type={type}
      leftIcon={getIcon()}
    />
  );
}

// Password Input Component
interface PasswordInputProps extends Omit<BaseInputProps, 'type'> {
  showStrengthIndicator?: boolean;
}

export function PasswordInput({
  showStrengthIndicator = true,
  ...props
}: PasswordInputProps) {
  const [strength, setStrength] = useState<'weak' | 'medium' | 'strong'>('weak');

  useEffect(() => {
    if (showStrengthIndicator && typeof props.value === 'string') {
      const password = props.value;
      let score = 0;
      
      if (password.length >= 8) score++;
      if (/[a-z]/.test(password)) score++;
      if (/[A-Z]/.test(password)) score++;
      if (/[0-9]/.test(password)) score++;
      if (/[^A-Za-z0-9]/.test(password)) score++;
      
      if (score <= 2) setStrength('weak');
      else if (score <= 3) setStrength('medium');
      else setStrength('strong');
    }
  }, [props.value, showStrengthIndicator]);

  const getStrengthColor = () => {
    switch (strength) {
      case 'weak':
        return 'bg-red-500';
      case 'medium':
        return 'bg-yellow-500';
      case 'strong':
        return 'bg-green-500';
      default:
        return 'bg-gray-300';
    }
  };

  const getStrengthText = () => {
    switch (strength) {
      case 'weak':
        return 'Weak';
      case 'medium':
        return 'Medium';
      case 'strong':
        return 'Strong';
      default:
        return '';
    }
  };

  return (
    <div className="space-y-2">
      <BaseInput
        {...props}
        type="password"
        rightIcon={<LockClosedIcon />}
      />
      
      {showStrengthIndicator && (
        <div className="space-y-1">
          <div className="flex items-center justify-between text-xs text-gray-500">
            <span>Password strength</span>
            <span className={cn(
              "font-medium",
              strength === 'weak' && "text-red-600",
              strength === 'medium' && "text-yellow-600",
              strength === 'strong' && "text-green-600"
            )}>
              {getStrengthText()}
            </span>
          </div>
          <div className="w-full bg-gray-200 rounded-full h-1.5">
            <div
              className={cn("h-1.5 rounded-full transition-all duration-300", getStrengthColor())}
              style={{
                width: strength === 'weak' ? '33%' : strength === 'medium' ? '66%' : '100%'
              }}
            />
          </div>
        </div>
      )}
    </div>
  );
}

// Textarea Component
interface TextareaProps extends Omit<BaseInputProps, 'type'> {
  rows?: number;
  resize?: 'none' | 'vertical' | 'horizontal' | 'both';
}

export function Textarea({
  rows = 3,
  resize = 'vertical',
  ...props
}: TextareaProps) {
  const [isFocused, setIsFocused] = useState(false);

  const resizeClasses = {
    none: 'resize-none',
    vertical: 'resize-y',
    horizontal: 'resize-x',
    both: 'resize'
  };

  return (
    <div className="w-full">
      <div className="relative">
        <textarea
          id={props.id}
          name={props.name}
          value={props.value}
          onChange={(e) => props.onChange(e.target.value)}
          onBlur={() => {
            setIsFocused(false);
            props.onBlur?.();
          }}
          onFocus={() => {
            setIsFocused(true);
            props.onFocus?.();
          }}
          placeholder={props.placeholder}
          required={props.required}
          disabled={props.disabled}
          readOnly={props.readOnly}
          autoComplete={props.autoComplete}
          autoFocus={props.autoFocus}
          minLength={props.minLength}
          maxLength={props.maxLength}
          rows={rows}
          className={cn(
            "w-full border rounded-md transition-all duration-200 focus:outline-none focus:ring-2 focus:ring-opacity-50",
            "px-4 py-2.5 text-sm",
            resizeClasses[resize],
            props.error
              ? "border-red-300 focus:border-red-500 focus:ring-red-500"
              : isFocused
              ? "border-op-blue focus:border-op-blue focus:ring-op-blue"
              : "border-gray-300 hover:border-gray-400",
            props.disabled && "bg-gray-50 text-gray-500 cursor-not-allowed",
            props.readOnly && "bg-gray-50 text-gray-700"
          )}
        />
      </div>

      {/* Error Message */}
      {props.error && (
        <div className="mt-1 flex items-center space-x-1 text-sm text-red-600">
          <ExclamationTriangleIcon className="h-4 w-4 flex-shrink-0" />
          <span>{props.error}</span>
        </div>
      )}

      {/* Help Text */}
      {props.helpText && !props.error && (
        <div className="mt-1 flex items-center space-x-1 text-sm text-gray-500">
          <InformationCircleIcon className="h-4 w-4 flex-shrink-0" />
          <span>{props.helpText}</span>
        </div>
      )}
    </div>
  );
}

// Select Component
interface SelectProps extends Omit<BaseInputProps, 'type'> {
  options: { value: string; label: string; disabled?: boolean }[];
  multiple?: boolean;
  searchable?: boolean;
}

export function Select({
  options,
  multiple = false,
  searchable = false,
  ...props
}: SelectProps) {
  const [isOpen, setIsOpen] = useState(false);
  const [searchTerm, setSearchTerm] = useState('');
  const [selectedValues, setSelectedValues] = useState<string[]>(
    multiple ? (Array.isArray(props.value) ? props.value : []) : []
  );

  const filteredOptions = options.filter(option =>
    option.label.toLowerCase().includes(searchTerm.toLowerCase())
  );

  const handleSelect = (value: string) => {
    if (multiple) {
      const newValues = selectedValues.includes(value)
        ? selectedValues.filter(v => v !== value)
        : [...selectedValues, value];
      setSelectedValues(newValues);
      props.onChange(newValues as any);
    } else {
      props.onChange(value);
      setIsOpen(false);
    }
  };

  const removeValue = (value: string) => {
    const newValues = selectedValues.filter(v => v !== value);
    setSelectedValues(newValues);
    props.onChange(newValues as any);
  };

  const displayValue = multiple
    ? selectedValues.map(v => options.find(o => o.value === v)?.label).join(', ')
    : options.find(o => o.value === props.value)?.label || props.placeholder;

  return (
    <div className="w-full relative">
      <div className="relative">
        <button
          type="button"
          onClick={() => setIsOpen(!isOpen)}
          disabled={props.disabled}
          className={cn(
            "w-full border rounded-md transition-all duration-200 focus:outline-none focus:ring-2 focus:ring-opacity-50 text-left",
            "px-4 py-2.5 text-sm",
            props.error
              ? "border-red-300 focus:border-red-500 focus:ring-red-500"
              : "border-gray-300 hover:border-gray-400 focus:border-op-blue focus:ring-op-blue",
            props.disabled && "bg-gray-50 text-gray-500 cursor-not-allowed",
            props.readOnly && "bg-gray-50 text-gray-700"
          )}
        >
          <div className="flex items-center justify-between">
            <span className={displayValue ? "text-gray-900" : "text-gray-500"}>
              {displayValue || "Select an option"}
            </span>
            <ChevronDownIcon className={cn(
              "h-5 w-5 text-gray-400 transition-transform duration-200",
              isOpen && "transform rotate-180"
            )} />
          </div>
        </button>
      </div>

      {/* Dropdown */}
      {isOpen && (
        <div className="absolute z-10 w-full mt-1 bg-white border border-gray-300 rounded-md shadow-lg">
          {/* Search Input */}
          {searchable && (
            <div className="p-2 border-b border-gray-200">
              <input
                type="text"
                placeholder="Search options..."
                value={searchTerm}
                onChange={(e) => setSearchTerm(e.target.value)}
                className="w-full px-3 py-2 text-sm border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-op-blue focus:border-op-blue"
              />
            </div>
          )}

          {/* Options */}
          <div className="max-h-60 overflow-auto">
            {filteredOptions.length > 0 ? (
              filteredOptions.map((option) => (
                <button
                  key={option.value}
                  type="button"
                  onClick={() => handleSelect(option.value)}
                  disabled={option.disabled}
                  className={cn(
                    "w-full px-4 py-2 text-sm text-left hover:bg-gray-100 transition-colors",
                    option.disabled && "text-gray-400 cursor-not-allowed",
                    multiple && selectedValues.includes(option.value) && "bg-op-blue text-white hover:bg-op-blue-600"
                  )}
                >
                  <div className="flex items-center space-x-2">
                    {multiple && (
                      <div className={cn(
                        "w-4 h-4 border-2 rounded transition-colors",
                        selectedValues.includes(option.value)
                          ? "border-op-blue bg-op-blue"
                          : "border-gray-300"
                      )}>
                        {selectedValues.includes(option.value) && (
                          <CheckIcon className="w-3 h-3 text-white" />
                        )}
                      </div>
                    )}
                    <span>{option.label}</span>
                  </div>
                </button>
              ))
            ) : (
              <div className="px-4 py-2 text-sm text-gray-500 text-center">
                No options found
              </div>
            )}
          </div>
        </div>
      )}

      {/* Selected Values Display (Multiple) */}
      {multiple && selectedValues.length > 0 && (
        <div className="mt-2 flex flex-wrap gap-2">
          {selectedValues.map((value) => (
            <span
              key={value}
              className="inline-flex items-center px-2 py-1 rounded-full text-xs bg-op-blue text-white"
            >
              {options.find(o => o.value === value)?.label}
              <button
                type="button"
                onClick={() => removeValue(value)}
                className="ml-1 hover:bg-op-blue-600 rounded-full transition-colors"
              >
                <XMarkIcon className="w-3 h-3" />
              </button>
            </span>
          ))}
        </div>
      )}

      {/* Error Message */}
      {props.error && (
        <div className="mt-1 flex items-center space-x-1 text-sm text-red-600">
          <ExclamationTriangleIcon className="h-4 w-4 flex-shrink-0" />
          <span>{props.error}</span>
        </div>
      )}

      {/* Help Text */}
      {props.helpText && !props.error && (
        <div className="mt-1 flex items-center space-x-1 text-sm text-gray-500">
          <InformationCircleIcon className="h-4 w-4 flex-shrink-0" />
          <span>{props.helpText}</span>
        </div>
      )}
    </div>
  );
}

// Checkbox Component
interface CheckboxProps extends Omit<BaseInputProps, 'type'> {
  label: string;
  description?: string;
}

export function Checkbox({
  label,
  description,
  ...props
}: CheckboxProps) {
  const isChecked = Array.isArray(props.value) 
    ? props.value.includes(props.name)
    : Boolean(props.value);

  return (
    <div className="flex items-start space-x-3">
      <div className="flex items-center h-5">
        <input
          id={props.id}
          name={props.name}
          type="checkbox"
          checked={isChecked}
          onChange={(e) => {
            if (Array.isArray(props.value)) {
              const newValues = e.target.checked
                ? [...props.value, props.name]
                : props.value.filter(v => v !== props.name);
              props.onChange(newValues as any);
            } else {
              props.onChange(e.target.checked as any);
            }
          }}
          disabled={props.disabled}
          readOnly={props.readOnly}
          className={cn(
            "h-4 w-4 text-op-blue border-gray-300 rounded focus:ring-op-blue focus:ring-opacity-50 transition-colors",
            props.disabled && "bg-gray-100 text-gray-400 cursor-not-allowed"
          )}
        />
      </div>
      
      <div className="text-sm">
        <label
          htmlFor={props.id}
          className={cn(
            "font-medium text-gray-900",
            props.disabled && "text-gray-400 cursor-not-allowed"
          )}
        >
          {label}
        </label>
        {description && (
          <p className="text-gray-500 mt-1">{description}</p>
        )}
      </div>
    </div>
  );
}

// Radio Group Component
interface RadioGroupProps extends Omit<BaseInputProps, 'type'> {
  options: { value: string; label: string; description?: string; disabled?: boolean }[];
  name: string;
}

export function RadioGroup({
  options,
  name,
  ...props
}: RadioGroupProps) {
  return (
    <div className="space-y-3">
      {options.map((option) => (
        <div key={option.value} className="flex items-start space-x-3">
          <div className="flex items-center h-5">
            <input
              id={`${name}-${option.value}`}
              name={name}
              type="radio"
              value={option.value}
              checked={props.value === option.value}
              onChange={(e) => props.onChange(e.target.value)}
              disabled={option.disabled || props.disabled}
              className={cn(
                "h-4 w-4 text-op-blue border-gray-300 focus:ring-op-blue focus:ring-opacity-50 transition-colors",
                (option.disabled || props.disabled) && "bg-gray-100 text-gray-400 cursor-not-allowed"
              )}
            />
          </div>
          
          <div className="text-sm">
            <label
              htmlFor={`${name}-${option.value}`}
              className={cn(
                "font-medium text-gray-900",
                (option.disabled || props.disabled) && "text-gray-400 cursor-not-allowed"
              )}
            >
              {option.label}
            </label>
            {option.description && (
              <p className="text-gray-500 mt-1">{option.description}</p>
            )}
          </div>
        </div>
      ))}
    </div>
  );
}

// Form Section Component
interface FormSectionProps {
  section: FormSection;
  data: Record<string, any>;
  errors: Record<string, string>;
  onChange: (name: string, value: any) => void;
  onBlur: (name: string) => void;
  className?: string;
}

export function FormSection({
  section,
  data,
  errors,
  onChange,
  onBlur,
  className = ""
}: FormSectionProps) {
  const [isCollapsed, setIsCollapsed] = useState(section.collapsed || false);

  return (
    <div className={cn("border border-gray-200 rounded-lg", className)}>
      {/* Section Header */}
      <div className="px-6 py-4 border-b border-gray-200 bg-gray-50">
        <div className="flex items-center justify-between">
          <div>
            <h3 className="text-lg font-medium text-gray-900">{section.title}</h3>
            {section.description && (
              <p className="text-sm text-gray-500 mt-1">{section.description}</p>
            )}
          </div>
          
          {section.collapsible && (
            <button
              type="button"
              onClick={() => setIsCollapsed(!isCollapsed)}
              className="text-gray-400 hover:text-gray-600 transition-colors"
            >
              <ChevronDownIcon className={cn(
                "h-5 w-5 transition-transform duration-200",
                isCollapsed && "transform rotate-180"
              )} />
            </button>
          )}
        </div>
      </div>

      {/* Section Content */}
      {!isCollapsed && (
        <div className="p-6 space-y-6">
          {section.fields.map((field) => (
            <div key={field.name}>
              <label htmlFor={field.name} className="block text-sm font-medium text-gray-700 mb-2">
                {field.label}
                {field.required && <span className="text-red-500 ml-1">*</span>}
              </label>
              
              {field.type === 'textarea' ? (
                <Textarea
                  id={field.name}
                  name={field.name}
                  value={data[field.name] || ''}
                  onChange={(value) => onChange(field.name, value)}
                  onBlur={() => onBlur(field.name)}
                  placeholder={field.placeholder}
                  required={field.required}
                  disabled={field.disabled}
                  readOnly={field.readOnly}
                  autoComplete={field.autoComplete}
                  autoFocus={field.autoFocus}
                  minLength={field.minLength}
                  maxLength={field.maxLength}
                  rows={4}
                  error={errors[field.name]}
                  helpText={field.helpText}
                />
              ) : field.type === 'select' ? (
                <Select
                  id={field.name}
                  name={field.name}
                  value={data[field.name] || ''}
                  onChange={(value) => onChange(field.name, value)}
                  onBlur={() => onBlur(field.name)}
                  placeholder={field.placeholder}
                  required={field.required}
                  disabled={field.disabled}
                  readOnly={field.readOnly}
                  autoComplete={field.autoComplete}
                  autoFocus={field.autoFocus}
                  options={field.options || []}
                  error={errors[field.name]}
                  helpText={field.helpText}
                />
              ) : field.type === 'checkbox' ? (
                <Checkbox
                  id={field.name}
                  name={field.name}
                  value={data[field.name] || false}
                  onChange={(value) => onChange(field.name, value)}
                  onBlur={() => onBlur(field.name)}
                  disabled={field.disabled}
                  readOnly={field.readOnly}
                  label={field.label}
                  description={field.helpText}
                />
              ) : field.type === 'radio' ? (
                <RadioGroup
                  id={field.name}
                  name={field.name}
                  value={data[field.name] || ''}
                  onChange={(value) => onChange(field.name, value)}
                  onBlur={() => onBlur(field.name)}
                  disabled={field.disabled}
                  readOnly={field.readOnly}
                  options={field.options || []}
                />
              ) : field.type === 'password' ? (
                <PasswordInput
                  id={field.name}
                  name={field.name}
                  value={data[field.name] || ''}
                  onChange={(value) => onChange(field.name, value)}
                  onBlur={() => onBlur(field.name)}
                  onFocus={() => {}}
                  placeholder={field.placeholder}
                  required={field.required}
                  disabled={field.disabled}
                  readOnly={field.readOnly}
                  autoComplete={field.autoComplete}
                  autoFocus={field.autoFocus}
                  minLength={field.minLength}
                  maxLength={field.maxLength}
                  pattern={field.pattern}
                  error={errors[field.name]}
                  helpText={field.helpText}
                />
              ) : (
                <TextInput
                  id={field.name}
                  name={field.name}
                  type={field.type as any}
                  value={data[field.name] || ''}
                  onChange={(value) => onChange(field.name, value)}
                  onBlur={() => onBlur(field.name)}
                  onFocus={() => {}}
                  placeholder={field.placeholder}
                  required={field.required}
                  disabled={field.disabled}
                  readOnly={field.readOnly}
                  autoComplete={field.autoComplete}
                  autoFocus={field.autoFocus}
                  min={field.min}
                  max={field.max}
                  step={field.step}
                  minLength={field.minLength}
                  maxLength={field.maxLength}
                  pattern={field.pattern}
                  error={errors[field.name]}
                  helpText={field.helpText}
                />
              )}
            </div>
          ))}
        </div>
      )}
    </div>
  );
}

// Form Component
interface FormProps {
  config: FormConfig;
  data: Record<string, any>;
  errors: Record<string, string>;
  onChange: (name: string, value: any) => void;
  onBlur: (name: string) => void;
  className?: string;
}

export function Form({
  config,
  data,
  errors,
  onChange,
  onBlur,
  className = ""
}: FormProps) {
  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (config.onSubmit) {
      config.onSubmit(data);
    }
  };

  return (
    <form onSubmit={handleSubmit} className={cn("space-y-6", className)}>
      {/* Form Header */}
      {config.title && (
        <div className="text-center">
          <h2 className="text-2xl font-bold text-gray-900">{config.title}</h2>
          {config.subtitle && (
            <p className="text-gray-600 mt-2">{config.subtitle}</p>
          )}
        </div>
      )}

      {/* Form Sections */}
      {config.sections.map((section, index) => (
        <FormSection
          key={index}
          section={section}
          data={data}
          errors={errors}
          onChange={onChange}
          onBlur={onBlur}
        />
      ))}

      {/* Form Actions */}
      <div className="flex items-center justify-end space-x-3 pt-6 border-t border-gray-200">
        {config.showCancel && (
          <button
            type="button"
            onClick={config.onCancel}
            disabled={config.loading || config.disabled}
            className="px-4 py-2 text-sm font-medium text-gray-700 bg-white border border-gray-300 rounded-md hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-op-blue transition-colors"
          >
            {config.cancelText || 'Cancel'}
          </button>
        )}
        
        <button
          type="submit"
          disabled={config.loading || config.disabled}
          className="px-4 py-2 text-sm font-medium text-white bg-op-blue border border-transparent rounded-md hover:bg-op-blue-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-op-blue transition-colors disabled:opacity-50 disabled:cursor-not-allowed"
        >
          {config.loading ? (
            <div className="flex items-center space-x-2">
              <div className="animate-spin h-4 w-4 border-2 border-white border-t-transparent rounded-full" />
              <span>Submitting...</span>
            </div>
          ) : (
            config.submitText || 'Submit'
          )}
        </button>
      </div>
    </form>
  );
}
