/**
 * AdGenesis - Premium Dropdown Component
 * Feature-rich dropdown with search, groups, and keyboard navigation
 */

import React, { useState, useRef, useEffect, useCallback, createContext, useContext } from 'react';
import { createPortal } from 'react-dom';
import { cn } from '../../lib/utils';
import './Dropdown.css';

// Icons
const ChevronDownIcon = () => (
  <svg width="16" height="16" viewBox="0 0 16 16" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round">
    <path d="M4 6L8 10L12 6" />
  </svg>
);

const CheckIcon = () => (
  <svg width="16" height="16" viewBox="0 0 16 16" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round">
    <path d="M3 8L6 11L13 4" />
  </svg>
);

const SearchIcon = () => (
  <svg width="16" height="16" viewBox="0 0 16 16" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round">
    <circle cx="7" cy="7" r="4" />
    <path d="M10 10L14 14" />
  </svg>
);

// Dropdown Context
const DropdownContext = createContext(null);

/**
 * Main Dropdown Component
 */
export const Dropdown = ({
  children,
  trigger,
  placement = 'bottom-start',
  offset = 8,
  closeOnSelect = true,
  closeOnClickOutside = true,
  className,
}) => {
  const [isOpen, setIsOpen] = useState(false);
  const [position, setPosition] = useState({ top: 0, left: 0 });
  const triggerRef = useRef(null);
  const menuRef = useRef(null);
  const [activeIndex, setActiveIndex] = useState(-1);

  // Calculate position
  const updatePosition = useCallback(() => {
    if (!triggerRef.current) return;

    const rect = triggerRef.current.getBoundingClientRect();
    const scrollTop = window.scrollY;
    const scrollLeft = window.scrollX;

    let top = 0;
    let left = 0;

    switch (placement) {
      case 'bottom-start':
        top = rect.bottom + scrollTop + offset;
        left = rect.left + scrollLeft;
        break;
      case 'bottom-end':
        top = rect.bottom + scrollTop + offset;
        left = rect.right + scrollLeft;
        break;
      case 'bottom':
        top = rect.bottom + scrollTop + offset;
        left = rect.left + scrollLeft + rect.width / 2;
        break;
      case 'top-start':
        top = rect.top + scrollTop - offset;
        left = rect.left + scrollLeft;
        break;
      case 'top-end':
        top = rect.top + scrollTop - offset;
        left = rect.right + scrollLeft;
        break;
      case 'top':
        top = rect.top + scrollTop - offset;
        left = rect.left + scrollLeft + rect.width / 2;
        break;
      default:
        top = rect.bottom + scrollTop + offset;
        left = rect.left + scrollLeft;
    }

    setPosition({ top, left, width: rect.width });
  }, [placement, offset]);

  // Handle click outside
  useEffect(() => {
    if (!closeOnClickOutside || !isOpen) return;

    const handleClickOutside = (e) => {
      if (
        triggerRef.current?.contains(e.target) ||
        menuRef.current?.contains(e.target)
      ) {
        return;
      }
      setIsOpen(false);
    };

    document.addEventListener('mousedown', handleClickOutside);
    return () => document.removeEventListener('mousedown', handleClickOutside);
  }, [isOpen, closeOnClickOutside]);

  // Update position on open
  useEffect(() => {
    if (isOpen) {
      updatePosition();
      window.addEventListener('resize', updatePosition);
      window.addEventListener('scroll', updatePosition);
    }
    return () => {
      window.removeEventListener('resize', updatePosition);
      window.removeEventListener('scroll', updatePosition);
    };
  }, [isOpen, updatePosition]);

  // Keyboard navigation
  const handleKeyDown = (e) => {
    if (!isOpen) {
      if (e.key === 'Enter' || e.key === ' ' || e.key === 'ArrowDown') {
        e.preventDefault();
        setIsOpen(true);
      }
      return;
    }

    switch (e.key) {
      case 'Escape':
        e.preventDefault();
        setIsOpen(false);
        triggerRef.current?.focus();
        break;
      case 'ArrowDown':
        e.preventDefault();
        setActiveIndex((prev) => prev + 1);
        break;
      case 'ArrowUp':
        e.preventDefault();
        setActiveIndex((prev) => (prev > 0 ? prev - 1 : prev));
        break;
      default:
        break;
    }
  };

  const handleSelect = () => {
    if (closeOnSelect) {
      setIsOpen(false);
    }
  };

  const contextValue = {
    isOpen,
    setIsOpen,
    activeIndex,
    setActiveIndex,
    handleSelect,
  };

  return (
    <DropdownContext.Provider value={contextValue}>
      <div className={cn('dropdown', className)} onKeyDown={handleKeyDown}>
        <div
          ref={triggerRef}
          className="dropdown-trigger"
          onClick={() => setIsOpen(!isOpen)}
          role="button"
          tabIndex={0}
          aria-expanded={isOpen}
          aria-haspopup="menu"
        >
          {trigger}
        </div>
        {isOpen && createPortal(
          <div
            ref={menuRef}
            className={cn('dropdown-menu', `dropdown-${placement}`)}
            style={{
              top: position.top,
              left: position.left,
              minWidth: position.width,
            }}
            role="menu"
          >
            {children}
          </div>,
          document.body
        )}
      </div>
    </DropdownContext.Provider>
  );
};

