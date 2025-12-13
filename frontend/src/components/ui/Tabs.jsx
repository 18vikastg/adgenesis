/**
 * AdGenesis - Premium Tabs Component
 * Animated tabs with multiple variants and orientations
 */

import React, { useState, useRef, useEffect, createContext, useContext } from 'react';
import { cn } from '../../lib/utils';
import './Tabs.css';

// Tabs Context
const TabsContext = createContext(null);

/**
 * Tabs Container
 */
export const Tabs = ({
  children,
  defaultValue,
  value,
  onValueChange,
  variant = 'default',
  size = 'md',
  orientation = 'horizontal',
  className,
  ...props
}) => {
  const [internalValue, setInternalValue] = useState(defaultValue);
  const currentValue = value !== undefined ? value : internalValue;
  const [indicatorStyle, setIndicatorStyle] = useState({});
  const tabRefs = useRef(new Map());

  const handleValueChange = (newValue) => {
    if (value === undefined) {
      setInternalValue(newValue);
    }
    onValueChange?.(newValue);
  };

  const registerTab = (value, element) => {
    tabRefs.current.set(value, element);
  };

  const unregisterTab = (value) => {
    tabRefs.current.delete(value);
  };

  // Update indicator position
  useEffect(() => {
    const activeTab = tabRefs.current.get(currentValue);
    if (activeTab) {
      if (orientation === 'horizontal') {
        setIndicatorStyle({
          width: activeTab.offsetWidth,
          transform: `translateX(${activeTab.offsetLeft}px)`,
        });
      } else {
        setIndicatorStyle({
          height: activeTab.offsetHeight,
          transform: `translateY(${activeTab.offsetTop}px)`,
        });
      }
    }
  }, [currentValue, orientation]);

  const contextValue = {
    value: currentValue,
    onValueChange: handleValueChange,
    variant,
    size,
    orientation,
    registerTab,
    unregisterTab,
    indicatorStyle,
  };

  return (
    <TabsContext.Provider value={contextValue}>
      <div
        className={cn(
          'tabs',
          `tabs-${variant}`,
          `tabs-${size}`,
          `tabs-${orientation}`,
          className
        )}
        {...props}
      >
        {children}
      </div>
    </TabsContext.Provider>
  );
};

/**
 * Tab List
 */
export const TabList = ({ children, className, ...props }) => {
  const { variant, orientation, indicatorStyle } = useContext(TabsContext);

  return (
    <div
      className={cn('tab-list', className)}
      role="tablist"
      aria-orientation={orientation}
      {...props}
    >
      {children}
      {variant === 'default' && (
        <div className="tab-indicator" style={indicatorStyle} />
      )}
    </div>
  );
};

/**
 * Tab Trigger
 */
export const Tab = ({
  children,
  value,
  disabled = false,
  icon,
  badge,
  className,
  ...props
}) => {
  const tabRef = useRef(null);
  const {
    value: currentValue,
    onValueChange,
    variant,
    registerTab,
    unregisterTab,
  } = useContext(TabsContext);

  const isSelected = currentValue === value;

  useEffect(() => {
    if (tabRef.current) {
      registerTab(value, tabRef.current);
    }
    return () => unregisterTab(value);
  }, [value, registerTab, unregisterTab]);

  const handleClick = () => {
    if (!disabled) {
      onValueChange(value);
    }
  };

  const handleKeyDown = (e) => {
    if (e.key === 'Enter' || e.key === ' ') {
      e.preventDefault();
      handleClick();
    }
  };

  return (
    <button
      ref={tabRef}
      className={cn(
        'tab',
        isSelected && 'tab-selected',
        disabled && 'tab-disabled',
        variant === 'pills' && isSelected && 'tab-pills-selected',
        variant === 'bordered' && isSelected && 'tab-bordered-selected',
        className
      )}
      onClick={handleClick}
      onKeyDown={handleKeyDown}
      role="tab"
      aria-selected={isSelected}
      aria-disabled={disabled}
      tabIndex={disabled ? -1 : 0}
      {...props}
    >
      {icon && <span className="tab-icon">{icon}</span>}
      <span className="tab-label">{children}</span>
      {badge !== undefined && (
        <span className="tab-badge">{badge}</span>
      )}
    </button>
  );
};

/**
 * Tab Panel
 */
export const TabPanel = ({
  children,
  value,
  forceMount = false,
  className,
  ...props
}) => {
  const { value: currentValue } = useContext(TabsContext);
  const isSelected = currentValue === value;

  if (!forceMount && !isSelected) {
    return null;
  }

  return (
    <div
      className={cn(
        'tab-panel',
        !isSelected && 'tab-panel-hidden',
        className
      )}
      role="tabpanel"
      tabIndex={0}
      hidden={!isSelected}
      {...props}
    >
      {children}
    </div>
  );
};

/**
 * Segmented Control (Alternative Tabs Style)
 */
export const SegmentedControl = ({
  options = [],
  value,
  onChange,
  size = 'md',
  fullWidth = false,
  disabled = false,
  className,
  ...props
}) => {
  const [indicatorStyle, setIndicatorStyle] = useState({});
  const segmentRefs = useRef(new Map());

  useEffect(() => {
    const activeSegment = segmentRefs.current.get(value);
    if (activeSegment) {
      setIndicatorStyle({
        width: activeSegment.offsetWidth,
        transform: `translateX(${activeSegment.offsetLeft}px)`,
      });
    }
  }, [value]);

  return (
    <div
      className={cn(
        'segmented-control',
        `segmented-${size}`,
        fullWidth && 'segmented-full',
        disabled && 'segmented-disabled',
        className
      )}
      role="radiogroup"
      {...props}
    >
      <div className="segmented-indicator" style={indicatorStyle} />
      {options.map((option) => (
        <button
          key={option.value}
          ref={(el) => {
            if (el) segmentRefs.current.set(option.value, el);
          }}
          className={cn(
            'segment',
            value === option.value && 'segment-selected',
            option.disabled && 'segment-disabled'
          )}
          onClick={() => !disabled && !option.disabled && onChange?.(option.value)}
          role="radio"
          aria-checked={value === option.value}
          disabled={disabled || option.disabled}
        >
          {option.icon && <span className="segment-icon">{option.icon}</span>}
          <span className="segment-label">{option.label}</span>
        </button>
      ))}
    </div>
  );
};

/**
 * Vertical Tabs
 */
export const VerticalTabs = ({
  children,
  value,
  onValueChange,
  className,
  ...props
}) => {
  return (
    <Tabs
      value={value}
      onValueChange={onValueChange}
      orientation="vertical"
      className={cn('vertical-tabs', className)}
      {...props}
    >
      {children}
    </Tabs>
  );
};

export default Tabs;
