/**
 * AdGenesis - About Page
 * Company information and mission
 * Developed by Vikas TG
 */

import React from 'react';
import { Link } from 'react-router-dom';
import './AboutPage.css';

// Logo Icon
const LogoIcon = () => (
  <svg width="40" height="40" viewBox="0 0 40 40" fill="none" xmlns="http://www.w3.org/2000/svg">
    <defs>
      <linearGradient id="logoGradAbout" x1="0%" y1="0%" x2="100%" y2="100%">
        <stop offset="0%" stopColor="#8B5CF6" />
        <stop offset="100%" stopColor="#06B6D4" />
      </linearGradient>
    </defs>
    <rect width="40" height="40" rx="12" fill="url(#logoGradAbout)" />
    <path d="M20 10L28 18L20 26L12 18L20 10Z" fill="white" fillOpacity="0.95" />
    <path d="M12 24L20 32L28 24" stroke="white" strokeWidth="2.5" strokeLinecap="round" strokeLinejoin="round" />
  </svg>
);

const ArrowRightIcon = () => (
  <svg width="20" height="20" viewBox="0 0 20 20" fill="none" stroke="currentColor" strokeWidth="2">
    <line x1="4" y1="10" x2="16" y2="10" />
    <polyline points="11,5 16,10 11,15" />
  </svg>
);

// Values data
const VALUES = [
  {
    icon: '🎯',
    title: 'Simplicity First',
    description: 'We believe great design tools should be intuitive. No steep learning curves—just start creating.',
  },
  {
    icon: '✨',
    title: 'AI for Everyone',
    description: 'Democratizing AI-powered design. Professional results without professional training.',
  },
  {
    icon: '🚀',
    title: 'Innovation',
    description: 'Constantly pushing boundaries with cutting-edge technology to empower creators worldwide.',
  },
  {
    icon: '💜',
    title: 'User-Centric',
    description: 'Every feature we build starts with understanding and solving real user needs.',
  },
];

const STATS = [
  { value: '50K+', label: 'Active Users' },
  { value: '10K+', label: 'Templates' },
  { value: '1M+', label: 'Designs Created' },
  { value: '4.9', label: 'User Rating' },
];

