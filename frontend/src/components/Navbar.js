import React, { useState } from 'react';
import { Link, useLocation } from 'react-router-dom';

const SparklesIcon = () => (
  <svg width="24" height="24" viewBox="0 0 24 24" fill="none">
    <path d="M12 2L13.5 7.5L19 9L13.5 10.5L12 16L10.5 10.5L5 9L10.5 7.5L12 2Z" fill="currentColor" />
    <path d="M18 14L19 17L22 18L19 19L18 22L17 19L14 18L17 17L18 14Z" fill="currentColor" opacity="0.7" />
  </svg>
);

const MenuIcon = () => (
  <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round">
    <path d="M4 6H20M4 12H20M4 18H20" />
  </svg>
);

const Navbar = () => {
  const location = useLocation();
  const [mobileMenuOpen, setMobileMenuOpen] = useState(false);
  
  const isActive = (path) => location.pathname === path;
  
  // Hide navbar on design studio (it has its own navigation)
  if (location.pathname === '/studio') {
    return null;
  }

  const navLinks = [
    { path: '/studio', label: 'Design Studio', highlight: true },
    { path: '/editor', label: 'Editor' },
    { path: '/guidelines', label: 'Brand Kit' },
    { path: '/export', label: 'Export' },
  ];

  return (
    <nav className="navbar">
      <div className="navbar-container">
        <div className="navbar-content">
          {/* Logo */}
          <Link to="/" className="navbar-logo">
            <span className="navbar-logo-icon">
              <SparklesIcon />
            </span>
            <span className="navbar-logo-text">AdGenesis</span>
          </Link>

          {/* Desktop Navigation */}
          <div className="navbar-links">
            {navLinks.map((link) => (
              <Link
                key={link.path}
                to={link.path}
                className={`navbar-link ${isActive(link.path) ? 'active' : ''} ${link.highlight ? 'highlight' : ''}`}
              >
                {link.label}
              </Link>
            ))}
          </div>

          {/* Right Section */}
          <div className="navbar-right">
            <button className="navbar-cta">
              <SparklesIcon />
              <span>Start Creating</span>
            </button>
            
            {/* Mobile Menu Button */}
            <button 
              className="navbar-mobile-toggle"
              onClick={() => setMobileMenuOpen(!mobileMenuOpen)}
            >
              <MenuIcon />
            </button>
          </div>
        </div>

        {/* Mobile Menu */}
        {mobileMenuOpen && (
          <div className="navbar-mobile-menu">
            {navLinks.map((link) => (
              <Link
                key={link.path}
                to={link.path}
                className={`navbar-mobile-link ${isActive(link.path) ? 'active' : ''}`}
                onClick={() => setMobileMenuOpen(false)}
              >
                {link.label}
              </Link>
            ))}
          </div>
        )}
      </div>

      <style jsx>{`
        .navbar {
          position: fixed;
          top: 0;
          left: 0;
          right: 0;
          z-index: 1000;
          background: rgba(10, 10, 15, 0.9);
          backdrop-filter: blur(20px);
          border-bottom: 1px solid rgba(255, 255, 255, 0.06);
        }

        .navbar-container {
          max-width: 1400px;
          margin: 0 auto;
          padding: 0 24px;
        }

        .navbar-content {
          display: flex;
          align-items: center;
          justify-content: space-between;
          height: 64px;
        }

        .navbar-logo {
          display: flex;
          align-items: center;
          gap: 10px;
          text-decoration: none;
        }

        .navbar-logo-icon {
          display: flex;
          align-items: center;
          justify-content: center;
          width: 36px;
          height: 36px;
          background: linear-gradient(135deg, #8b5cf6 0%, #06b6d4 100%);
          border-radius: 10px;
          color: white;
        }

        .navbar-logo-text {
          font-size: 20px;
          font-weight: 700;
          color: #f1f5f9;
          letter-spacing: -0.02em;
        }

        .navbar-links {
          display: flex;
          align-items: center;
          gap: 8px;
        }

        .navbar-link {
          padding: 8px 16px;
          font-size: 14px;
          font-weight: 500;
          color: #94a3b8;
          text-decoration: none;
          border-radius: 8px;
          transition: all 0.15s ease;
        }

        .navbar-link:hover {
          color: #e2e8f0;
          background: rgba(255, 255, 255, 0.05);
        }

        .navbar-link.active {
          color: #a78bfa;
          background: rgba(139, 92, 246, 0.15);
        }

        .navbar-link.highlight {
          color: #f1f5f9;
          background: linear-gradient(135deg, rgba(139, 92, 246, 0.2) 0%, rgba(6, 182, 212, 0.15) 100%);
          border: 1px solid rgba(139, 92, 246, 0.3);
        }

        .navbar-link.highlight:hover {
          background: linear-gradient(135deg, rgba(139, 92, 246, 0.3) 0%, rgba(6, 182, 212, 0.2) 100%);
        }

        .navbar-right {
          display: flex;
          align-items: center;
          gap: 16px;
        }

        .navbar-cta {
          display: flex;
          align-items: center;
          gap: 8px;
          padding: 10px 20px;
          font-size: 14px;
          font-weight: 600;
          color: white;
          background: linear-gradient(135deg, #8b5cf6 0%, #7c3aed 100%);
          border: none;
          border-radius: 10px;
          cursor: pointer;
          transition: all 0.2s ease;
        }

        .navbar-cta:hover {
          background: linear-gradient(135deg, #a78bfa 0%, #8b5cf6 100%);
          box-shadow: 0 8px 20px rgba(139, 92, 246, 0.3);
          transform: translateY(-1px);
        }

        .navbar-cta svg {
          width: 18px;
          height: 18px;
        }

        .navbar-mobile-toggle {
          display: none;
          align-items: center;
          justify-content: center;
          width: 40px;
          height: 40px;
          color: #94a3b8;
          background: transparent;
          border: none;
          cursor: pointer;
        }

        .navbar-mobile-menu {
          display: none;
          flex-direction: column;
          padding: 16px 0;
          border-top: 1px solid rgba(255, 255, 255, 0.06);
        }

        .navbar-mobile-link {
          padding: 12px 16px;
          font-size: 15px;
          font-weight: 500;
          color: #94a3b8;
          text-decoration: none;
          border-radius: 8px;
        }

        .navbar-mobile-link:hover,
        .navbar-mobile-link.active {
          color: #f1f5f9;
          background: rgba(255, 255, 255, 0.05);
        }

        @media (max-width: 768px) {
          .navbar-links {
            display: none;
          }

          .navbar-cta span {
            display: none;
          }

          .navbar-mobile-toggle {
            display: flex;
          }

          .navbar-mobile-menu {
            display: flex;
          }
        }
      `}</style>
    </nav>
  );
};

export default Navbar;
