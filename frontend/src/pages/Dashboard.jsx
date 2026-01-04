/**
 * Dashboard - Canva-inspired Home Page
 * Shows recent designs, templates, and quick actions
 */

import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { useQuery } from 'react-query';
import { getDesigns } from '../services/api';
import './Dashboard.css';

// Icons
const SparklesIcon = () => (
  <svg width="24" height="24" viewBox="0 0 24 24" fill="currentColor">
    <path d="M12 2L14.5 8.5L21 10L14.5 11.5L12 18L9.5 11.5L3 10L9.5 8.5L12 2Z" />
  </svg>
);

const ImageIcon = () => (
  <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
    <rect x="3" y="3" width="18" height="18" rx="2" />
    <circle cx="8.5" cy="8.5" r="1.5" />
    <path d="M21 15l-5-5L5 21" />
  </svg>
);

const VideoIcon = () => (
  <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
    <rect x="2" y="4" width="20" height="16" rx="2" />
    <path d="M10 9l5 3-5 3V9z" fill="currentColor" />
  </svg>
);

const PresentationIcon = () => (
  <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
    <rect x="2" y="3" width="20" height="14" rx="2" />
    <line x1="8" y1="21" x2="16" y2="21" />
    <line x1="12" y1="17" x2="12" y2="21" />
  </svg>
);

const SocialIcon = () => (
  <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
    <rect x="2" y="2" width="20" height="20" rx="5" />
    <line x1="8" y1="12" x2="16" y2="12" />
    <line x1="12" y1="8" x2="12" y2="16" />
  </svg>
);

const PrintIcon = () => (
  <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
    <path d="M6 9V2h12v7" />
    <path d="M6 18H4a2 2 0 01-2-2v-5a2 2 0 012-2h16a2 2 0 012 2v5a2 2 0 01-2 2h-2" />
    <rect x="6" y="14" width="12" height="8" />
  </svg>
);

const ArrowRightIcon = () => (
  <svg width="20" height="20" viewBox="0 0 20 20" fill="none" stroke="currentColor" strokeWidth="2">
    <line x1="4" y1="10" x2="16" y2="10" />
    <polyline points="11,5 16,10 11,15" />
  </svg>
);

const CloseIcon = () => (
  <svg width="20" height="20" viewBox="0 0 20 20" fill="none" stroke="currentColor" strokeWidth="2">
    <line x1="15" y1="5" x2="5" y2="15" />
    <line x1="5" y1="5" x2="15" y2="15" />
  </svg>
);

const LightbulbIcon = () => (
  <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
    <path d="M9 18h6M10 22h4M12 2v1M4.93 4.93l.7.7M2 12h1M20 12h1M18.36 5.64l-.7.7M16 6a4 4 0 10-3 6.83V16H11v-3.17a4 4 0 01-3-3.83z" />
  </svg>
);

// Quick tips for new users
const QUICK_TIPS = [
  { icon: '🎨', title: 'Create with AI', desc: 'Describe your design and let AI generate it for you' },
  { icon: '📐', title: 'Choose a size', desc: 'Start with preset sizes for social media, print, and more' },
  { icon: '📋', title: 'Use templates', desc: 'Browse our template gallery for inspiration' },
  { icon: '⌨️', title: 'Keyboard shortcuts', desc: 'Press ? in the editor to see all shortcuts' },
];

// Design size presets
const DESIGN_CATEGORIES = [
  {
    id: 'social',
    name: 'Social Media',
    icon: <SocialIcon />,
    color: '#E91E63',
    sizes: [
      { name: 'Instagram Post', width: 1080, height: 1080 },
      { name: 'Instagram Story', width: 1080, height: 1920 },
      { name: 'Facebook Post', width: 1200, height: 630 },
      { name: 'Twitter Post', width: 1600, height: 900 },
      { name: 'LinkedIn Post', width: 1200, height: 627 },
    ],
  },
  {
    id: 'video',
    name: 'Video',
    icon: <VideoIcon />,
    color: '#FF5722',
    sizes: [
      { name: 'YouTube Thumbnail', width: 1280, height: 720 },
      { name: 'Video (16:9)', width: 1920, height: 1080 },
      { name: 'TikTok Video', width: 1080, height: 1920 },
    ],
  },
  {
    id: 'presentation',
    name: 'Presentation',
    icon: <PresentationIcon />,
    color: '#2196F3',
    sizes: [
      { name: 'Presentation (16:9)', width: 1920, height: 1080 },
      { name: 'Presentation (4:3)', width: 1024, height: 768 },
    ],
  },
  {
    id: 'print',
    name: 'Print',
    icon: <PrintIcon />,
    color: '#4CAF50',
    sizes: [
      { name: 'Poster', width: 1587, height: 2245 },
      { name: 'Flyer', width: 1275, height: 1650 },
      { name: 'Business Card', width: 1050, height: 600 },
      { name: 'A4 Document', width: 2480, height: 3508 },
    ],
  },
];

