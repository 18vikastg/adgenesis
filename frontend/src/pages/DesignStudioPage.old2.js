/**
 * AdGenesis - Premium Design Studio Page
 * World-class Canva/Figma-inspired design experience
 */

import React, { useState, useEffect, useRef, useCallback } from 'react';
import { useQuery, useMutation, useQueryClient } from 'react-query';
import { generateDesign, getDesigns, saveDesign } from '../services/api';
import { fabric } from 'fabric';
import { AIAssistant, AIFloatingButton } from '../components/ai/AIAssistant';
import { 
  Button, 
  Modal, 
  ModalHeader, 
  ModalTitle, 
  ModalBody, 
  ModalFooter,
  Select,
  Tabs,
  TabList,
  Tab,
  TabPanel,
  SegmentedControl 
} from '../components/ui';
import { cn, generateId, debounce } from '../lib/utils';
import { PLATFORMS, FORMATS, INDUSTRIES, colors } from '../lib/constants';
import './DesignStudioPage.css';

const ML_SERVICE_URL = process.env.REACT_APP_ML_URL || 'http://localhost:8001';

// Icons
const SparklesIcon = () => (
  <svg width="20" height="20" viewBox="0 0 20 20" fill="none">
    <path d="M10 2L11.5 6.5L16 8L11.5 9.5L10 14L8.5 9.5L4 8L8.5 6.5L10 2Z" fill="currentColor" />
    <path d="M15 12L15.75 14.25L18 15L15.75 15.75L15 18L14.25 15.75L12 15L14.25 14.25L15 12Z" fill="currentColor" opacity="0.7" />
  </svg>
);

const PlusIcon = () => (
  <svg width="20" height="20" viewBox="0 0 20 20" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round">
    <path d="M10 4V16M4 10H16" />
  </svg>
);

const DownloadIcon = () => (
  <svg width="18" height="18" viewBox="0 0 18 18" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round">
    <path d="M9 2V12M9 12L5 8M9 12L13 8M2 15H16" />
  </svg>
);

const EditIcon = () => (
  <svg width="18" height="18" viewBox="0 0 18 18" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round">
    <path d="M13.5 2.5L15.5 4.5M2 16H4L14 6L12 4L2 14V16Z" />
  </svg>
);

const TemplateIcon = () => (
  <svg width="18" height="18" viewBox="0 0 18 18" fill="none" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round">
    <rect x="2" y="2" width="14" height="14" rx="2" />
    <path d="M2 7H16M7 7V16" />
  </svg>
);

const LayersIcon = () => (
  <svg width="18" height="18" viewBox="0 0 18 18" fill="none" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round">
    <path d="M9 2L16 6L9 10L2 6L9 2Z" />
    <path d="M2 9L9 13L16 9" />
    <path d="M2 12L9 16L16 12" />
  </svg>
);

const GridIcon = () => (
  <svg width="18" height="18" viewBox="0 0 18 18" fill="none" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round">
    <rect x="2" y="2" width="5" height="5" rx="1" />
    <rect x="11" y="2" width="5" height="5" rx="1" />
    <rect x="2" y="11" width="5" height="5" rx="1" />
    <rect x="11" y="11" width="5" height="5" rx="1" />
  </svg>
);

const HistoryIcon = () => (
  <svg width="18" height="18" viewBox="0 0 18 18" fill="none" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round">
    <path d="M2 9C2 5.13 5.13 2 9 2C12.87 2 16 5.13 16 9C16 12.87 12.87 16 9 16C6.5 16 4.32 14.62 3.17 12.5" />
    <path d="M2 14V10H6" />
    <path d="M9 5V9L12 11" />
  </svg>
);

