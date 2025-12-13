/**
 * AdGenesis - Premium Modal Component
 * Accessible, animated modals with multiple sizes and variants
 */

import React, { useEffect, useRef, useCallback } from 'react';
import { createPortal } from 'react-dom';
import { cn } from '../../lib/utils';
import './Modal.css';

// Icons
const CloseIcon = () => (
  <svg width="20" height="20" viewBox="0 0 20 20" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round">
    <path d="M15 5L5 15M5 5l10 10" />
  </svg>
);

const SuccessIcon = () => (
  <svg width="48" height="48" viewBox="0 0 48 48" fill="none">
    <circle cx="24" cy="24" r="20" fill="url(#success-gradient)" />
    <path d="M16 24L21 29L32 18" stroke="white" strokeWidth="3" strokeLinecap="round" strokeLinejoin="round" />
    <defs>
      <linearGradient id="success-gradient" x1="4" y1="4" x2="44" y2="44">
        <stop stopColor="#10B981" />
        <stop offset="1" stopColor="#059669" />
      </linearGradient>
    </defs>
  </svg>
);

const WarningIcon = () => (
  <svg width="48" height="48" viewBox="0 0 48 48" fill="none">
    <circle cx="24" cy="24" r="20" fill="url(#warning-gradient)" />
    <path d="M24 16V26" stroke="white" strokeWidth="3" strokeLinecap="round" />
    <circle cx="24" cy="32" r="2" fill="white" />
    <defs>
      <linearGradient id="warning-gradient" x1="4" y1="4" x2="44" y2="44">
        <stop stopColor="#F59E0B" />
        <stop offset="1" stopColor="#D97706" />
      </linearGradient>
    </defs>
  </svg>
);

const ErrorIcon = () => (
  <svg width="48" height="48" viewBox="0 0 48 48" fill="none">
    <circle cx="24" cy="24" r="20" fill="url(#error-gradient)" />
    <path d="M18 18L30 30M30 18L18 30" stroke="white" strokeWidth="3" strokeLinecap="round" />
    <defs>
      <linearGradient id="error-gradient" x1="4" y1="4" x2="44" y2="44">
        <stop stopColor="#EF4444" />
        <stop offset="1" stopColor="#DC2626" />
      </linearGradient>
    </defs>
  </svg>
);

const InfoIcon = () => (
  <svg width="48" height="48" viewBox="0 0 48 48" fill="none">
    <circle cx="24" cy="24" r="20" fill="url(#info-gradient)" />
    <path d="M24 20V32" stroke="white" strokeWidth="3" strokeLinecap="round" />
    <circle cx="24" cy="14" r="2" fill="white" />
    <defs>
      <linearGradient id="info-gradient" x1="4" y1="4" x2="44" y2="44">
        <stop stopColor="#8B5CF6" />
        <stop offset="1" stopColor="#7C3AED" />
      </linearGradient>
    </defs>
  </svg>
);

const statusIcons = {
  success: SuccessIcon,
  warning: WarningIcon,
  error: ErrorIcon,
  info: InfoIcon,
};

/**
 * Modal Component
 */
export const Modal = ({
  isOpen,
  onClose,
  children,
  size = 'md',
  closeOnOverlay = true,
  closeOnEscape = true,
  showCloseButton = true,
  className,
  overlayClassName,
  ...props
}) => {
  const modalRef = useRef(null);
  const previousActiveElement = useRef(null);

  // Handle escape key
  const handleKeyDown = useCallback((e) => {
    if (closeOnEscape && e.key === 'Escape') {
      onClose?.();
    }
  }, [closeOnEscape, onClose]);

  // Handle overlay click
  const handleOverlayClick = (e) => {
    if (closeOnOverlay && e.target === e.currentTarget) {
      onClose?.();
    }
  };

  // Focus management
  useEffect(() => {
    if (isOpen) {
      previousActiveElement.current = document.activeElement;
      modalRef.current?.focus();
      document.body.style.overflow = 'hidden';
      document.addEventListener('keydown', handleKeyDown);
    } else {
      document.body.style.overflow = '';
      previousActiveElement.current?.focus();
    }

    return () => {
      document.body.style.overflow = '';
      document.removeEventListener('keydown', handleKeyDown);
    };
  }, [isOpen, handleKeyDown]);

  if (!isOpen) return null;

  return createPortal(
    <div
      className={cn('modal-overlay', overlayClassName)}
      onClick={handleOverlayClick}
      role="presentation"
    >
      <div
        ref={modalRef}
        className={cn(
          'modal-container',
          `modal-${size}`,
          className
        )}
        role="dialog"
        aria-modal="true"
        tabIndex={-1}
        {...props}
      >
        {showCloseButton && (
          <button
            className="modal-close"
            onClick={onClose}
            aria-label="Close modal"
          >
            <CloseIcon />
          </button>
        )}
        {children}
      </div>
    </div>,
    document.body
  );
};

