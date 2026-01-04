/**
 * AdGenesis - Premium Landing Page
 * Canva-inspired design with elegant aesthetics
 * Developed by Vikas TG
 */

import React, { useState, useEffect } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import './LandingPage.css';

// Logo Icon
const LogoIcon = () => (
  <svg width="40" height="40" viewBox="0 0 40 40" fill="none" xmlns="http://www.w3.org/2000/svg">
    <defs>
      <linearGradient id="logoGrad" x1="0%" y1="0%" x2="100%" y2="100%">
        <stop offset="0%" stopColor="#8B5CF6" />
        <stop offset="100%" stopColor="#06B6D4" />
      </linearGradient>
    </defs>
    <rect width="40" height="40" rx="12" fill="url(#logoGrad)" />
    <path d="M20 10L28 18L20 26L12 18L20 10Z" fill="white" fillOpacity="0.95" />
    <path d="M12 24L20 32L28 24" stroke="white" strokeWidth="2.5" strokeLinecap="round" strokeLinejoin="round" />
  </svg>
);

// Feature Icons
const SparkleIcon = () => (
  <svg width="32" height="32" viewBox="0 0 32 32" fill="none" stroke="currentColor" strokeWidth="2">
    <path d="M16 4L18.5 12L26 14L18.5 16L16 24L13.5 16L6 14L13.5 12L16 4Z" />
  </svg>
);

const TemplateIcon = () => (
  <svg width="32" height="32" viewBox="0 0 32 32" fill="none" stroke="currentColor" strokeWidth="2">
    <rect x="4" y="4" width="24" height="24" rx="3" />
    <line x1="4" y1="12" x2="28" y2="12" />
    <line x1="12" y1="12" x2="12" y2="28" />
  </svg>
);

const ImageGenIcon = () => (
  <svg width="32" height="32" viewBox="0 0 32 32" fill="none" stroke="currentColor" strokeWidth="2">
    <rect x="4" y="6" width="24" height="20" rx="3" />
    <circle cx="11" cy="13" r="3" />
    <path d="M28 22L22 16L10 26" />
  </svg>
);

const BrandIcon = () => (
  <svg width="32" height="32" viewBox="0 0 32 32" fill="none" stroke="currentColor" strokeWidth="2">
    <circle cx="16" cy="16" r="12" />
    <path d="M16 8V16L22 20" />
  </svg>
);

const CollabIcon = () => (
  <svg width="32" height="32" viewBox="0 0 32 32" fill="none" stroke="currentColor" strokeWidth="2">
    <circle cx="12" cy="12" r="5" />
    <circle cx="22" cy="14" r="4" />
    <path d="M4 26C4 22 7.5 19 12 19C14 19 15.8 19.6 17.2 20.6" />
    <path d="M18 26C18 23 20 21 22 21C24 21 28 22 28 26" />
  </svg>
);

const ExportIcon = () => (
  <svg width="32" height="32" viewBox="0 0 32 32" fill="none" stroke="currentColor" strokeWidth="2">
    <path d="M16 4V20" />
    <path d="M10 14L16 20L22 14" />
    <path d="M6 24H26" />
  </svg>
);

const ArrowRightIcon = () => (
  <svg width="20" height="20" viewBox="0 0 20 20" fill="none" stroke="currentColor" strokeWidth="2">
    <line x1="4" y1="10" x2="16" y2="10" />
    <polyline points="11,5 16,10 11,15" />
  </svg>
);

const PlayIcon = () => (
  <svg width="24" height="24" viewBox="0 0 24 24" fill="currentColor">
    <path d="M8 5v14l11-7z" />
  </svg>
);

// Sample template previews
const TEMPLATE_PREVIEWS = [
  { id: 1, name: 'Instagram Post', color: '#E91E63', size: '1080×1080' },
  { id: 2, name: 'YouTube Thumbnail', color: '#F44336', size: '1280×720' },
  { id: 3, name: 'Facebook Cover', color: '#2196F3', size: '1640×624' },
  { id: 4, name: 'Twitter Header', color: '#00BCD4', size: '1500×500' },
  { id: 5, name: 'LinkedIn Banner', color: '#0077B5', size: '1584×396' },
  { id: 6, name: 'Poster', color: '#9C27B0', size: '18×24 in' },
];

