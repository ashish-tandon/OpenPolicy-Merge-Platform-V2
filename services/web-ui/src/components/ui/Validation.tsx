'use client';

import { ReactNode, useState, useEffect, useRef } from 'react';
import { 
  ExclamationTriangleIcon, 
  CheckCircleIcon,
  InformationCircleIcon,
  EyeIcon,
  EyeSlashIcon
} from '@heroicons/react/24/outline';

// Utility function for combining class names
const cn = (...classes: (string | undefined | null | false)[]) => {
  return classes.filter(Boolean).join(' ');
};

// Validation Types
export type ValidationRule = {
  required?: boolean;
  minLength?: number;
  maxLength?: number;
  pattern?: RegExp;
  email?: boolean;
  url?: boolean;
  numeric?: boolean;
  integer?: boolean;
  positive?: boolean;
  negative?: boolean;
  min?: number;
  max?: number;
  custom?: (value: any) => boolean | string;
};

export type ValidationResult = {
  isValid: boolean;
  errors: string[];
  warnings: string[];
  touched: boolean;
};

export type FieldValidation = {
  value: any;
  rules: ValidationRule;
  result: ValidationResult;
};

// Validation Hook
export function useValidation(initialValue: any, rules: ValidationRule) {
  const [value, setValue] = useState(initialValue);
  const [result, setResult] = useState<ValidationResult>({
    isValid: true,
    errors: [],
    warnings: [],
    touched: false
  });

  const validate = (val: any): ValidationResult => {
    const errors: string[] = [];
    const warnings: string[] = [];

    // Required validation
    if (rules.required && (!val || (typeof val === 'string' && val.trim() === ''))) {
      errors.push('This field is required');
    }

    if (val && typeof val === 'string') {
      // Min length validation
      if (rules.minLength && val.length < rules.minLength) {
        errors.push(`Minimum length is ${rules.minLength} characters`);
      }

      // Max length validation
      if (rules.maxLength && val.length > rules.maxLength) {
        errors.push(`Maximum length is ${rules.maxLength} characters`);
      }

      // Pattern validation
      if (rules.pattern && !rules.pattern.test(val)) {
        errors.push('Invalid format');
      }

      // Email validation
      if (rules.email && !/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(val)) {
        errors.push('Invalid email format');
      }

      // URL validation
      if (rules.url && !/^https?:\/\/.+/.test(val)) {
        errors.push('Invalid URL format');
      }
    }

    if (val !== null && val !== undefined && !isNaN(Number(val))) {
      const numVal = Number(val);

      // Numeric validation
      if (rules.numeric && isNaN(numVal)) {
        errors.push('Must be a number');
      }

      // Integer validation
      if (rules.integer && !Number.isInteger(numVal)) {
        errors.push('Must be an integer');
      }

      // Positive validation
      if (rules.positive && numVal <= 0) {
        errors.push('Must be positive');
      }

      // Negative validation
      if (rules.negative && numVal >= 0) {
        errors.push('Must be negative');
      }

      // Min value validation
      if (rules.min !== undefined && numVal < rules.min) {
        errors.push(`Minimum value is ${rules.min}`);
      }

      // Max value validation
      if (rules.max !== undefined && numVal > rules.max) {
        errors.push(`Maximum value is ${rules.max}`);
      }
    }

    // Custom validation
    if (rules.custom) {
      const customResult = rules.custom(val);
      if (typeof customResult === 'string') {
        errors.push(customResult);
      } else if (!customResult) {
        errors.push('Invalid value');
      }
    }

    return {
      isValid: errors.length === 0,
      errors,
      warnings,
      touched: true
    };
  };

  const updateValue = (newValue: any) => {
    setValue(newValue);
    const validationResult = validate(newValue);
    setResult(validationResult);
  };

  const validateField = () => {
    const validationResult = validate(value);
    setResult(validationResult);
    return validationResult;
  };

  const reset = () => {
    setValue(initialValue);
    setResult({
      isValid: true,
      errors: [],
      warnings: [],
      touched: false
    });
  };

  return {
    value,
    result,
    updateValue,
    validateField,
    reset
  };
}

