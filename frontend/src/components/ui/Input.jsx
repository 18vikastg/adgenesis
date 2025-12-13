/**
 * AdGenesis - Premium Input Components
 * Text inputs, textareas, selects with micro-interactions
 */

import React, { forwardRef, useState } from 'react';
import './Input.css';

// Text Input
export const Input = forwardRef(({
  label,
  error,
  hint,
  icon,
  iconPosition = 'left',
  suffix,
  size = 'md',
  variant = 'default',
  fullWidth = true,
  className = '',
  ...props
}, ref) => {
  const [focused, setFocused] = useState(false);
  
  return (
    <div className={`input-wrapper ${fullWidth ? 'input-full' : ''} ${className}`}>
      {label && (
        <label className="input-label">
          {label}
          {props.required && <span className="input-required">*</span>}
        </label>
      )}
      
      <div className={`input-container input-${size} input-${variant} ${focused ? 'input-focused' : ''} ${error ? 'input-error' : ''} ${props.disabled ? 'input-disabled' : ''}`}>
        {icon && iconPosition === 'left' && (
          <span className="input-icon input-icon-left">{icon}</span>
        )}
        
        <input
          ref={ref}
          className="input-field"
          onFocus={(e) => {
            setFocused(true);
            props.onFocus?.(e);
          }}
          onBlur={(e) => {
            setFocused(false);
            props.onBlur?.(e);
          }}
          {...props}
        />
        
        {icon && iconPosition === 'right' && (
          <span className="input-icon input-icon-right">{icon}</span>
        )}
        
        {suffix && <span className="input-suffix">{suffix}</span>}
      </div>
      
      {(error || hint) && (
        <span className={`input-message ${error ? 'input-message-error' : ''}`}>
          {error || hint}
        </span>
      )}
    </div>
  );
});

Input.displayName = 'Input';

// Textarea
export const Textarea = forwardRef(({
  label,
  error,
  hint,
  resize = 'vertical',
  rows = 4,
  className = '',
  ...props
}, ref) => {
  const [focused, setFocused] = useState(false);
  
  return (
    <div className={`input-wrapper input-full ${className}`}>
      {label && (
        <label className="input-label">
          {label}
          {props.required && <span className="input-required">*</span>}
        </label>
      )}
      
      <div className={`textarea-container ${focused ? 'input-focused' : ''} ${error ? 'input-error' : ''}`}>
        <textarea
          ref={ref}
          className="textarea-field"
          rows={rows}
          style={{ resize }}
          onFocus={(e) => {
            setFocused(true);
            props.onFocus?.(e);
          }}
          onBlur={(e) => {
            setFocused(false);
            props.onBlur?.(e);
          }}
          {...props}
        />
      </div>
      
      {(error || hint) && (
        <span className={`input-message ${error ? 'input-message-error' : ''}`}>
          {error || hint}
        </span>
      )}
    </div>
  );
});

Textarea.displayName = 'Textarea';

// Select
export const Select = forwardRef(({
  label,
  error,
  hint,
  options = [],
  placeholder = 'Select an option',
  size = 'md',
  className = '',
  ...props
}, ref) => {
  const [focused, setFocused] = useState(false);
  
  return (
    <div className={`input-wrapper input-full ${className}`}>
      {label && (
        <label className="input-label">
          {label}
          {props.required && <span className="input-required">*</span>}
        </label>
      )}
      
      <div className={`select-container input-${size} ${focused ? 'input-focused' : ''} ${error ? 'input-error' : ''}`}>
        <select
          ref={ref}
          className="select-field"
          onFocus={(e) => {
            setFocused(true);
            props.onFocus?.(e);
          }}
          onBlur={(e) => {
            setFocused(false);
            props.onBlur?.(e);
          }}
          {...props}
        >
          {placeholder && (
            <option value="" disabled>
              {placeholder}
            </option>
          )}
          {options.map((option) => (
            <option key={option.value} value={option.value}>
              {option.label}
            </option>
          ))}
        </select>
        
        <span className="select-arrow">
          <svg width="12" height="12" viewBox="0 0 12 12" fill="none">
            <path d="M3 4.5L6 7.5L9 4.5" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round"/>
          </svg>
        </span>
      </div>
      
      {(error || hint) && (
        <span className={`input-message ${error ? 'input-message-error' : ''}`}>
          {error || hint}
        </span>
      )}
    </div>
  );
});

Select.displayName = 'Select';

// Search Input
export const SearchInput = forwardRef(({
  onSearch,
  placeholder = 'Search...',
  loading = false,
  className = '',
  ...props
}, ref) => {
  const [value, setValue] = useState('');
  
  const handleKeyDown = (e) => {
    if (e.key === 'Enter' && onSearch) {
      onSearch(value);
    }
  };
  
  return (
    <div className={`search-container ${className}`}>
      <span className="search-icon">
        {loading ? (
          <svg className="animate-spin" width="18" height="18" viewBox="0 0 24 24" fill="none">
            <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4" />
            <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4z" />
          </svg>
        ) : (
          <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
            <circle cx="11" cy="11" r="8" />
            <path d="M21 21l-4.35-4.35" />
          </svg>
        )}
      </span>
      
      <input
        ref={ref}
        type="text"
        className="search-field"
        placeholder={placeholder}
        value={value}
        onChange={(e) => setValue(e.target.value)}
        onKeyDown={handleKeyDown}
        {...props}
      />
      
      {value && (
        <button
          type="button"
          className="search-clear"
          onClick={() => {
            setValue('');
            onSearch?.('');
          }}
        >
          <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
            <path d="M18 6L6 18M6 6l12 12" />
          </svg>
        </button>
      )}
    </div>
  );
});

SearchInput.displayName = 'SearchInput';

// Number Input with Stepper
export const NumberInput = forwardRef(({
  label,
  min,
  max,
  step = 1,
  value,
  onChange,
  className = '',
  ...props
}, ref) => {
  const handleIncrement = () => {
    const newValue = (value || 0) + step;
    if (max === undefined || newValue <= max) {
      onChange?.(newValue);
    }
  };
  
  const handleDecrement = () => {
    const newValue = (value || 0) - step;
    if (min === undefined || newValue >= min) {
      onChange?.(newValue);
    }
  };
  
  return (
    <div className={`number-input-wrapper ${className}`}>
      {label && <label className="input-label">{label}</label>}
      
      <div className="number-input-container">
        <button type="button" className="number-btn number-btn-dec" onClick={handleDecrement}>
          <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
            <path d="M5 12h14" />
          </svg>
        </button>
        
        <input
          ref={ref}
          type="number"
          className="number-field"
          value={value}
          onChange={(e) => onChange?.(parseFloat(e.target.value) || 0)}
          min={min}
          max={max}
          step={step}
          {...props}
        />
        
        <button type="button" className="number-btn number-btn-inc" onClick={handleIncrement}>
          <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
            <path d="M12 5v14M5 12h14" />
          </svg>
        </button>
      </div>
    </div>
  );
});

NumberInput.displayName = 'NumberInput';

export default Input;
