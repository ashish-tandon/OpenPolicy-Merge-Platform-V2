'use client';

import { useState, useRef, useEffect } from 'react';
import { 
  ExclamationCircleIcon, 
  CheckCircleIcon,
  EyeIcon,
  EyeSlashIcon
} from '@heroicons/react/24/outline';
import { cn } from '@/lib/utils';

// Form Input Component
interface FormInputProps {
  label: string;
  name: string;
  type?: 'text' | 'email' | 'password' | 'number' | 'tel' | 'url' | 'search';
  value: string;
  onChange: (value: string) => void;
  placeholder?: string;
  required?: boolean;
  disabled?: boolean;
  error?: string;
  success?: string;
  helpText?: string;
  className?: string;
  autoComplete?: string;
  maxLength?: number;
  minLength?: number;
  pattern?: string;
}

export function FormInput({
  label,
  name,
  type = 'text',
  value,
  onChange,
  placeholder,
  required = false,
  disabled = false,
  error,
  success,
  helpText,
  className = "",
  autoComplete,
  maxLength,
  minLength,
  pattern
}: FormInputProps) {
  const [showPassword, setShowPassword] = useState(false);
  const [isFocused, setIsFocused] = useState(false);
  const inputRef = useRef<HTMLInputElement>(null);

  const inputType = type === 'password' && showPassword ? 'text' : type;
  const hasError = !!error;
  const hasSuccess = !!success;

  return (
    <div className={cn("space-y-2", className)}>
      <label 
        htmlFor={name}
        className="block text-sm font-medium text-gray-700"
      >
        {label}
        {required && <span className="text-red-500 ml-1">*</span>}
      </label>
      
      <div className="relative">
        <input
          ref={inputRef}
          id={name}
          name={name}
          type={inputType}
          value={value}
          onChange={(e) => onChange(e.target.value)}
          onFocus={() => setIsFocused(true)}
          onBlur={() => setIsFocused(false)}
          placeholder={placeholder}
          required={required}
          disabled={disabled}
          autoComplete={autoComplete}
          maxLength={maxLength}
          minLength={minLength}
          pattern={pattern}
          className={cn(
            "block w-full px-3 py-2 border rounded-md shadow-sm transition-colors",
            "focus:outline-none focus:ring-2 focus:ring-offset-0",
            "disabled:bg-gray-50 disabled:text-gray-500 disabled:cursor-not-allowed",
            {
              "border-gray-300 focus:border-op-blue focus:ring-op-blue": !hasError && !hasSuccess,
              "border-red-300 focus:border-red-500 focus:ring-red-500": hasError,
              "border-green-300 focus:border-green-500 focus:ring-green-500": hasSuccess,
              "pr-10": type === 'password'
            }
          )}
          aria-describedby={`${name}-help ${name}-error ${name}-success`}
          aria-invalid={hasError}
        />
        
        {/* Password toggle button */}
        {type === 'password' && (
          <button
            type="button"
            onClick={() => setShowPassword(!showPassword)}
            className="absolute inset-y-0 right-0 pr-3 flex items-center"
            aria-label={showPassword ? 'Hide password' : 'Show password'}
          >
            {showPassword ? (
              <EyeSlashIcon className="h-5 w-5 text-gray-400 hover:text-gray-600" />
            ) : (
              <EyeIcon className="h-5 w-5 text-gray-400 hover:text-gray-600" />
            )}
          </button>
        )}
        
        {/* Status icons */}
        {hasError && (
          <ExclamationCircleIcon className="absolute inset-y-0 right-0 pr-3 flex items-center h-5 w-5 text-red-500" />
        )}
        {hasSuccess && !hasError && (
          <CheckCircleIcon className="absolute inset-y-0 right-0 pr-3 flex items-center h-5 w-5 text-green-500" />
        )}
      </div>
      
      {/* Help text */}
      {helpText && (
        <p id={`${name}-help`} className="text-sm text-gray-500">
          {helpText}
        </p>
      )}
      
      {/* Error message */}
      {hasError && (
        <p id={`${name}-error`} className="text-sm text-red-600" role="alert">
          {error}
        </p>
      )}
      
      {/* Success message */}
      {hasSuccess && (
        <p id={`${name}-success`} className="text-sm text-green-600" role="status">
          {success}
        </p>
      )}
    </div>
  );
}

// Form Textarea Component
interface FormTextareaProps {
  label: string;
  name: string;
  value: string;
  onChange: (value: string) => void;
  placeholder?: string;
  required?: boolean;
  disabled?: boolean;
  error?: string;
  success?: string;
  helpText?: string;
  className?: string;
  rows?: number;
  maxLength?: number;
  minLength?: number;
}