// Form Validation Hook
export function useFormValidation<T extends Record<string, any>>(initialValues: T, validationRules: Record<keyof T, ValidationRule>) {
  const [values, setValues] = useState<T>(initialValues);
  const [errors, setErrors] = useState<Record<keyof T, string[]>>({} as Record<keyof T, string[]>);
  const [touched, setTouched] = useState<Record<keyof T, boolean>>({} as Record<keyof T, boolean>);
  const [isValid, setIsValid] = useState(true);

  const validateField = (field: keyof T, value: any) => {
    const rules = validationRules[field];
    const fieldErrors: string[] = [];

    // Required validation
    if (rules.required && (!value || (typeof value === 'string' && value.trim() === ''))) {
      fieldErrors.push('This field is required');
    }

    if (value && typeof value === 'string') {
      // Min length validation
      if (rules.minLength && value.length < rules.minLength) {
        fieldErrors.push(`Minimum length is ${rules.minLength} characters`);
      }

      // Max length validation
      if (rules.maxLength && value.length > rules.maxLength) {
        fieldErrors.push(`Maximum length is ${rules.maxLength} characters`);
      }

      // Pattern validation
      if (rules.pattern && !rules.pattern.test(value)) {
        fieldErrors.push('Invalid format');
      }

      // Email validation
      if (rules.email && !/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(value)) {
        fieldErrors.push('Invalid email format');
      }

      // URL validation
      if (rules.url && !/^https?:\/\/.+/.test(value)) {
        fieldErrors.push('Invalid URL format');
      }
    }

    if (value !== null && value !== undefined && !isNaN(Number(value))) {
      const numVal = Number(value);

      // Numeric validation
      if (rules.numeric && isNaN(numVal)) {
        fieldErrors.push('Must be a number');
      }

      // Integer validation
      if (rules.integer && !Number.isInteger(numVal)) {
        fieldErrors.push('Must be an integer');
      }

      // Positive validation
      if (rules.positive && numVal <= 0) {
        fieldErrors.push('Must be positive');
      }

      // Negative validation
      if (rules.negative && numVal >= 0) {
        fieldErrors.push('Must be negative');
      }

      // Min value validation
      if (rules.min !== undefined && numVal < rules.min) {
        fieldErrors.push(`Minimum value is ${rules.min}`);
      }

      // Max value validation
      if (rules.max !== undefined && numVal > rules.max) {
        fieldErrors.push(`Maximum value is ${rules.max}`);
      }
    }

    // Custom validation
    if (rules.custom) {
      const customResult = rules.custom(value);
      if (typeof customResult === 'string') {
        fieldErrors.push(customResult);
      } else if (!customResult) {
        fieldErrors.push('Invalid value');
      }
    }

    return fieldErrors;
  };

  const updateField = (field: keyof T, value: any) => {
    const newValues = { ...values, [field]: value };
    const newErrors = { ...errors, [field]: validateField(field, value) };
    const newTouched = { ...touched, [field]: true };

    setValues(newValues);
    setErrors(newErrors);
    setTouched(newTouched);

    // Check overall form validity
    const hasErrors = Object.values(newErrors).some(fieldErrors => fieldErrors.length > 0);
    setIsValid(!hasErrors);
  };

  const validateForm = () => {
    const newErrors: Record<keyof T, string[]> = {} as Record<keyof T, string[]>;
    let hasErrors = false;

    Object.keys(validationRules).forEach((field) => {
      const fieldKey = field as keyof T;
      const fieldErrors = validateField(fieldKey, values[fieldKey]);
      newErrors[fieldKey] = fieldErrors;
      
      if (fieldErrors.length > 0) {
        hasErrors = true;
      }
    });

    setErrors(newErrors);
    setIsValid(!hasErrors);
    return !hasErrors;
  };

  const reset = () => {
    setValues(initialValues);
    setErrors({} as Record<keyof T, string[]>);
    setTouched({} as Record<keyof T, boolean>);
    setIsValid(true);
  };

  return {
    values,
    errors,
    touched,
    isValid,
    updateField,
    validateForm,
    reset
  };
}

