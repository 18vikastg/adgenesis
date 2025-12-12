import React, { useState, useEffect } from 'react';

const ML_SERVICE_URL = process.env.REACT_APP_ML_URL || 'http://localhost:8001';

/**
 * Template Gallery Component
 * Browse and select from professional templates
 */
const TemplateGallery = ({ onSelectTemplate, onClose }) => {
  const [templates, setTemplates] = useState([]);
  const [categories, setCategories] = useState([]);
  const [selectedCategory, setSelectedCategory] = useState('all');
  const [loading, setLoading] = useState(true);
  const [hoveredTemplate, setHoveredTemplate] = useState(null);

  // Fetch templates on mount
  useEffect(() => {
    fetchTemplates();
  }, []);

  const fetchTemplates = async () => {
    try {
      const response = await fetch(`${ML_SERVICE_URL}/templates`);
      const data = await response.json();
      setTemplates(data.templates || []);
      setCategories(['all', ...(data.categories || [])]);
    } catch (error) {
      console.error('Failed to fetch templates:', error);
      // Use fallback templates
      setTemplates(fallbackTemplates);
      setCategories(['all', 'Technology', 'Fashion', 'Business', 'Sales', 'Events']);
    } finally {
      setLoading(false);
    }
  };

  const filteredTemplates = selectedCategory === 'all'
    ? templates
    : templates.filter(t => t.category === selectedCategory);

  // Template preview colors
  const getPreviewStyle = (template) => {
    const paletteStyles = {
      'tech_dark': { background: 'linear-gradient(135deg, #0f0f1a, #1a1a2e)', accent: '#3b82f6' },
      'tech_light': { background: 'linear-gradient(180deg, #f0f9ff, #e0f2fe)', accent: '#0284c7' },
      'fashion_vibrant': { background: 'linear-gradient(135deg, #ff6b9d, #ffc2d1)', accent: '#ffe66d' },
      'fashion_minimal': { background: '#faf5f0', accent: '#8b7355' },
      'sale_urgent': { background: 'linear-gradient(135deg, #dc2626, #f87171)', accent: '#fbbf24' },
      'sale_black_friday': { background: '#000000', accent: '#fbbf24' },
      'business_corporate': { background: 'linear-gradient(180deg, #1e3a5f, #0a1929)', accent: '#fbbf24' },
      'business_modern': { background: '#ffffff', accent: '#1e40af' },
      'food_warm': { background: 'linear-gradient(180deg, #fef3c7, #fde68a)', accent: '#ef4444' },
      'food_fresh': { background: 'linear-gradient(135deg, #dcfce7, #bbf7d0)', accent: '#16a34a' },
      'wellness_calm': { background: 'linear-gradient(180deg, #f0fdf4, #bbf7d0)', accent: '#059669' },
      'luxury_gold': { background: 'linear-gradient(135deg, #1a1a1a, #2d2d2d)', accent: '#d4af37' },
      'creative_gradient': { background: 'linear-gradient(135deg, #667eea, #f093fb)', accent: '#ffffff' },
      'minimalist_clean': { background: '#ffffff', accent: '#18181b' },
      'event_party': { background: 'linear-gradient(135deg, #7c3aed, #d946ef)', accent: '#ffffff' },
      'education_bright': { background: 'linear-gradient(180deg, #dbeafe, #bfdbfe)', accent: '#1d4ed8' },
    };
    return paletteStyles[template.palette] || paletteStyles['creative_gradient'];
  };

  const handleSelect = (template) => {
    onSelectTemplate(template);
  };

  if (loading) {
    return (
      <div className="fixed inset-0 bg-black/80 flex items-center justify-center z-50">
        <div className="bg-white rounded-xl p-8 text-center">
          <div className="animate-spin w-8 h-8 border-4 border-blue-600 border-t-transparent rounded-full mx-auto mb-4"></div>
          <p className="text-gray-600">Loading templates...</p>
        </div>
      </div>
    );
  }

  return (
    <div className="fixed inset-0 bg-black/80 flex items-center justify-center z-50 p-4">
      <div className="bg-white rounded-2xl w-full max-w-6xl max-h-[90vh] flex flex-col overflow-hidden shadow-2xl">
        {/* Header */}
        <div className="px-6 py-4 border-b flex items-center justify-between">
          <div>
            <h2 className="text-2xl font-bold text-gray-900">Choose a Template</h2>
            <p className="text-gray-500 text-sm mt-1">Start with a professionally designed template</p>
          </div>
          <button
            onClick={onClose}
            className="p-2 hover:bg-gray-100 rounded-full transition-colors"
          >
            <svg className="w-6 h-6 text-gray-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
            </svg>
          </button>
        </div>

        {/* Categories */}
        <div className="px-6 py-3 border-b bg-gray-50 flex items-center space-x-2 overflow-x-auto">
          {categories.map((category) => (
            <button
              key={category}
              onClick={() => setSelectedCategory(category)}
              className={`px-4 py-2 rounded-full text-sm font-medium whitespace-nowrap transition-all ${
                selectedCategory === category
                  ? 'bg-blue-600 text-white'
                  : 'bg-white text-gray-600 hover:bg-gray-100 border border-gray-200'
              }`}
            >
              {category === 'all' ? 'All Templates' : category}
            </button>
          ))}
        </div>

        {/* Templates Grid */}
        <div className="flex-1 overflow-y-auto p-6">
          <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-4">
            {filteredTemplates.map((template) => {
              const style = getPreviewStyle(template);
              return (
                <div
                  key={template.id}
                  className="group cursor-pointer"
                  onMouseEnter={() => setHoveredTemplate(template.id)}
                  onMouseLeave={() => setHoveredTemplate(null)}
                  onClick={() => handleSelect(template)}
                >
                  <div 
                    className="aspect-square rounded-xl overflow-hidden border-2 border-transparent group-hover:border-blue-500 transition-all relative shadow-md group-hover:shadow-xl"
                    style={{ background: style.background }}
                  >
                    {/* Template Preview */}
                    <div className="absolute inset-0 flex flex-col items-center justify-center p-4">
                      {/* Decorative elements based on layout */}
                      {template.layout === 'hero' && (
                        <>
                          <div 
                            className="w-3/4 h-3 rounded mb-2"
                            style={{ backgroundColor: style.accent }}
                          />
                          <div 
                            className="w-1/2 h-2 rounded mb-4 opacity-50"
                            style={{ backgroundColor: style.accent }}
                          />
                          <div 
                            className="w-1/3 h-6 rounded"
                            style={{ backgroundColor: style.accent }}
                          />
                        </>
                      )}
                      {template.layout === 'split' && (
                        <div className="w-full h-full flex">
                          <div className="w-1/2 p-3 flex flex-col justify-center">
                            <div className="w-full h-2 rounded mb-2" style={{ backgroundColor: style.accent }} />
                            <div className="w-3/4 h-2 rounded mb-4 opacity-50" style={{ backgroundColor: style.accent }} />
                            <div className="w-1/2 h-4 rounded" style={{ backgroundColor: style.accent }} />
                          </div>
                          <div className="w-1/2" style={{ backgroundColor: style.accent, opacity: 0.3 }} />
                        </div>
                      )}
                      {template.layout === 'sale' && (
                        <>
                          <div className="text-4xl font-bold mb-2" style={{ color: style.accent }}>50%</div>
                          <div className="text-lg font-bold" style={{ color: style.accent, opacity: 0.7 }}>OFF</div>
                        </>
                      )}
                      {template.layout === 'minimal' && (
                        <>
                          <div className="w-1/4 h-1 rounded mb-3" style={{ backgroundColor: style.accent }} />
                          <div className="w-2/3 h-2 rounded mb-2" style={{ backgroundColor: style.accent }} />
                          <div className="w-1/2 h-2 rounded opacity-50" style={{ backgroundColor: style.accent }} />
                        </>
                      )}
                      {template.layout === 'event' && (
                        <>
                          <div className="w-1/4 h-4 rounded-full mb-3" style={{ backgroundColor: style.accent }} />
                          <div className="w-3/4 h-3 rounded mb-2" style={{ backgroundColor: style.accent }} />
                          <div className="w-1/2 h-2 rounded mb-4 opacity-50" style={{ backgroundColor: style.accent }} />
                          <div className="w-1/3 h-5 rounded" style={{ backgroundColor: style.accent }} />
                        </>
                      )}
                      {template.layout === 'product' && (
                        <>
                          <div className="w-1/2 h-1/2 rounded-full mb-4 opacity-20" style={{ backgroundColor: style.accent }} />
                          <div className="w-2/3 h-2 rounded mb-2" style={{ backgroundColor: style.accent }} />
                          <div className="text-lg font-bold" style={{ color: style.accent }}>$99</div>
                        </>
                      )}
                      {template.layout === 'quote' && (
                        <>
                          <div className="text-4xl opacity-30" style={{ color: style.accent }}>"</div>
                          <div className="w-3/4 h-2 rounded mb-2" style={{ backgroundColor: style.accent }} />
                          <div className="w-2/3 h-2 rounded mb-2 opacity-70" style={{ backgroundColor: style.accent }} />
                          <div className="w-1/4 h-1 rounded mt-3" style={{ backgroundColor: style.accent }} />
                        </>
                      )}
                      {template.layout === 'story' && (
                        <>
                          <div className="w-1/2 h-1/2 rounded-full mb-4 opacity-20" style={{ backgroundColor: style.accent }} />
                          <div className="w-3/4 h-3 rounded mb-2" style={{ backgroundColor: style.accent }} />
                          <div className="text-2xl mt-4" style={{ color: style.accent }}>↑</div>
                        </>
                      )}
                    </div>

                    {/* Hover overlay */}
                    <div className={`absolute inset-0 bg-blue-600/90 flex items-center justify-center transition-opacity ${
                      hoveredTemplate === template.id ? 'opacity-100' : 'opacity-0'
                    }`}>
                      <span className="text-white font-semibold">Use Template</span>
                    </div>
                  </div>
                  
                  {/* Template info */}
                  <div className="mt-2">
                    <h3 className="font-medium text-gray-900 text-sm">{template.name}</h3>
                    <p className="text-xs text-gray-500">{template.category}</p>
                  </div>
                </div>
              );
            })}
          </div>

          {filteredTemplates.length === 0 && (
            <div className="text-center py-12">
              <p className="text-gray-500">No templates found in this category</p>
            </div>
          )}
        </div>

        {/* Footer */}
        <div className="px-6 py-4 border-t bg-gray-50 flex items-center justify-between">
          <p className="text-sm text-gray-500">
            {filteredTemplates.length} templates available
          </p>
          <button
            onClick={onClose}
            className="px-4 py-2 text-gray-600 hover:text-gray-900"
          >
            Cancel
          </button>
        </div>
      </div>
    </div>
  );
};