// Featured templates (mock data)
const FEATURED_TEMPLATES = [
  {
    id: 1,
    name: 'Modern Product Launch',
    category: 'Marketing',
    thumbnail: 'https://images.unsplash.com/photo-1611532736597-de2d4265fba3?w=400&h=400&fit=crop',
    color: '#8B5CF6',
  },
  {
    id: 2,
    name: 'Tech Startup Promo',
    category: 'Business',
    thumbnail: 'https://images.unsplash.com/photo-1518770660439-4636190af475?w=400&h=400&fit=crop',
    color: '#06B6D4',
  },
  {
    id: 3,
    name: 'Fashion Sale',
    category: 'Retail',
    thumbnail: 'https://images.unsplash.com/photo-1441984904996-e0b6ba687e04?w=400&h=400&fit=crop',
    color: '#F59E0B',
  },
  {
    id: 4,
    name: 'Food Delivery',
    category: 'Food & Drink',
    thumbnail: 'https://images.unsplash.com/photo-1504674900247-0877df9cc836?w=400&h=400&fit=crop',
    color: '#EF4444',
  },
  {
    id: 5,
    name: 'Fitness Motivation',
    category: 'Health',
    thumbnail: 'https://images.unsplash.com/photo-1534438327276-14e5300c3a48?w=400&h=400&fit=crop',
    color: '#10B981',
  },
  {
    id: 6,
    name: 'Event Announcement',
    category: 'Events',
    thumbnail: 'https://images.unsplash.com/photo-1492684223066-81342ee5ff30?w=400&h=400&fit=crop',
    color: '#EC4899',
  },
];