const FEATURES = [
  {
    icon: <SparkleIcon />,
    title: 'AI-Powered Design',
    description: 'Describe your vision and watch AI create stunning designs in seconds. Magic happens with just a prompt.',
    color: '#8B5CF6',
  },
  {
    icon: <TemplateIcon />,
    title: 'Professional Templates',
    description: 'Start with thousands of professionally designed templates for any occasion or platform.',
    color: '#06B6D4',
  },
  {
    icon: <ImageGenIcon />,
    title: 'Image Generation',
    description: 'Create unique images with AI. Generate backgrounds, illustrations, and graphics effortlessly.',
    color: '#10B981',
  },
  {
    icon: <BrandIcon />,
    title: 'Brand Kit',
    description: 'Keep your brand consistent. Store colors, fonts, and logos in one place for easy access.',
    color: '#F59E0B',
  },
  {
    icon: <CollabIcon />,
    title: 'Team Collaboration',
    description: 'Work together seamlessly. Share, comment, and edit designs with your team in real-time.',
    color: '#EC4899',
  },
  {
    icon: <ExportIcon />,
    title: 'Export Anywhere',
    description: 'Download in any format - PNG, JPG, PDF, SVG. Perfect for print or digital use.',
    color: '#3B82F6',
  },
];

const TESTIMONIALS = [
  {
    name: 'Sarah Chen',
    role: 'Marketing Director',
    company: 'TechStart Inc.',
    text: 'AdGenesis transformed our content creation process. What used to take hours now takes minutes.',
    avatar: 'SC',
  },
  {
    name: 'Michael Rivera',
    role: 'Freelance Designer',
    company: 'Self-employed',
    text: 'The AI features are incredible. It understands exactly what I need and delivers beautiful results.',
    avatar: 'MR',
  },
  {
    name: 'Emily Watson',
    role: 'Social Media Manager',
    company: 'BrandBoost Agency',
    text: 'Our social media engagement increased 3x after switching to AdGenesis. The templates are perfect.',
    avatar: 'EW',
  },
];