// Fallback templates if API fails
const fallbackTemplates = [
  { id: 'tech-startup-hero', name: 'Tech Startup Hero', category: 'Technology', palette: 'tech_dark', layout: 'hero', fonts: 'tech' },
  { id: 'fashion-sale', name: 'Fashion Sale', category: 'Fashion', palette: 'fashion_vibrant', layout: 'sale', fonts: 'fun' },
  { id: 'business-corporate', name: 'Business Corporate', category: 'Business', palette: 'business_corporate', layout: 'split', fonts: 'classic' },
  { id: 'food-delivery', name: 'Food Delivery', category: 'Food', palette: 'food_warm', layout: 'product', fonts: 'bold' },
  { id: 'event-webinar', name: 'Event Webinar', category: 'Events', palette: 'education_bright', layout: 'event', fonts: 'modern' },
  { id: 'minimal-elegant', name: 'Minimal Elegant', category: 'Minimal', palette: 'minimalist_clean', layout: 'minimal', fonts: 'minimal' },
  { id: 'luxury-premium', name: 'Luxury Premium', category: 'Luxury', palette: 'luxury_gold', layout: 'hero', fonts: 'luxury' },
  { id: 'creative-gradient', name: 'Creative Gradient', category: 'Creative', palette: 'creative_gradient', layout: 'hero', fonts: 'fun' },
  { id: 'wellness-calm', name: 'Wellness Calm', category: 'Wellness', palette: 'wellness_calm', layout: 'minimal', fonts: 'elegant' },
  { id: 'black-friday', name: 'Black Friday Sale', category: 'Sales', palette: 'sale_black_friday', layout: 'sale', fonts: 'bold' },
  { id: 'inspirational-quote', name: 'Inspirational Quote', category: 'Quotes', palette: 'minimalist_clean', layout: 'quote', fonts: 'elegant' },
  { id: 'story-swipe', name: 'Story Swipe Up', category: 'Social', palette: 'creative_gradient', layout: 'story', fonts: 'fun' },
];

export default TemplateGallery;