// Validation Message Component
interface ValidationMessageProps {
  type: 'error' | 'warning' | 'info' | 'success';
  message: string;
  className?: string;
  showIcon?: boolean;
}

export function ValidationMessage({
  type,
  message,
  className = "",
  showIcon = true
}: ValidationMessageProps) {
  const getIcon = () => {
    switch (type) {
      case 'error':
        return <ExclamationTriangleIcon className="h-4 w-4 text-red-500" />;
      case 'warning':
        return <ExclamationTriangleIcon className="h-4 w-4 text-yellow-500" />;
      case 'info':
        return <InformationCircleIcon className="h-4 w-4 text-blue-500" />;
      case 'success':
        return <CheckCircleIcon className="h-4 w-4 text-green-500" />;
      default:
        return null;
    }
  };

  const getColorClasses = () => {
    switch (type) {
      case 'error':
        return 'text-red-800 bg-red-50 border-red-200';
      case 'warning':
        return 'text-yellow-800 bg-yellow-50 border-yellow-200';
      case 'info':
        return 'text-blue-800 bg-blue-50 border-blue-200';
      case 'success':
        return 'text-green-800 bg-green-50 border-green-200';
      default:
        return 'text-gray-800 bg-gray-50 border-gray-200';
    }
  };

  return (
    <div className={cn(
      "flex items-start space-x-2 p-3 rounded-md border",
      getColorClasses(),
      className
    )}>
      {showIcon && getIcon()}
      <span className="text-sm font-medium">{message}</span>
    </div>
  );
}

// Validation Field Component
interface ValidationFieldProps {
  label: string;
  name: string;
  value: any;
  onChange: (value: any) => void;
  onBlur?: () => void;
  rules: ValidationRule;
  type?: 'text' | 'email' | 'password' | 'number' | 'url' | 'tel';
  placeholder?: string;
  className?: string;
  disabled?: boolean;
  required?: boolean;
  showValidation?: boolean;
}

export function ValidationField({
  label,
  name,
  value,
  onChange,
  onBlur,
  rules,
  type = 'text',
  placeholder,
  className = "",
  disabled = false,
  required = false,
  showValidation = true
}: ValidationFieldProps) {
  const { result, updateValue, validateField } = useValidation(value, rules);
  const [showPassword, setShowPassword] = useState(false);

  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const newValue = type === 'number' ? Number(e.target.value) : e.target.value;
    updateValue(newValue);
    onChange(newValue);
  };

  const handleBlur = () => {
    validateField();
    onBlur?.();
  };

  const getInputType = () => {
    if (type === 'password') {
      return showPassword ? 'text' : 'password';
    }
    return type;
  };

  const getInputClasses = () => {
    const baseClasses = "w-full px-3 py-2 border rounded-md focus:outline-none focus:ring-2 focus:ring-offset-2 transition-colors";
    
    if (result.touched && !result.isValid) {
      return cn(baseClasses, "border-red-300 focus:ring-red-500 focus:border-red-500");
    }
    
    if (result.touched && result.isValid) {
      return cn(baseClasses, "border-green-300 focus:ring-green-500 focus:border-green-500");
    }
    
    return cn(baseClasses, "border-gray-300 focus:ring-op-blue focus:border-op-blue");
  };

  return (
    <div className={cn("space-y-2", className)}>
      <label htmlFor={name} className="block text-sm font-medium text-gray-700">
        {label}
        {required && <span className="text-red-500 ml-1">*</span>}
      </label>
      
      <div className="relative">
        <input
          id={name}
          name={name}
          type={getInputType()}
          value={value || ''}
          onChange={handleChange}
          onBlur={handleBlur}
          placeholder={placeholder}
          disabled={disabled}
          className={getInputClasses()}
          aria-invalid={result.touched && !result.isValid}
          aria-describedby={result.touched && !result.isValid ? `${name}-error` : undefined}
        />
        
        {type === 'password' && (
          <button
            type="button"
            onClick={() => setShowPassword(!showPassword)}
            className="absolute right-3 top-1/2 transform -translate-y-1/2 text-gray-400 hover:text-gray-600"
            aria-label={showPassword ? 'Hide password' : 'Show password'}
          >
            {showPassword ? (
              <EyeSlashIcon className="h-4 w-4" />
            ) : (
              <EyeIcon className="h-4 w-4" />
            )}
          </button>
        )}
      </div>
      
      {showValidation && result.touched && (
        <div className="space-y-1">
          {result.errors.map((error, index) => (
            <ValidationMessage
              key={index}
              type="error"
              message={error}
              className="text-xs"
              showIcon={false}
            />
          ))}
          
          {result.warnings.map((warning, index) => (
            <ValidationMessage
              key={index}
              type="warning"
              message={warning}
              className="text-xs"
              showIcon={false}
            />
          ))}
        </div>
      )}
    </div>
  );
}

