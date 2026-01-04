/**
 * Dashboard Layout - Canva-inspired
 * Main application shell with sidebar navigation
 */

import React, { useState } from 'react';
import { Outlet, NavLink, useNavigate } from 'react-router-dom';
import './DashboardLayout.css';

// Icons
const HomeIcon = () => (
  <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
    <path d="M3 9l9-7 9 7v11a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2z" />
    <polyline points="9,22 9,12 15,12 15,22" />
  </svg>
);

const TemplatesIcon = () => (
  <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
    <rect x="3" y="3" width="18" height="18" rx="2" ry="2" />
    <line x1="3" y1="9" x2="21" y2="9" />
    <line x1="9" y1="21" x2="9" y2="9" />
  </svg>
);

const ProjectsIcon = () => (
  <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
    <path d="M22 19a2 2 0 0 1-2 2H4a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h5l2 3h9a2 2 0 0 1 2 2z" />
  </svg>
);

const BrandIcon = () => (
  <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
    <circle cx="12" cy="12" r="10" />
    <path d="M8 14s1.5 2 4 2 4-2 4-2" />
    <line x1="9" y1="9" x2="9.01" y2="9" />
    <line x1="15" y1="9" x2="15.01" y2="9" />
  </svg>
);

const AnalyzeIcon = () => (
  <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
    <path d="M3 7V5a2 2 0 0 1 2-2h2" />
    <path d="M17 3h2a2 2 0 0 1 2 2v2" />
    <path d="M21 17v2a2 2 0 0 1-2 2h-2" />
    <path d="M7 21H5a2 2 0 0 1-2-2v-2" />
    <circle cx="12" cy="12" r="4" />
    <path d="M12 8v1" />
    <path d="M12 15v1" />
    <path d="M8 12h1" />
    <path d="M15 12h1" />
  </svg>
);

const PlusIcon = () => (
  <svg width="20" height="20" viewBox="0 0 20 20" fill="none" stroke="currentColor" strokeWidth="2.5" strokeLinecap="round">
    <line x1="10" y1="4" x2="10" y2="16" />
    <line x1="4" y1="10" x2="16" y2="10" />
  </svg>
);

const SparklesIcon = () => (
  <svg width="20" height="20" viewBox="0 0 20 20" fill="currentColor">
    <path d="M10 2L11.5 6.5L16 8L11.5 9.5L10 14L8.5 9.5L4 8L8.5 6.5L10 2Z" />
    <path d="M15 12L15.75 14.25L18 15L15.75 15.75L15 18L14.25 15.75L12 15L14.25 14.25L15 12Z" opacity="0.7" />
  </svg>
);

const SearchIcon = () => (
  <svg width="20" height="20" viewBox="0 0 20 20" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round">
    <circle cx="9" cy="9" r="6" />
    <line x1="14" y1="14" x2="18" y2="18" />
  </svg>
);

const MenuIcon = () => (
  <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round">
    <line x1="3" y1="6" x2="21" y2="6" />
    <line x1="3" y1="12" x2="21" y2="12" />
    <line x1="3" y1="18" x2="21" y2="18" />
  </svg>
);

const DashboardLayout = () => {
  const [sidebarExpanded, setSidebarExpanded] = useState(true);
  const [searchQuery, setSearchQuery] = useState('');
  const navigate = useNavigate();

  const navItems = [
    { path: '/dashboard', icon: <HomeIcon />, label: 'Home' },
    { path: '/dashboard/templates', icon: <TemplatesIcon />, label: 'Templates' },
    { path: '/dashboard/projects', icon: <ProjectsIcon />, label: 'Projects' },
    { path: '/dashboard/brand-kit', icon: <BrandIcon />, label: 'Brand Kit' },
    { path: '/dashboard/analyze', icon: <AnalyzeIcon />, label: 'Analyze Design' },
  ];

  const handleCreateDesign = () => {
    navigate('/editor');
  };

  return (
    <div className="dashboard-layout">
      {/* Sidebar */}
      <aside className={`sidebar ${sidebarExpanded ? 'expanded' : 'collapsed'}`}>
        {/* Logo */}
        <div className="sidebar-header">
          <div className="logo" onClick={() => navigate('/dashboard')}>
            <div className="logo-icon">
              <SparklesIcon />
            </div>
            {sidebarExpanded && <span className="logo-text">AdGenesis</span>}
          </div>
          <button 
            className="sidebar-toggle"
            onClick={() => setSidebarExpanded(!sidebarExpanded)}
          >
            <MenuIcon />
          </button>
        </div>

        {/* Create Button */}
        <button className="create-button" onClick={handleCreateDesign}>
          <PlusIcon />
          {sidebarExpanded && <span>Create Design</span>}
        </button>

        {/* Navigation */}
        <nav className="sidebar-nav">
          {navItems.map((item) => (
            <NavLink
              key={item.path}
              to={item.path}
              className={({ isActive }) => `nav-item ${isActive ? 'active' : ''}`}
              end={item.path === '/dashboard'}
            >
              <span className="nav-icon">{item.icon}</span>
              {sidebarExpanded && <span className="nav-label">{item.label}</span>}
            </NavLink>
          ))}
        </nav>

        {/* Sidebar Footer */}
        <div className="sidebar-footer">
          {sidebarExpanded && (
            <div className="upgrade-card">
              <div className="upgrade-icon">✨</div>
              <div className="upgrade-content">
                <p className="upgrade-title">Upgrade to Pro</p>
                <p className="upgrade-desc">Unlock AI image generation</p>
              </div>
            </div>
          )}
        </div>
      </aside>

      {/* Main Content */}
      <main className="main-content">
        {/* Top Bar */}
        <header className="top-bar">
          <div className="search-container">
            <SearchIcon />
            <input
              type="text"
              placeholder="Search designs, templates..."
              value={searchQuery}
              onChange={(e) => setSearchQuery(e.target.value)}
              className="search-input"
            />
            <kbd className="search-shortcut">⌘K</kbd>
          </div>

          <div className="top-bar-actions">
            <button className="ai-button" onClick={handleCreateDesign}>
              <SparklesIcon />
              <span>AI Generate</span>
            </button>
            
            <div className="user-menu">
              <div className="avatar">
                <span>V</span>
              </div>
            </div>
          </div>
        </header>

        {/* Page Content */}
        <div className="page-content">
          <Outlet />
        </div>
      </main>
    </div>
  );
};

export default DashboardLayout;
