/**
 * AdGenesis - Premium Button Component
 * World-class SaaS button with variants, sizes, and micro-interactions
 */

import React, { forwardRef } from 'react';
import './Button.css';

const Button = forwardRef(({
  children,
  variant = 'primary',
  size = 'md',
  icon,
  iconPosition = 'left',
  loading = false,
  disabled = false,
  fullWidth = false,
  className = '',
  onClick,
  type = 'button',
  ...props
}, ref) => {
  
  const baseClasses = 'btn';
  const variantClasses = `btn-${variant}`;
  const sizeClasses = `btn-${size}`;
  const stateClasses = [
    loading && 'btn-loading',
    disabled && 'btn-disabled',
    fullWidth && 'btn-full',
  ].filter(Boolean).join(' ');

  const handleClick = (e) => {
    if (loading || disabled) {
      e.preventDefault();
      return;
    }
    onClick?.(e);
  };

  return (
    <button
      ref={ref}
      type={type}
      className={`${baseClasses} ${variantClasses} ${sizeClasses} ${stateClasses} ${className}`}
      onClick={handleClick}
      disabled={disabled || loading}
      {...props}
    >
      {loading && (
        <span className="btn-spinner">
          <svg className="animate-spin" viewBox="0 0 24 24" fill="none">
            <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4" />
            <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z" />
          </svg>
        </span>
      )}
      
      {icon && iconPosition === 'left' && !loading && (
        <span className="btn-icon btn-icon-left">{icon}</span>
      )}
      
      <span className="btn-content">{children}</span>
      
      {icon && iconPosition === 'right' && !loading && (
        <span className="btn-icon btn-icon-right">{icon}</span>
      )}
      
      <span className="btn-shine" />
    </button>
  );
});

Button.displayName = 'Button';

// Icon Button variant
export const IconButton = forwardRef(({
  icon,
  variant = 'ghost',
  size = 'md',
  className = '',
  tooltip,
  ...props
}, ref) => {
  return (
    <button
      ref={ref}
      className={`icon-btn icon-btn-${variant} icon-btn-${size} ${className}`}
      title={tooltip}
      {...props}
    >
      {icon}
    </button>
  );
});

IconButton.displayName = 'IconButton';

// Button Group
export const ButtonGroup = ({ children, className = '' }) => {
  return (
    <div className={`btn-group ${className}`}>
      {children}
    </div>
  );
};

export default Button;
