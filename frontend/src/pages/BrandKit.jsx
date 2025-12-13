/**
 * Brand Kit Page - Full-featured brand assets management
 */

import React, { useState, useCallback } from 'react';
import './BrandKit.css';

// Icons
const ColorIcon = () => (
  <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
    <circle cx="12" cy="12" r="10" />
    <path d="M12 2v4M12 18v4M2 12h4M18 12h4" />
  </svg>
);

const FontIcon = () => (
  <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
    <path d="M4 7V4h16v3" />
    <path d="M9 20h6" />
    <path d="M12 4v16" />
  </svg>
);

const LogoIcon = () => (
  <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
    <rect x="3" y="3" width="18" height="18" rx="2" />
    <path d="M9 9h6v6H9z" />
  </svg>
);

const PlusIcon = () => (
  <svg width="20" height="20" viewBox="0 0 20 20" fill="none" stroke="currentColor" strokeWidth="2">
    <line x1="10" y1="4" x2="10" y2="16" />
    <line x1="4" y1="10" x2="16" y2="10" />
  </svg>
);

const DeleteIcon = () => (
  <svg width="16" height="16" viewBox="0 0 16 16" fill="none" stroke="currentColor" strokeWidth="1.5">
    <path d="M3 4h10M5 4V3a1 1 0 011-1h4a1 1 0 011 1v1" />
    <path d="M12 4v9a1 1 0 01-1 1H5a1 1 0 01-1-1V4" />
  </svg>
);

const CopyIcon = () => (
  <svg width="16" height="16" viewBox="0 0 16 16" fill="none" stroke="currentColor" strokeWidth="1.5">
    <rect x="5" y="5" width="8" height="8" rx="1" />
    <path d="M3 11V3a1 1 0 011-1h8" />
  </svg>
);

const CheckIcon = () => (
  <svg width="16" height="16" viewBox="0 0 16 16" fill="none" stroke="currentColor" strokeWidth="2">
    <polyline points="3,8 6,11 13,4" />
  </svg>
);

const CloseIcon = () => (
  <svg width="20" height="20" viewBox="0 0 20 20" fill="none" stroke="currentColor" strokeWidth="2">
    <path d="M15 5L5 15M5 5l10 10" />
  </svg>
);

// Available Google Fonts
const AVAILABLE_FONTS = [
  'Inter', 'Poppins', 'Roboto', 'Open Sans', 'Montserrat', 
  'Lato', 'Oswald', 'Raleway', 'Playfair Display', 'Source Sans Pro',
  'Merriweather', 'PT Sans', 'Nunito', 'Ubuntu', 'Rubik',
  'Work Sans', 'Quicksand', 'Karla', 'Barlow', 'DM Sans'
];

// Color palette presets
const COLOR_PALETTES = [
  { name: 'Modern Purple', colors: ['#8B5CF6', '#A78BFA', '#C4B5FD', '#DDD6FE', '#EDE9FE'] },
  { name: 'Ocean Teal', colors: ['#06B6D4', '#22D3EE', '#67E8F9', '#A5F3FC', '#CFFAFE'] },
  { name: 'Sunset Orange', colors: ['#F59E0B', '#FBBF24', '#FCD34D', '#FDE68A', '#FEF3C7'] },
  { name: 'Forest Green', colors: ['#10B981', '#34D399', '#6EE7B7', '#A7F3D0', '#D1FAE5'] },
  { name: 'Bold Red', colors: ['#EF4444', '#F87171', '#FCA5A5', '#FECACA', '#FEE2E2'] },
  { name: 'Corporate Blue', colors: ['#3B82F6', '#60A5FA', '#93C5FD', '#BFDBFE', '#DBEAFE'] },
];