const LandingPage = () => {
  const navigate = useNavigate();
  const [mobileMenuOpen, setMobileMenuOpen] = useState(false);
  const [scrolled, setScrolled] = useState(false);

  useEffect(() => {
    const handleScroll = () => {
      setScrolled(window.scrollY > 20);
    };
    window.addEventListener('scroll', handleScroll);
    return () => window.removeEventListener('scroll', handleScroll);
  }, []);

  return (
    <div className="landing-page">
      {/* Navigation */}
      <nav className={`landing-nav ${scrolled ? 'scrolled' : ''}`}>
        <div className="nav-container">
          <Link to="/" className="nav-logo">
            <LogoIcon />
            <span className="logo-text">AdGenesis</span>
          </Link>

          <div className={`nav-links ${mobileMenuOpen ? 'open' : ''}`}>
            <Link to="/dashboard/templates" className="nav-link">Templates</Link>
            <Link to="/about" className="nav-link">Features</Link>
            <Link to="/about" className="nav-link">Pricing</Link>
            <Link to="/about" className="nav-link">About</Link>
          </div>

          <div className="nav-actions">
            <Link to="/dashboard" className="nav-signin">Sign in</Link>
            <Link to="/dashboard" className="nav-cta">
              Get Started Free
              <ArrowRightIcon />
            </Link>
          </div>

          <button 
            className="mobile-menu-btn"
            onClick={() => setMobileMenuOpen(!mobileMenuOpen)}
            aria-label="Toggle menu"
          >
            <span></span>
            <span></span>
            <span></span>
          </button>
        </div>
      </nav>

      {/* Hero Section */}
      <section className="hero-section">
        <div className="hero-bg-effects">
          <div className="hero-gradient-orb orb-1"></div>
          <div className="hero-gradient-orb orb-2"></div>
          <div className="hero-grid-pattern"></div>
        </div>

        <div className="hero-container">
          <div className="hero-content">
            <div className="hero-badge">
              <SparkleIcon />
              <span>Now with AI Image Generation</span>
            </div>

            <h1 className="hero-title">
              Where creativity
              <span className="gradient-text"> meets simplicity</span>
            </h1>

            <p className="hero-subtitle">
              Design stunning graphics, social media posts, presentations, and more 
              with AI-powered tools. No design skills needed.
            </p>

            <div className="hero-cta-group">
              <button 
                className="hero-cta primary"
                onClick={() => navigate('/dashboard')}
              >
                Start Designing
                <ArrowRightIcon />
              </button>
              <button className="hero-cta secondary">
                <PlayIcon />
                Watch Demo
              </button>
            </div>

            <div className="hero-stats">
              <div className="stat">
                <span className="stat-value">10K+</span>
                <span className="stat-label">Templates</span>
              </div>
              <div className="stat-divider"></div>
              <div className="stat">
                <span className="stat-value">50K+</span>
                <span className="stat-label">Users</span>
              </div>
              <div className="stat-divider"></div>
              <div className="stat">
                <span className="stat-value">4.9★</span>
                <span className="stat-label">Rating</span>
              </div>
            </div>
          </div>

          <div className="hero-visual">
            <div className="hero-mockup">
              <div className="mockup-header">
                <div className="mockup-dots">
                  <span></span>
                  <span></span>
                  <span></span>
                </div>
                <span className="mockup-title">AdGenesis Editor</span>
              </div>
              <div className="mockup-content">
                <div className="mockup-sidebar">
                  <div className="mock-item"></div>
                  <div className="mock-item"></div>
                  <div className="mock-item"></div>
                  <div className="mock-item"></div>
                </div>
                <div className="mockup-canvas">
                  <div className="mock-design">
                    <div className="mock-heading"></div>
                    <div className="mock-text"></div>
                    <div className="mock-image"></div>
                  </div>
                </div>
              </div>
            </div>
            <div className="floating-card card-1">
              <SparkleIcon />
              <span>AI Generated</span>
            </div>
            <div className="floating-card card-2">
              <span className="check">✓</span>
              <span>Design Ready</span>
            </div>
          </div>
        </div>
      </section>

      {/* Templates Preview Section */}
      <section className="templates-section">
        <div className="section-container">
          <div className="section-header">
            <h2 className="section-title">Templates for anything you need</h2>
            <p className="section-subtitle">
              Start with professionally designed templates and customize to make them your own
            </p>
          </div>

          <div className="templates-carousel">
            {TEMPLATE_PREVIEWS.map((template) => (
              <div 
                key={template.id} 
                className="template-card"
                style={{ '--card-color': template.color }}
              >
                <div className="template-preview">
                  <div className="template-placeholder" style={{ background: template.color }}>
                    <span>{template.name.charAt(0)}</span>
                  </div>
                </div>
                <div className="template-info">
                  <h4>{template.name}</h4>
                  <span className="template-size">{template.size}</span>
                </div>
              </div>
            ))}
          </div>

          <div className="templates-cta">
            <Link to="/dashboard/templates" className="browse-templates-btn">
              Browse all templates
              <ArrowRightIcon />
            </Link>
          </div>
        </div>
      </section>

      {/* AI Generator Section */}
      <section className="ai-section">
        <div className="section-container">
          <div className="ai-content">
            <div className="ai-text">
              <span className="ai-badge">✨ AI Magic</span>
              <h2 className="ai-title">Create with the power of AI</h2>
              <p className="ai-description">
                Simply describe what you want, and watch as AI transforms your words 
                into stunning visuals. Generate complete designs, images, or get smart 
                suggestions instantly.
              </p>
              <ul className="ai-features">
                <li>
                  <span className="check-icon">✓</span>
                  Text-to-design generation
                </li>
                <li>
                  <span className="check-icon">✓</span>
                  AI image creation
                </li>
                <li>
                  <span className="check-icon">✓</span>
                  Smart layout suggestions
                </li>
                <li>
                  <span className="check-icon">✓</span>
                  Auto color schemes
                </li>
              </ul>
              <button 
                className="ai-cta"
                onClick={() => navigate('/editor')}
              >
                Try AI Generator
                <ArrowRightIcon />
              </button>
            </div>
            <div className="ai-visual">
              <div className="ai-demo">
                <div className="ai-prompt-box">
                  <span className="ai-icon">🪄</span>
                  <div className="ai-typing">
                    Create a modern poster for a tech startup...
                    <span className="cursor">|</span>
                  </div>
                </div>
                <div className="ai-result">
                  <div className="result-preview">
                    <div className="result-gradient"></div>
                  </div>
                  <span className="generating">✨ Generated in 3 seconds</span>
                </div>
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* Features Section */}
      <section className="features-section">
        <div className="section-container">
          <div className="section-header">
            <h2 className="section-title">Everything you need to create</h2>
            <p className="section-subtitle">
              Powerful features that make design accessible to everyone
            </p>
          </div>

          <div className="features-grid">
            {FEATURES.map((feature, index) => (
              <div 
                key={index} 
                className="feature-card"
                style={{ '--feature-color': feature.color }}
              >
                <div className="feature-icon" style={{ color: feature.color }}>
                  {feature.icon}
                </div>
                <h3 className="feature-title">{feature.title}</h3>
                <p className="feature-description">{feature.description}</p>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* Testimonials Section */}
      <section className="testimonials-section">
        <div className="section-container">
          <div className="section-header">
            <h2 className="section-title">Loved by creators worldwide</h2>
            <p className="section-subtitle">
              See what our users have to say about their experience
            </p>
          </div>

          <div className="testimonials-grid">
            {TESTIMONIALS.map((testimonial, index) => (
              <div key={index} className="testimonial-card">
                <p className="testimonial-text">"{testimonial.text}"</p>
                <div className="testimonial-author">
                  <div className="author-avatar">
                    {testimonial.avatar}
                  </div>
                  <div className="author-info">
                    <span className="author-name">{testimonial.name}</span>
                    <span className="author-role">{testimonial.role}</span>
                  </div>
                </div>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* CTA Section */}
      <section className="cta-section">
        <div className="cta-container">
          <div className="cta-content">
            <h2>Ready to create something amazing?</h2>
            <p>Join thousands of creators who trust AdGenesis for their design needs.</p>
            <button 
              className="cta-button"
              onClick={() => navigate('/dashboard')}
            >
              Start Creating for Free
              <ArrowRightIcon />
            </button>
          </div>
        </div>
      </section>

      {/* Footer */}
      <footer className="landing-footer">
        <div className="footer-container">
          <div className="footer-main">
            <div className="footer-brand">
              <div className="footer-logo">
                <LogoIcon />
                <span>AdGenesis</span>
              </div>
              <p className="footer-tagline">
                Design made simple. Create stunning visuals with AI-powered tools.
              </p>
              <div className="footer-social">
                <button type="button" aria-label="Twitter" className="social-link">
                  <svg viewBox="0 0 24 24" fill="currentColor"><path d="M18.244 2.25h3.308l-7.227 8.26 8.502 11.24H16.17l-5.214-6.817L4.99 21.75H1.68l7.73-8.835L1.254 2.25H8.08l4.713 6.231zm-1.161 17.52h1.833L7.084 4.126H5.117z"/></svg>
                </button>
                <button type="button" aria-label="Instagram" className="social-link">
                  <svg viewBox="0 0 24 24" fill="currentColor"><path d="M12 2c2.717 0 3.056.01 4.122.06 1.065.05 1.79.217 2.428.465.66.254 1.216.598 1.772 1.153.509.5.902 1.105 1.153 1.772.247.637.415 1.363.465 2.428.047 1.066.06 1.405.06 4.122 0 2.717-.01 3.056-.06 4.122-.05 1.065-.218 1.79-.465 2.428a4.883 4.883 0 01-1.153 1.772c-.5.508-1.105.902-1.772 1.153-.637.247-1.363.415-2.428.465-1.066.047-1.405.06-4.122.06-2.717 0-3.056-.01-4.122-.06-1.065-.05-1.79-.218-2.428-.465a4.89 4.89 0 01-1.772-1.153 4.904 4.904 0 01-1.153-1.772c-.248-.637-.415-1.363-.465-2.428C2.013 15.056 2 14.717 2 12c0-2.717.01-3.056.06-4.122.05-1.066.217-1.79.465-2.428a4.88 4.88 0 011.153-1.772A4.897 4.897 0 015.45 2.525c.638-.248 1.362-.415 2.428-.465C8.944 2.013 9.283 2 12 2zm0 5a5 5 0 100 10 5 5 0 000-10zm6.5-.25a1.25 1.25 0 10-2.5 0 1.25 1.25 0 002.5 0zM12 9a3 3 0 110 6 3 3 0 010-6z"/></svg>
                </button>
                <button type="button" aria-label="LinkedIn" className="social-link">
                  <svg viewBox="0 0 24 24" fill="currentColor"><path d="M20.5 2h-17A1.5 1.5 0 002 3.5v17A1.5 1.5 0 003.5 22h17a1.5 1.5 0 001.5-1.5v-17A1.5 1.5 0 0020.5 2zM8 19H5v-9h3zM6.5 8.25A1.75 1.75 0 118.3 6.5a1.78 1.78 0 01-1.8 1.75zM19 19h-3v-4.74c0-1.42-.6-1.93-1.38-1.93A1.74 1.74 0 0013 14.19a.66.66 0 000 .14V19h-3v-9h2.9v1.3a3.11 3.11 0 012.7-1.4c1.55 0 3.36.86 3.36 3.66z"/></svg>
                </button>
                <button type="button" aria-label="YouTube" className="social-link">
                  <svg viewBox="0 0 24 24" fill="currentColor"><path d="M23.498 6.186a3.016 3.016 0 00-2.122-2.136C19.505 3.545 12 3.545 12 3.545s-7.505 0-9.377.505A3.017 3.017 0 00.502 6.186C0 8.07 0 12 0 12s0 3.93.502 5.814a3.016 3.016 0 002.122 2.136c1.871.505 9.376.505 9.376.505s7.505 0 9.377-.505a3.015 3.015 0 002.122-2.136C24 15.93 24 12 24 12s0-3.93-.502-5.814zM9.545 15.568V8.432L15.818 12l-6.273 3.568z"/></svg>
                </button>
              </div>
            </div>

            <div className="footer-links-grid">
              <div className="footer-column">
                <h4>Product</h4>
                <ul>
                  <li><Link to="/features">Features</Link></li>
                  <li><Link to="/templates">Templates</Link></li>
                  <li><Link to="/pricing">Pricing</Link></li>
                  <li><Link to="/">AI Generator</Link></li>
                </ul>
              </div>
              <div className="footer-column">
                <h4>Company</h4>
                <ul>
                  <li><Link to="/about">About Us</Link></li>
                  <li><Link to="/careers">Careers</Link></li>
                  <li><Link to="/blog">Blog</Link></li>
                  <li><Link to="/press">Press</Link></li>
                </ul>
              </div>
              <div className="footer-column">
                <h4>Resources</h4>
                <ul>
                  <li><Link to="/help">Help Center</Link></li>
                  <li><Link to="/tutorials">Tutorials</Link></li>
                  <li><Link to="/api">API</Link></li>
                  <li><Link to="/community">Community</Link></li>
                </ul>
              </div>
              <div className="footer-column">
                <h4>Legal</h4>
                <ul>
                  <li><Link to="/privacy">Privacy Policy</Link></li>
                  <li><Link to="/terms">Terms of Service</Link></li>
                  <li><Link to="/cookies">Cookie Policy</Link></li>
                  <li><Link to="/security">Security</Link></li>
                </ul>
              </div>
            </div>
          </div>

          <div className="footer-bottom">
            <div className="footer-copyright">
              <p>© {new Date().getFullYear()} AdGenesis. All rights reserved.</p>
              <p className="footer-developer">
                Developed with ❤️ by <strong>Vikas TG</strong>
              </p>
            </div>
            <div className="footer-locale">
              <select className="locale-select">
                <option value="en">🌐 English</option>
                <option value="es">🌐 Español</option>
                <option value="fr">🌐 Français</option>
              </select>
            </div>
          </div>
        </div>
      </footer>
    </div>
  );
};

export default LandingPage;