/**
 * Dropdown Item
 */
export const DropdownItem = ({
  children,
  icon,
  shortcut,
  disabled = false,
  selected = false,
  danger = false,
  onClick,
  className,
  ...props
}) => {
  const { handleSelect } = useContext(DropdownContext);

  const handleClick = (e) => {
    if (disabled) return;
    onClick?.(e);
    handleSelect();
  };

  return (
    <button
      className={cn(
        'dropdown-item',
        disabled && 'dropdown-item-disabled',
        selected && 'dropdown-item-selected',
        danger && 'dropdown-item-danger',
        className
      )}
      onClick={handleClick}
      disabled={disabled}
      role="menuitem"
      {...props}
    >
      {icon && <span className="dropdown-item-icon">{icon}</span>}
      <span className="dropdown-item-content">{children}</span>
      {selected && (
        <span className="dropdown-item-check">
          <CheckIcon />
        </span>
      )}
      {shortcut && <span className="dropdown-item-shortcut">{shortcut}</span>}
    </button>
  );
};

/**
 * Dropdown Group
 */
export const DropdownGroup = ({ children, label, className }) => (
  <div className={cn('dropdown-group', className)} role="group">
    {label && <div className="dropdown-group-label">{label}</div>}
    {children}
  </div>
);

/**
 * Dropdown Divider
 */
export const DropdownDivider = ({ className }) => (
  <div className={cn('dropdown-divider', className)} role="separator" />
);

/**
 * Searchable Dropdown (Select Component)
 */