const Dashboard = () => {
  const navigate = useNavigate();
  const [selectedCategory, setSelectedCategory] = useState(null);
  const [showWelcome, setShowWelcome] = useState(false);
  
  // Check if first-time user
  useEffect(() => {
    const hasSeenWelcome = localStorage.getItem('adgenesis_welcome_seen');
    if (!hasSeenWelcome) {
      setShowWelcome(true);
    }
  }, []);
  
  const dismissWelcome = () => {
    localStorage.setItem('adgenesis_welcome_seen', 'true');
    setShowWelcome(false);
  };
  
  // Fetch recent designs
  const { data: recentDesigns, isLoading } = useQuery('designs', getDesigns);

  const handleCreateWithAI = () => {
    navigate('/editor', { state: { mode: 'ai' } });
  };

  const handleCreateWithSize = (category, size) => {
    navigate('/editor', { 
      state: { 
        width: size.width, 
        height: size.height,
        name: size.name,
        category: category.name
      } 
    });
  };

  const handleOpenDesign = (designId) => {
    navigate(`/editor/${designId}`);
  };

  const handleUseTemplate = (template) => {
    navigate('/editor', { state: { templateId: template.id } });
  };

  return (
    <div className="dashboard">
      {/* Welcome Banner for New Users */}
      {showWelcome && (
        <div className="welcome-banner">
          <button className="welcome-dismiss" onClick={dismissWelcome}>
            <CloseIcon />
          </button>
          <div className="welcome-content">
            <div className="welcome-icon">
              <LightbulbIcon />
            </div>
            <div className="welcome-text">
              <h2>Welcome to AdGenesis! 🎉</h2>
              <p>Create stunning designs in minutes. Here are some quick tips to get you started:</p>
            </div>
          </div>
          <div className="welcome-tips">
            {QUICK_TIPS.map((tip, index) => (
              <div key={index} className="welcome-tip">
                <span className="tip-icon">{tip.icon}</span>
                <div className="tip-content">
                  <strong>{tip.title}</strong>
                  <span>{tip.desc}</span>
                </div>
              </div>
            ))}
          </div>
          <button className="welcome-start" onClick={dismissWelcome}>
            <SparklesIcon />
            Get Started
          </button>
        </div>
      )}

      {/* Hero Section */}
      <section className="dashboard-hero">
        <div className="hero-content">
          <h1 className="hero-title">
            What will you <span className="gradient-text">design</span> today?
          </h1>
          <p className="hero-subtitle">
            Create stunning ads with AI-powered design generation
          </p>
          
          <button className="hero-cta" onClick={handleCreateWithAI}>
            <SparklesIcon />
            <span>Create with AI</span>
            <ArrowRightIcon />
          </button>
        </div>
        
        <div className="hero-visual">
          <div className="hero-cards">
            <div className="hero-card card-1">
              <img src="https://images.unsplash.com/photo-1563986768609-322da13575f3?w=300&h=300&fit=crop" alt="Design 1" />
            </div>
            <div className="hero-card card-2">
              <img src="https://images.unsplash.com/photo-1561070791-2526d30994b5?w=300&h=300&fit=crop" alt="Design 2" />
            </div>
            <div className="hero-card card-3">
              <img src="https://images.unsplash.com/photo-1558655146-9f40138edfeb?w=300&h=300&fit=crop" alt="Design 3" />
            </div>
          </div>
        </div>
      </section>

      {/* Quick Start */}
      <section className="dashboard-section">
        <div className="section-header">
          <h2 className="section-title">Start designing</h2>
          <a href="/dashboard/templates" className="section-link">
            See all <ArrowRightIcon />
          </a>
        </div>
        
        <div className="category-grid">
          {DESIGN_CATEGORIES.map((category) => (
            <div
              key={category.id}
              className={`category-card ${selectedCategory?.id === category.id ? 'active' : ''}`}
              onClick={() => setSelectedCategory(
                selectedCategory?.id === category.id ? null : category
              )}
              style={{ '--category-color': category.color }}
            >
              <div className="category-icon">
                {category.icon}
              </div>
              <span className="category-name">{category.name}</span>
            </div>
          ))}
        </div>

        {/* Size picker dropdown */}
        {selectedCategory && (
          <div className="size-picker animate-fadeInUp">
            <div className="size-picker-header">
              <h3>Choose a {selectedCategory.name} size</h3>
              <button 
                className="size-picker-close"
                onClick={() => setSelectedCategory(null)}
              >
                ×
              </button>
            </div>
            <div className="size-list">
              {selectedCategory.sizes.map((size, index) => (
                <button
                  key={index}
                  className="size-item"
                  onClick={() => handleCreateWithSize(selectedCategory, size)}
                >
                  <div className="size-preview" style={{
                    aspectRatio: `${size.width} / ${size.height}`,
                    maxWidth: size.width > size.height ? '60px' : '40px',
                  }} />
                  <div className="size-info">
                    <span className="size-name">{size.name}</span>
                    <span className="size-dimensions">{size.width} × {size.height} px</span>
                  </div>
                </button>
              ))}
            </div>
          </div>
        )}
      </section>

      {/* Recent Designs */}
      <section className="dashboard-section">
        <div className="section-header">
          <h2 className="section-title">Recent designs</h2>
          <a href="/dashboard/projects" className="section-link">
            See all <ArrowRightIcon />
          </a>
        </div>
        
        <div className="designs-grid">
          {isLoading ? (
            // Skeleton loaders
            Array.from({ length: 4 }).map((_, i) => (
              <div key={i} className="design-card skeleton">
                <div className="design-thumbnail skeleton" />
                <div className="design-info">
                  <div className="skeleton" style={{ width: '60%', height: '16px' }} />
                  <div className="skeleton" style={{ width: '40%', height: '12px', marginTop: '8px' }} />
                </div>
              </div>
            ))
          ) : recentDesigns?.length > 0 ? (
            recentDesigns.slice(0, 8).map((design) => (
              <div
                key={design.id}
                className="design-card"
                onClick={() => handleOpenDesign(design.id)}
              >
                <div className="design-thumbnail">
                  {design.preview_url ? (
                    <img src={design.preview_url} alt={design.prompt} />
                  ) : (
                    <div className="design-placeholder">
                      <ImageIcon />
                    </div>
                  )}
                  <div className="design-overlay">
                    <span>Edit design</span>
                  </div>
                </div>
                <div className="design-info">
                  <h4 className="design-name">{design.prompt?.slice(0, 30) || 'Untitled'}</h4>
                  <span className="design-date">
                    {new Date(design.created_at).toLocaleDateString()}
                  </span>
                </div>
              </div>
            ))
          ) : (
            <div className="empty-state">
              <ImageIcon />
              <h3>No designs yet</h3>
              <p>Create your first design to get started</p>
              <button className="empty-cta" onClick={handleCreateWithAI}>
                <SparklesIcon />
                Create with AI
              </button>
            </div>
          )}
        </div>
      </section>

      {/* Templates */}
      <section className="dashboard-section">
        <div className="section-header">
          <h2 className="section-title">Featured templates</h2>
          <a href="/dashboard/templates" className="section-link">
            Browse all <ArrowRightIcon />
          </a>
        </div>
        
        <div className="templates-grid">
          {FEATURED_TEMPLATES.map((template) => (
            <div
              key={template.id}
              className="template-card"
              onClick={() => handleUseTemplate(template)}
            >
              <div className="template-thumbnail">
                <img src={template.thumbnail} alt={template.name} />
                <div className="template-overlay">
                  <button className="template-use-btn">Use template</button>
                </div>
              </div>
              <div className="template-info">
                <h4 className="template-name">{template.name}</h4>
                <span className="template-category">{template.category}</span>
              </div>
            </div>
          ))}
        </div>
      </section>
    </div>
  );
};

export default Dashboard;
