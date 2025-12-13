/**
 * Templates Page - Canva-style Template Gallery
 * Professional templates with categories, search, and filtering
 */

import React, { useState, useMemo } from 'react';
import { useNavigate } from 'react-router-dom';
import { 
  TEMPLATES, 
  TEMPLATE_CATEGORIES,
} from '../data/templates';
import './Templates.css';

// Icons
const SearchIcon = () => (
  <svg width="20" height="20" viewBox="0 0 20 20" fill="none" stroke="currentColor" strokeWidth="2">
    <circle cx="9" cy="9" r="6" />
    <line x1="14" y1="14" x2="18" y2="18" />
  </svg>
);

const StarIcon = () => (
  <svg width="16" height="16" viewBox="0 0 16 16" fill="currentColor">
    <path d="M8 1l1.8 5.5h5.8l-4.7 3.4 1.8 5.5L8 12l-4.7 3.4 1.8-5.5-4.7-3.4h5.8z" />
  </svg>
);

const HeartIcon = ({ filled }) => (
  <svg width="20" height="20" viewBox="0 0 20 20" fill={filled ? "currentColor" : "none"} stroke="currentColor" strokeWidth="2">
    <path d="M10 17.5s-7-4.5-7-9c0-2.5 2-4.5 4.5-4.5 1.5 0 2.5.5 3.5 2 1-1.5 2-2 3.5-2 2.5 0 4.5 2 4.5 4.5 0 4.5-7 9-7 9z" />
  </svg>
);

const PlusIcon = () => (
  <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
    <line x1="12" y1="5" x2="12" y2="19" />
    <line x1="5" y1="12" x2="19" y2="12" />
  </svg>
);

const CloseIcon = () => (
  <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
    <line x1="18" y1="6" x2="6" y2="18" />
    <line x1="6" y1="6" x2="18" y2="18" />
  </svg>
);

