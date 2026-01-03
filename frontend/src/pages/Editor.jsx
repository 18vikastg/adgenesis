/**
 * Editor - Professional Canva-style Design Editor
 * Full-featured canvas editor with AI blueprint generation
 */

import React, { useState, useEffect, useRef, useCallback } from 'react';
import { useNavigate, useLocation, useParams } from 'react-router-dom';
import { useQuery, useQueryClient } from 'react-query';
import { fabric } from 'fabric';
import { getDesign, generateDesign, generateDesignBlueprint, checkMLHealth } from '../services/api';
import './Editor.css';

// Constants
const ML_SERVICE_URL = process.env.REACT_APP_ML_URL || 'http://localhost:8001';

// Icons
const ArrowLeftIcon = () => (
  <svg width="20" height="20" viewBox="0 0 20 20" fill="none" stroke="currentColor" strokeWidth="2">
    <line x1="16" y1="10" x2="4" y2="10" />
    <polyline points="9,5 4,10 9,15" />
  </svg>
);

const SparklesIcon = () => (
  <svg width="20" height="20" viewBox="0 0 20 20" fill="currentColor">
    <path d="M10 2L11.5 6.5L16 8L11.5 9.5L10 14L8.5 9.5L4 8L8.5 6.5L10 2Z" />
  </svg>
);

const TextIcon = () => (
  <svg width="20" height="20" viewBox="0 0 20 20" fill="none" stroke="currentColor" strokeWidth="2">
    <path d="M4 6V4h12v2M10 4v12M7 16h6" />
  </svg>
);

const ImageIcon = () => (
  <svg width="20" height="20" viewBox="0 0 20 20" fill="none" stroke="currentColor" strokeWidth="2">
    <rect x="2" y="2" width="16" height="16" rx="2" />
    <circle cx="7" cy="7" r="2" />
    <path d="M18 13l-4-4-9 9" />
  </svg>
);

const ShapesIcon = () => (
  <svg width="20" height="20" viewBox="0 0 20 20" fill="none" stroke="currentColor" strokeWidth="2">
    <rect x="3" y="3" width="8" height="8" rx="1" />
    <circle cx="14" cy="14" r="4" />
  </svg>
);

const UploadIcon = () => (
  <svg width="20" height="20" viewBox="0 0 20 20" fill="none" stroke="currentColor" strokeWidth="2">
    <path d="M10 14V4M10 4l-4 4M10 4l4 4" />
    <path d="M3 14v2a2 2 0 002 2h10a2 2 0 002-2v-2" />
  </svg>
);

const TemplatesIcon = () => (
  <svg width="20" height="20" viewBox="0 0 20 20" fill="none" stroke="currentColor" strokeWidth="2">
    <rect x="2" y="2" width="16" height="16" rx="2" />
    <line x1="2" y1="7" x2="18" y2="7" />
    <line x1="7" y1="18" x2="7" y2="7" />
  </svg>
);

const LayersIcon = () => (
  <svg width="20" height="20" viewBox="0 0 20 20" fill="none" stroke="currentColor" strokeWidth="2">
    <path d="M10 2l8 4-8 4-8-4 8-4z" />
    <path d="M2 10l8 4 8-4" />
    <path d="M2 14l8 4 8-4" />
  </svg>
);

const DownloadIcon = () => (
  <svg width="20" height="20" viewBox="0 0 20 20" fill="none" stroke="currentColor" strokeWidth="2">
    <path d="M10 3v10M10 13l-4-4M10 13l4-4" />
    <path d="M3 15v2a1 1 0 001 1h12a1 1 0 001-1v-2" />
  </svg>
);

const SaveIcon = () => (
  <svg width="20" height="20" viewBox="0 0 20 20" fill="none" stroke="currentColor" strokeWidth="2">
    <path d="M15 17H5a2 2 0 01-2-2V5a2 2 0 012-2h7l5 5v9a2 2 0 01-2 2z" />
    <path d="M14 17v-5H6v5" />
    <path d="M6 3v4h6" />
  </svg>
);

const UndoIcon = () => (
  <svg width="18" height="18" viewBox="0 0 18 18" fill="none" stroke="currentColor" strokeWidth="2">
    <path d="M3 7h8a4 4 0 110 8H7" />
    <path d="M6 4L3 7l3 3" />
  </svg>
);

const RedoIcon = () => (
  <svg width="18" height="18" viewBox="0 0 18 18" fill="none" stroke="currentColor" strokeWidth="2">
    <path d="M15 7H7a4 4 0 100 8h4" />
    <path d="M12 4l3 3-3 3" />
  </svg>
);

const ZoomInIcon = () => (
  <svg width="18" height="18" viewBox="0 0 18 18" fill="none" stroke="currentColor" strokeWidth="2">
    <circle cx="8" cy="8" r="5" />
    <path d="M12 12l4 4" />
    <path d="M8 6v4M6 8h4" />
  </svg>
);

const ZoomOutIcon = () => (
  <svg width="18" height="18" viewBox="0 0 18 18" fill="none" stroke="currentColor" strokeWidth="2">
    <circle cx="8" cy="8" r="5" />
    <path d="M12 12l4 4" />
    <path d="M6 8h4" />
  </svg>
);

const DeleteIcon = () => (
  <svg width="18" height="18" viewBox="0 0 18 18" fill="none" stroke="currentColor" strokeWidth="2">
    <path d="M3 5h12M6 5V3a1 1 0 011-1h4a1 1 0 011 1v2" />
    <path d="M14 5v10a1 1 0 01-1 1H5a1 1 0 01-1-1V5" />
  </svg>
);

const CopyIcon = () => (
  <svg width="18" height="18" viewBox="0 0 18 18" fill="none" stroke="currentColor" strokeWidth="2">
    <rect x="6" y="6" width="10" height="10" rx="1" />
    <path d="M4 12H3a1 1 0 01-1-1V3a1 1 0 011-1h8a1 1 0 011 1v1" />
  </svg>
);

const CloseIcon = () => (
  <svg width="20" height="20" viewBox="0 0 20 20" fill="none" stroke="currentColor" strokeWidth="2">
    <path d="M15 5L5 15M5 5l10 10" />
  </svg>
);

const PNGIcon = () => (
  <svg width="32" height="32" viewBox="0 0 32 32" fill="currentColor">
    <rect x="4" y="4" width="24" height="24" rx="2" fill="#10B981" />
    <text x="16" y="19" textAnchor="middle" fill="white" fontSize="8" fontWeight="bold">PNG</text>
  </svg>
);

const JPGIcon = () => (
  <svg width="32" height="32" viewBox="0 0 32 32" fill="currentColor">
    <rect x="4" y="4" width="24" height="24" rx="2" fill="#3B82F6" />
    <text x="16" y="19" textAnchor="middle" fill="white" fontSize="8" fontWeight="bold">JPG</text>
  </svg>
);

const PDFIcon = () => (
  <svg width="32" height="32" viewBox="0 0 32 32" fill="currentColor">
    <rect x="4" y="4" width="24" height="24" rx="2" fill="#EF4444" />
    <text x="16" y="19" textAnchor="middle" fill="white" fontSize="8" fontWeight="bold">PDF</text>
  </svg>
);

const SVGIcon = () => (
  <svg width="32" height="32" viewBox="0 0 32 32" fill="currentColor">
    <rect x="4" y="4" width="24" height="24" rx="2" fill="#F59E0B" />
    <text x="16" y="19" textAnchor="middle" fill="white" fontSize="8" fontWeight="bold">SVG</text>
  </svg>
);

const EyeIcon = () => (
  <svg width="16" height="16" viewBox="0 0 16 16" fill="none" stroke="currentColor" strokeWidth="1.5">
    <path d="M1 8s2.5-5 7-5 7 5 7 5-2.5 5-7 5-7-5-7-5z" />
    <circle cx="8" cy="8" r="2" />
  </svg>
);

const EyeOffIcon = () => (
  <svg width="16" height="16" viewBox="0 0 16 16" fill="none" stroke="currentColor" strokeWidth="1.5">
    <path d="M1 8s2.5-5 7-5 7 5 7 5-2.5 5-7 5-7-5-7-5z" />
    <path d="M2 2l12 12" />
  </svg>
);

const LockIcon = () => (
  <svg width="16" height="16" viewBox="0 0 16 16" fill="none" stroke="currentColor" strokeWidth="1.5">
    <rect x="3" y="7" width="10" height="7" rx="1" />
    <path d="M5 7V5a3 3 0 016 0v2" />
  </svg>
);

const MoveUpIcon = () => (
  <svg width="14" height="14" viewBox="0 0 14 14" fill="none" stroke="currentColor" strokeWidth="1.5">
    <path d="M7 11V3M7 3l-3 3M7 3l3 3" />
  </svg>
);

const MoveDownIcon = () => (
  <svg width="14" height="14" viewBox="0 0 14 14" fill="none" stroke="currentColor" strokeWidth="1.5">
    <path d="M7 3v8M7 11l-3-3M7 11l3-3" />
  </svg>
);

const KeyboardIcon = () => (
  <svg width="18" height="18" viewBox="0 0 18 18" fill="none" stroke="currentColor" strokeWidth="1.5">
    <rect x="1" y="4" width="16" height="10" rx="2" />
    <line x1="4" y1="7" x2="6" y2="7" />
    <line x1="8" y1="7" x2="10" y2="7" />
    <line x1="12" y1="7" x2="14" y2="7" />
    <line x1="5" y1="10" x2="13" y2="10" />
  </svg>
);

const QuestionIcon = () => (
  <svg width="18" height="18" viewBox="0 0 18 18" fill="none" stroke="currentColor" strokeWidth="1.5">
    <circle cx="9" cy="9" r="7" />
    <path d="M7 7a2 2 0 112.5 1.9c-.5.2-.5.6-.5 1.1M9 13h.01" />
  </svg>
);

// Export formats configuration
const EXPORT_FORMATS = [
  { id: 'png', name: 'PNG', desc: 'Best for web, transparent backgrounds', icon: PNGIcon, quality: true },
  { id: 'jpg', name: 'JPG', desc: 'Best for photos, smaller file size', icon: JPGIcon, quality: true },
  { id: 'pdf', name: 'PDF', desc: 'Best for print, documents', icon: PDFIcon, quality: false },
  { id: 'svg', name: 'SVG', desc: 'Best for scalable graphics', icon: SVGIcon, quality: false },
];

// Platform mapping for backend
const mapPlatformToBackend = (platform) => {
  const mapping = {
    instagram: 'meta',
    facebook: 'meta',
    twitter: 'google',
    linkedin: 'linkedin',
    youtube: 'google',
  };
  return mapping[platform] || 'meta';
};

const mapFormatToBackend = (format) => {
  const mapping = {
    post: 'square',
    square: 'square',
    story: 'story',
    reel: 'story',
    landscape: 'landscape',
    cover: 'landscape',
    portrait: 'portrait',
  };
  return mapping[format] || 'square';
};

