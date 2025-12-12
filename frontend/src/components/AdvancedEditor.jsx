import React, { useState, useEffect, useRef, useCallback } from 'react';
import { fabric } from 'fabric';

const ML_SERVICE_URL = process.env.REACT_APP_ML_URL || 'http://localhost:8001';
const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000';

/**
 * Advanced Canva-like Design Editor
 * Full-featured editing with layers, properties, and professional tools
 */
const AdvancedEditor = ({ design, onSave, onClose }) => {
  // State
  const [selectedElement, setSelectedElement] = useState(null);
  const [layers, setLayers] = useState([]);
  const [zoom, setZoom] = useState(1);
  const [showGrid, setShowGrid] = useState(false);
  const [history, setHistory] = useState([]);
  const [historyIndex, setHistoryIndex] = useState(-1);
  const [activeTab, setActiveTab] = useState('elements');
  const [isSaving, setIsSaving] = useState(false);
  
  // Refs
  const canvasRef = useRef(null);
  const fabricCanvasRef = useRef(null);
  const containerRef = useRef(null);

  // Available fonts
  const fonts = [
    'Montserrat', 'Inter', 'Playfair Display', 'Roboto', 'Open Sans',
    'Lato', 'Poppins', 'Oswald', 'Raleway', 'Bebas Neue', 'Anton',
    'Arial', 'Georgia', 'Times New Roman', 'Helvetica'
  ];

  // Preset colors
  const presetColors = [
    '#000000', '#ffffff', '#ef4444', '#f97316', '#fbbf24', '#22c55e',
    '#3b82f6', '#8b5cf6', '#ec4899', '#6b7280', '#1e3a8a', '#064e3b'
  ];

  // Initialize canvas
  useEffect(() => {
    if (!canvasRef.current || fabricCanvasRef.current) return;

    const canvas = new fabric.Canvas(canvasRef.current, {
      width: 800,
      height: 800,
      backgroundColor: '#ffffff',
      preserveObjectStacking: true,
      selection: true,
    });

    fabricCanvasRef.current = canvas;

    // Event handlers
    canvas.on('selection:created', handleSelection);
    canvas.on('selection:updated', handleSelection);
    canvas.on('selection:cleared', () => setSelectedElement(null));
    canvas.on('object:modified', saveToHistory);
    canvas.on('object:added', updateLayers);
    canvas.on('object:removed', updateLayers);

    // Load design if provided
    if (design?.canvas_data) {
      loadDesignToCanvas(design.canvas_data);
    }

    return () => {
      canvas.dispose();
      fabricCanvasRef.current = null;
    };
  }, []);

  // Load design into canvas
  const loadDesignToCanvas = useCallback((canvasData) => {
    const canvas = fabricCanvasRef.current;
    if (!canvas) return;

    canvas.clear();

    // Set background
    const bgColor = canvasData.background || canvasData.backgroundColor || '#ffffff';
    canvas.setBackgroundColor(bgColor, canvas.renderAll.bind(canvas));

    // Calculate scale
    const designWidth = canvasData.width || 1080;
    const designHeight = canvasData.height || 1080;
    const scale = Math.min(800 / designWidth, 800 / designHeight);

    // Load objects
    const objects = canvasData.objects || [];
    objects.forEach((objData, index) => {
      let fabricObj = null;

      if (objData.type === 'textbox' || objData.type === 'text') {
        fabricObj = new fabric.Textbox(objData.text || 'Text', {
          left: (objData.left || objData.x || 0) * scale,
          top: (objData.top || objData.y || 0) * scale,
          width: objData.width ? objData.width * scale : 300,
          fontSize: (objData.fontSize || 24) * scale,
          fill: objData.fill || objData.color || '#000000',
          fontFamily: objData.fontFamily || 'Inter',
          fontWeight: objData.fontWeight || 'normal',
          fontStyle: objData.fontStyle || 'normal',
          textAlign: objData.textAlign || 'left',
          lineHeight: objData.lineHeight || 1.2,
          opacity: objData.opacity || 1,
          name: objData.name || `text-${index}`,
        });
      } else if (objData.type === 'rect' || objData.type === 'rectangle') {
        fabricObj = new fabric.Rect({
          left: (objData.left || objData.x || 0) * scale,
          top: (objData.top || objData.y || 0) * scale,
          width: (objData.width || 100) * scale,
          height: (objData.height || 100) * scale,
          fill: objData.fill || objData.color || '#3b82f6',
          rx: (objData.rx || objData.borderRadius || 0) * scale,
          ry: (objData.ry || objData.borderRadius || 0) * scale,
          opacity: objData.opacity || 1,
          name: objData.name || `rect-${index}`,
        });
      } else if (objData.type === 'circle') {
        const radius = ((objData.width || 100) / 2) * scale;
        fabricObj = new fabric.Circle({
          left: (objData.left || objData.x || 0) * scale,
          top: (objData.top || objData.y || 0) * scale,
          radius: radius,
          fill: objData.fill || objData.color || '#22c55e',
          opacity: objData.opacity || 1,
          name: objData.name || `circle-${index}`,
        });
      }

      if (fabricObj) {
        canvas.add(fabricObj);
      }
    });

    canvas.renderAll();
    updateLayers();
    saveToHistory();
  }, []);

  // Handle selection
  const handleSelection = (e) => {
    if (e.selected && e.selected[0]) {
      setSelectedElement(e.selected[0]);
    }
  };

  // Update layers list
  const updateLayers = useCallback(() => {
    const canvas = fabricCanvasRef.current;
    if (!canvas) return;
    
    const objects = canvas.getObjects().map((obj, index) => ({
      id: index,
      name: obj.name || `Layer ${index + 1}`,
      type: obj.type,
      visible: obj.visible !== false,
      locked: obj.lockMovementX && obj.lockMovementY,
    }));
    
    setLayers(objects.reverse()); // Top layers first
  }, []);

  // Save to history
  const saveToHistory = useCallback(() => {
    const canvas = fabricCanvasRef.current;
    if (!canvas) return;

    const json = canvas.toJSON(['name']);
    setHistory(prev => [...prev.slice(0, historyIndex + 1), json]);
    setHistoryIndex(prev => prev + 1);
  }, [historyIndex]);

  // Undo
  const undo = () => {
    if (historyIndex > 0) {
      const canvas = fabricCanvasRef.current;
      canvas.loadFromJSON(history[historyIndex - 1], () => {
        canvas.renderAll();
        updateLayers();
      });
      setHistoryIndex(prev => prev - 1);
    }
  };

  // Redo
  const redo = () => {
    if (historyIndex < history.length - 1) {
      const canvas = fabricCanvasRef.current;
      canvas.loadFromJSON(history[historyIndex + 1], () => {
        canvas.renderAll();
        updateLayers();
      });
      setHistoryIndex(prev => prev + 1);
    }
  };

  // Add text
  const addText = (preset = 'heading') => {
    const canvas = fabricCanvasRef.current;
    const presets = {
      heading: { text: 'Add Heading', fontSize: 48, fontWeight: 'bold' },
      subheading: { text: 'Add Subheading', fontSize: 32, fontWeight: '600' },
      body: { text: 'Add body text here', fontSize: 18, fontWeight: 'normal' },
    };
    
    const config = presets[preset];
    const text = new fabric.Textbox(config.text, {
      left: 100,
      top: 100,
      width: 400,
      fontSize: config.fontSize,
      fontWeight: config.fontWeight,
      fontFamily: 'Inter',
      fill: '#000000',
      name: `text-${Date.now()}`,
    });

    canvas.add(text);
    canvas.setActiveObject(text);
    canvas.renderAll();
    saveToHistory();
  };

  // Add shape
  const addShape = (type) => {
    const canvas = fabricCanvasRef.current;
    let shape;

    switch (type) {
      case 'rectangle':
        shape = new fabric.Rect({
          left: 100,
          top: 100,
          width: 200,
          height: 150,
          fill: '#3b82f6',
          rx: 8,
          ry: 8,
          name: `rect-${Date.now()}`,
        });
        break;
      case 'circle':
        shape = new fabric.Circle({
          left: 100,
          top: 100,
          radius: 75,
          fill: '#22c55e',
          name: `circle-${Date.now()}`,
        });
        break;
      case 'line':
        shape = new fabric.Line([50, 50, 250, 50], {
          stroke: '#000000',
          strokeWidth: 3,
          name: `line-${Date.now()}`,
        });
        break;
      case 'button':
        // Create a button group
        const rect = new fabric.Rect({
          width: 200,
          height: 50,
          fill: '#3b82f6',
          rx: 8,
          ry: 8,
        });
        const btnText = new fabric.Text('Click Here', {
          fontSize: 18,
          fontFamily: 'Inter',
          fontWeight: '600',
          fill: '#ffffff',
          originX: 'center',
          originY: 'center',
          left: 100,
          top: 25,
        });
        shape = new fabric.Group([rect, btnText], {
          left: 100,
          top: 100,
          name: `button-${Date.now()}`,
        });
        break;
      default:
        return;
    }

    canvas.add(shape);
    canvas.setActiveObject(shape);
    canvas.renderAll();
    saveToHistory();
  };

  // Delete selected
  const deleteSelected = () => {
    const canvas = fabricCanvasRef.current;
    const active = canvas.getActiveObject();
    if (active) {
      canvas.remove(active);
      setSelectedElement(null);
      saveToHistory();
    }
  };

  // Duplicate selected
  const duplicateSelected = () => {
    const canvas = fabricCanvasRef.current;
    const active = canvas.getActiveObject();
    if (active) {
      active.clone((cloned) => {
        cloned.set({
          left: active.left + 20,
          top: active.top + 20,
          name: `${active.name}-copy`,
        });
        canvas.add(cloned);
        canvas.setActiveObject(cloned);
        canvas.renderAll();
        saveToHistory();
      });
    }
  };

  // Update element property
  const updateProperty = (property, value) => {
    if (!selectedElement) return;
    selectedElement.set(property, value);
    fabricCanvasRef.current.renderAll();
    saveToHistory();
  };

  // Change background color
  const changeBackground = (color) => {
    const canvas = fabricCanvasRef.current;
    canvas.setBackgroundColor(color, canvas.renderAll.bind(canvas));
    saveToHistory();
  };

  // Bring to front/back
  const bringToFront = () => {
    const canvas = fabricCanvasRef.current;
    const active = canvas.getActiveObject();
    if (active) {
      canvas.bringToFront(active);
      updateLayers();
    }
  };

  const sendToBack = () => {
    const canvas = fabricCanvasRef.current;
    const active = canvas.getActiveObject();
    if (active) {
      canvas.sendToBack(active);
      updateLayers();
    }
  };

  // Export
  const exportDesign = (format) => {
    const canvas = fabricCanvasRef.current;
    let dataURL;

    switch (format) {
      case 'png':
        dataURL = canvas.toDataURL({ format: 'png', multiplier: 2 });
        break;
      case 'jpg':
        dataURL = canvas.toDataURL({ format: 'jpeg', quality: 0.9, multiplier: 2 });
        break;
      case 'svg':
        const svg = canvas.toSVG();
        const blob = new Blob([svg], { type: 'image/svg+xml' });
        dataURL = URL.createObjectURL(blob);
        break;
      default:
        return;
    }

    const link = document.createElement('a');
    link.download = `design-${Date.now()}.${format}`;
    link.href = dataURL;
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
  };

  // Save design
  const handleSave = async () => {
    setIsSaving(true);
    try {
      const canvas = fabricCanvasRef.current;
      const canvasData = canvas.toJSON(['name']);
      canvasData.width = design?.canvas_data?.width || 1080;
      canvasData.height = design?.canvas_data?.height || 1080;
      
      if (onSave) {
        await onSave({
          ...design,
          canvas_data: canvasData,
        });
      }
    } catch (error) {
      console.error('Save failed:', error);
    } finally {
      setIsSaving(false);
    }
  };

  // Keyboard shortcuts
  useEffect(() => {
    const handleKeyDown = (e) => {
      if ((e.metaKey || e.ctrlKey) && e.key === 'z' && !e.shiftKey) {
        e.preventDefault();
        undo();
      }
      if ((e.metaKey || e.ctrlKey) && e.key === 'z' && e.shiftKey) {
        e.preventDefault();
        redo();
      }
      if ((e.metaKey || e.ctrlKey) && e.key === 's') {
        e.preventDefault();
        handleSave();
      }
      if ((e.key === 'Delete' || e.key === 'Backspace') && selectedElement) {
        // Only delete if not editing text
        if (document.activeElement.tagName !== 'INPUT' && document.activeElement.tagName !== 'TEXTAREA') {
          e.preventDefault();
          deleteSelected();
        }
      }
      if ((e.metaKey || e.ctrlKey) && e.key === 'd') {
        e.preventDefault();
        duplicateSelected();
      }
    };

    window.addEventListener('keydown', handleKeyDown);
    return () => window.removeEventListener('keydown', handleKeyDown);
  }, [selectedElement, historyIndex]);

  return (
    <div className="fixed inset-0 bg-gray-900 flex flex-col z-50">
      {/* Top Toolbar */}
      <div className="bg-gray-800 border-b border-gray-700 px-4 py-2 flex items-center justify-between">
        <div className="flex items-center space-x-4">
          <button
            onClick={onClose}
            className="text-gray-300 hover:text-white px-3 py-1.5 rounded hover:bg-gray-700"
          >
            ← Back
          </button>
          <div className="h-6 w-px bg-gray-600" />
          <h1 className="text-white font-medium">
            {design?.prompt || 'Design Editor'}
          </h1>
        </div>

        <div className="flex items-center space-x-2">
          {/* History */}
          <button
            onClick={undo}
            disabled={historyIndex <= 0}
            className="p-2 text-gray-300 hover:text-white hover:bg-gray-700 rounded disabled:opacity-40"
            title="Undo (Ctrl+Z)"
          >
            <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M3 10h10a8 8 0 018 8v2M3 10l6 6m-6-6l6-6" />
            </svg>
          </button>
          <button
            onClick={redo}
            disabled={historyIndex >= history.length - 1}
            className="p-2 text-gray-300 hover:text-white hover:bg-gray-700 rounded disabled:opacity-40"
            title="Redo (Ctrl+Shift+Z)"
          >
            <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M21 10h-10a8 8 0 00-8 8v2M21 10l-6 6m6-6l-6-6" />
            </svg>
          </button>

          <div className="h-6 w-px bg-gray-600 mx-2" />

          {/* Zoom */}
          <select
            value={zoom}
            onChange={(e) => setZoom(parseFloat(e.target.value))}
            className="bg-gray-700 text-white text-sm px-2 py-1.5 rounded border-0"
          >
            <option value={0.5}>50%</option>
            <option value={0.75}>75%</option>
            <option value={1}>100%</option>
            <option value={1.25}>125%</option>
            <option value={1.5}>150%</option>
          </select>

          <div className="h-6 w-px bg-gray-600 mx-2" />

          {/* Export */}
          <div className="relative group">
            <button className="px-3 py-1.5 text-gray-300 hover:text-white hover:bg-gray-700 rounded flex items-center space-x-1">
              <span>Export</span>
              <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 9l-7 7-7-7" />
              </svg>
            </button>
            <div className="absolute right-0 top-full mt-1 bg-gray-800 rounded shadow-xl opacity-0 invisible group-hover:opacity-100 group-hover:visible transition-all z-50 min-w-[120px]">
              <button onClick={() => exportDesign('png')} className="block w-full px-4 py-2 text-left text-gray-300 hover:bg-gray-700 hover:text-white">PNG</button>
              <button onClick={() => exportDesign('jpg')} className="block w-full px-4 py-2 text-left text-gray-300 hover:bg-gray-700 hover:text-white">JPG</button>
              <button onClick={() => exportDesign('svg')} className="block w-full px-4 py-2 text-left text-gray-300 hover:bg-gray-700 hover:text-white">SVG</button>
            </div>
          </div>

          {/* Save */}
          <button
            onClick={handleSave}
            disabled={isSaving}
            className="px-4 py-1.5 bg-blue-600 text-white rounded hover:bg-blue-700 disabled:opacity-50 flex items-center space-x-2"
          >
            {isSaving ? (
              <>
                <svg className="animate-spin h-4 w-4" viewBox="0 0 24 24">
                  <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4" fill="none" />
                  <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4z" />
                </svg>
                <span>Saving...</span>
              </>
            ) : (
              <span>Save</span>
            )}
          </button>
        </div>
      </div>

      {/* Main Content */}
      <div className="flex-1 flex overflow-hidden">
        {/* Left Sidebar - Elements */}
        <div className="w-72 bg-gray-800 border-r border-gray-700 flex flex-col">
          {/* Tabs */}
          <div className="flex border-b border-gray-700">
            {['elements', 'text', 'shapes', 'layers'].map((tab) => (
              <button
                key={tab}
                onClick={() => setActiveTab(tab)}
                className={`flex-1 px-3 py-3 text-sm capitalize ${
                  activeTab === tab
                    ? 'text-white border-b-2 border-blue-500 bg-gray-700/50'
                    : 'text-gray-400 hover:text-white'
                }`}
              >
                {tab}
              </button>
            ))}
          </div>

          {/* Tab Content */}
          <div className="flex-1 overflow-y-auto p-4">
            {activeTab === 'elements' && (
              <div className="space-y-4">
                <div>
                  <h3 className="text-xs font-semibold text-gray-400 uppercase mb-2">Quick Add</h3>
                  <div className="grid grid-cols-2 gap-2">
                    <button
                      onClick={() => addText('heading')}
                      className="p-3 bg-gray-700 hover:bg-gray-600 rounded-lg text-left"
                    >
                      <span className="text-lg font-bold text-white block">Aa</span>
                      <span className="text-xs text-gray-400">Heading</span>
                    </button>
                    <button
                      onClick={() => addShape('button')}
                      className="p-3 bg-gray-700 hover:bg-gray-600 rounded-lg text-left"
                    >
                      <span className="text-sm bg-blue-600 text-white px-2 py-1 rounded inline-block">Button</span>
                      <span className="text-xs text-gray-400 block mt-1">CTA</span>
                    </button>
                    <button
                      onClick={() => addShape('rectangle')}
                      className="p-3 bg-gray-700 hover:bg-gray-600 rounded-lg text-left"
                    >
                      <div className="w-8 h-6 bg-blue-500 rounded"></div>
                      <span className="text-xs text-gray-400 block mt-1">Rectangle</span>
                    </button>
                    <button
                      onClick={() => addShape('circle')}
                      className="p-3 bg-gray-700 hover:bg-gray-600 rounded-lg text-left"
                    >
                      <div className="w-6 h-6 bg-green-500 rounded-full"></div>
                      <span className="text-xs text-gray-400 block mt-1">Circle</span>
                    </button>
                  </div>
                </div>

                <div>
                  <h3 className="text-xs font-semibold text-gray-400 uppercase mb-2">Background</h3>
                  <div className="flex flex-wrap gap-2">
                    {presetColors.map((color) => (
                      <button
                        key={color}
                        onClick={() => changeBackground(color)}
                        className="w-8 h-8 rounded border-2 border-gray-600 hover:border-white transition-colors"
                        style={{ backgroundColor: color }}
                      />
                    ))}
                    <input
                      type="color"
                      onChange={(e) => changeBackground(e.target.value)}
                      className="w-8 h-8 rounded cursor-pointer"
                    />
                  </div>
                </div>
              </div>
            )}

            {activeTab === 'text' && (
              <div className="space-y-3">
                <button
                  onClick={() => addText('heading')}
                  className="w-full p-4 bg-gray-700 hover:bg-gray-600 rounded-lg text-left"
                >
                  <span className="text-2xl font-bold text-white">Add a heading</span>
                </button>
                <button
                  onClick={() => addText('subheading')}
                  className="w-full p-3 bg-gray-700 hover:bg-gray-600 rounded-lg text-left"
                >
                  <span className="text-lg font-semibold text-white">Add a subheading</span>
                </button>
                <button
                  onClick={() => addText('body')}
                  className="w-full p-3 bg-gray-700 hover:bg-gray-600 rounded-lg text-left"
                >
                  <span className="text-sm text-gray-300">Add body text</span>
                </button>
              </div>
            )}

            {activeTab === 'shapes' && (
              <div className="grid grid-cols-3 gap-3">
                <button
                  onClick={() => addShape('rectangle')}
                  className="aspect-square bg-gray-700 hover:bg-gray-600 rounded-lg flex items-center justify-center"
                >
                  <div className="w-10 h-8 bg-blue-500 rounded" />
                </button>
                <button
                  onClick={() => addShape('circle')}
                  className="aspect-square bg-gray-700 hover:bg-gray-600 rounded-lg flex items-center justify-center"
                >
                  <div className="w-10 h-10 bg-green-500 rounded-full" />
                </button>
                <button
                  onClick={() => addShape('line')}
                  className="aspect-square bg-gray-700 hover:bg-gray-600 rounded-lg flex items-center justify-center"
                >
                  <div className="w-10 h-1 bg-white rounded" />
                </button>
              </div>
            )}

            {activeTab === 'layers' && (
              <div className="space-y-1">
                {layers.map((layer, index) => (
                  <div
                    key={layer.id}
                    onClick={() => {
                      const canvas = fabricCanvasRef.current;
                      const obj = canvas.item(layers.length - 1 - index);
                      if (obj) canvas.setActiveObject(obj);
                      canvas.renderAll();
                    }}
                    className={`p-2 rounded cursor-pointer flex items-center space-x-2 ${
                      selectedElement?.name === layer.name ? 'bg-blue-600' : 'hover:bg-gray-700'
                    }`}
                  >
                    <span className="text-xs text-gray-400 w-4">{index + 1}</span>
                    <span className="text-sm text-white truncate flex-1">{layer.name}</span>
                    <span className="text-xs text-gray-500">{layer.type}</span>
                  </div>
                ))}
                {layers.length === 0 && (
                  <p className="text-gray-500 text-sm text-center py-4">No layers yet</p>
                )}
              </div>
            )}
          </div>
        </div>

        {/* Canvas Area */}
        <div 
          ref={containerRef}
          className="flex-1 bg-gray-900 flex items-center justify-center overflow-auto p-8"
        >
          <div 
            className="bg-white shadow-2xl"
            style={{ transform: `scale(${zoom})`, transformOrigin: 'center' }}
          >
            <canvas ref={canvasRef} />
          </div>
        </div>

        {/* Right Sidebar - Properties */}
        <div className="w-72 bg-gray-800 border-l border-gray-700 overflow-y-auto">
          {selectedElement ? (
            <div className="p-4 space-y-4">
              <div className="flex items-center justify-between">
                <h3 className="text-white font-medium">Properties</h3>
                <div className="flex space-x-1">
                  <button
                    onClick={bringToFront}
                    className="p-1.5 text-gray-400 hover:text-white hover:bg-gray-700 rounded"
                    title="Bring to Front"
                  >
                    <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M5 15l7-7 7 7" />
                    </svg>
                  </button>
                  <button
                    onClick={sendToBack}
                    className="p-1.5 text-gray-400 hover:text-white hover:bg-gray-700 rounded"
                    title="Send to Back"
                  >
                    <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 9l-7 7-7-7" />
                    </svg>
                  </button>
                  <button
                    onClick={duplicateSelected}
                    className="p-1.5 text-gray-400 hover:text-white hover:bg-gray-700 rounded"
                    title="Duplicate (Ctrl+D)"
                  >
                    <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M8 16H6a2 2 0 01-2-2V6a2 2 0 012-2h8a2 2 0 012 2v2m-6 12h8a2 2 0 002-2v-8a2 2 0 00-2-2h-8a2 2 0 00-2 2v8a2 2 0 002 2z" />
                    </svg>
                  </button>
                  <button
                    onClick={deleteSelected}
                    className="p-1.5 text-gray-400 hover:text-red-500 hover:bg-gray-700 rounded"
                    title="Delete"
                  >
                    <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16" />
                    </svg>
                  </button>
                </div>
              </div>

              {/* Position & Size */}
              <div className="space-y-2">
                <h4 className="text-xs text-gray-400 uppercase">Position</h4>
                <div className="grid grid-cols-2 gap-2">
                  <div>
                    <label className="text-xs text-gray-500">X</label>
                    <input
                      type="number"
                      value={Math.round(selectedElement.left || 0)}
                      onChange={(e) => updateProperty('left', parseFloat(e.target.value))}
                      className="w-full bg-gray-700 text-white text-sm px-2 py-1.5 rounded"
                    />
                  </div>
                  <div>
                    <label className="text-xs text-gray-500">Y</label>
                    <input
                      type="number"
                      value={Math.round(selectedElement.top || 0)}
                      onChange={(e) => updateProperty('top', parseFloat(e.target.value))}
                      className="w-full bg-gray-700 text-white text-sm px-2 py-1.5 rounded"
                    />
                  </div>
                </div>
              </div>

              {/* Text Properties */}
              {(selectedElement.type === 'textbox' || selectedElement.type === 'i-text') && (
                <>
                  <div className="space-y-2">
                    <h4 className="text-xs text-gray-400 uppercase">Font</h4>
                    <select
                      value={selectedElement.fontFamily || 'Inter'}
                      onChange={(e) => updateProperty('fontFamily', e.target.value)}
                      className="w-full bg-gray-700 text-white text-sm px-2 py-1.5 rounded"
                    >
                      {fonts.map((font) => (
                        <option key={font} value={font}>{font}</option>
                      ))}
                    </select>
                    <div className="flex space-x-2">
                      <input
                        type="number"
                        value={selectedElement.fontSize || 24}
                        onChange={(e) => updateProperty('fontSize', parseFloat(e.target.value))}
                        className="w-20 bg-gray-700 text-white text-sm px-2 py-1.5 rounded"
                        min="8"
                        max="200"
                      />
                      <div className="flex bg-gray-700 rounded overflow-hidden">
                        <button
                          onClick={() => updateProperty('fontWeight', selectedElement.fontWeight === 'bold' ? 'normal' : 'bold')}
                          className={`px-3 py-1.5 text-sm ${selectedElement.fontWeight === 'bold' ? 'bg-blue-600 text-white' : 'text-gray-300'}`}
                        >
                          B
                        </button>
                        <button
                          onClick={() => updateProperty('fontStyle', selectedElement.fontStyle === 'italic' ? 'normal' : 'italic')}
                          className={`px-3 py-1.5 text-sm italic ${selectedElement.fontStyle === 'italic' ? 'bg-blue-600 text-white' : 'text-gray-300'}`}
                        >
                          I
                        </button>
                      </div>
                    </div>
                  </div>

                  <div className="space-y-2">
                    <h4 className="text-xs text-gray-400 uppercase">Alignment</h4>
                    <div className="flex bg-gray-700 rounded overflow-hidden">
                      {['left', 'center', 'right'].map((align) => (
                        <button
                          key={align}
                          onClick={() => updateProperty('textAlign', align)}
                          className={`flex-1 py-1.5 text-sm ${selectedElement.textAlign === align ? 'bg-blue-600 text-white' : 'text-gray-300'}`}
                        >
                          {align === 'left' && '⫷'}
                          {align === 'center' && '☰'}
                          {align === 'right' && '⫸'}
                        </button>
                      ))}
                    </div>
                  </div>
                </>
              )}

              {/* Color */}
              <div className="space-y-2">
                <h4 className="text-xs text-gray-400 uppercase">Color</h4>
                <div className="flex items-center space-x-2">
                  <input
                    type="color"
                    value={selectedElement.fill || '#000000'}
                    onChange={(e) => updateProperty('fill', e.target.value)}
                    className="w-10 h-10 rounded cursor-pointer"
                  />
                  <input
                    type="text"
                    value={selectedElement.fill || '#000000'}
                    onChange={(e) => updateProperty('fill', e.target.value)}
                    className="flex-1 bg-gray-700 text-white text-sm px-2 py-1.5 rounded"
                  />
                </div>
                <div className="flex flex-wrap gap-1">
                  {presetColors.map((color) => (
                    <button
                      key={color}
                      onClick={() => updateProperty('fill', color)}
                      className="w-6 h-6 rounded border border-gray-600 hover:border-white"
                      style={{ backgroundColor: color }}
                    />
                  ))}
                </div>
              </div>

              {/* Opacity */}
              <div className="space-y-2">
                <h4 className="text-xs text-gray-400 uppercase">
                  Opacity: {Math.round((selectedElement.opacity || 1) * 100)}%
                </h4>
                <input
                  type="range"
                  min="0"
                  max="1"
                  step="0.01"
                  value={selectedElement.opacity || 1}
                  onChange={(e) => updateProperty('opacity', parseFloat(e.target.value))}
                  className="w-full"
                />
              </div>

              {/* Rotation */}
              <div className="space-y-2">
                <h4 className="text-xs text-gray-400 uppercase">
                  Rotation: {Math.round(selectedElement.angle || 0)}°
                </h4>
                <input
                  type="range"
                  min="0"
                  max="360"
                  value={selectedElement.angle || 0}
                  onChange={(e) => updateProperty('angle', parseFloat(e.target.value))}
                  className="w-full"
                />
              </div>
            </div>
          ) : (
            <div className="p-4 text-center">
              <div className="text-gray-500 py-8">
                <svg className="w-12 h-12 mx-auto mb-3 opacity-50" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={1.5} d="M15 15l-2 5L9 9l11 4-5 2zm0 0l5 5M7.188 2.239l.777 2.897M5.136 7.965l-2.898-.777M13.95 4.05l-2.122 2.122m-5.657 5.656l-2.12 2.122" />
                </svg>
                <p className="text-sm">Select an element to edit its properties</p>
              </div>
            </div>
          )}
        </div>
      </div>
    </div>
  );
};

export default AdvancedEditor;