// Platform specs
const PLATFORM_SPECS = {
  instagram: {
    post: { width: 1080, height: 1080, label: 'Post (1:1)' },
    story: { width: 1080, height: 1920, label: 'Story (9:16)' },
    reel: { width: 1080, height: 1920, label: 'Reel (9:16)' },
    landscape: { width: 1080, height: 566, label: 'Landscape' },
  },
  facebook: {
    post: { width: 1200, height: 630, label: 'Post' },
    cover: { width: 820, height: 312, label: 'Cover' },
    story: { width: 1080, height: 1920, label: 'Story' },
    square: { width: 1200, height: 1200, label: 'Square' },
  },
  twitter: {
    post: { width: 1600, height: 900, label: 'Post' },
    header: { width: 1500, height: 500, label: 'Header' },
    square: { width: 1200, height: 1200, label: 'Square' },
  },
  linkedin: {
    post: { width: 1200, height: 627, label: 'Post' },
    cover: { width: 1584, height: 396, label: 'Cover' },
    square: { width: 1200, height: 1200, label: 'Square' },
  },
  youtube: {
    thumbnail: { width: 1280, height: 720, label: 'Thumbnail' },
    banner: { width: 2560, height: 1440, label: 'Banner' },
  },
};

// Quick prompts by category
const QUICK_PROMPTS = {
  trending: [
    { label: '🚀 Tech Launch', prompt: 'Modern tech product launch with futuristic gradient' },
    { label: '✨ AI Powered', prompt: 'AI technology showcase with neural network visuals' },
    { label: '🎯 Marketing', prompt: 'Bold marketing campaign with conversion focus' },
  ],
  seasonal: [
    { label: '🎄 Holiday', prompt: 'Festive holiday promotion with warm colors' },
    { label: '☀️ Summer', prompt: 'Vibrant summer campaign with beach vibes' },
    { label: '🌸 Spring', prompt: 'Fresh spring collection with floral elements' },
  ],
  business: [
    { label: '💼 Corporate', prompt: 'Professional corporate announcement' },
    { label: '📊 Finance', prompt: 'Trust-building financial services ad' },
    { label: '🤝 B2B', prompt: 'B2B partnership announcement' },
  ],
  lifestyle: [
    { label: '🍔 Food', prompt: 'Appetizing food delivery promotion' },
    { label: '💄 Beauty', prompt: 'Elegant beauty product showcase' },
    { label: '🏃 Fitness', prompt: 'Energetic fitness motivation poster' },
  ],
};