export function FormTextarea({
  label,
  name,
  value,
  onChange,
  placeholder,
  required = false,
  disabled = false,
  error,
  success,
  helpText,
  className = "",
  rows = 3,
  maxLength,
  minLength
}: FormTextareaProps) {
  const hasError = !!error;
  const hasSuccess = !!success;

  return (
    <div className={cn("space-y-2", className)}>
      <label 
        htmlFor={name}
        className="block text-sm font-medium text-gray-700"
      >
        {label}
        {required && <span className="text-red-500 ml-1">*</span>}
      </label>
      
      <textarea
        id={name}
        name={name}
        value={value}
        onChange={(e) => onChange(e.target.value)}
        placeholder={placeholder}
        required={required}
        disabled={disabled}
        rows={rows}
        maxLength={maxLength}
        minLength={minLength}
        className={cn(
          "block w-full px-3 py-2 border rounded-md shadow-sm transition-colors",
          "focus:outline-none focus:ring-2 focus:ring-offset-0",
          "disabled:bg-gray-50 disabled:text-gray-500 disabled:cursor-not-allowed",
          "resize-vertical",
          {
            "border-gray-300 focus:border-op-blue focus:ring-op-blue": !hasError && !hasSuccess,
            "border-red-300 focus:border-red-500 focus:ring-red-500": hasError,
            "border-green-300 focus:border-green-500 focus:ring-green-500": hasSuccess
          }
        )}
        aria-describedby={`${name}-help ${name}-error ${name}-success`}
        aria-invalid={hasError}
      />
      
      {/* Help text */}
      {helpText && (
        <p id={`${name}-help`} className="text-sm text-gray-500">
          {helpText}
        </p>
      )}
      
      {/* Error message */}
      {hasError && (
        <p id={`${name}-error`} className="text-sm text-red-600" role="alert">
          {error}
        </p>
      )}
      
      {/* Success message */}
      {hasSuccess && (
        <p id={`${name}-success`} className="text-sm text-green-600" role="status">
          {success}
        </p>
      )}
    </div>
  );
}

// Form Select Component
interface FormSelectOption {
  value: string;
  label: string;
  disabled?: boolean;
}

interface FormSelectProps {
  label: string;
  name: string;
  value: string;
  onChange: (value: string) => void;
  options: FormSelectOption[];
  placeholder?: string;
  required?: boolean;
  disabled?: boolean;
  error?: string;
  success?: string;
  helpText?: string;
  className?: string;
  multiple?: boolean;
}

export function FormSelect({
  label,
  name,
  value,
  onChange,
  options,
  placeholder,
  required = false,
  disabled = false,
  error,
  success,
  helpText,
  className = "",
  multiple = false
}: FormSelectProps) {
  const hasError = !!error;
  const hasSuccess = !!success;

  return (
    <div className={cn("space-y-2", className)}>
      <label 
        htmlFor={name}
        className="block text-sm font-medium text-gray-700"
      >
        {label}
        {required && <span className="text-red-500 ml-1">*</span>}
      </label>
      
      <select
        id={name}
        name={name}
        value={value}
        onChange={(e) => onChange(e.target.value)}
        required={required}
        disabled={disabled}
        multiple={multiple}
        className={cn(
          "block w-full px-3 py-2 border rounded-md shadow-sm transition-colors",
          "focus:outline-none focus:ring-2 focus:ring-offset-0",
          "disabled:bg-gray-50 disabled:text-gray-500 disabled:cursor-not-allowed",
          "bg-white",
          {
            "border-gray-300 focus:border-op-blue focus:ring-op-blue": !hasError && !hasSuccess,
            "border-red-300 focus:border-red-500 focus:ring-red-500": hasError,
            "border-green-300 focus:border-green-500 focus:ring-green-500": hasSuccess
          }
        )}
        aria-describedby={`${name}-help ${name}-error ${name}-success`}
        aria-invalid={hasError}
      >
        {placeholder && (
          <option value="" disabled>
            {placeholder}
          </option>
        )}
        {options.map((option) => (
          <option
            key={option.value}
            value={option.value}
            disabled={option.disabled}
          >
            {option.label}
          </option>
        ))}
      </select>
      
      {/* Help text */}
      {helpText && (
        <p id={`${name}-help`} className="text-sm text-gray-500">
          {helpText}
        </p>
      )}
      
      {/* Error message */}
      {hasError && (
        <p id={`${name}-error`} className="text-sm text-red-600" role="alert">
          {error}
        </p>
      )}
      
      {/* Success message */}
      {hasSuccess && (
        <p id={`${name}-success`} className="text-sm text-green-600" role="status">
          {success}
        </p>
      )}
    </div>
  );
}

// Form Checkbox Component
interface FormCheckboxProps {
  label: string;
  name: string;
  checked: boolean;
  onChange: (checked: boolean) => void;
  required?: boolean;
  disabled?: boolean;
  error?: string;
  helpText?: string;
  className?: string;
}