/**
 * Modal Header
 */
export const ModalHeader = ({ children, className, ...props }) => (
  <div className={cn('modal-header', className)} {...props}>
    {children}
  </div>
);

/**
 * Modal Title
 */
export const ModalTitle = ({ children, className, ...props }) => (
  <h2 className={cn('modal-title', className)} {...props}>
    {children}
  </h2>
);

/**
 * Modal Description
 */
export const ModalDescription = ({ children, className, ...props }) => (
  <p className={cn('modal-description', className)} {...props}>
    {children}
  </p>
);

/**
 * Modal Body
 */
export const ModalBody = ({ children, className, ...props }) => (
  <div className={cn('modal-body', className)} {...props}>
    {children}
  </div>
);

/**
 * Modal Footer
 */
export const ModalFooter = ({ children, className, align = 'right', ...props }) => (
  <div className={cn('modal-footer', `modal-footer-${align}`, className)} {...props}>
    {children}
  </div>
);

/**
 * Confirmation Modal
 */
export const ConfirmModal = ({
  isOpen,
  onClose,
  onConfirm,
  title = 'Confirm Action',
  description = 'Are you sure you want to proceed?',
  confirmText = 'Confirm',
  cancelText = 'Cancel',
  variant = 'primary',
  loading = false,
}) => {
  const handleConfirm = async () => {
    await onConfirm?.();
  };

  return (
    <Modal isOpen={isOpen} onClose={onClose} size="sm">
      <ModalHeader>
        <ModalTitle>{title}</ModalTitle>
        <ModalDescription>{description}</ModalDescription>
      </ModalHeader>
      <ModalFooter>
        <button
          className="modal-btn modal-btn-secondary"
          onClick={onClose}
          disabled={loading}
        >
          {cancelText}
        </button>
        <button
          className={cn('modal-btn', `modal-btn-${variant}`)}
          onClick={handleConfirm}
          disabled={loading}
        >
          {loading ? (
            <span className="modal-btn-loading">
              <span className="spinner" />
              Processing...
            </span>
          ) : (
            confirmText
          )}
        </button>
      </ModalFooter>
    </Modal>
  );
};

/**
 * Alert Modal with Status
 */
export const AlertModal = ({
  isOpen,
  onClose,
  status = 'info',
  title,
  description,
  actionText = 'Got it',
}) => {
  const StatusIcon = statusIcons[status];

  return (
    <Modal isOpen={isOpen} onClose={onClose} size="sm">
      <div className="alert-modal-content">
        <div className="alert-modal-icon">
          <StatusIcon />
        </div>
        <ModalTitle className="alert-modal-title">{title}</ModalTitle>
        {description && (
          <ModalDescription className="alert-modal-description">
            {description}
          </ModalDescription>
        )}
        <button
          className={cn('modal-btn', `modal-btn-${status === 'error' ? 'danger' : status === 'warning' ? 'warning' : 'primary'}`)}
          onClick={onClose}
          style={{ width: '100%', marginTop: '16px' }}
        >
          {actionText}
        </button>
      </div>
    </Modal>
  );
};

/**
 * Image Preview Modal
 */
export const ImageModal = ({
  isOpen,
  onClose,
  src,
  alt = 'Preview',
  title,
}) => {
  return (
    <Modal isOpen={isOpen} onClose={onClose} size="lg" className="image-modal">
      <div className="image-modal-content">
        {title && <div className="image-modal-title">{title}</div>}
        <img src={src} alt={alt} className="image-modal-img" />
      </div>
    </Modal>
  );
};

/**
 * Drawer (Slide-in Panel)
 */
export const Drawer = ({
  isOpen,
  onClose,
  children,
  position = 'right',
  size = 'md',
  title,
  showCloseButton = true,
  className,
  ...props
}) => {
  const drawerRef = useRef(null);

  useEffect(() => {
    if (isOpen) {
      document.body.style.overflow = 'hidden';
    } else {
      document.body.style.overflow = '';
    }

    return () => {
      document.body.style.overflow = '';
    };
  }, [isOpen]);

  if (!isOpen) return null;

  return createPortal(
    <div className="drawer-overlay" onClick={onClose}>
      <div
        ref={drawerRef}
        className={cn(
          'drawer-container',
          `drawer-${position}`,
          `drawer-${size}`,
          isOpen && 'drawer-open',
          className
        )}
        onClick={(e) => e.stopPropagation()}
        {...props}
      >
        {(title || showCloseButton) && (
          <div className="drawer-header">
            {title && <h3 className="drawer-title">{title}</h3>}
            {showCloseButton && (
              <button className="drawer-close" onClick={onClose}>
                <CloseIcon />
              </button>
            )}
          </div>
        )}
        <div className="drawer-content">
          {children}
        </div>
      </div>
    </div>,
    document.body
  );
};

export default Modal;