const DesignStudioPage = () => {
  // Core state
  const [prompt, setPrompt] = useState('');
  const [platform, setPlatform] = useState('instagram');
  const [format, setFormat] = useState('post');
  const [industry, setIndustry] = useState('technology');
  
  // Design state
  const [currentDesign, setCurrentDesign] = useState(null);
  const [designHistory, setDesignHistory] = useState([]);
  const [historyIndex, setHistoryIndex] = useState(-1);
  
  // UI state
  const [isGenerating, setIsGenerating] = useState(false);
  const [showAI, setShowAI] = useState(false);
  const [showTemplates, setShowTemplates] = useState(false);
  const [showExport, setShowExport] = useState(false);
  const [activePanel, setActivePanel] = useState('generate');
  const [exportFormat, setExportFormat] = useState('png');
  const [exportQuality, setExportQuality] = useState('high');
  
  // Refs
  const canvasRef = useRef(null);
  const fabricRef = useRef(null);
  const queryClient = useQueryClient();

  // Queries
  const { data: savedDesigns } = useQuery('designs', getDesigns);

  // Get current canvas dimensions
  const canvasSize = PLATFORM_SPECS[platform]?.[format] || { width: 1080, height: 1080 };

  // Initialize canvas
  useEffect(() => {
    if (canvasRef.current && !fabricRef.current) {
      const canvas = new fabric.Canvas(canvasRef.current, {
        width: 600,
        height: 600,
        backgroundColor: '#1a1a2e',
        preserveObjectStacking: true,
        selection: true,
      });
      fabricRef.current = canvas;
      
      // Add gradient background by default
      renderDefaultCanvas(canvas);
    }

    return () => {
      if (fabricRef.current) {
        fabricRef.current.dispose();
        fabricRef.current = null;
      }
    };
  }, []);

  // Render default canvas state
  const renderDefaultCanvas = (canvas) => {
    canvas.clear();
    
    // Create gradient background
    const gradient = new fabric.Gradient({
      type: 'linear',
      coords: { x1: 0, y1: 0, x2: 600, y2: 600 },
      colorStops: [
        { offset: 0, color: '#1a1a2e' },
        { offset: 1, color: '#16213e' },
      ],
    });
    
    canvas.setBackgroundColor(gradient, canvas.renderAll.bind(canvas));
    
    // Add placeholder text
    const text = new fabric.Text('Your design will appear here', {
      left: 300,
      top: 280,
      fontSize: 18,
      fill: '#64748b',
      fontFamily: 'Inter, sans-serif',
      originX: 'center',
      originY: 'center',
      selectable: false,
    });
    
    const subtext = new fabric.Text('Enter a prompt or choose a template to get started', {
      left: 300,
      top: 320,
      fontSize: 14,
      fill: '#475569',
      fontFamily: 'Inter, sans-serif',
      originX: 'center',
      originY: 'center',
      selectable: false,
    });
    
    canvas.add(text, subtext);
    canvas.renderAll();
  };

  // Generate design
  const handleGenerate = async () => {
    if (!prompt.trim() || isGenerating) return;

    setIsGenerating(true);
    
    try {
      // Call ML service
      const response = await fetch(`${ML_SERVICE_URL}/generate`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          prompt,
          platform,
          format,
          industry,
        }),
      });

      if (!response.ok) throw new Error('Generation failed');

      const designSpec = await response.json();

      // Save to backend
      const savedDesign = await generateDesign({ prompt, platform, format });

      // Merge design data
      const fullDesign = {
        id: savedDesign.id || generateId(),
        prompt,
        platform,
        format,
        canvas_data: {
          ...designSpec,
          width: canvasSize.width,
          height: canvasSize.height,
        },
        created_at: new Date().toISOString(),
      };

      setCurrentDesign(fullDesign);
      addToHistory(fullDesign);
      renderDesignToCanvas(fullDesign.canvas_data);
      queryClient.invalidateQueries('designs');
      
    } catch (error) {
      console.error('Generation error:', error);
      // Show error state
    } finally {
      setIsGenerating(false);
    }
  };

  // Render design to canvas
  const renderDesignToCanvas = useCallback((data) => {
    if (!fabricRef.current || !data) return;

    const canvas = fabricRef.current;
    canvas.clear();

    // Set background
    const bgColor = data.background || data.background_color || '#1a1a2e';
    
    if (data.gradient) {
      const gradient = new fabric.Gradient({
        type: 'linear',
        coords: { x1: 0, y1: 0, x2: 600, y2: 600 },
        colorStops: data.gradient.stops || [
          { offset: 0, color: data.gradient.from || bgColor },
          { offset: 1, color: data.gradient.to || bgColor },
        ],
      });
      canvas.setBackgroundColor(gradient, canvas.renderAll.bind(canvas));
    } else {
      canvas.setBackgroundColor(bgColor, canvas.renderAll.bind(canvas));
    }

    // Calculate scale
    const scale = Math.min(600 / (data.width || 1080), 600 / (data.height || 1080));

    // Render elements
    const elements = data.objects || data.elements || [];
    elements.forEach((obj) => {
      let fabricObj = null;
      const x = (obj.left || obj.x || 0) * scale;
      const y = (obj.top || obj.y || 0) * scale;

      if (obj.type === 'textbox' || obj.type === 'text') {
        fabricObj = new fabric.Textbox(obj.text || '', {
          left: x,
          top: y,
          width: obj.width ? obj.width * scale : undefined,
          fontSize: (obj.fontSize || 24) * scale,
          fill: obj.fill || obj.color || '#ffffff',
          fontFamily: obj.fontFamily || 'Inter',
          fontWeight: obj.fontWeight || 'normal',
          fontStyle: obj.fontStyle || 'normal',
          textAlign: obj.textAlign || 'left',
          lineHeight: obj.lineHeight || 1.2,
          opacity: obj.opacity !== undefined ? obj.opacity : 1,
        });
      } else if (obj.type === 'rect' || obj.type === 'rectangle') {
        fabricObj = new fabric.Rect({
          left: x,
          top: y,
          width: (obj.width || 100) * scale,
          height: (obj.height || 100) * scale,
          fill: obj.fill || obj.color || '#3b82f6',
          rx: (obj.rx || obj.borderRadius || 0) * scale,
          ry: (obj.ry || obj.borderRadius || 0) * scale,
          opacity: obj.opacity !== undefined ? obj.opacity : 1,
        });
      } else if (obj.type === 'circle') {
        fabricObj = new fabric.Circle({
          left: x,
          top: y,
          radius: ((obj.radius || obj.width / 2 || 50)) * scale,
          fill: obj.fill || obj.color || '#22c55e',
          opacity: obj.opacity !== undefined ? obj.opacity : 1,
        });
      } else if (obj.type === 'line') {
        fabricObj = new fabric.Line(
          [x, y, (obj.x2 || obj.left + 100) * scale, (obj.y2 || obj.top) * scale],
          {
            stroke: obj.stroke || obj.color || '#ffffff',
            strokeWidth: (obj.strokeWidth || 2) * scale,
            opacity: obj.opacity !== undefined ? obj.opacity : 1,
          }
        );
      }

      if (fabricObj) {
        canvas.add(fabricObj);
      }
    });

    canvas.renderAll();
  }, []);

  // Add to history
  const addToHistory = (design) => {
    setDesignHistory((prev) => [...prev.slice(0, historyIndex + 1), design]);
    setHistoryIndex((prev) => prev + 1);
  };

  // Undo
  const handleUndo = () => {
    if (historyIndex > 0) {
      setHistoryIndex(historyIndex - 1);
      const design = designHistory[historyIndex - 1];
      setCurrentDesign(design);
      renderDesignToCanvas(design.canvas_data);
    }
  };

  // Redo
  const handleRedo = () => {
    if (historyIndex < designHistory.length - 1) {
      setHistoryIndex(historyIndex + 1);
      const design = designHistory[historyIndex + 1];
      setCurrentDesign(design);
      renderDesignToCanvas(design.canvas_data);
    }
  };

  // Export design
  const handleExport = () => {
    if (!fabricRef.current) return;

    const multiplier = exportQuality === 'high' ? 3 : exportQuality === 'medium' ? 2 : 1;
    const dataURL = fabricRef.current.toDataURL({
      format: exportFormat === 'jpg' ? 'jpeg' : exportFormat,
      quality: exportFormat === 'jpg' ? 0.9 : 1,
      multiplier,
    });

    const link = document.createElement('a');
    link.download = `adgenesis-design-${Date.now()}.${exportFormat}`;
    link.href = dataURL;
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
    
    setShowExport(false);
  };

  // Apply quick prompt
  const handleQuickPrompt = (quickPrompt) => {
    setPrompt(quickPrompt.prompt);
  };

  // Handle AI suggestion
  const handleAISuggestion = (suggestion) => {
    console.log('AI suggestion:', suggestion);
    // Implement AI suggestion application
  };

  return (
    <div className="design-studio">
      {/* Left Sidebar - Tools & Options */}
      <aside className="studio-sidebar">
        {/* Logo/Brand */}
        <div className="sidebar-header">
          <div className="sidebar-logo">
            <SparklesIcon />
            <span>AdGenesis</span>
          </div>
        </div>

        {/* Panel Navigation */}
        <nav className="sidebar-nav">
          <button
            className={cn('sidebar-nav-item', activePanel === 'generate' && 'active')}
            onClick={() => setActivePanel('generate')}
          >
            <SparklesIcon />
            <span>Generate</span>
          </button>
          <button
            className={cn('sidebar-nav-item', activePanel === 'templates' && 'active')}
            onClick={() => setActivePanel('templates')}
          >
            <TemplateIcon />
            <span>Templates</span>
          </button>
          <button
            className={cn('sidebar-nav-item', activePanel === 'elements' && 'active')}
            onClick={() => setActivePanel('elements')}
          >
            <LayersIcon />
            <span>Elements</span>
          </button>
          <button
            className={cn('sidebar-nav-item', activePanel === 'projects' && 'active')}
            onClick={() => setActivePanel('projects')}
          >
            <GridIcon />
            <span>Projects</span>
          </button>
        </nav>

        {/* Panel Content */}
        <div className="sidebar-content">
          {activePanel === 'generate' && (
            <div className="panel-generate">
              {/* Platform & Format Selection */}
              <div className="form-section">
                <label className="form-label">Platform</label>
                <div className="platform-grid">
                  {Object.keys(PLATFORM_SPECS).map((p) => (
                    <button
                      key={p}
                      className={cn('platform-btn', platform === p && 'active')}
                      onClick={() => {
                        setPlatform(p);
                        setFormat(Object.keys(PLATFORM_SPECS[p])[0]);
                      }}
                    >
                      {p.charAt(0).toUpperCase() + p.slice(1)}
                    </button>
                  ))}
                </div>
              </div>

              <div className="form-section">
                <label className="form-label">Format</label>
                <div className="format-grid">
                  {Object.entries(PLATFORM_SPECS[platform] || {}).map(([key, spec]) => (
                    <button
                      key={key}
                      className={cn('format-btn', format === key && 'active')}
                      onClick={() => setFormat(key)}
                    >
                      <span className="format-name">{spec.label}</span>
                      <span className="format-size">{spec.width}×{spec.height}</span>
                    </button>
                  ))}
                </div>
              </div>

              {/* Prompt Input */}
              <div className="form-section">
                <label className="form-label">Describe your design</label>
                <textarea
                  value={prompt}
                  onChange={(e) => setPrompt(e.target.value)}
                  placeholder="E.g., Modern tech startup launch poster with gradient background and bold typography..."
                  className="prompt-input"
                  rows={4}
                />
              </div>

              {/* Quick Prompts */}
              <div className="form-section">
                <label className="form-label">Quick prompts</label>
                <div className="quick-prompts-grid">
                  {Object.entries(QUICK_PROMPTS).map(([category, prompts]) => (
                    <div key={category} className="quick-prompt-category">
                      {prompts.slice(0, 2).map((qp, idx) => (
                        <button
                          key={idx}
                          className="quick-prompt-btn"
                          onClick={() => handleQuickPrompt(qp)}
                        >
                          {qp.label}
                        </button>
                      ))}
                    </div>
                  ))}
                </div>
              </div>

              {/* Generate Button */}
              <Button
                variant="primary"
                size="lg"
                fullWidth
                icon={<SparklesIcon />}
                loading={isGenerating}
                onClick={handleGenerate}
                disabled={!prompt.trim()}
              >
                {isGenerating ? 'Generating...' : 'Generate Design'}
              </Button>
            </div>
          )}

          {activePanel === 'templates' && (
            <div className="panel-templates">
              <p className="panel-description">
                Choose from professionally designed templates
              </p>
              <div className="template-categories">
                {['Business', 'Social Media', 'Marketing', 'Events'].map((cat) => (
                  <button key={cat} className="template-category-btn">
                    {cat}
                  </button>
                ))}
              </div>
              <div className="template-grid">
                {/* Template previews would go here */}
                <div className="template-placeholder">
                  <TemplateIcon />
                  <span>Templates coming soon</span>
                </div>
              </div>
            </div>
          )}

          {activePanel === 'elements' && (
            <div className="panel-elements">
              <p className="panel-description">
                Add shapes, text, and images to your design
              </p>
              <div className="element-sections">
                <div className="element-section">
                  <label className="element-section-label">Shapes</label>
                  <div className="element-grid">
                    <button className="element-btn">□ Rectangle</button>
                    <button className="element-btn">○ Circle</button>
                    <button className="element-btn">△ Triangle</button>
                    <button className="element-btn">— Line</button>
                  </div>
                </div>
                <div className="element-section">
                  <label className="element-section-label">Text</label>
                  <div className="element-grid">
                    <button className="element-btn">Aa Heading</button>
                    <button className="element-btn">Aa Subheading</button>
                    <button className="element-btn">Aa Body</button>
                  </div>
                </div>
              </div>
            </div>
          )}

          {activePanel === 'projects' && (
            <div className="panel-projects">
              <p className="panel-description">
                Your saved designs
              </p>
              <div className="projects-list">
                {savedDesigns?.length > 0 ? (
                  savedDesigns.slice(0, 10).map((design) => (
                    <div
                      key={design.id}
                      className="project-item"
                      onClick={() => {
                        setCurrentDesign(design);
                        if (design.canvas_data) {
                          renderDesignToCanvas(design.canvas_data);
                        }
                      }}
                    >
                      <div className="project-thumbnail" />
                      <div className="project-info">
                        <span className="project-name">{design.prompt?.slice(0, 30) || 'Untitled'}</span>
                        <span className="project-date">
                          {new Date(design.created_at).toLocaleDateString()}
                        </span>
                      </div>
                    </div>
                  ))
                ) : (
                  <div className="projects-empty">
                    <p>No saved designs yet</p>
                    <span>Generate your first design to get started</span>
                  </div>
                )}
              </div>
            </div>
          )}
        </div>
      </aside>

      {/* Main Canvas Area */}
      <main className="studio-main">
        {/* Top Toolbar */}
        <header className="studio-toolbar">
          <div className="toolbar-left">
            <button className="toolbar-btn" onClick={handleUndo} disabled={historyIndex <= 0}>
              <HistoryIcon />
            </button>
            <button className="toolbar-btn" onClick={handleRedo} disabled={historyIndex >= designHistory.length - 1}>
              <HistoryIcon style={{ transform: 'scaleX(-1)' }} />
            </button>
            <div className="toolbar-divider" />
            <span className="canvas-size-label">
              {canvasSize.width} × {canvasSize.height}
            </span>
          </div>

          <div className="toolbar-center">
            {currentDesign && (
              <span className="design-title">{currentDesign.prompt?.slice(0, 40)}...</span>
            )}
          </div>

          <div className="toolbar-right">
            <Button
              variant="ghost"
              size="sm"
              icon={<EditIcon />}
              onClick={() => {/* Open full editor */}}
            >
              Edit
            </Button>
            <Button
              variant="primary"
              size="sm"
              icon={<DownloadIcon />}
              onClick={() => setShowExport(true)}
              disabled={!currentDesign}
            >
              Export
            </Button>
          </div>
        </header>

        {/* Canvas Container */}
        <div className="canvas-container">
          <div className="canvas-wrapper">
            <canvas ref={canvasRef} />
          </div>
          
          {/* Zoom controls would go here */}
        </div>
      </main>

      {/* AI Assistant */}
      {showAI && (
        <AIAssistant
          isOpen={showAI}
          onClose={() => setShowAI(false)}
          onApplySuggestion={handleAISuggestion}
          currentDesign={currentDesign}
        />
      )}

      {/* AI Floating Button */}
      {!showAI && (
        <AIFloatingButton onClick={() => setShowAI(true)} />
      )}

      {/* Export Modal */}
      <Modal isOpen={showExport} onClose={() => setShowExport(false)} size="sm">
        <ModalHeader>
          <ModalTitle>Export Design</ModalTitle>
        </ModalHeader>
        <ModalBody>
          <div className="export-options">
            <div className="export-option-group">
              <label className="export-label">Format</label>
              <SegmentedControl
                options={[
                  { value: 'png', label: 'PNG' },
                  { value: 'jpg', label: 'JPG' },
                  { value: 'svg', label: 'SVG' },
                ]}
                value={exportFormat}
                onChange={setExportFormat}
                fullWidth
              />
            </div>
            <div className="export-option-group">
              <label className="export-label">Quality</label>
              <SegmentedControl
                options={[
                  { value: 'low', label: '1x' },
                  { value: 'medium', label: '2x' },
                  { value: 'high', label: '3x' },
                ]}
                value={exportQuality}
                onChange={setExportQuality}
                fullWidth
              />
            </div>
            <div className="export-preview-info">
              <p>
                Output size: {canvasSize.width * (exportQuality === 'high' ? 3 : exportQuality === 'medium' ? 2 : 1)} × {canvasSize.height * (exportQuality === 'high' ? 3 : exportQuality === 'medium' ? 2 : 1)}px
              </p>
            </div>
          </div>
        </ModalBody>
        <ModalFooter>
          <Button variant="secondary" onClick={() => setShowExport(false)}>
            Cancel
          </Button>
          <Button variant="primary" icon={<DownloadIcon />} onClick={handleExport}>
            Download
          </Button>
        </ModalFooter>
      </Modal>
    </div>
  );
};

export default DesignStudioPage;