const Templates = () => {
  const navigate = useNavigate();
  const [selectedCategory, setSelectedCategory] = useState('all');
  const [searchQuery, setSearchQuery] = useState('');
  const [selectedPlatform, setSelectedPlatform] = useState('all');
  const [favorites, setFavorites] = useState(new Set());
  const [viewMode, setViewMode] = useState('grid');
  const [previewTemplate, setPreviewTemplate] = useState(null);

  // Filter templates
  const filteredTemplates = useMemo(() => {
    let result = TEMPLATES;
    
    if (selectedCategory !== 'all') {
      result = result.filter(t => t.category === selectedCategory);
    }
    
    if (selectedPlatform !== 'all') {
      result = result.filter(t => t.platform === selectedPlatform);
    }
    
    if (searchQuery.trim()) {
      const query = searchQuery.toLowerCase();
      result = result.filter(t => 
        t.name.toLowerCase().includes(query) ||
        t.tags.some(tag => tag.toLowerCase().includes(query))
      );
    }
    
    return result;
  }, [selectedCategory, selectedPlatform, searchQuery]);

  const handleUseTemplate = (template) => {
    navigate('/editor', { 
      state: { 
        template,
        width: template.format === 'story' ? 1080 : 1080,
        height: template.format === 'story' ? 1920 : 1080,
      } 
    });
  };

  const handlePreview = (template, e) => {
    e.stopPropagation();
    setPreviewTemplate(template);
  };

  const closePreview = () => {
    setPreviewTemplate(null);
  };

  const toggleFavorite = (id, e) => {
    e.stopPropagation();
    setFavorites(prev => {
      const newFavorites = new Set(prev);
      if (newFavorites.has(id)) {
        newFavorites.delete(id);
      } else {
        newFavorites.add(id);
      }
      return newFavorites;
    });
  };

  return (
    <div className="templates-page">
      {/* Header */}
      <div className="templates-header">
        <div className="templates-header-content">
          <h1>Templates</h1>
          <p>Start with a professionally designed template and make it your own</p>
        </div>
        
        <div className="templates-search">
          <SearchIcon />
          <input
            type="text"
            placeholder="Search templates..."
            value={searchQuery}
            onChange={(e) => setSearchQuery(e.target.value)}
          />
        </div>
      </div>

      {/* Categories */}
      <div className="templates-categories">
        <div className="categories-scroll">
          {TEMPLATE_CATEGORIES.map(category => (
            <button
              key={category.id}
              className={`category-pill ${selectedCategory === category.id ? 'active' : ''}`}
              onClick={() => setSelectedCategory(category.id)}
            >
              <span className="category-icon">{category.icon}</span>
              <span className="category-name">{category.name}</span>
            </button>
          ))}
        </div>
      </div>

      {/* Filters Bar */}
      <div className="templates-filters">
        <div className="filter-group">
          <label>Platform:</label>
          <select 
            value={selectedPlatform} 
            onChange={(e) => setSelectedPlatform(e.target.value)}
          >
            <option value="all">All Platforms</option>
            <option value="instagram">Instagram</option>
            <option value="facebook">Facebook</option>
            <option value="twitter">Twitter</option>
            <option value="linkedin">LinkedIn</option>
            <option value="youtube">YouTube</option>
            <option value="tiktok">TikTok</option>
            <option value="pinterest">Pinterest</option>
          </select>
        </div>
        
        <div className="filter-results">
          {filteredTemplates.length} templates found
        </div>
        
        <div className="view-toggle">
          <button 
            className={viewMode === 'grid' ? 'active' : ''}
            onClick={() => setViewMode('grid')}
          >
            <svg width="18" height="18" viewBox="0 0 18 18" fill="currentColor">
              <rect x="1" y="1" width="7" height="7" rx="1" />
              <rect x="10" y="1" width="7" height="7" rx="1" />
              <rect x="1" y="10" width="7" height="7" rx="1" />
              <rect x="10" y="10" width="7" height="7" rx="1" />
            </svg>
          </button>
          <button 
            className={viewMode === 'list' ? 'active' : ''}
            onClick={() => setViewMode('list')}
          >
            <svg width="18" height="18" viewBox="0 0 18 18" fill="currentColor">
              <rect x="1" y="2" width="16" height="3" rx="1" />
              <rect x="1" y="7.5" width="16" height="3" rx="1" />
              <rect x="1" y="13" width="16" height="3" rx="1" />
            </svg>
          </button>
        </div>
      </div>

      {/* Templates Grid */}
      <div className={`templates-grid ${viewMode}`}>
        {/* Create Blank */}
        <div 
          className="template-card create-blank"
          onClick={() => navigate('/editor')}
        >
          <div className="create-blank-content">
            <div className="create-icon">
              <PlusIcon />
            </div>
            <span>Create blank design</span>
          </div>
        </div>

        {/* Template Cards */}
        {filteredTemplates.map(template => (
          <div 
            key={template.id}
            className={`template-card ${template.format === 'story' ? 'story' : ''}`}
            onClick={() => handleUseTemplate(template)}
          >
            <div className="template-preview">
              <img 
                src={template.thumbnail} 
                alt={template.name}
                loading="lazy"
              />
              
              <div className="template-overlay">
                <button 
                  className="preview-template-btn"
                  onClick={(e) => handlePreview(template, e)}
                >
                  Preview
                </button>
                <button className="use-template-btn">
                  Use Template
                </button>
              </div>
              
              <button 
                className={`favorite-btn ${favorites.has(template.id) ? 'active' : ''}`}
                onClick={(e) => toggleFavorite(template.id, e)}
              >
                <HeartIcon filled={favorites.has(template.id)} />
              </button>
              
              {template.premium && (
                <div className="premium-badge">
                  <StarIcon /> PRO
                </div>
              )}
              
              <div className="format-badge">
                {template.format}
              </div>
            </div>
            
            <div className="template-info">
              <h3>{template.name}</h3>
              <div className="template-meta">
                <span className="platform">{template.platform}</span>
                <span className="separator">•</span>
                <span className="category">{template.category}</span>
              </div>
            </div>
          </div>
        ))}
      </div>

      {/* Empty State */}
      {filteredTemplates.length === 0 && (
        <div className="templates-empty">
          <div className="empty-icon">🔍</div>
          <h3>No templates found</h3>
          <p>Try adjusting your search or filter to find what you're looking for</p>
          <button onClick={() => {
            setSearchQuery('');
            setSelectedCategory('all');
            setSelectedPlatform('all');
          }}>
            Clear filters
          </button>
        </div>
      )}

      {/* Preview Modal */}
      {previewTemplate && (
        <div className="template-preview-modal" onClick={closePreview}>
          <div className="preview-modal-content" onClick={(e) => e.stopPropagation()}>
            <button className="preview-close-btn" onClick={closePreview}>
              <CloseIcon />
            </button>
            
            <div className="preview-layout">
              {/* Preview Image */}
              <div className="preview-image-section">
                <img 
                  src={previewTemplate.thumbnail} 
                  alt={previewTemplate.name}
                  className={previewTemplate.format === 'story' ? 'story-format' : ''}
                />
              </div>
              
              {/* Preview Details */}
              <div className="preview-details-section">
                <div className="preview-header">
                  {previewTemplate.premium && (
                    <span className="preview-pro-badge">
                      <StarIcon /> PRO
                    </span>
                  )}
                  <h2>{previewTemplate.name}</h2>
                  <p className="preview-description">
                    A professional {previewTemplate.category} template designed for {previewTemplate.platform}.
                    Perfect for creating engaging content that stands out.
                  </p>
                </div>
                
                <div className="preview-meta">
                  <div className="meta-item">
                    <span className="meta-label">Platform</span>
                    <span className="meta-value">{previewTemplate.platform}</span>
                  </div>
                  <div className="meta-item">
                    <span className="meta-label">Category</span>
                    <span className="meta-value">{previewTemplate.category}</span>
                  </div>
                  <div className="meta-item">
                    <span className="meta-label">Format</span>
                    <span className="meta-value">{previewTemplate.format}</span>
                  </div>
                  <div className="meta-item">
                    <span className="meta-label">Size</span>
                    <span className="meta-value">
                      {previewTemplate.format === 'story' ? '1080 × 1920px' : '1080 × 1080px'}
                    </span>
                  </div>
                </div>
                
                <div className="preview-tags">
                  <span className="tags-label">Tags:</span>
                  <div className="tags-list">
                    {previewTemplate.tags.map(tag => (
                      <span key={tag} className="tag">{tag}</span>
                    ))}
                  </div>
                </div>
                
                <div className="preview-colors">
                  <span className="colors-label">Color Palette:</span>
                  <div className="colors-list">
                    {previewTemplate.colors.map((color, i) => (
                      <div 
                        key={i} 
                        className="color-swatch" 
                        style={{ backgroundColor: color }}
                        title={color}
                      />
                    ))}
                  </div>
                </div>
                
                <div className="preview-actions">
                  <button 
                    className={`favorite-action ${favorites.has(previewTemplate.id) ? 'active' : ''}`}
                    onClick={() => toggleFavorite(previewTemplate.id, { stopPropagation: () => {} })}
                  >
                    <HeartIcon filled={favorites.has(previewTemplate.id)} />
                    {favorites.has(previewTemplate.id) ? 'Saved' : 'Save'}
                  </button>
                  <button 
                    className="use-action"
                    onClick={() => handleUseTemplate(previewTemplate)}
                  >
                    Use this template
                  </button>
                </div>
              </div>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};

export default Templates;