export function FormCheckbox({
  label,
  name,
  checked,
  onChange,
  required = false,
  disabled = false,
  error,
  helpText,
  className = ""
}: FormCheckboxProps) {
  const hasError = !!error;

  return (
    <div className={cn("space-y-2", className)}>
      <div className="flex items-start">
        <div className="flex items-center h-5">
          <input
            id={name}
            name={name}
            type="checkbox"
            checked={checked}
            onChange={(e) => onChange(e.target.checked)}
            required={required}
            disabled={disabled}
            className={cn(
              "h-4 w-4 rounded border-gray-300 transition-colors",
              "focus:ring-2 focus:ring-offset-0",
              "disabled:bg-gray-50 disabled:text-gray-500 disabled:cursor-not-allowed",
              {
                "text-op-blue focus:ring-op-blue focus:border-op-blue": !hasError,
                "text-red-600 focus:ring-red-500 focus:border-red-500": hasError
              }
            )}
            aria-describedby={`${name}-help ${name}-error`}
            aria-invalid={hasError}
          />
        </div>
        <div className="ml-3 text-sm">
          <label 
            htmlFor={name}
            className={cn(
              "font-medium",
              {
                "text-gray-700": !disabled,
                "text-gray-500": disabled
              }
            )}
          >
            {label}
            {required && <span className="text-red-500 ml-1">*</span>}
          </label>
        </div>
      </div>
      
      {/* Help text */}
      {helpText && (
        <p id={`${name}-help`} className="text-sm text-gray-500 ml-7">
          {helpText}
        </p>
      )}
      
      {/* Error message */}
      {hasError && (
        <p id={`${name}-error`} className="text-sm text-red-600 ml-7" role="alert">
          {error}
        </p>
      )}
    </div>
  );
}

// Form Radio Group Component
interface FormRadioOption {
  value: string;
  label: string;
  disabled?: boolean;
  helpText?: string;
}

interface FormRadioGroupProps {
  label: string;
  name: string;
  value: string;
  onChange: (value: string) => void;
  options: FormRadioOption[];
  required?: boolean;
  disabled?: boolean;
  error?: string;
  helpText?: string;
  className?: string;
  layout?: 'horizontal' | 'vertical';
}

export function FormRadioGroup({
  label,
  name,
  value,
  onChange,
  options,
  required = false,
  disabled = false,
  error,
  helpText,
  className = "",
  layout = 'vertical'
}: FormRadioGroupProps) {
  const hasError = !!error;

  return (
    <div className={cn("space-y-3", className)}>
      <div className="text-sm font-medium text-gray-700">
        {label}
        {required && <span className="text-red-500 ml-1">*</span>}
      </div>
      
      <div className={cn(
        "space-y-2",
        {
          "space-y-2": layout === 'vertical',
          "space-x-6": layout === 'horizontal'
        }
      )}>
        {options.map((option) => (
          <div key={option.value} className={cn(
            "flex items-start",
            {
              "flex-col": layout === 'vertical',
              "flex-row items-center": layout === 'horizontal'
            }
          )}>
            <div className="flex items-center h-5">
              <input
                id={`${name}-${option.value}`}
                name={name}
                type="radio"
                value={option.value}
                checked={value === option.value}
                onChange={(e) => onChange(e.target.value)}
                required={required}
                disabled={disabled || option.disabled}
                className={cn(
                  "h-4 w-4 border-gray-300 transition-colors",
                  "focus:ring-2 focus:ring-offset-0",
                  "disabled:bg-gray-50 disabled:text-gray-500 disabled:cursor-not-allowed",
                  {
                    "text-op-blue focus:ring-op-blue focus:border-op-blue": !hasError,
                    "text-red-600 focus:ring-red-500 focus:border-red-500": hasError
                  }
                )}
                aria-describedby={`${name}-help ${name}-error`}
                aria-invalid={hasError}
              />
            </div>
            <div className={cn(
              "text-sm",
              {
                "ml-3": layout === 'vertical',
                "ml-2": layout === 'horizontal'
              }
            )}>
              <label 
                htmlFor={`${name}-${option.value}`}
                className={cn(
                  "font-medium",
                  {
                    "text-gray-700": !disabled && !option.disabled,
                    "text-gray-500": disabled || option.disabled
                  }
                )}
              >
                {option.label}
              </label>
              {option.helpText && (
                <p className="text-gray-500 mt-1">{option.helpText}</p>
              )}
            </div>
          </div>
        ))}
      </div>
      
      {/* Help text */}
      {helpText && (
        <p id={`${name}-help`} className="text-sm text-gray-500">
          {helpText}
        </p>
      )}
      
      {/* Error message */}
      {hasError && (
        <p id={`${name}-error`} className="text-sm text-red-600" role="alert">
          {error}
        </p>
      )}
    </div>
  );
}

// Form Fieldset Component
interface FormFieldsetProps {
  legend: string;
  children: React.ReactNode;
  className?: string;
  disabled?: boolean;
}

export function FormFieldset({
  legend,
  children,
  className = "",
  disabled = false
}: FormFieldsetProps) {
  return (
    <fieldset 
      className={cn("space-y-4", className)} 
      disabled={disabled}
    >
      <legend className="text-lg font-medium text-gray-900">
        {legend}
      </legend>
      {children}
    </fieldset>
  );
}

// Form Actions Component
interface FormActionsProps {
  children: React.ReactNode;
  className?: string;
}

export function FormActions({
  children,
  className = ""
}: FormActionsProps) {
  return (
    <div className={cn("flex items-center justify-end space-x-3 pt-4", className)}>
      {children}
    </div>
  );
}