// AI Prompt suggestions
const AI_SUGGESTIONS = [
  { icon: '🚀', text: 'Modern tech product launch' },
  { icon: '✨', text: 'Elegant fashion collection' },
  { icon: '🍔', text: 'Appetizing food delivery' },
  { icon: '💼', text: 'Professional business announcement' },
  { icon: '🎉', text: 'Exciting event promotion' },
  { icon: '🏋️', text: 'Energetic fitness campaign' },
];

const Editor = () => {
  const navigate = useNavigate();
  const location = useLocation();
  const { projectId } = useParams();
  const queryClient = useQueryClient();
  
  // Canvas refs
  const canvasRef = useRef(null);
  const fabricRef = useRef(null);
  const containerRef = useRef(null);
  
  // State
  const [canvasSize, setCanvasSize] = useState({ 
    width: location.state?.width || 1080, 
    height: location.state?.height || 1080 
  });
  const [zoom, setZoom] = useState(0.5);
  const [activePanel, setActivePanel] = useState('ai');
  const [selectedObject, setSelectedObject] = useState(null);
  
  // AI state
  const [prompt, setPrompt] = useState('');
  const [isGenerating, setIsGenerating] = useState(false);
  const [generationProgress, setGenerationProgress] = useState(0);
  const [generationType, setGenerationType] = useState('layout'); // 'layout' or 'image'
  const [aiStyle, setAiStyle] = useState('modern');
  const [aiModel, setAiModel] = useState('sdxl-turbo');
  const [generatedImage, setGeneratedImage] = useState(null);
  
  // History for undo/redo
  const [history, setHistory] = useState([]);
  const [historyIndex, setHistoryIndex] = useState(-1);
  
  // Export modal state
  const [showExportModal, setShowExportModal] = useState(false);
  const [exportFormat, setExportFormat] = useState('png');
  const [exportQuality, setExportQuality] = useState(1);
  const [exportScale, setExportScale] = useState(1);
  const [isExporting, setIsExporting] = useState(false);
  
  // Layers state
  const [layers, setLayers] = useState([]);
  const [selectedLayerId, setSelectedLayerId] = useState(null);
  
  // Project state
  const [projectName, setProjectName] = useState(location.state?.name || 'Untitled Design');
  const [isSaving, setIsSaving] = useState(false);
  const [lastSaved, setLastSaved] = useState(null);
  const currentProjectId = useRef(location.state?.projectId || `project-${Date.now()}`);
  
  // Keyboard shortcuts modal
  const [showShortcutsModal, setShowShortcutsModal] = useState(false);
  
  // Load existing design
  const { data: existingDesign } = useQuery(
    ['design', projectId],
    () => getDesign(projectId),
    { enabled: !!projectId }
  );

  // Initialize canvas
  useEffect(() => {
    if (!canvasRef.current || fabricRef.current) return;

    const canvas = new fabric.Canvas(canvasRef.current, {
      width: canvasSize.width * zoom,
      height: canvasSize.height * zoom,
      backgroundColor: '#1a1a2e',
      preserveObjectStacking: true,
      selection: true,
    });

    // Set up scaling
    canvas.setZoom(zoom);

    // Event handlers
    canvas.on('selection:created', (e) => {
      setSelectedObject(e.selected[0]);
      setSelectedLayerId(e.selected[0]?.id || null);
    });
    canvas.on('selection:updated', (e) => {
      setSelectedObject(e.selected[0]);
      setSelectedLayerId(e.selected[0]?.id || null);
    });
    canvas.on('selection:cleared', () => {
      setSelectedObject(null);
      setSelectedLayerId(null);
    });
    canvas.on('object:modified', () => {
      saveToHistory();
      updateLayers();
    });
    canvas.on('object:added', () => updateLayers());
    canvas.on('object:removed', () => updateLayers());

    fabricRef.current = canvas;
    
    // Add default background first, imported design will be loaded in separate useEffect
    if (location.state?.template?.design) {
      // Load template if passed in state
      loadTemplateDesign(location.state.template.design, canvas);
    } else {
      // Add default background
      addDefaultBackground();
    }
    
    return () => {
      canvas.dispose();
      fabricRef.current = null;
    };
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, []);

  // Load imported design from sessionStorage (separate effect to ensure canvas is ready)
  useEffect(() => {
    // Check for imported design after a brief delay to ensure canvas is initialized
    const checkForImportedDesign = () => {
      const importedDesignData = sessionStorage.getItem('importedDesign');
      if (!importedDesignData) return;
      
      if (!fabricRef.current) {
        // Canvas not ready yet, retry
        setTimeout(checkForImportedDesign, 100);
        return;
      }
      
      try {
        console.log('Found imported design in sessionStorage');
        const importedDesign = JSON.parse(importedDesignData);
        sessionStorage.removeItem('importedDesign'); // Clear immediately
        
        // Load the design
        const canvas = fabricRef.current;
        canvas.clear();
        
        const blueprint = importedDesign.blueprint;
        const layersData = importedDesign.layers || blueprint?.layers || [];
        const originalImage = importedDesign.originalImage; // The uploaded image
        
        console.log('Loading blueprint:', blueprint);
        console.log('Loading layers:', layersData.length);
        console.log('Has original image:', !!originalImage);
        
        // CRITICAL: Set zoom to 1 so positions match exactly
        canvas.setZoom(1);
        setZoom(1);
        
        // LOAD THE ORIGINAL IMAGE AS BACKGROUND
        if (originalImage) {
          fabric.Image.fromURL(originalImage, (img) => {
            const imgWidth = img.width;
            const imgHeight = img.height;
            
            console.log('Image dimensions:', imgWidth, 'x', imgHeight);
            console.log('Layers to add:', layersData);
            console.log('Text layers:', layersData.filter(l => l.type === 'text'));
            
            // Update canvas to match image size exactly
            canvas.setWidth(imgWidth);
            canvas.setHeight(imgHeight);
            setCanvasSize({ width: imgWidth, height: imgHeight });
            
            // Add image as background (not editable)
            img.set({
              left: 0,
              top: 0,
              scaleX: 1,
              scaleY: 1,
              selectable: false,
              evented: false,
              id: 'background_image',
            });
            
            canvas.add(img);
            canvas.sendToBack(img);
            
            // Add text layers on top - positioned exactly over the original text
            const textLayers = layersData.filter(l => l.type === 'text');
            console.log('Adding', textLayers.length, 'text layers to canvas');
            
            textLayers.forEach((layer, index) => {
              const x = layer.position?.x || 100;
              const y = layer.position?.y || 100;
              const w = layer.size?.width || 200;
              const bgColor = layer.background_color || '#000000';
              const fontSize = layer.font_size || 32;
              
              console.log(`Creating text "${layer.content}" at (${x}, ${y})`);
              
              // Create editable text with OPAQUE background
              const textObj = new fabric.Textbox(layer.content || 'Text', {
                left: x,
                top: y,
                width: Math.max(w + 10, 80),
                fontSize: fontSize,
                fontFamily: layer.font_family || 'Arial',
                fontWeight: layer.font_weight || 'bold',
                fill: layer.color || '#ffffff',
                textAlign: layer.alignment || 'left',
                lineHeight: 1.0,
                editable: true,
                selectable: true,
                id: layer.id || `text_${index}`,
                backgroundColor: bgColor,
                padding: 4,
              });
              
              canvas.add(textObj);
              console.log('Added text object to canvas');
            });
            
            canvas.renderAll();
            console.log('Canvas rendered with', canvas.getObjects().length, 'objects');
          }, { crossOrigin: 'anonymous' });
        } else {
          // No image - just set background color and add layers
          if (blueprint?.canvas?.background) {
            const bg = blueprint.canvas.background;
            if (bg.type === 'solid') {
              canvas.setBackgroundColor(bg.color || '#1a1a2e', canvas.renderAll.bind(canvas));
            }
          } else {
            canvas.setBackgroundColor('#1a1a2e', canvas.renderAll.bind(canvas));
          }
          const cw = blueprint?.canvas?.width || canvasSize.width;
          const ch = blueprint?.canvas?.height || canvasSize.height;
          canvas.setWidth(cw);
          canvas.setHeight(ch);
          addTextLayers(canvas, layersData, cw, ch);
        }
        
        setProjectName('Imported Design');
        
      } catch (e) {
        console.error('Failed to load imported design:', e);
      }
    };
    
    // Add editable text layers on top of the image
    // These COVER the original text so you can edit/delete them
    const addTextLayers = (canvas, layersData, canvasWidth, canvasHeight) => {
      const textLayers = layersData.filter(l => l.type === 'text');
      
      console.log('Adding', textLayers.length, 'editable text layers');
      
      textLayers.forEach((layer, index) => {
        const x = layer.position?.x || 100;
        const y = layer.position?.y || 100;
        const w = layer.size?.width || 200;
        const h = layer.size?.height || 40;
        const bgColor = layer.background_color || '#000000';
        const fontSize = layer.font_size || 32;
        
        // Create editable text with OPAQUE background to cover original
        const textObj = new fabric.Textbox(layer.content || 'Text', {
          left: x,
          top: y,
          width: Math.max(w + 10, 80), // Slightly wider to fully cover
          fontSize: fontSize,
          fontFamily: layer.font_family || 'Arial',
          fontWeight: layer.font_weight || 'bold',
          fill: layer.color || '#ffffff',
          textAlign: layer.alignment || 'left',
          lineHeight: 1.0,
          editable: true,
          selectable: true,
          id: layer.id || `text_${index}`,
          // OPAQUE background covers original text in image
          backgroundColor: bgColor,
          padding: 4,
        });
        
        canvas.add(textObj);
        console.log(`Text: "${layer.content}" at (${x}, ${y}) with bg ${bgColor}`);
      });
      
      canvas.renderAll();
    };
        
    // Start checking after component mounts
    setTimeout(checkForImportedDesign, 200);
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, []);

  // Load template design onto canvas
  const loadTemplateDesign = (design, canvas) => {
    if (!design || !canvas) return;
    
    canvas.clear();
    
    // Set background
    if (design.background) {
      if (design.background.type === 'gradient' && design.background.gradient) {
        const grad = design.background.gradient;
        const gradient = new fabric.Gradient({
          type: 'linear',
          coords: {
            x1: 0,
            y1: 0,
            x2: grad.angle === 180 ? 0 : canvasSize.width,
            y2: grad.angle === 180 || grad.angle === 135 ? canvasSize.height : 0
          },
          colorStops: grad.stops.map(s => ({
            offset: s.offset,
            color: s.color
          }))
        });
        
        const bg = new fabric.Rect({
          left: 0,
          top: 0,
          width: canvasSize.width,
          height: canvasSize.height,
          fill: gradient,
          selectable: false,
          evented: false,
        });
        canvas.add(bg);
        canvas.sendToBack(bg);
      } else if (design.background.type === 'solid') {
        canvas.setBackgroundColor(design.background.color, canvas.renderAll.bind(canvas));
      }
    }
    
    // Add elements
    if (design.elements && Array.isArray(design.elements)) {
      design.elements.forEach(element => {
        let obj = null;
        
        switch (element.type) {
          case 'text':
            obj = new fabric.Textbox(element.content || 'Text', {
              left: element.x - (element.width || 300) / 2,
              top: element.y - (element.fontSize || 48) / 2,
              width: element.width || 300,
              fontSize: element.fontSize || 48,
              fontFamily: element.fontFamily || 'Inter',
              fontWeight: element.fontWeight || 'normal',
              fill: element.fill || '#ffffff',
              textAlign: element.textAlign || 'center',
              lineHeight: element.lineHeight || 1.2,
              letterSpacing: element.letterSpacing || 0,
              originX: 'center',
              originY: 'center',
            });
            obj.set({ left: element.x, top: element.y });
            break;
            
          case 'rectangle':
            obj = new fabric.Rect({
              left: element.x,
              top: element.y,
              width: element.width || 200,
              height: element.height || 100,
              fill: element.fill || '#8B5CF6',
              rx: element.rx || 0,
              ry: element.ry || 0,
              originX: 'center',
              originY: 'center',
            });
            break;
            
          case 'circle':
            obj = new fabric.Circle({
              left: element.x,
              top: element.y,
              radius: element.radius || 50,
              fill: element.fill || '#06B6D4',
              originX: 'center',
              originY: 'center',
            });
            break;
            
          default:
            break;
        }
        
        if (obj) {
          canvas.add(obj);
        }
      });
    }
    
    canvas.renderAll();
    saveToHistory();
  };

  // Load imported design from Analyze page
  const loadImportedDesign = (importedData, canvas) => {
    if (!importedData || !canvas) return;
    
    console.log('Loading imported design:', importedData);
    
    canvas.clear();
    
    const blueprint = importedData.blueprint;
    const layers = importedData.layers || [];
    
    // Update canvas size if provided
    if (blueprint?.canvas) {
      const newWidth = blueprint.canvas.width || 1080;
      const newHeight = blueprint.canvas.height || 1080;
      setCanvasSize({ width: newWidth, height: newHeight });
    }
    
    // Set background
    if (blueprint?.canvas?.background) {
      const bg = blueprint.canvas.background;
      if (bg.type === 'solid') {
        canvas.setBackgroundColor(bg.color, canvas.renderAll.bind(canvas));
      } else if (bg.type === 'gradient') {
        const gradient = new fabric.Gradient({
          type: 'linear',
          coords: { 
            x1: 0, 
            y1: 0, 
            x2: bg.angle === 90 ? canvasSize.width : 0, 
            y2: bg.angle !== 90 ? canvasSize.height : 0 
          },
          colorStops: bg.colors?.map((color, i) => ({
            offset: i / (bg.colors.length - 1 || 1),
            color: color
          })) || [
            { offset: 0, color: '#1a1a2e' },
            { offset: 1, color: '#16213e' },
          ],
        });
        
        const bgRect = new fabric.Rect({
          left: 0,
          top: 0,
          width: canvasSize.width,
          height: canvasSize.height,
          fill: gradient,
          selectable: false,
          evented: false,
          id: 'background',
        });
        canvas.add(bgRect);
        canvas.sendToBack(bgRect);
      }
    } else {
      // Default dark background
      canvas.setBackgroundColor('#1a1a2e', canvas.renderAll.bind(canvas));
    }
    
    // Calculate scale factor for display
    const scale = Math.min(
      (canvasSize.width * zoom) / (blueprint?.canvas?.width || 1080),
      (canvasSize.height * zoom) / (blueprint?.canvas?.height || 1080)
    );
    
    // Add layers as editable objects
    layers.forEach((layer, index) => {
      let obj = null;
      
      if (layer.type === 'text') {
        // Create editable text box
        obj = new fabric.Textbox(layer.content || 'Text', {
          left: layer.position?.x || 100,
          top: layer.position?.y || 100,
          width: layer.size?.width || 400,
          fontSize: layer.font_size || 36,
          fontFamily: layer.font_family || 'Inter, sans-serif',
          fontWeight: layer.font_weight || 'normal',
          fill: layer.color || '#ffffff',
          textAlign: layer.alignment || 'left',
          lineHeight: 1.2,
          id: layer.id || `text_${index}`,
          role: layer.role,
          editable: true,
          selectable: true,
        });
        
        // Style CTA buttons differently
        if (layer.role === 'cta' && layer.background_color) {
          // Add background rect for CTA
          const padding = 20;
          const ctaBg = new fabric.Rect({
            left: layer.position?.x - padding,
            top: layer.position?.y - 10,
            width: (layer.size?.width || 200) + padding * 2,
            height: (layer.font_size || 36) + 24,
            fill: layer.background_color,
            rx: layer.border_radius || 8,
            ry: layer.border_radius || 8,
            id: `${layer.id}_bg`,
            selectable: true,
          });
          canvas.add(ctaBg);
        }
      } else if (layer.type === 'image' && !layer.placeholder) {
        // Image placeholder
        obj = new fabric.Rect({
          left: layer.position?.x || 100,
          top: layer.position?.y || 100,
          width: layer.size?.width || 200,
          height: layer.size?.height || 200,
          fill: 'rgba(139, 92, 246, 0.2)',
          stroke: '#8b5cf6',
          strokeWidth: 2,
          strokeDashArray: [5, 5],
          id: layer.id || `image_${index}`,
          role: 'image_placeholder',
          selectable: true,
        });
        
        // Add placeholder text
        const placeholderText = new fabric.Text('Drop image here', {
          left: (layer.position?.x || 100) + (layer.size?.width || 200) / 2,
          top: (layer.position?.y || 100) + (layer.size?.height || 200) / 2,
          fontSize: 14,
          fill: '#8b5cf6',
          originX: 'center',
          originY: 'center',
          selectable: false,
          evented: false,
        });
        canvas.add(placeholderText);
      } else if (layer.type === 'shape') {
        obj = new fabric.Rect({
          left: layer.position?.x || 100,
          top: layer.position?.y || 100,
          width: layer.size?.width || 100,
          height: layer.size?.height || 100,
          fill: layer.fill || '#8b5cf6',
          rx: layer.border_radius || 0,
          ry: layer.border_radius || 0,
          id: layer.id || `shape_${index}`,
          selectable: true,
        });
      }
      
      if (obj) {
        canvas.add(obj);
      }
    });
    
    canvas.renderAll();
    saveToHistory();
    updateLayers();
    
    console.log('Imported design loaded with', layers.length, 'layers');
  };

  // Update canvas size
  useEffect(() => {
    if (!fabricRef.current) return;
    const canvas = fabricRef.current;
    canvas.setWidth(canvasSize.width * zoom);
    canvas.setHeight(canvasSize.height * zoom);
    canvas.setZoom(zoom);
    canvas.renderAll();
  }, [canvasSize, zoom]);

  // Load existing design
  useEffect(() => {
    if (existingDesign?.canvas_data && fabricRef.current) {
      fabricRef.current.loadFromJSON(existingDesign.canvas_data, () => {
        fabricRef.current.renderAll();
      });
    }
  }, [existingDesign]);

  const addDefaultBackground = () => {
    if (!fabricRef.current) return;
    const canvas = fabricRef.current;
    
    // Create gradient background
    const gradient = new fabric.Gradient({
      type: 'linear',
      coords: { x1: 0, y1: 0, x2: canvasSize.width, y2: canvasSize.height },
      colorStops: [
        { offset: 0, color: '#1a1a2e' },
        { offset: 1, color: '#16213e' },
      ],
    });
    
    const bg = new fabric.Rect({
      left: 0,
      top: 0,
      width: canvasSize.width,
      height: canvasSize.height,
      fill: gradient,
      selectable: false,
      evented: false,
    });
    
    canvas.add(bg);
    canvas.sendToBack(bg);
    canvas.renderAll();
  };

  const saveToHistory = useCallback(() => {
    if (!fabricRef.current) return;
    const json = fabricRef.current.toJSON();
    setHistory(prev => [...prev.slice(0, historyIndex + 1), json]);
    setHistoryIndex(prev => prev + 1);
  }, [historyIndex]);

  const undo = () => {
    if (historyIndex <= 0) return;
    const newIndex = historyIndex - 1;
    setHistoryIndex(newIndex);
    fabricRef.current?.loadFromJSON(history[newIndex], () => {
      fabricRef.current?.renderAll();
    });
  };

  const redo = () => {
    if (historyIndex >= history.length - 1) return;
    const newIndex = historyIndex + 1;
    setHistoryIndex(newIndex);
    fabricRef.current?.loadFromJSON(history[newIndex], () => {
      fabricRef.current?.renderAll();
    });
  };

  // AI Generation using local LLM blueprint
  const handleGenerate = async () => {
    if (!prompt.trim() || isGenerating) return;
    
    setIsGenerating(true);
    setGenerationProgress(0);
    
    // Simulate progress
    const progressInterval = setInterval(() => {
      setGenerationProgress(prev => Math.min(prev + 5, 85));
    }, 300);
    
    try {
      // Get brand rules from localStorage (Brand Kit)
      const savedBrandKit = localStorage.getItem('adgenesis_brand_kit');
      const brandRules = savedBrandKit ? JSON.parse(savedBrandKit) : {};
      
      // Determine platform and format from canvas size
      const platform = location.state?.platform || 'meta';
      const format = canvasSize.width === canvasSize.height ? 'square' : 
                     canvasSize.width > canvasSize.height ? 'landscape' : 'story';
      
      console.log('Generating design with:', { prompt, platform, format, brandRules });
      
      // Call the local LLM blueprint generation API
      const result = await generateDesignBlueprint({
        prompt,
        platform,
        format,
        brandRules: {
          colors: brandRules.colors || [],
          fonts: brandRules.fonts || [],
          logo: brandRules.logo || null,
        },
      });
      
      setGenerationProgress(90);
      
      if (result.success && result.blueprint) {
        console.log('Generated blueprint:', result.blueprint);
        
        // Render the blueprint to canvas
        renderBlueprintToCanvas(result.blueprint);
        
        setGenerationProgress(100);
        saveToHistory();
        
        // Show generation info
        if (result.generation_time) {
          console.log(`Design generated in ${result.generation_time.toFixed(2)}s`);
        }
      } else {
        throw new Error(result.error || 'Blueprint generation failed');
      }
      
      queryClient.invalidateQueries('designs');
      
    } catch (error) {
      console.error('Generation error:', error);
      
      // Fallback to mock design for demo purposes
      console.log('Using fallback design...');
      renderFallbackDesign();
      setGenerationProgress(100);
      saveToHistory();
    } finally {
      clearInterval(progressInterval);
      setIsGenerating(false);
      setGenerationProgress(0);
    }
  };
  
  // Render AI-generated blueprint to Fabric.js canvas
  const renderBlueprintToCanvas = (blueprint) => {
    if (!fabricRef.current || !blueprint) return;
    const canvas = fabricRef.current;
    
    // Clear canvas
    canvas.clear();
    
    // Get background color from blueprint
    const bgColor = blueprint.background?.color || 
                    blueprint.color_palette?.background || 
                    '#1a1a2e';
    
    // Create background
    const bg = new fabric.Rect({
      left: 0,
      top: 0,
      width: canvasSize.width,
      height: canvasSize.height,
      fill: bgColor,
      selectable: false,
      evented: false,
      id: 'background',
    });
    canvas.add(bg);
    canvas.sendToBack(bg);
    
    // Helper to convert percentage to pixels
    const toPixelX = (percent) => (percent / 100) * canvasSize.width;
    const toPixelY = (percent) => (percent / 100) * canvasSize.height;
    const toPixelW = (percent) => (percent / 100) * canvasSize.width;
    const toPixelH = (percent) => (percent / 100) * canvasSize.height;
    
    // Add elements from blueprint
    if (blueprint.elements && Array.isArray(blueprint.elements)) {
      blueprint.elements.forEach((element, index) => {
        let obj = null;
        const elementId = element.id || `element-${index}-${Date.now()}`;
        
        // Get position (convert from percentage if needed)
        const posX = element.position?.x !== undefined ? toPixelX(element.position.x) : (element.x || canvasSize.width / 2);
        const posY = element.position?.y !== undefined ? toPixelY(element.position.y) : (element.y || canvasSize.height / 2);
        const width = element.size?.width !== undefined ? toPixelW(element.size.width) : (element.width || 400);
        const height = element.size?.height !== undefined ? toPixelH(element.size.height) : (element.height || 100);
        
        switch (element.type) {
          case 'text':
            obj = new fabric.Textbox(element.content || 'Text', {
              left: posX,
              top: posY,
              width: width,
              fontSize: element.font_size || element.fontSize || 48,
              fontFamily: element.font_family || element.fontFamily || 'Inter',
              fontWeight: element.font_weight || element.fontWeight || 'bold',
              fill: element.color || element.fill || '#ffffff',
              textAlign: element.align || element.textAlign || 'left',
              lineHeight: element.line_height || 1.2,
              letterSpacing: element.letter_spacing || 0,
              id: elementId,
              name: element.style || element.type,
            });
            break;
            
          case 'cta_button':
            // Create button background
            const btnWidth = width || 200;
            const btnHeight = height || 56;
            const btnColor = blueprint.color_palette?.primary || '#8B5CF6';
            
            const btnBg = new fabric.Rect({
              left: posX,
              top: posY,
              width: btnWidth,
              height: btnHeight,
              fill: btnColor,
              rx: element.corner_radius || 28,
              ry: element.corner_radius || 28,
              id: `${elementId}-bg`,
              name: 'cta_button_bg',
            });
            canvas.add(btnBg);
            
            // Create button text
            obj = new fabric.Text(element.text || 'Click Here', {
              left: posX + btnWidth / 2,
              top: posY + btnHeight / 2,
              fontSize: element.font_size || 18,
              fontFamily: element.font_family || 'Inter',
              fontWeight: element.font_weight || 'bold',
              fill: element.text_color || '#ffffff',
              originX: 'center',
              originY: 'center',
              id: `${elementId}-text`,
              name: 'cta_button_text',
            });
            break;
            
          case 'shape':
          case 'rectangle':
            obj = new fabric.Rect({
              left: posX,
              top: posY,
              width: width,
              height: height,
              fill: element.fill || element.color || '#8B5CF6',
              rx: element.corner_radius || element.rx || 8,
              ry: element.corner_radius || element.ry || 8,
              id: elementId,
              name: element.role || 'shape',
            });
            break;
            
          case 'circle':
            obj = new fabric.Circle({
              left: posX,
              top: posY,
              radius: width ? width / 2 : 50,
              fill: element.fill || element.color || '#06B6D4',
              id: elementId,
              name: element.role || 'circle',
            });
            break;
            
          case 'image_placeholder':
            // Create placeholder rectangle for image
            obj = new fabric.Rect({
              left: posX,
              top: posY,
              width: width,
              height: height,
              fill: '#374151',
              stroke: '#6B7280',
              strokeWidth: 2,
              strokeDashArray: [5, 5],
              rx: element.corner_radius || 8,
              ry: element.corner_radius || 8,
              id: elementId,
              name: 'image_placeholder',
            });
            
            // Add text label on placeholder
            const labelText = new fabric.Text('📷 Drop Image', {
              left: posX + width / 2,
              top: posY + height / 2,
              fontSize: 16,
              fill: '#9CA3AF',
              fontFamily: 'Inter',
              originX: 'center',
              originY: 'center',
              selectable: false,
              evented: false,
            });
            
            canvas.add(obj);
            canvas.add(labelText);
            return; // Skip adding obj again
            
          default:
            break;
        }
        
        if (obj) {
          canvas.add(obj);
        }
      });
    }
    
    canvas.renderAll();
    updateLayers();
  };
  
  // Fallback design when API fails
  const renderFallbackDesign = () => {
    if (!fabricRef.current) return;
    const canvas = fabricRef.current;
    
    canvas.clear();
    
    // Background
    const bg = new fabric.Rect({
      left: 0,
      top: 0,
      width: canvasSize.width,
      height: canvasSize.height,
      fill: '#1a1a2e',
      selectable: false,
      evented: false,
    });
    canvas.add(bg);
    
    // Headline
    const headline = new fabric.Textbox(prompt.split(' ').slice(0, 4).join(' ') || 'Your Headline', {
      left: canvasSize.width / 2,
      top: canvasSize.height * 0.3,
      width: canvasSize.width * 0.8,
      fontSize: 64,
      fontFamily: 'Inter',
      fontWeight: 'bold',
      fill: '#ffffff',
      textAlign: 'center',
      originX: 'center',
      originY: 'center',
    });
    canvas.add(headline);
    
    // Subheadline
    const subheadline = new fabric.Textbox('Add your subheadline here', {
      left: canvasSize.width / 2,
      top: canvasSize.height * 0.5,
      width: canvasSize.width * 0.7,
      fontSize: 28,
      fontFamily: 'Inter',
      fontWeight: 'normal',
      fill: '#a0a0a0',
      textAlign: 'center',
      originX: 'center',
      originY: 'center',
    });
    canvas.add(subheadline);
    
    // CTA Button
    const ctaButton = new fabric.Rect({
      left: canvasSize.width / 2,
      top: canvasSize.height * 0.75,
      width: 200,
      height: 56,
      fill: '#8B5CF6',
      rx: 28,
      ry: 28,
      originX: 'center',
      originY: 'center',
    });
    canvas.add(ctaButton);
    
    const ctaText = new fabric.Text('Get Started', {
      left: canvasSize.width / 2,
      top: canvasSize.height * 0.75,
      fontSize: 18,
      fontFamily: 'Inter',
      fontWeight: 'bold',
      fill: '#ffffff',
      originX: 'center',
      originY: 'center',
    });
    canvas.add(ctaText);
    
    canvas.renderAll();
    updateLayers();
  };

  // Add image to canvas
  const addImageToCanvas = (imageUrl) => {
    if (!fabricRef.current) return;
    
    fabric.Image.fromURL(imageUrl, (img) => {
      // Scale to fit canvas
      const scale = Math.min(
        canvasSize.width / img.width,
        canvasSize.height / img.height
      );
      
      img.set({
        left: canvasSize.width / 2,
        top: canvasSize.height / 2,
        scaleX: scale,
        scaleY: scale,
        originX: 'center',
        originY: 'center',
      });
      
      fabricRef.current.clear();
      fabricRef.current.add(img);
      fabricRef.current.renderAll();
    }, { crossOrigin: 'anonymous' });
  };

  const renderDesignToCanvas = (data) => {
    if (!fabricRef.current || !data) return;
    const canvas = fabricRef.current;
    
    // Clear canvas
    canvas.clear();
    
    // Set background
    const bgColor = data.background_color || '#1a1a2e';
    
    if (data.background_gradient) {
      const gradient = new fabric.Gradient({
        type: 'linear',
        coords: { x1: 0, y1: 0, x2: canvasSize.width, y2: canvasSize.height },
        colorStops: data.background_gradient.stops || [
          { offset: 0, color: bgColor },
          { offset: 1, color: '#16213e' },
        ],
      });
      
      const bg = new fabric.Rect({
        left: 0,
        top: 0,
        width: canvasSize.width,
        height: canvasSize.height,
        fill: gradient,
        selectable: false,
        evented: false,
      });
      canvas.add(bg);
    } else {
      canvas.setBackgroundColor(bgColor, canvas.renderAll.bind(canvas));
    }
    
    // Add elements
    if (data.elements && Array.isArray(data.elements)) {
      data.elements.forEach(element => {
        let obj = null;
        
        switch (element.type) {
          case 'text':
            obj = new fabric.Textbox(element.content || 'Text', {
              left: element.x || 100,
              top: element.y || 100,
              width: element.width || 400,
              fontSize: element.fontSize || 48,
              fontFamily: element.fontFamily || 'Inter',
              fontWeight: element.fontWeight || 'bold',
              fill: element.fill || '#ffffff',
              textAlign: element.textAlign || 'center',
            });
            break;
            
          case 'rectangle':
          case 'shape':
            obj = new fabric.Rect({
              left: element.x || 100,
              top: element.y || 100,
              width: element.width || 200,
              height: element.height || 100,
              fill: element.fill || '#8B5CF6',
              rx: element.rx || 8,
              ry: element.ry || 8,
            });
            break;
            
          case 'circle':
            obj = new fabric.Circle({
              left: element.x || 100,
              top: element.y || 100,
              radius: element.radius || 50,
              fill: element.fill || '#06B6D4',
            });
            break;
            
          case 'image':
            if (element.src) {
              fabric.Image.fromURL(element.src, (img) => {
                img.set({
                  left: element.x || 0,
                  top: element.y || 0,
                  scaleX: element.width ? element.width / img.width : 1,
                  scaleY: element.height ? element.height / img.height : 1,
                });
                canvas.add(img);
                canvas.renderAll();
              }, { crossOrigin: 'anonymous' });
            }
            return;
            
          default:
            return;
        }
        
        if (obj) {
          canvas.add(obj);
        }
      });
    }
    
    canvas.renderAll();
  };

  // Add text with different styles
  const addText = (style = 'heading') => {
    if (!fabricRef.current) return;
    
    const textStyles = {
      heading: {
        text: 'Add a heading',
        fontSize: 64,
        fontWeight: 'bold',
        fontFamily: 'Inter',
      },
      subheading: {
        text: 'Add a subheading',
        fontSize: 36,
        fontWeight: '600',
        fontFamily: 'Inter',
      },
      body: {
        text: 'Add body text here. Click to edit.',
        fontSize: 24,
        fontWeight: 'normal',
        fontFamily: 'Inter',
      },
      caption: {
        text: 'Caption text',
        fontSize: 16,
        fontWeight: 'normal',
        fontFamily: 'Inter',
      },
    };
    
    const config = textStyles[style] || textStyles.heading;
    
    const text = new fabric.Textbox(config.text, {
      left: canvasSize.width / 2,
      top: canvasSize.height / 2,
      width: style === 'body' ? 500 : 400,
      fontSize: config.fontSize,
      fontFamily: config.fontFamily,
      fontWeight: config.fontWeight,
      fill: '#ffffff',
      textAlign: 'center',
      originX: 'center',
      originY: 'center',
      lineHeight: 1.2,
    });
    
    fabricRef.current.add(text);
    fabricRef.current.setActiveObject(text);
    fabricRef.current.renderAll();
    saveToHistory();
    updateLayers();
  };

  // Add shape
  const addShape = (type) => {
    if (!fabricRef.current) return;
    let shape;
    
    switch (type) {
      case 'rectangle':
        shape = new fabric.Rect({
          left: canvasSize.width / 2 - 100,
          top: canvasSize.height / 2 - 50,
          width: 200,
          height: 100,
          fill: '#8B5CF6',
          rx: 8,
          ry: 8,
        });
        break;
      case 'circle':
        shape = new fabric.Circle({
          left: canvasSize.width / 2 - 50,
          top: canvasSize.height / 2 - 50,
          radius: 50,
          fill: '#06B6D4',
        });
        break;
      case 'triangle':
        shape = new fabric.Triangle({
          left: canvasSize.width / 2 - 50,
          top: canvasSize.height / 2 - 50,
          width: 100,
          height: 100,
          fill: '#F59E0B',
        });
        break;
      default:
        return;
    }
    
    fabricRef.current.add(shape);
    fabricRef.current.setActiveObject(shape);
    fabricRef.current.renderAll();
    saveToHistory();
  };

  // Upload image
  const handleImageUpload = (e) => {
    const file = e.target.files?.[0];
    if (!file || !fabricRef.current) return;
    
    const reader = new FileReader();
    reader.onload = (event) => {
      fabric.Image.fromURL(event.target.result, (img) => {
        const maxSize = Math.min(canvasSize.width, canvasSize.height) * 0.5;
        const scale = Math.min(maxSize / img.width, maxSize / img.height);
        
        img.set({
          left: canvasSize.width / 2 - (img.width * scale) / 2,
          top: canvasSize.height / 2 - (img.height * scale) / 2,
          scaleX: scale,
          scaleY: scale,
        });
        
        fabricRef.current.add(img);
        fabricRef.current.setActiveObject(img);
        fabricRef.current.renderAll();
        saveToHistory();
      });
    };
    reader.readAsDataURL(file);
  };

  // Delete selected object
  const deleteSelected = () => {
    if (!fabricRef.current || !selectedObject) return;
    fabricRef.current.remove(selectedObject);
    fabricRef.current.renderAll();
    setSelectedObject(null);
    saveToHistory();
  };

  // Duplicate selected object
  const duplicateSelected = () => {
    if (!fabricRef.current || !selectedObject) return;
    selectedObject.clone((cloned) => {
      cloned.set({
        left: cloned.left + 20,
        top: cloned.top + 20,
      });
      fabricRef.current.add(cloned);
      fabricRef.current.setActiveObject(cloned);
      fabricRef.current.renderAll();
      saveToHistory();
    });
  };

  // Update layers from canvas
  const updateLayers = useCallback(() => {
    if (!fabricRef.current) return;
    const objects = fabricRef.current.getObjects();
    const newLayers = objects
      .filter(obj => obj.selectable !== false) // Exclude background
      .map((obj, index) => ({
        id: obj.id || `layer-${index}`,
        name: getLayerName(obj, index),
        type: obj.type,
        visible: obj.visible !== false,
        locked: obj.selectable === false && obj.evented === false,
        object: obj,
      }))
      .reverse(); // Top layer first
    setLayers(newLayers);
  }, []);

  // Get friendly layer name
  const getLayerName = (obj, index) => {
    if (obj.name) return obj.name;
    switch (obj.type) {
      case 'textbox':
        return obj.text?.substring(0, 20) || 'Text';
      case 'rect':
        return 'Rectangle';
      case 'circle':
        return 'Circle';
      case 'triangle':
        return 'Triangle';
      case 'image':
        return 'Image';
      default:
        return `Layer ${index + 1}`;
    }
  };

  // Layer visibility toggle
  const toggleLayerVisibility = (layerId) => {
    const layer = layers.find(l => l.id === layerId);
    if (layer && layer.object) {
      layer.object.set('visible', !layer.object.visible);
      fabricRef.current?.renderAll();
      updateLayers();
    }
  };

  // Layer lock toggle
  const toggleLayerLock = (layerId) => {
    const layer = layers.find(l => l.id === layerId);
    if (layer && layer.object) {
      const isLocked = !layer.object.selectable;
      layer.object.set({
        selectable: isLocked,
        evented: isLocked,
      });
      fabricRef.current?.renderAll();
      updateLayers();
    }
  };

  // Move layer up/down
  const moveLayer = (layerId, direction) => {
    const layer = layers.find(l => l.id === layerId);
    if (!layer || !layer.object || !fabricRef.current) return;
    
    if (direction === 'up') {
      fabricRef.current.bringForward(layer.object);
    } else {
      fabricRef.current.sendBackwards(layer.object);
    }
    fabricRef.current.renderAll();
    updateLayers();
    saveToHistory();
  };

  // Select layer
  const selectLayer = (layerId) => {
    const layer = layers.find(l => l.id === layerId);
    if (layer && layer.object && fabricRef.current) {
      fabricRef.current.setActiveObject(layer.object);
      fabricRef.current.renderAll();
      setSelectedLayerId(layerId);
    }
  };

  // Delete layer
  const deleteLayer = (layerId) => {
    const layer = layers.find(l => l.id === layerId);
    if (layer && layer.object && fabricRef.current) {
      fabricRef.current.remove(layer.object);
      fabricRef.current.renderAll();
      saveToHistory();
    }
  };

  // Enhanced Export with options
  const handleExport = async () => {
    if (!fabricRef.current) return;
    
    setIsExporting(true);
    
    try {
      // Reset zoom for export
      const originalZoom = fabricRef.current.getZoom();
      fabricRef.current.setZoom(1);
      fabricRef.current.setWidth(canvasSize.width);
      fabricRef.current.setHeight(canvasSize.height);
      
      let dataURL;
      const projectName = location.state?.name || 'design';
      const filename = `${projectName.replace(/[^a-z0-9]/gi, '_')}.${exportFormat}`;
      
      if (exportFormat === 'svg') {
        // SVG export
        const svg = fabricRef.current.toSVG();
        const blob = new Blob([svg], { type: 'image/svg+xml' });
        dataURL = URL.createObjectURL(blob);
        
        const link = document.createElement('a');
        link.download = filename;
        link.href = dataURL;
        link.click();
        URL.revokeObjectURL(dataURL);
      } else if (exportFormat === 'pdf') {
        // PDF export using canvas to PDF
        const canvas = fabricRef.current.toCanvasElement(exportScale);
        dataURL = canvas.toDataURL('image/png', 1);
        
        // Simple PDF generation (base64 image in HTML)
        const pdfContent = `
          <html>
            <head><title>${projectName}</title></head>
            <body style="margin:0;padding:0;display:flex;justify-content:center;align-items:center;min-height:100vh;">
              <img src="${dataURL}" style="max-width:100%;height:auto;" />
            </body>
          </html>
        `;
        const blob = new Blob([pdfContent], { type: 'text/html' });
        const pdfUrl = URL.createObjectURL(blob);
        
        // Open in new window for print to PDF
        const printWindow = window.open(pdfUrl);
        if (printWindow) {
          printWindow.onload = () => {
            printWindow.print();
          };
        }
        URL.revokeObjectURL(pdfUrl);
      } else {
        // PNG/JPG export
        dataURL = fabricRef.current.toDataURL({
          format: exportFormat === 'jpg' ? 'jpeg' : 'png',
          quality: exportQuality,
          multiplier: exportScale,
        });
        
        const link = document.createElement('a');
        link.download = filename;
        link.href = dataURL;
        link.click();
      }
      
      // Restore zoom
      fabricRef.current.setZoom(originalZoom);
      fabricRef.current.setWidth(canvasSize.width * originalZoom);
      fabricRef.current.setHeight(canvasSize.height * originalZoom);
      fabricRef.current.renderAll();
      
      setShowExportModal(false);
    } catch (error) {
      console.error('Export error:', error);
      alert('Export failed. Please try again.');
    } finally {
      setIsExporting(false);
    }
  };

  // Quick export (direct PNG)
  const quickExport = () => {
    setExportFormat('png');
    setShowExportModal(true);
  };

  // Save project to localStorage
  const saveProject = useCallback(async () => {
    if (!fabricRef.current) return;
    
    setIsSaving(true);
    
    try {
      // Generate thumbnail
      const tempZoom = fabricRef.current.getZoom();
      fabricRef.current.setZoom(0.3);
      fabricRef.current.setWidth(canvasSize.width * 0.3);
      fabricRef.current.setHeight(canvasSize.height * 0.3);
      
      const thumbnail = fabricRef.current.toDataURL({
        format: 'png',
        quality: 0.5,
      });
      
      // Restore zoom
      fabricRef.current.setZoom(tempZoom);
      fabricRef.current.setWidth(canvasSize.width * tempZoom);
      fabricRef.current.setHeight(canvasSize.height * tempZoom);
      
      // Get canvas data
      const canvasData = fabricRef.current.toJSON();
      
      // Load existing projects
      const existingProjects = JSON.parse(localStorage.getItem('adgenesis_projects') || '[]');
      
      // Find or create project
      const projectIndex = existingProjects.findIndex(p => p.id === currentProjectId.current);
      
      const projectData = {
        id: currentProjectId.current,
        name: projectName,
        width: canvasSize.width,
        height: canvasSize.height,
        canvasData,
        thumbnail,
        createdAt: projectIndex >= 0 ? existingProjects[projectIndex].createdAt : new Date().toISOString(),
        updatedAt: new Date().toISOString(),
      };
      
      if (projectIndex >= 0) {
        existingProjects[projectIndex] = projectData;
      } else {
        existingProjects.unshift(projectData);
      }
      
      // Save to localStorage
      localStorage.setItem('adgenesis_projects', JSON.stringify(existingProjects));
      setLastSaved(new Date());
      
    } catch (error) {
      console.error('Save error:', error);
      alert('Failed to save project.');
    } finally {
      setIsSaving(false);
    }
  }, [projectName, canvasSize]);

  // Auto-save on changes
  useEffect(() => {
    const autoSaveTimer = setTimeout(() => {
      if (historyIndex > 0) {
        saveProject();
      }
    }, 30000); // Auto-save every 30 seconds if there are changes
    
    return () => clearTimeout(autoSaveTimer);
  }, [historyIndex, saveProject]);

  // Load project from localStorage if passed via state
  useEffect(() => {
    if (location.state?.canvasData && fabricRef.current) {
      fabricRef.current.loadFromJSON(location.state.canvasData, () => {
        fabricRef.current.renderAll();
        updateLayers();
      });
    }
  }, [location.state?.canvasData]);

  // Keyboard shortcuts
  useEffect(() => {
    const handleKeyDown = (e) => {
      // Don't trigger shortcuts when typing in inputs
      if (e.target.tagName === 'INPUT' || e.target.tagName === 'TEXTAREA') {
        // Only allow Escape and Ctrl+S in inputs
        if (e.key !== 'Escape' && !((e.ctrlKey || e.metaKey) && e.key === 's')) {
          return;
        }
      }
      
      const isTextEditing = fabricRef.current?.getActiveObject()?.isEditing;
      
      // Save: Ctrl+S
      if ((e.ctrlKey || e.metaKey) && e.key === 's') {
        e.preventDefault();
        saveProject();
        return;
      }
      
      // Escape: Deselect or close modal
      if (e.key === 'Escape') {
        if (showExportModal) {
          setShowExportModal(false);
        } else {
          fabricRef.current?.discardActiveObject();
          fabricRef.current?.renderAll();
        }
        return;
      }
      
      // Don't handle other shortcuts if text is being edited
      if (isTextEditing) return;
      
      // Delete/Backspace: Delete selected
      if (e.key === 'Delete' || e.key === 'Backspace') {
        e.preventDefault();
        deleteSelected();
        return;
      }
      
      // Undo: Ctrl+Z
      if ((e.ctrlKey || e.metaKey) && e.key === 'z' && !e.shiftKey) {
        e.preventDefault();
        undo();
        return;
      }
      
      // Redo: Ctrl+Shift+Z or Ctrl+Y
      if ((e.ctrlKey || e.metaKey) && (e.key === 'y' || (e.key === 'z' && e.shiftKey))) {
        e.preventDefault();
        redo();
        return;
      }
      
      // Duplicate: Ctrl+D
      if ((e.ctrlKey || e.metaKey) && e.key === 'd') {
        e.preventDefault();
        duplicateSelected();
        return;
      }
      
      // Copy: Ctrl+C
      if ((e.ctrlKey || e.metaKey) && e.key === 'c') {
        const activeObj = fabricRef.current?.getActiveObject();
        if (activeObj) {
          activeObj.clone((cloned) => {
            window.copiedObject = cloned;
          });
        }
        return;
      }
      
      // Paste: Ctrl+V
      if ((e.ctrlKey || e.metaKey) && e.key === 'v') {
        if (window.copiedObject) {
          window.copiedObject.clone((cloned) => {
            cloned.set({
              left: cloned.left + 20,
              top: cloned.top + 20,
            });
            fabricRef.current?.add(cloned);
            fabricRef.current?.setActiveObject(cloned);
            fabricRef.current?.renderAll();
            saveToHistory();
            updateLayers();
          });
        }
        return;
      }
      
      // Select All: Ctrl+A
      if ((e.ctrlKey || e.metaKey) && e.key === 'a') {
        e.preventDefault();
        const canvas = fabricRef.current;
        if (canvas) {
          canvas.discardActiveObject();
          const sel = new fabric.ActiveSelection(canvas.getObjects(), { canvas });
          canvas.setActiveObject(sel);
          canvas.renderAll();
        }
        return;
      }
      
      // Export: Ctrl+E
      if ((e.ctrlKey || e.metaKey) && e.key === 'e') {
        e.preventDefault();
        setShowExportModal(true);
        return;
      }
      
      // Add text: T
      if (e.key === 't' && !e.ctrlKey && !e.metaKey) {
        addText('heading');
        return;
      }
      
      // Add rectangle: R
      if (e.key === 'r' && !e.ctrlKey && !e.metaKey) {
        addShape('rectangle');
        return;
      }
      
      // Add circle: C
      if (e.key === 'c' && !e.ctrlKey && !e.metaKey) {
        addShape('circle');
        return;
      }
      
      // Bring forward: ]
      if (e.key === ']') {
        const canvas = fabricRef.current;
        const activeObj = canvas?.getActiveObject();
        if (activeObj) {
          canvas.bringForward(activeObj);
          canvas.renderAll();
          updateLayers();
        }
        return;
      }
      
      // Send backward: [
      if (e.key === '[') {
        const canvas = fabricRef.current;
        const activeObj = canvas?.getActiveObject();
        if (activeObj) {
          canvas.sendBackwards(activeObj);
          canvas.renderAll();
          updateLayers();
        }
        return;
      }
      
      // Zoom in: +/=
      if ((e.key === '+' || e.key === '=') && (e.ctrlKey || e.metaKey)) {
        e.preventDefault();
        handleZoom(0.1);
        return;
      }
      
      // Zoom out: -
      if (e.key === '-' && (e.ctrlKey || e.metaKey)) {
        e.preventDefault();
        handleZoom(-0.1);
        return;
      }
      
      // Show shortcuts: ?
      if (e.key === '?' || (e.shiftKey && e.key === '/')) {
        setShowShortcutsModal(true);
        return;
      }
    };
    
    window.addEventListener('keydown', handleKeyDown);
    return () => window.removeEventListener('keydown', handleKeyDown);
  }, [saveProject, deleteSelected, undo, redo, duplicateSelected, showExportModal, addText, addShape, updateLayers, saveToHistory]);

  // Zoom controls
  const handleZoom = (delta) => {
    setZoom(prev => Math.min(Math.max(prev + delta, 0.2), 2));
  };

  return (
    <div className="editor">
      {/* Header */}
      <header className="editor-header">
        <div className="header-left">
          <button className="header-btn back-btn" onClick={() => navigate('/')}>
            <ArrowLeftIcon />
          </button>
          <div className="project-info">
            <input 
              type="text" 
              className="project-name" 
              value={projectName}
              onChange={(e) => setProjectName(e.target.value)}
              placeholder="Untitled Design"
            />
            <div className="project-meta-info">
              <span className="project-size">
                {canvasSize.width} × {canvasSize.height} px
              </span>
              {lastSaved && (
                <span className="save-status">
                  Saved {new Date(lastSaved).toLocaleTimeString()}
                </span>
              )}
            </div>
          </div>
        </div>
        
        <div className="header-center">
          <div className="history-controls">
            <button 
              className="header-btn" 
              onClick={undo}
              disabled={historyIndex <= 0}
              title="Undo (Ctrl+Z)"
            >
              <UndoIcon />
            </button>
            <button 
              className="header-btn" 
              onClick={redo}
              disabled={historyIndex >= history.length - 1}
              title="Redo (Ctrl+Y)"
            >
              <RedoIcon />
            </button>
          </div>
          
          <div className="zoom-controls">
            <button className="header-btn" onClick={() => handleZoom(-0.1)} title="Zoom Out">
              <ZoomOutIcon />
            </button>
            <span className="zoom-level">{Math.round(zoom * 100)}%</span>
            <button className="header-btn" onClick={() => handleZoom(0.1)} title="Zoom In">
              <ZoomInIcon />
            </button>
          </div>
        </div>
        
        <div className="header-right">
          <button 
            className="header-btn save-btn" 
            onClick={saveProject}
            disabled={isSaving}
            title="Save Project (Ctrl+S)"
          >
            <SaveIcon />
            <span>{isSaving ? 'Saving...' : 'Save'}</span>
          </button>
          <button 
            className="header-btn shortcuts-btn"
            onClick={() => setShowShortcutsModal(true)}
            title="Keyboard Shortcuts (?)"
          >
            <KeyboardIcon />
          </button>
          <button className="header-btn export-btn" onClick={quickExport}>
            <DownloadIcon />
            <span>Export</span>
          </button>
        </div>
      </header>

      {/* Keyboard Shortcuts Modal */}
      {showShortcutsModal && (
        <div className="modal-overlay" onClick={() => setShowShortcutsModal(false)}>
          <div className="shortcuts-modal" onClick={e => e.stopPropagation()}>
            <div className="modal-header">
              <h2>
                <KeyboardIcon />
                Keyboard Shortcuts
              </h2>
              <button className="modal-close" onClick={() => setShowShortcutsModal(false)}>
                <CloseIcon />
              </button>
            </div>
            
            <div className="shortcuts-content">
              <div className="shortcuts-group">
                <h3>General</h3>
                <div className="shortcut-item">
                  <span className="shortcut-keys"><kbd>Ctrl</kbd> + <kbd>S</kbd></span>
                  <span className="shortcut-desc">Save project</span>
                </div>
                <div className="shortcut-item">
                  <span className="shortcut-keys"><kbd>Ctrl</kbd> + <kbd>E</kbd></span>
                  <span className="shortcut-desc">Open export dialog</span>
                </div>
                <div className="shortcut-item">
                  <span className="shortcut-keys"><kbd>Esc</kbd></span>
                  <span className="shortcut-desc">Deselect / Close modals</span>
                </div>
              </div>
              
              <div className="shortcuts-group">
                <h3>Edit</h3>
                <div className="shortcut-item">
                  <span className="shortcut-keys"><kbd>Ctrl</kbd> + <kbd>Z</kbd></span>
                  <span className="shortcut-desc">Undo</span>
                </div>
                <div className="shortcut-item">
                  <span className="shortcut-keys"><kbd>Ctrl</kbd> + <kbd>Shift</kbd> + <kbd>Z</kbd></span>
                  <span className="shortcut-desc">Redo</span>
                </div>
                <div className="shortcut-item">
                  <span className="shortcut-keys"><kbd>Ctrl</kbd> + <kbd>C</kbd></span>
                  <span className="shortcut-desc">Copy</span>
                </div>
                <div className="shortcut-item">
                  <span className="shortcut-keys"><kbd>Ctrl</kbd> + <kbd>V</kbd></span>
                  <span className="shortcut-desc">Paste</span>
                </div>
                <div className="shortcut-item">
                  <span className="shortcut-keys"><kbd>Ctrl</kbd> + <kbd>D</kbd></span>
                  <span className="shortcut-desc">Duplicate selected</span>
                </div>
                <div className="shortcut-item">
                  <span className="shortcut-keys"><kbd>Delete</kbd></span>
                  <span className="shortcut-desc">Delete selected</span>
                </div>
                <div className="shortcut-item">
                  <span className="shortcut-keys"><kbd>Ctrl</kbd> + <kbd>A</kbd></span>
                  <span className="shortcut-desc">Select all</span>
                </div>
              </div>
              
              <div className="shortcuts-group">
                <h3>Quick Add</h3>
                <div className="shortcut-item">
                  <span className="shortcut-keys"><kbd>T</kbd></span>
                  <span className="shortcut-desc">Add text</span>
                </div>
                <div className="shortcut-item">
                  <span className="shortcut-keys"><kbd>R</kbd></span>
                  <span className="shortcut-desc">Add rectangle</span>
                </div>
                <div className="shortcut-item">
                  <span className="shortcut-keys"><kbd>C</kbd></span>
                  <span className="shortcut-desc">Add circle</span>
                </div>
              </div>
              
              <div className="shortcuts-group">
                <h3>Layers</h3>
                <div className="shortcut-item">
                  <span className="shortcut-keys"><kbd>]</kbd></span>
                  <span className="shortcut-desc">Bring forward</span>
                </div>
                <div className="shortcut-item">
                  <span className="shortcut-keys"><kbd>[</kbd></span>
                  <span className="shortcut-desc">Send backward</span>
                </div>
              </div>
              
              <div className="shortcuts-group">
                <h3>View</h3>
                <div className="shortcut-item">
                  <span className="shortcut-keys"><kbd>Ctrl</kbd> + <kbd>+</kbd></span>
                  <span className="shortcut-desc">Zoom in</span>
                </div>
                <div className="shortcut-item">
                  <span className="shortcut-keys"><kbd>Ctrl</kbd> + <kbd>-</kbd></span>
                  <span className="shortcut-desc">Zoom out</span>
                </div>
              </div>
            </div>
          </div>
        </div>
      )}

      {/* Export Modal */}
      {showExportModal && (
        <div className="modal-overlay" onClick={() => setShowExportModal(false)}>
          <div className="export-modal" onClick={e => e.stopPropagation()}>
            <div className="modal-header">
              <h2>Export Design</h2>
              <button className="modal-close" onClick={() => setShowExportModal(false)}>
                <CloseIcon />
              </button>
            </div>
            
            <div className="modal-body">
              <div className="format-section">
                <h3>File Type</h3>
                <div className="format-grid">
                  {EXPORT_FORMATS.map(format => (
                    <button
                      key={format.id}
                      className={`format-option ${exportFormat === format.id ? 'active' : ''}`}
                      onClick={() => setExportFormat(format.id)}
                    >
                      <format.icon />
                      <span className="format-name">{format.name}</span>
                      <span className="format-desc">{format.desc}</span>
                    </button>
                  ))}
                </div>
              </div>
              
              {(exportFormat === 'png' || exportFormat === 'jpg') && (
                <div className="quality-section">
                  <h3>Quality</h3>
                  <div className="slider-container">
                    <input
                      type="range"
                      min="0.1"
                      max="1"
                      step="0.1"
                      value={exportQuality}
                      onChange={(e) => setExportQuality(parseFloat(e.target.value))}
                    />
                    <span className="slider-value">{Math.round(exportQuality * 100)}%</span>
                  </div>
                </div>
              )}
              
              <div className="scale-section">
                <h3>Scale</h3>
                <div className="scale-options">
                  {[1, 2, 3, 4].map(scale => (
                    <button
                      key={scale}
                      className={`scale-option ${exportScale === scale ? 'active' : ''}`}
                      onClick={() => setExportScale(scale)}
                    >
                      {scale}x
                      <span className="scale-size">
                        {canvasSize.width * scale} × {canvasSize.height * scale}
                      </span>
                    </button>
                  ))}
                </div>
              </div>
              
              <div className="export-preview">
                <div className="preview-info">
                  <span className="info-label">Output:</span>
                  <span className="info-value">
                    {canvasSize.width * exportScale} × {canvasSize.height * exportScale} px
                  </span>
                </div>
              </div>
            </div>
            
            <div className="modal-footer">
              <button className="cancel-btn" onClick={() => setShowExportModal(false)}>
                Cancel
              </button>
              <button 
                className="export-confirm-btn"
                onClick={handleExport}
                disabled={isExporting}
              >
                {isExporting ? (
                  <>
                    <div className="spinner" />
                    Exporting...
                  </>
                ) : (
                  <>
                    <DownloadIcon />
                    Download {exportFormat.toUpperCase()}
                  </>
                )}
              </button>
            </div>
          </div>
        </div>
      )}

      <div className="editor-body">
        {/* Left Toolbar */}
        <aside className="editor-toolbar">
          <button 
            className={`toolbar-btn ${activePanel === 'ai' ? 'active' : ''}`}
            onClick={() => setActivePanel('ai')}
            title="AI Generate"
          >
            <SparklesIcon />
            <span>AI</span>
          </button>
          <button 
            className={`toolbar-btn ${activePanel === 'templates' ? 'active' : ''}`}
            onClick={() => setActivePanel('templates')}
            title="Templates"
          >
            <TemplatesIcon />
            <span>Templates</span>
          </button>
          <button 
            className={`toolbar-btn ${activePanel === 'text' ? 'active' : ''}`}
            onClick={() => setActivePanel('text')}
            title="Text"
          >
            <TextIcon />
            <span>Text</span>
          </button>
          <button 
            className={`toolbar-btn ${activePanel === 'shapes' ? 'active' : ''}`}
            onClick={() => setActivePanel('shapes')}
            title="Shapes"
          >
            <ShapesIcon />
            <span>Shapes</span>
          </button>
          <button 
            className={`toolbar-btn ${activePanel === 'uploads' ? 'active' : ''}`}
            onClick={() => setActivePanel('uploads')}
            title="Uploads"
          >
            <UploadIcon />
            <span>Uploads</span>
          </button>
          <button 
            className={`toolbar-btn ${activePanel === 'layers' ? 'active' : ''}`}
            onClick={() => setActivePanel('layers')}
            title="Layers"
          >
            <LayersIcon />
            <span>Layers</span>
          </button>
        </aside>

        {/* Left Panel */}
        <aside className="editor-panel">
          {activePanel === 'ai' && (
            <div className="panel-content">
              <h3 className="panel-title">
                <SparklesIcon />
                AI Generate
              </h3>
              <p className="panel-desc">
                Describe your design and let AI create it for you
              </p>
              
              {/* Generation Type Toggle */}
              <div className="generation-type-toggle">
                <button 
                  className={`type-btn ${generationType === 'layout' ? 'active' : ''}`}
                  onClick={() => setGenerationType('layout')}
                >
                  📐 Layout
                </button>
                <button 
                  className={`type-btn ${generationType === 'image' ? 'active' : ''}`}
                  onClick={() => setGenerationType('image')}
                >
                  🖼️ AI Image
                </button>
              </div>
              
              <div className="ai-input-container">
                <textarea
                  className="ai-input"
                  placeholder={generationType === 'image' 
                    ? "Describe the image... e.g., 'Sleek smartphone floating in colorful nebula space'"
                    : "Describe your design... e.g., 'Modern tech startup ad with purple gradient'"
                  }
                  value={prompt}
                  onChange={(e) => setPrompt(e.target.value)}
                  rows={4}
                />
                
                {/* Style & Model Options for Image Generation */}
                {generationType === 'image' && (
                  <div className="ai-options">
                    <div className="option-group">
                      <label>Style:</label>
                      <select value={aiStyle} onChange={(e) => setAiStyle(e.target.value)}>
                        <option value="modern">Modern</option>
                        <option value="vibrant">Vibrant</option>
                        <option value="elegant">Elegant</option>
                        <option value="minimalist">Minimalist</option>
                        <option value="playful">Playful</option>
                        <option value="corporate">Corporate</option>
                      </select>
                    </div>
                    <div className="option-group">
                      <label>Model:</label>
                      <select value={aiModel} onChange={(e) => setAiModel(e.target.value)}>
                        <option value="sdxl-turbo">SDXL Turbo (Fast)</option>
                        <option value="sdxl">SDXL (Quality)</option>
                        <option value="playground">Playground v2.5</option>
                        <option value="flux">FLUX.1</option>
                      </select>
                    </div>
                  </div>
                )}
                
                <button 
                  className="generate-btn"
                  onClick={handleGenerate}
                  disabled={!prompt.trim() || isGenerating}
                >
                  {isGenerating ? (
                    <>
                      <div className="spinner" />
                      Generating... {generationProgress}%
                    </>
                  ) : (
                    <>
                      <SparklesIcon />
                      {generationType === 'image' ? 'Generate Image' : 'Generate Design'}
                    </>
                  )}
                </button>
                
                {isGenerating && (
                  <div className="progress-bar">
                    <div 
                      className="progress-fill" 
                      style={{ width: `${generationProgress}%` }}
                    />
                  </div>
                )}
              </div>
              
              <div className="suggestions">
                <span className="suggestions-label">Quick ideas:</span>
                <div className="suggestion-chips">
                  {AI_SUGGESTIONS.map((suggestion, i) => (
                    <button
                      key={i}
                      className="suggestion-chip"
                      onClick={() => setPrompt(suggestion.text)}
                    >
                      {suggestion.icon} {suggestion.text}
                    </button>
                  ))}
                </div>
              </div>
            </div>
          )}

          {activePanel === 'text' && (
            <div className="panel-content">
              <h3 className="panel-title">
                <TextIcon />
                Text
              </h3>
              <p className="panel-desc">Click to add text to your design</p>
              
              <div className="text-options">
                <button className="add-text-btn heading" onClick={() => addText('heading')}>
                  <span className="text-preview heading-preview">Add a heading</span>
                  <span className="text-size">64px Bold</span>
                </button>
                <button className="add-text-btn subheading" onClick={() => addText('subheading')}>
                  <span className="text-preview subheading-preview">Add a subheading</span>
                  <span className="text-size">36px Semibold</span>
                </button>
                <button className="add-text-btn body" onClick={() => addText('body')}>
                  <span className="text-preview body-preview">Add body text</span>
                  <span className="text-size">24px Regular</span>
                </button>
                <button className="add-text-btn caption" onClick={() => addText('caption')}>
                  <span className="text-preview caption-preview">Add caption</span>
                  <span className="text-size">16px Regular</span>
                </button>
              </div>
              
              {/* Font Combinations */}
              <div className="font-combos-section">
                <h4>Font Combinations</h4>
                <div className="font-combos">
                  <button className="font-combo-btn" onClick={() => {
                    addText('heading');
                    setTimeout(() => addText('body'), 100);
                  }}>
                    <span className="combo-heading" style={{ fontFamily: 'Inter' }}>Inter</span>
                    <span className="combo-body" style={{ fontFamily: 'Inter' }}>+ Inter</span>
                  </button>
                  <button className="font-combo-btn" onClick={() => {
                    addText('heading');
                    setTimeout(() => addText('body'), 100);
                  }}>
                    <span className="combo-heading" style={{ fontFamily: 'Playfair Display' }}>Playfair</span>
                    <span className="combo-body" style={{ fontFamily: 'Source Sans Pro' }}>+ Source Sans</span>
                  </button>
                  <button className="font-combo-btn" onClick={() => {
                    addText('heading');
                    setTimeout(() => addText('body'), 100);
                  }}>
                    <span className="combo-heading" style={{ fontFamily: 'Oswald' }}>Oswald</span>
                    <span className="combo-body" style={{ fontFamily: 'Lato' }}>+ Lato</span>
                  </button>
                </div>
              </div>
            </div>
          )}

          {activePanel === 'shapes' && (
            <div className="panel-content">
              <h3 className="panel-title">
                <ShapesIcon />
                Shapes
              </h3>
              
              <div className="shapes-grid">
                <button className="shape-btn" onClick={() => addShape('rectangle')}>
                  <div className="shape-preview rectangle" />
                  <span>Rectangle</span>
                </button>
                <button className="shape-btn" onClick={() => addShape('circle')}>
                  <div className="shape-preview circle" />
                  <span>Circle</span>
                </button>
                <button className="shape-btn" onClick={() => addShape('triangle')}>
                  <div className="shape-preview triangle" />
                  <span>Triangle</span>
                </button>
              </div>
            </div>
          )}

          {activePanel === 'uploads' && (
            <div className="panel-content">
              <h3 className="panel-title">
                <UploadIcon />
                Uploads
              </h3>
              
              <label className="upload-area">
                <input 
                  type="file" 
                  accept="image/*" 
                  onChange={handleImageUpload}
                  hidden
                />
                <UploadIcon />
                <span>Upload an image</span>
                <span className="upload-hint">or drag and drop</span>
              </label>
            </div>
          )}

          {activePanel === 'templates' && (
            <div className="panel-content">
              <h3 className="panel-title">
                <TemplatesIcon />
                Templates
              </h3>
              <p className="panel-desc">
                Choose a template to start with
              </p>
              {/* Template grid would go here */}
            </div>
          )}

          {activePanel === 'layers' && (
            <div className="panel-content">
              <h3 className="panel-title">
                <LayersIcon />
                Layers
              </h3>
              <p className="panel-desc">
                Manage your design layers
              </p>
              
              <div className="layers-list">
                {layers.length === 0 ? (
                  <div className="empty-layers">
                    <p>No layers yet</p>
                    <span>Add elements to see them here</span>
                  </div>
                ) : (
                  layers.map((layer, index) => (
                    <div 
                      key={layer.id}
                      className={`layer-item ${selectedLayerId === layer.id ? 'selected' : ''} ${!layer.visible ? 'hidden' : ''}`}
                      onClick={() => selectLayer(layer.id)}
                    >
                      <div className="layer-info">
                        <span className="layer-type">
                          {layer.type === 'textbox' && '📝'}
                          {layer.type === 'rect' && '⬜'}
                          {layer.type === 'circle' && '⭕'}
                          {layer.type === 'triangle' && '🔺'}
                          {layer.type === 'image' && '🖼️'}
                          {!['textbox', 'rect', 'circle', 'triangle', 'image'].includes(layer.type) && '📦'}
                        </span>
                        <span className="layer-name">{layer.name}</span>
                      </div>
                      
                      <div className="layer-actions">
                        <button 
                          className="layer-action-btn"
                          onClick={(e) => { e.stopPropagation(); moveLayer(layer.id, 'up'); }}
                          disabled={index === 0}
                          title="Move Up"
                        >
                          <MoveUpIcon />
                        </button>
                        <button 
                          className="layer-action-btn"
                          onClick={(e) => { e.stopPropagation(); moveLayer(layer.id, 'down'); }}
                          disabled={index === layers.length - 1}
                          title="Move Down"
                        >
                          <MoveDownIcon />
                        </button>
                        <button 
                          className={`layer-action-btn ${!layer.visible ? 'inactive' : ''}`}
                          onClick={(e) => { e.stopPropagation(); toggleLayerVisibility(layer.id); }}
                          title={layer.visible ? 'Hide' : 'Show'}
                        >
                          {layer.visible ? <EyeIcon /> : <EyeOffIcon />}
                        </button>
                        <button 
                          className={`layer-action-btn ${layer.locked ? 'active' : ''}`}
                          onClick={(e) => { e.stopPropagation(); toggleLayerLock(layer.id); }}
                          title={layer.locked ? 'Unlock' : 'Lock'}
                        >
                          <LockIcon />
                        </button>
                        <button 
                          className="layer-action-btn delete"
                          onClick={(e) => { e.stopPropagation(); deleteLayer(layer.id); }}
                          title="Delete"
                        >
                          <DeleteIcon />
                        </button>
                      </div>
                    </div>
                  ))
                )}
              </div>
            </div>
          )}
        </aside>

        {/* Canvas Area */}
        <main className="canvas-area" ref={containerRef}>
          <div className="canvas-wrapper">
            <canvas ref={canvasRef} />
          </div>
        </main>

        {/* Right Panel - Properties */}
        {selectedObject && (
          <aside className="properties-panel">
            <div className="properties-header">
              <h3>Properties</h3>
              <div className="properties-actions">
                <button 
                  className="prop-action-btn"
                  onClick={duplicateSelected}
                  title="Duplicate"
                >
                  <CopyIcon />
                </button>
                <button 
                  className="prop-action-btn delete"
                  onClick={deleteSelected}
                  title="Delete"
                >
                  <DeleteIcon />
                </button>
              </div>
            </div>
            
            <div className="properties-content">
              {/* Position */}
              <div className="property-group">
                <label className="property-label">Position</label>
                <div className="property-row">
                  <div className="property-input">
                    <span className="input-label">X</span>
                    <input 
                      type="number" 
                      value={Math.round(selectedObject.left || 0)}
                      onChange={(e) => {
                        selectedObject.set('left', Number(e.target.value));
                        fabricRef.current?.renderAll();
                      }}
                    />
                  </div>
                  <div className="property-input">
                    <span className="input-label">Y</span>
                    <input 
                      type="number" 
                      value={Math.round(selectedObject.top || 0)}
                      onChange={(e) => {
                        selectedObject.set('top', Number(e.target.value));
                        fabricRef.current?.renderAll();
                      }}
                    />
                  </div>
                </div>
              </div>
              
              {/* Size */}
              <div className="property-group">
                <label className="property-label">Size</label>
                <div className="property-row">
                  <div className="property-input">
                    <span className="input-label">W</span>
                    <input 
                      type="number" 
                      value={Math.round(selectedObject.width * (selectedObject.scaleX || 1))}
                      onChange={(e) => {
                        const newWidth = Number(e.target.value);
                        selectedObject.set('scaleX', newWidth / selectedObject.width);
                        fabricRef.current?.renderAll();
                      }}
                    />
                  </div>
                  <div className="property-input">
                    <span className="input-label">H</span>
                    <input 
                      type="number" 
                      value={Math.round(selectedObject.height * (selectedObject.scaleY || 1))}
                      onChange={(e) => {
                        const newHeight = Number(e.target.value);
                        selectedObject.set('scaleY', newHeight / selectedObject.height);
                        fabricRef.current?.renderAll();
                      }}
                    />
                  </div>
                </div>
              </div>
              
              {/* Color (for shapes and text) */}
              {(selectedObject.type === 'rect' || selectedObject.type === 'circle' || selectedObject.type === 'textbox') && (
                <div className="property-group">
                  <label className="property-label">Color</label>
                  <div className="color-picker">
                    <input 
                      type="color" 
                      value={selectedObject.fill || '#ffffff'}
                      onChange={(e) => {
                        selectedObject.set('fill', e.target.value);
                        fabricRef.current?.renderAll();
                      }}
                    />
                    <span>{selectedObject.fill || '#ffffff'}</span>
                  </div>
                </div>
              )}
              
              {/* Text properties */}
              {selectedObject.type === 'textbox' && (
                <>
                  <div className="property-group">
                    <label className="property-label">Font Family</label>
                    <select 
                      className="full-width-input"
                      value={selectedObject.fontFamily || 'Inter'}
                      onChange={(e) => {
                        selectedObject.set('fontFamily', e.target.value);
                        fabricRef.current?.renderAll();
                      }}
                    >
                      <option value="Inter">Inter</option>
                      <option value="Arial">Arial</option>
                      <option value="Helvetica">Helvetica</option>
                      <option value="Georgia">Georgia</option>
                      <option value="Times New Roman">Times New Roman</option>
                      <option value="Playfair Display">Playfair Display</option>
                      <option value="Roboto">Roboto</option>
                      <option value="Open Sans">Open Sans</option>
                      <option value="Montserrat">Montserrat</option>
                      <option value="Oswald">Oswald</option>
                    </select>
                  </div>
                  <div className="property-group">
                    <label className="property-label">Font Size</label>
                    <input 
                      type="number" 
                      className="full-width-input"
                      value={selectedObject.fontSize || 48}
                      onChange={(e) => {
                        selectedObject.set('fontSize', Number(e.target.value));
                        fabricRef.current?.renderAll();
                      }}
                    />
                  </div>
                  <div className="property-group">
                    <label className="property-label">Font Weight</label>
                    <select 
                      className="full-width-input"
                      value={selectedObject.fontWeight || 'normal'}
                      onChange={(e) => {
                        selectedObject.set('fontWeight', e.target.value);
                        fabricRef.current?.renderAll();
                      }}
                    >
                      <option value="normal">Normal</option>
                      <option value="500">Medium</option>
                      <option value="600">Semibold</option>
                      <option value="bold">Bold</option>
                      <option value="900">Black</option>
                    </select>
                  </div>
                  <div className="property-group">
                    <label className="property-label">Text Align</label>
                    <div className="text-align-buttons">
                      <button 
                        className={`align-btn ${selectedObject.textAlign === 'left' ? 'active' : ''}`}
                        onClick={() => {
                          selectedObject.set('textAlign', 'left');
                          fabricRef.current?.renderAll();
                        }}
                        title="Left"
                      >
                        <svg width="16" height="16" viewBox="0 0 16 16" fill="currentColor">
                          <rect x="2" y="3" width="12" height="2"/>
                          <rect x="2" y="7" width="8" height="2"/>
                          <rect x="2" y="11" width="10" height="2"/>
                        </svg>
                      </button>
                      <button 
                        className={`align-btn ${selectedObject.textAlign === 'center' ? 'active' : ''}`}
                        onClick={() => {
                          selectedObject.set('textAlign', 'center');
                          fabricRef.current?.renderAll();
                        }}
                        title="Center"
                      >
                        <svg width="16" height="16" viewBox="0 0 16 16" fill="currentColor">
                          <rect x="2" y="3" width="12" height="2"/>
                          <rect x="4" y="7" width="8" height="2"/>
                          <rect x="3" y="11" width="10" height="2"/>
                        </svg>
                      </button>
                      <button 
                        className={`align-btn ${selectedObject.textAlign === 'right' ? 'active' : ''}`}
                        onClick={() => {
                          selectedObject.set('textAlign', 'right');
                          fabricRef.current?.renderAll();
                        }}
                        title="Right"
                      >
                        <svg width="16" height="16" viewBox="0 0 16 16" fill="currentColor">
                          <rect x="2" y="3" width="12" height="2"/>
                          <rect x="6" y="7" width="8" height="2"/>
                          <rect x="4" y="11" width="10" height="2"/>
                        </svg>
                      </button>
                    </div>
                  </div>
                  <div className="property-group">
                    <label className="property-label">Line Height</label>
                    <input 
                      type="range" 
                      min="0.8" 
                      max="2.5" 
                      step="0.1"
                      value={selectedObject.lineHeight || 1.2}
                      onChange={(e) => {
                        selectedObject.set('lineHeight', Number(e.target.value));
                        fabricRef.current?.renderAll();
                      }}
                    />
                    <span className="range-value">{selectedObject.lineHeight?.toFixed(1) || '1.2'}</span>
                  </div>
                </>
              )}
              
              {/* Opacity */}
              <div className="property-group">
                <label className="property-label">Opacity</label>
                <input 
                  type="range" 
                  min="0" 
                  max="1" 
                  step="0.1"
                  value={selectedObject.opacity || 1}
                  onChange={(e) => {
                    selectedObject.set('opacity', Number(e.target.value));
                    fabricRef.current?.renderAll();
                  }}
                />
              </div>
            </div>
          </aside>
        )}
      </div>
    </div>
  );
};

export default Editor;