// Validation Form Component
interface ValidationFormProps {
  children: ReactNode;
  onSubmit: (values: any) => void;
  onValidationError?: (errors: Record<string, string[]>) => void;
  className?: string;
  disabled?: boolean;
}

export function ValidationForm({
  children,
  onSubmit,
  onValidationError,
  className = "",
  disabled = false
}: ValidationFormProps) {
  const [isSubmitting, setIsSubmitting] = useState(false);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setIsSubmitting(true);
    
    try {
      // Form submission logic would go here
      // This is a placeholder for the actual implementation
      await new Promise(resolve => setTimeout(resolve, 100));
      
      // Simulate successful submission
      onSubmit({});
    } catch (error) {
      console.error('Form submission error:', error);
    } finally {
      setIsSubmitting(false);
    }
  };

  return (
    <form onSubmit={handleSubmit} className={cn("space-y-6", className)}>
      {children}
      
      <button
        type="submit"
        disabled={disabled || isSubmitting}
        className={cn(
          "w-full px-4 py-2 text-sm font-medium text-white bg-op-blue rounded-md",
          "hover:bg-op-blue-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-op-blue",
          "disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
        )}
      >
        {isSubmitting ? 'Submitting...' : 'Submit'}
      </button>
    </form>
  );
}

// Validation Summary Component
interface ValidationSummaryProps {
  errors: Record<string, string[]>;
  className?: string;
  showFieldNames?: boolean;
}

export function ValidationSummary({
  errors,
  className = "",
  showFieldNames = true
}: ValidationSummaryProps) {
  const allErrors = Object.entries(errors).flatMap(([field, fieldErrors]) =>
    fieldErrors.map(error => ({ field, error }))
  );

  if (allErrors.length === 0) {
    return null;
  }

  return (
    <div className={cn("p-4 bg-red-50 border border-red-200 rounded-md", className)}>
      <h3 className="text-sm font-medium text-red-800 mb-2">
        Please correct the following errors:
      </h3>
      
      <ul className="space-y-1">
        {allErrors.map(({ field, error }, index) => (
          <li key={index} className="text-sm text-red-700">
            {showFieldNames && (
              <span className="font-medium capitalize">{field}: </span>
            )}
            {error}
          </li>
        ))}
      </ul>
    </div>
  );
}

// Real-time Validation Component
interface RealTimeValidationProps {
  value: any;
  rules: ValidationRule;
  children: (validationResult: ValidationResult) => ReactNode;
  className?: string;
  debounceMs?: number;
}

export function RealTimeValidation({
  value,
  rules,
  children,
  className = "",
  debounceMs = 300
}: RealTimeValidationProps) {
  const { result, updateValue } = useValidation(value, rules);
  const timeoutRef = useRef<NodeJS.Timeout>();

  useEffect(() => {
    if (timeoutRef.current) {
      clearTimeout(timeoutRef.current);
    }

    timeoutRef.current = setTimeout(() => {
      updateValue(value);
    }, debounceMs);

    return () => {
      if (timeoutRef.current) {
        clearTimeout(timeoutRef.current);
      }
    };
  }, [value, debounceMs, updateValue]);

  return (
    <div className={className}>
      {children(result)}
    </div>
  );
}