const BrandKit = () => {
  // Brand colors state
  const [brandColors, setBrandColors] = useState([
    { hex: '#8B5CF6', name: 'Primary Purple' },
    { hex: '#06B6D4', name: 'Accent Teal' },
    { hex: '#F59E0B', name: 'Warning Orange' },
    { hex: '#EF4444', name: 'Error Red' },
    { hex: '#10B981', name: 'Success Green' },
    { hex: '#1E1E2E', name: 'Dark Background' },
    { hex: '#FFFFFF', name: 'White' },
  ]);
  const [newColor, setNewColor] = useState('#000000');
  const [newColorName, setNewColorName] = useState('');
  const [copiedColor, setCopiedColor] = useState(null);
  const [showColorModal, setShowColorModal] = useState(false);
  
  // Brand fonts state
  const [brandFonts, setBrandFonts] = useState([
    { name: 'Inter', type: 'Headings', weight: '700' },
    { name: 'Poppins', type: 'Body', weight: '400' },
    { name: 'Source Sans Pro', type: 'Captions', weight: '300' },
  ]);
  const [showFontModal, setShowFontModal] = useState(false);
  const [selectedFont, setSelectedFont] = useState('Inter');
  const [selectedFontType, setSelectedFontType] = useState('Primary');
  const [selectedFontWeight, setSelectedFontWeight] = useState('400');
  
  // Logos state
  const [logos, setLogos] = useState([]);
  
  // Add color
  const addColor = () => {
    if (newColor && !brandColors.find(c => c.hex === newColor)) {
      setBrandColors([...brandColors, { 
        hex: newColor, 
        name: newColorName || `Color ${brandColors.length + 1}` 
      }]);
      setNewColor('#000000');
      setNewColorName('');
      setShowColorModal(false);
    }
  };

  // Remove color
  const removeColor = (hex) => {
    setBrandColors(brandColors.filter(c => c.hex !== hex));
  };

  // Copy color to clipboard
  const copyColor = (hex) => {
    navigator.clipboard.writeText(hex);
    setCopiedColor(hex);
    setTimeout(() => setCopiedColor(null), 2000);
  };

  // Apply preset palette
  const applyPalette = (palette) => {
    const newColors = palette.colors.map((hex, i) => ({
      hex,
      name: `${palette.name} ${i + 1}`
    }));
    setBrandColors([...brandColors, ...newColors.filter(nc => !brandColors.find(c => c.hex === nc.hex))]);
  };

  // Add font
  const addFont = () => {
    if (!brandFonts.find(f => f.name === selectedFont && f.type === selectedFontType)) {
      setBrandFonts([...brandFonts, {
        name: selectedFont,
        type: selectedFontType,
        weight: selectedFontWeight,
      }]);
      setShowFontModal(false);
    }
  };

  // Remove font
  const removeFont = (name, type) => {
    setBrandFonts(brandFonts.filter(f => !(f.name === name && f.type === type)));
  };

  // Handle logo upload
  const handleLogoUpload = useCallback((e) => {
    const files = e.target.files;
    if (!files) return;
    
    Array.from(files).forEach(file => {
      const reader = new FileReader();
      reader.onload = (event) => {
        setLogos(prev => [...prev, {
          id: Date.now() + Math.random(),
          name: file.name,
          src: event.target.result,
          type: file.name.includes('dark') ? 'Dark' : file.name.includes('light') ? 'Light' : 'Default'
        }]);
      };
      reader.readAsDataURL(file);
    });
  }, []);

  // Remove logo
  const removeLogo = (id) => {
    setLogos(logos.filter(l => l.id !== id));
  };

  return (
    <div className="brand-kit-page">
      {/* Header */}
      <div className="brand-kit-header">
        <div className="header-content">
          <h1>Brand Kit</h1>
          <p>Manage your brand assets for consistent designs across all projects</p>
        </div>
        <button className="save-brand-btn">
          <CheckIcon />
          Save Changes
        </button>
      </div>

      <div className="brand-sections">
        {/* Colors Section */}
        <section className="brand-section">
          <div className="section-header">
            <div className="section-icon colors">
              <ColorIcon />
            </div>
            <div className="section-info">
              <h2>Brand Colors</h2>
              <p>Define your brand's color palette for consistent visuals</p>
            </div>
            <button className="add-btn-header" onClick={() => setShowColorModal(true)}>
              <PlusIcon />
              Add Color
            </button>
          </div>
          
          <div className="colors-grid">
            {brandColors.map((color, index) => (
              <div key={index} className="color-card">
                <div 
                  className="color-swatch-large" 
                  style={{ backgroundColor: color.hex }}
                >
                  <div className="color-actions">
                    <button 
                      className="color-action-btn"
                      onClick={() => copyColor(color.hex)}
                      title="Copy"
                    >
                      {copiedColor === color.hex ? <CheckIcon /> : <CopyIcon />}
                    </button>
                    <button 
                      className="color-action-btn delete"
                      onClick={() => removeColor(color.hex)}
                      title="Delete"
                    >
                      <DeleteIcon />
                    </button>
                  </div>
                </div>
                <div className="color-info">
                  <span className="color-name">{color.name}</span>
                  <span className="color-hex">{color.hex}</span>
                </div>
              </div>
            ))}
          </div>

          {/* Color Palettes */}
          <div className="palettes-section">
            <h3>Quick Add Palettes</h3>
            <div className="palettes-grid">
              {COLOR_PALETTES.map((palette, index) => (
                <button 
                  key={index} 
                  className="palette-btn"
                  onClick={() => applyPalette(palette)}
                >
                  <div className="palette-preview">
                    {palette.colors.slice(0, 5).map((c, i) => (
                      <div key={i} className="palette-color" style={{ backgroundColor: c }} />
                    ))}
                  </div>
                  <span>{palette.name}</span>
                </button>
              ))}
            </div>
          </div>
        </section>

        {/* Fonts Section */}
        <section className="brand-section">
          <div className="section-header">
            <div className="section-icon fonts">
              <FontIcon />
            </div>
            <div className="section-info">
              <h2>Brand Fonts</h2>
              <p>Define your brand's typography hierarchy</p>
            </div>
            <button className="add-btn-header" onClick={() => setShowFontModal(true)}>
              <PlusIcon />
              Add Font
            </button>
          </div>
          
          <div className="fonts-grid">
            {brandFonts.map((font, index) => (
              <div key={index} className="font-card">
                <div 
                  className="font-preview-large" 
                  style={{ fontFamily: font.name, fontWeight: font.weight }}
                >
                  <span className="preview-letter">Aa</span>
                  <span className="preview-text">The quick brown fox jumps over the lazy dog</span>
                </div>
                <div className="font-card-info">
                  <div className="font-details">
                    <span className="font-name">{font.name}</span>
                    <span className="font-meta">{font.type} • {font.weight}</span>
                  </div>
                  <div className="font-actions">
                    <button 
                      className="font-action-btn delete"
                      onClick={() => removeFont(font.name, font.type)}
                      title="Remove"
                    >
                      <DeleteIcon />
                    </button>
                  </div>
                </div>
              </div>
            ))}
          </div>
        </section>

        {/* Logos Section */}
        <section className="brand-section">
          <div className="section-header">
            <div className="section-icon logos">
              <LogoIcon />
            </div>
            <div className="section-info">
              <h2>Brand Logos</h2>
              <p>Upload and manage your logo variations</p>
            </div>
          </div>
          
          <div className="logos-grid">
            {logos.map((logo) => (
              <div key={logo.id} className="logo-card">
                <div className="logo-preview">
                  <img src={logo.src} alt={logo.name} />
                </div>
                <div className="logo-info">
                  <span className="logo-name">{logo.name}</span>
                  <span className="logo-type">{logo.type}</span>
                </div>
                <div className="logo-actions">
                  <button 
                    className="logo-action-btn delete"
                    onClick={() => removeLogo(logo.id)}
                    title="Remove"
                  >
                    <DeleteIcon />
                  </button>
                </div>
              </div>
            ))}
            
            <label className="logo-upload-card">
              <input 
                type="file" 
                accept="image/*" 
                multiple
                onChange={handleLogoUpload}
                hidden 
              />
              <div className="upload-content">
                <div className="upload-icon">
                  <PlusIcon />
                </div>
                <span className="upload-text">Upload Logo</span>
                <span className="upload-hint">PNG, SVG, or JPG</span>
              </div>
            </label>
          </div>
        </section>
      </div>

      {/* Add Color Modal */}
      {showColorModal && (
        <div className="modal-overlay" onClick={() => setShowColorModal(false)}>
          <div className="brand-modal" onClick={e => e.stopPropagation()}>
            <div className="modal-header">
              <h3>Add Brand Color</h3>
              <button className="modal-close" onClick={() => setShowColorModal(false)}>
                <CloseIcon />
              </button>
            </div>
            <div className="modal-content">
              <div className="color-picker-section">
                <input 
                  type="color" 
                  value={newColor}
                  onChange={(e) => setNewColor(e.target.value)}
                  className="color-picker-input"
                />
                <div 
                  className="color-preview-box" 
                  style={{ backgroundColor: newColor }}
                />
              </div>
              <div className="input-group">
                <label>Color Name</label>
                <input 
                  type="text"
                  placeholder="e.g., Primary Blue"
                  value={newColorName}
                  onChange={(e) => setNewColorName(e.target.value)}
                />
              </div>
              <div className="input-group">
                <label>Hex Value</label>
                <input 
                  type="text"
                  value={newColor}
                  onChange={(e) => setNewColor(e.target.value)}
                />
              </div>
            </div>
            <div className="modal-actions">
              <button className="cancel-btn" onClick={() => setShowColorModal(false)}>Cancel</button>
              <button className="confirm-btn" onClick={addColor}>Add Color</button>
            </div>
          </div>
        </div>
      )}

      {/* Add Font Modal */}
      {showFontModal && (
        <div className="modal-overlay" onClick={() => setShowFontModal(false)}>
          <div className="brand-modal" onClick={e => e.stopPropagation()}>
            <div className="modal-header">
              <h3>Add Brand Font</h3>
              <button className="modal-close" onClick={() => setShowFontModal(false)}>
                <CloseIcon />
              </button>
            </div>
            <div className="modal-content">
              <div className="input-group">
                <label>Font Family</label>
                <select value={selectedFont} onChange={(e) => setSelectedFont(e.target.value)}>
                  {AVAILABLE_FONTS.map(font => (
                    <option key={font} value={font}>{font}</option>
                  ))}
                </select>
              </div>
              <div className="input-group">
                <label>Usage</label>
                <select value={selectedFontType} onChange={(e) => setSelectedFontType(e.target.value)}>
                  <option value="Headings">Headings</option>
                  <option value="Body">Body Text</option>
                  <option value="Captions">Captions</option>
                  <option value="Display">Display</option>
                  <option value="Accent">Accent</option>
                </select>
              </div>
              <div className="input-group">
                <label>Weight</label>
                <select value={selectedFontWeight} onChange={(e) => setSelectedFontWeight(e.target.value)}>
                  <option value="300">Light (300)</option>
                  <option value="400">Regular (400)</option>
                  <option value="500">Medium (500)</option>
                  <option value="600">Semibold (600)</option>
                  <option value="700">Bold (700)</option>
                  <option value="800">Extra Bold (800)</option>
                </select>
              </div>
              <div className="font-modal-preview" style={{ fontFamily: selectedFont, fontWeight: selectedFontWeight }}>
                <span>Preview: The quick brown fox jumps over the lazy dog</span>
              </div>
            </div>
            <div className="modal-actions">
              <button className="cancel-btn" onClick={() => setShowFontModal(false)}>Cancel</button>
              <button className="confirm-btn" onClick={addFont}>Add Font</button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};

export default BrandKit;