const AboutPage = () => {
  return (
    <div className="about-page">
      {/* Navigation */}
      <nav className="about-nav">
        <div className="nav-container">
          <Link to="/" className="nav-logo">
            <LogoIcon />
            <span className="logo-text">AdGenesis</span>
          </Link>

          <div className="nav-links">
            <Link to="/landing" className="nav-link">Home</Link>
            <Link to="/templates" className="nav-link">Templates</Link>
            <Link to="/pricing" className="nav-link">Pricing</Link>
            <Link to="/about" className="nav-link active">About</Link>
          </div>

          <div className="nav-actions">
            <Link to="/" className="nav-cta">
              Get Started
              <ArrowRightIcon />
            </Link>
          </div>
        </div>
      </nav>

      {/* Hero Section */}
      <section className="about-hero">
        <div className="hero-bg-effects">
          <div className="gradient-orb orb-1"></div>
          <div className="gradient-orb orb-2"></div>
        </div>
        <div className="hero-container">
          <span className="about-badge">About AdGenesis</span>
          <h1 className="hero-title">
            Empowering creativity
            <span className="gradient-text"> for everyone</span>
          </h1>
          <p className="hero-subtitle">
            We're building the future of design—where AI meets human creativity 
            to make professional-quality visuals accessible to all.
          </p>
        </div>
      </section>

      {/* Stats Section */}
      <section className="stats-section">
        <div className="stats-container">
          {STATS.map((stat, index) => (
            <div key={index} className="stat-item">
              <span className="stat-value">{stat.value}</span>
              <span className="stat-label">{stat.label}</span>
            </div>
          ))}
        </div>
      </section>

      {/* Mission Section */}
      <section className="mission-section">
        <div className="section-container">
          <div className="mission-content">
            <h2 className="section-title">Our Mission</h2>
            <p className="mission-text">
              At AdGenesis, we believe that great design shouldn't be limited to those with years of 
              training or expensive software. Our mission is to democratize design by combining the 
              power of artificial intelligence with intuitive tools that anyone can use.
            </p>
            <p className="mission-text">
              We're not just building a design tool—we're creating a platform that understands your 
              vision and helps bring it to life. Whether you're a small business owner creating social 
              media content, a marketer launching a campaign, or a creator expressing your ideas, 
              AdGenesis is here to make your designs shine.
            </p>
          </div>
          <div className="mission-visual">
            <div className="visual-card">
              <div className="visual-content">
                <div className="visual-icon">🎨</div>
                <span>Design Made Simple</span>
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* Values Section */}
      <section className="values-section">
        <div className="section-container">
          <div className="section-header">
            <h2 className="section-title">Our Values</h2>
            <p className="section-subtitle">
              The principles that guide everything we do
            </p>
          </div>
          <div className="values-grid">
            {VALUES.map((value, index) => (
              <div key={index} className="value-card">
                <span className="value-icon">{value.icon}</span>
                <h3 className="value-title">{value.title}</h3>
                <p className="value-description">{value.description}</p>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* Team Section */}
      <section className="team-section">
        <div className="section-container">
          <div className="section-header">
            <h2 className="section-title">Meet the Creator</h2>
            <p className="section-subtitle">
              The person behind AdGenesis
            </p>
          </div>
          <div className="team-content">
            <div className="team-card founder-card">
              <div className="member-avatar">
                <span>VT</span>
              </div>
              <div className="member-info">
                <h3 className="member-name">Vikas TG</h3>
                <span className="member-role">Founder & Developer</span>
                <p className="member-bio">
                  Full-stack developer passionate about creating tools that empower creativity. 
                  With a background in AI and web development, Vikas built AdGenesis to make 
                  professional design accessible to everyone.
                </p>
                <div className="member-social">
                  <button type="button" className="social-link" aria-label="GitHub">
                    <svg viewBox="0 0 24 24" fill="currentColor"><path d="M12 0c-6.626 0-12 5.373-12 12 0 5.302 3.438 9.8 8.207 11.387.599.111.793-.261.793-.577v-2.234c-3.338.726-4.033-1.416-4.033-1.416-.546-1.387-1.333-1.756-1.333-1.756-1.089-.745.083-.729.083-.729 1.205.084 1.839 1.237 1.839 1.237 1.07 1.834 2.807 1.304 3.492.997.107-.775.418-1.305.762-1.604-2.665-.305-5.467-1.334-5.467-5.931 0-1.311.469-2.381 1.236-3.221-.124-.303-.535-1.524.117-3.176 0 0 1.008-.322 3.301 1.23.957-.266 1.983-.399 3.003-.404 1.02.005 2.047.138 3.006.404 2.291-1.552 3.297-1.23 3.297-1.23.653 1.653.242 2.874.118 3.176.77.84 1.235 1.911 1.235 3.221 0 4.609-2.807 5.624-5.479 5.921.43.372.823 1.102.823 2.222v3.293c0 .319.192.694.801.576 4.765-1.589 8.199-6.086 8.199-11.386 0-6.627-5.373-12-12-12z"/></svg>
                  </button>
                  <button type="button" className="social-link" aria-label="LinkedIn">
                    <svg viewBox="0 0 24 24" fill="currentColor"><path d="M20.5 2h-17A1.5 1.5 0 002 3.5v17A1.5 1.5 0 003.5 22h17a1.5 1.5 0 001.5-1.5v-17A1.5 1.5 0 0020.5 2zM8 19H5v-9h3zM6.5 8.25A1.75 1.75 0 118.3 6.5a1.78 1.78 0 01-1.8 1.75zM19 19h-3v-4.74c0-1.42-.6-1.93-1.38-1.93A1.74 1.74 0 0013 14.19a.66.66 0 000 .14V19h-3v-9h2.9v1.3a3.11 3.11 0 012.7-1.4c1.55 0 3.36.86 3.36 3.66z"/></svg>
                  </button>
                  <button type="button" className="social-link" aria-label="Twitter">
                    <svg viewBox="0 0 24 24" fill="currentColor"><path d="M18.244 2.25h3.308l-7.227 8.26 8.502 11.24H16.17l-5.214-6.817L4.99 21.75H1.68l7.73-8.835L1.254 2.25H8.08l4.713 6.231zm-1.161 17.52h1.833L7.084 4.126H5.117z"/></svg>
                  </button>
                </div>
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* CTA Section */}
      <section className="about-cta">
        <div className="cta-container">
          <h2>Ready to start creating?</h2>
          <p>Join thousands of creators using AdGenesis to bring their ideas to life.</p>
          <Link to="/" className="cta-button">
            Start Creating for Free
            <ArrowRightIcon />
          </Link>
        </div>
      </section>

      {/* Footer */}
      <footer className="about-footer">
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
            </div>
            <div className="footer-links-grid">
              <div className="footer-column">
                <h4>Product</h4>
                <ul>
                  <li><Link to="/">Features</Link></li>
                  <li><Link to="/templates">Templates</Link></li>
                  <li><Link to="/pricing">Pricing</Link></li>
                </ul>
              </div>
              <div className="footer-column">
                <h4>Company</h4>
                <ul>
                  <li><Link to="/about">About Us</Link></li>
                  <li><Link to="/blog">Blog</Link></li>
                  <li><Link to="/careers">Careers</Link></li>
                </ul>
              </div>
              <div className="footer-column">
                <h4>Legal</h4>
                <ul>
                  <li><Link to="/privacy">Privacy</Link></li>
                  <li><Link to="/terms">Terms</Link></li>
                  <li><Link to="/cookies">Cookies</Link></li>
                </ul>
              </div>
            </div>
          </div>
          <div className="footer-bottom">
            <p>© {new Date().getFullYear()} AdGenesis. All rights reserved.</p>
            <p className="footer-developer">
              Developed with ❤️ by <strong>Vikas TG</strong>
            </p>
          </div>
        </div>
      </footer>
    </div>
  );
};

export default AboutPage;