export const Select = ({
  options = [],
  value,
  onChange,
  placeholder = 'Select an option',
  searchable = false,
  searchPlaceholder = 'Search...',
  multiple = false,
  disabled = false,
  error,
  label,
  className,
  ...props
}) => {
  const [isOpen, setIsOpen] = useState(false);
  const [search, setSearch] = useState('');
  const [activeIndex, setActiveIndex] = useState(0);
  const triggerRef = useRef(null);
  const menuRef = useRef(null);
  const searchRef = useRef(null);

  // Get selected option(s)
  const selectedOptions = multiple
    ? options.filter((opt) => value?.includes(opt.value))
    : options.find((opt) => opt.value === value);

  // Filter options based on search
  const filteredOptions = search
    ? options.filter((opt) =>
        opt.label.toLowerCase().includes(search.toLowerCase())
      )
    : options;

  // Handle option select
  const handleSelect = (option) => {
    if (multiple) {
      const newValue = value?.includes(option.value)
        ? value.filter((v) => v !== option.value)
        : [...(value || []), option.value];
      onChange?.(newValue);
    } else {
      onChange?.(option.value);
      setIsOpen(false);
    }
    setSearch('');
  };

  // Handle keyboard navigation
  const handleKeyDown = (e) => {
    if (disabled) return;

    switch (e.key) {
      case 'Enter':
      case ' ':
        e.preventDefault();
        if (isOpen && filteredOptions[activeIndex]) {
          handleSelect(filteredOptions[activeIndex]);
        } else {
          setIsOpen(true);
        }
        break;
      case 'Escape':
        setIsOpen(false);
        break;
      case 'ArrowDown':
        e.preventDefault();
        if (isOpen) {
          setActiveIndex((prev) =>
            prev < filteredOptions.length - 1 ? prev + 1 : prev
          );
        } else {
          setIsOpen(true);
        }
        break;
      case 'ArrowUp':
        e.preventDefault();
        if (isOpen) {
          setActiveIndex((prev) => (prev > 0 ? prev - 1 : 0));
        }
        break;
      default:
        break;
    }
  };

  // Focus search input when opened
  useEffect(() => {
    if (isOpen && searchable) {
      searchRef.current?.focus();
    }
  }, [isOpen, searchable]);

  // Close on click outside
  useEffect(() => {
    if (!isOpen) return;

    const handleClickOutside = (e) => {
      if (
        !triggerRef.current?.contains(e.target) &&
        !menuRef.current?.contains(e.target)
      ) {
        setIsOpen(false);
      }
    };

    document.addEventListener('mousedown', handleClickOutside);
    return () => document.removeEventListener('mousedown', handleClickOutside);
  }, [isOpen]);

  return (
    <div className={cn('select-wrapper', className)} {...props}>
      {label && <label className="select-label">{label}</label>}
      <div
        ref={triggerRef}
        className={cn(
          'select-trigger',
          isOpen && 'select-trigger-open',
          disabled && 'select-trigger-disabled',
          error && 'select-trigger-error'
        )}
        onClick={() => !disabled && setIsOpen(!isOpen)}
        onKeyDown={handleKeyDown}
        tabIndex={disabled ? -1 : 0}
        role="combobox"
        aria-expanded={isOpen}
        aria-haspopup="listbox"
      >
        <span className="select-value">
          {multiple ? (
            selectedOptions?.length > 0 ? (
              <span className="select-tags">
                {selectedOptions.map((opt) => (
                  <span key={opt.value} className="select-tag">
                    {opt.label}
                    <button
                      className="select-tag-remove"
                      onClick={(e) => {
                        e.stopPropagation();
                        handleSelect(opt);
                      }}
                    >
                      ×
                    </button>
                  </span>
                ))}
              </span>
            ) : (
              <span className="select-placeholder">{placeholder}</span>
            )
          ) : selectedOptions ? (
            <>
              {selectedOptions.icon && (
                <span className="select-value-icon">{selectedOptions.icon}</span>
              )}
              {selectedOptions.label}
            </>
          ) : (
            <span className="select-placeholder">{placeholder}</span>
          )}
        </span>
        <span className={cn('select-chevron', isOpen && 'select-chevron-open')}>
          <ChevronDownIcon />
        </span>
      </div>
      {isOpen && (
        <div ref={menuRef} className="select-menu" role="listbox">
          {searchable && (
            <div className="select-search">
              <SearchIcon />
              <input
                ref={searchRef}
                type="text"
                value={search}
                onChange={(e) => setSearch(e.target.value)}
                placeholder={searchPlaceholder}
                className="select-search-input"
              />
            </div>
          )}
          <div className="select-options">
            {filteredOptions.length > 0 ? (
              filteredOptions.map((option, index) => (
                <div
                  key={option.value}
                  className={cn(
                    'select-option',
                    (multiple
                      ? value?.includes(option.value)
                      : option.value === value) && 'select-option-selected',
                    index === activeIndex && 'select-option-active',
                    option.disabled && 'select-option-disabled'
                  )}
                  onClick={() => !option.disabled && handleSelect(option)}
                  role="option"
                  aria-selected={
                    multiple
                      ? value?.includes(option.value)
                      : option.value === value
                  }
                >
                  {option.icon && (
                    <span className="select-option-icon">{option.icon}</span>
                  )}
                  <span className="select-option-label">{option.label}</span>
                  {option.description && (
                    <span className="select-option-desc">
                      {option.description}
                    </span>
                  )}
                  {(multiple
                    ? value?.includes(option.value)
                    : option.value === value) && (
                    <span className="select-option-check">
                      <CheckIcon />
                    </span>
                  )}
                </div>
              ))
            ) : (
              <div className="select-empty">No options found</div>
            )}
          </div>
        </div>
      )}
      {error && <span className="select-error">{error}</span>}
    </div>
  );
};

export default Dropdown;
