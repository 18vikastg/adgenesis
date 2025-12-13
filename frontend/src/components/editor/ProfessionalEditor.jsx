/**
 * AdGenesis - Professional Canvas Editor
 * Canva/Figma-level editor with layers, alignment guides, snapping
 */

import React, { useRef, useEffect, useState, useCallback } from 'react';
import { fabric } from 'fabric';
import EditorToolbar from './EditorToolbar';
import LayersPanel from './LayersPanel';
import PropertiesPanel from './PropertiesPanel';
import AIAssistant from './AIAssistant';
import './ProfessionalEditor.css';

// Alignment Guide Line Class
const AlignmentGuideLine = fabric.util.createClass(fabric.Line, {
  type: 'alignmentGuideLine',
  evented: false,
  selectable: false,
  strokeDashArray: [5, 5],
});

const ProfessionalEditor = ({
  initialDesign = null,
  canvasWidth = 1080,
  canvasHeight = 1080,
  onSave,
  onExport,
}) => {
  const canvasRef = useRef(null);
  const fabricCanvasRef = useRef(null);
  const containerRef = useRef(null);
  
  // State
  const [canvas, setCanvas] = useState(null);
  const [selectedObject, setSelectedObject] = useState(null);
  const [layers, setLayers] = useState([]);
  const [zoom, setZoom] = useState(1);
  const [history, setHistory] = useState([]);
  const [historyIndex, setHistoryIndex] = useState(-1);
  const [isPanning, setIsPanning] = useState(false);
  const [showGrid, setShowGrid] = useState(false);
  const [snapToGrid, setSnapToGrid] = useState(true);
  const [showAIAssistant, setShowAIAssistant] = useState(false);
  const [activeTool, setActiveTool] = useState('select');
  const [clipboard, setClipboard] = useState(null);
  
  const GRID_SIZE = 10;
  const SNAP_THRESHOLD = 8;

  // Initialize canvas
  useEffect(() => {
    if (!canvasRef.current) return;

    const fabricCanvas = new fabric.Canvas(canvasRef.current, {
      width: canvasWidth,
      height: canvasHeight,
      backgroundColor: '#ffffff',
      preserveObjectStacking: true,
      selection: true,
      selectionColor: 'rgba(139, 92, 246, 0.15)',
      selectionBorderColor: '#8b5cf6',
      selectionLineWidth: 1,
      hoverCursor: 'pointer',
      moveCursor: 'move',
    });

    // Custom controls styling
    fabric.Object.prototype.set({
      transparentCorners: false,
      cornerColor: '#8b5cf6',
      cornerStrokeColor: '#ffffff',
      cornerSize: 10,
      cornerStyle: 'circle',
      borderColor: '#8b5cf6',
      borderScaleFactor: 1.5,
      padding: 8,
    });

    fabricCanvasRef.current = fabricCanvas;
    setCanvas(fabricCanvas);

    // Load initial design if provided
    if (initialDesign) {
      loadDesign(fabricCanvas, initialDesign);
    }

    return () => {
      fabricCanvas.dispose();
    };
  }, []);

  // Canvas event handlers
  useEffect(() => {
    if (!canvas) return;

    const handleSelection = (e) => {
      setSelectedObject(e.selected?.[0] || null);
    };

    const handleSelectionCleared = () => {
      setSelectedObject(null);
    };

    const handleObjectModified = () => {
      updateLayers();
      saveToHistory();
    };

    const handleObjectAdded = () => {
      updateLayers();
      saveToHistory();
    };

    const handleObjectRemoved = () => {
      updateLayers();
      saveToHistory();
    };

    // Snapping and alignment guides
    const handleObjectMoving = (e) => {
      if (!snapToGrid) return;
      
      const obj = e.target;
      const canvasWidth = canvas.width;
      const canvasHeight = canvas.height;
      
      // Snap to grid
      obj.set({
        left: Math.round(obj.left / GRID_SIZE) * GRID_SIZE,
        top: Math.round(obj.top / GRID_SIZE) * GRID_SIZE,
      });

      // Center alignment guides
      const objCenter = obj.getCenterPoint();
      const canvasCenterX = canvasWidth / 2;
      const canvasCenterY = canvasHeight / 2;

      // Check horizontal center alignment
      if (Math.abs(objCenter.x - canvasCenterX) < SNAP_THRESHOLD) {
        obj.set({ left: canvasCenterX - obj.width * obj.scaleX / 2 });
        showAlignmentGuide('vertical', canvasCenterX);
      }

      // Check vertical center alignment
      if (Math.abs(objCenter.y - canvasCenterY) < SNAP_THRESHOLD) {
        obj.set({ top: canvasCenterY - obj.height * obj.scaleY / 2 });
        showAlignmentGuide('horizontal', canvasCenterY);
      }

      // Check alignment with other objects
      canvas.getObjects().forEach((other) => {
        if (other === obj || other.type === 'alignmentGuideLine') return;

        const otherCenter = other.getCenterPoint();

        // Horizontal alignment
        if (Math.abs(objCenter.y - otherCenter.y) < SNAP_THRESHOLD) {
          obj.set({ top: otherCenter.y - obj.height * obj.scaleY / 2 });
          showAlignmentGuide('horizontal', otherCenter.y);
        }

        // Vertical alignment
        if (Math.abs(objCenter.x - otherCenter.x) < SNAP_THRESHOLD) {
          obj.set({ left: otherCenter.x - obj.width * obj.scaleX / 2 });
          showAlignmentGuide('vertical', otherCenter.x);
        }
      });
    };

    const handleObjectMoved = () => {
      clearAlignmentGuides();
    };

    canvas.on('selection:created', handleSelection);
    canvas.on('selection:updated', handleSelection);
    canvas.on('selection:cleared', handleSelectionCleared);
    canvas.on('object:modified', handleObjectModified);
    canvas.on('object:added', handleObjectAdded);
    canvas.on('object:removed', handleObjectRemoved);
    canvas.on('object:moving', handleObjectMoving);
    canvas.on('object:moved', handleObjectMoved);

    return () => {
      canvas.off('selection:created', handleSelection);
      canvas.off('selection:updated', handleSelection);
      canvas.off('selection:cleared', handleSelectionCleared);
      canvas.off('object:modified', handleObjectModified);
      canvas.off('object:added', handleObjectAdded);
      canvas.off('object:removed', handleObjectRemoved);
      canvas.off('object:moving', handleObjectMoving);
      canvas.off('object:moved', handleObjectMoved);
    };
  }, [canvas, snapToGrid]);

  // Keyboard shortcuts
  useEffect(() => {
    const handleKeyDown = (e) => {
      if (!canvas) return;
      
      const isCtrl = e.ctrlKey || e.metaKey;
      
      // Delete
      if (e.key === 'Delete' || e.key === 'Backspace') {
        if (selectedObject && !e.target.tagName.match(/INPUT|TEXTAREA/)) {
          deleteSelected();
          e.preventDefault();
        }
      }
      
      // Undo (Ctrl+Z)
      if (isCtrl && e.key === 'z' && !e.shiftKey) {
        undo();
        e.preventDefault();
      }
      
      // Redo (Ctrl+Shift+Z)
      if (isCtrl && e.key === 'z' && e.shiftKey) {
        redo();
        e.preventDefault();
      }
      
      // Copy (Ctrl+C)
      if (isCtrl && e.key === 'c') {
        copy();
        e.preventDefault();
      }
      
      // Paste (Ctrl+V)
      if (isCtrl && e.key === 'v') {
        paste();
        e.preventDefault();
      }
      
      // Duplicate (Ctrl+D)
      if (isCtrl && e.key === 'd') {
        duplicate();
        e.preventDefault();
      }
      
      // Save (Ctrl+S)
      if (isCtrl && e.key === 's') {
        handleSave();
        e.preventDefault();
      }
      
      // Select All (Ctrl+A)
      if (isCtrl && e.key === 'a' && !e.target.tagName.match(/INPUT|TEXTAREA/)) {
        selectAll();
        e.preventDefault();
      }

      // Arrow keys for nudging
      if (['ArrowUp', 'ArrowDown', 'ArrowLeft', 'ArrowRight'].includes(e.key) && selectedObject) {
        const nudge = e.shiftKey ? 10 : 1;
        const direction = {
          ArrowUp: { top: -nudge },
          ArrowDown: { top: nudge },
          ArrowLeft: { left: -nudge },
          ArrowRight: { left: nudge },
        }[e.key];
        
        selectedObject.set(direction);
        canvas.requestRenderAll();
        e.preventDefault();
      }
    };

    window.addEventListener('keydown', handleKeyDown);
    return () => window.removeEventListener('keydown', handleKeyDown);
  }, [canvas, selectedObject, history, historyIndex, clipboard]);

  // Helper functions
  const showAlignmentGuide = (orientation, position) => {
    clearAlignmentGuides();
    
    const line = orientation === 'horizontal'
      ? new AlignmentGuideLine([0, position, canvas.width, position], {
          stroke: '#8b5cf6',
          strokeWidth: 1,
        })
      : new AlignmentGuideLine([position, 0, position, canvas.height], {
          stroke: '#8b5cf6',
          strokeWidth: 1,
        });
    
    canvas.add(line);
    canvas.requestRenderAll();
  };

  const clearAlignmentGuides = () => {
    const guides = canvas?.getObjects('alignmentGuideLine') || [];
    guides.forEach((guide) => canvas.remove(guide));
    canvas?.requestRenderAll();
  };

  const updateLayers = useCallback(() => {
    if (!canvas) return;
    
    const objects = canvas.getObjects().filter(obj => obj.type !== 'alignmentGuideLine');
    const layerData = objects.map((obj, index) => ({
      id: obj.id || `layer_${index}`,
      name: obj.name || getObjectName(obj),
      type: obj.type,
      visible: obj.visible !== false,
      locked: obj.selectable === false,
      object: obj,
    }));
    
    setLayers(layerData.reverse());
  }, [canvas]);

  const getObjectName = (obj) => {
    switch (obj.type) {
      case 'textbox':
      case 'i-text':
        return obj.text?.substring(0, 20) || 'Text';
      case 'rect':
        return 'Rectangle';
      case 'circle':
        return 'Circle';
      case 'triangle':
        return 'Triangle';
      case 'image':
        return 'Image';
      case 'path':
        return 'Shape';
      case 'group':
        return 'Group';
      default:
        return 'Element';
    }
  };

  const saveToHistory = useCallback(() => {
    if (!canvas) return;
    
    const json = canvas.toJSON(['id', 'name']);
    const newHistory = history.slice(0, historyIndex + 1);
    newHistory.push(json);
    
    if (newHistory.length > 50) {
      newHistory.shift();
    }
    
    setHistory(newHistory);
    setHistoryIndex(newHistory.length - 1);
  }, [canvas, history, historyIndex]);

  const loadDesign = (targetCanvas, design) => {
    if (!design?.elements) return;
    
    design.elements.forEach((el) => {
      let fabricObj;
      
      switch (el.type) {
        case 'textbox':
        case 'text':
          fabricObj = new fabric.Textbox(el.text || 'Text', {
            left: el.x || 0,
            top: el.y || 0,
            width: el.width || 200,
            fontSize: el.fontSize || 24,
            fontFamily: el.fontFamily || 'Inter',
            fontWeight: el.fontWeight || 'normal',
            fontStyle: el.fontStyle || 'normal',
            fill: el.color || '#000000',
            textAlign: el.textAlign || 'left',
            lineHeight: el.lineHeight || 1.4,
            letterSpacing: el.letterSpacing || 0,
            opacity: el.opacity || 1,
          });
          break;
          
        case 'rect':
          fabricObj = new fabric.Rect({
            left: el.x || 0,
            top: el.y || 0,
            width: el.width || 100,
            height: el.height || 100,
            fill: el.color || '#3b82f6',
            rx: el.borderRadius || 0,
            ry: el.borderRadius || 0,
            opacity: el.opacity || 1,
          });
          break;
          
        case 'circle':
          fabricObj = new fabric.Circle({
            left: el.x || 0,
            top: el.y || 0,
            radius: (el.width || 100) / 2,
            fill: el.color || '#8b5cf6',
            opacity: el.opacity || 1,
          });
          break;
          
        case 'triangle':
          fabricObj = new fabric.Triangle({
            left: el.x || 0,
            top: el.y || 0,
            width: el.width || 100,
            height: el.height || 100,
            fill: el.color || '#10b981',
            opacity: el.opacity || 1,
          });
          break;
          
        default:
          return;
      }
      
      if (fabricObj) {
        fabricObj.id = el.id || `el_${Date.now()}_${Math.random().toString(36).substr(2, 9)}`;
        fabricObj.name = el.name || getObjectName(fabricObj);
        targetCanvas.add(fabricObj);
      }
    });

    // Set background
    if (design.background_gradient) {
      // Parse gradient and apply
      targetCanvas.setBackgroundColor(design.background_color || '#ffffff', targetCanvas.renderAll.bind(targetCanvas));
    } else if (design.background_color) {
      targetCanvas.setBackgroundColor(design.background_color, targetCanvas.renderAll.bind(targetCanvas));
    }

    targetCanvas.renderAll();
    updateLayers();
  };

  // Actions
  const undo = useCallback(() => {
    if (historyIndex <= 0 || !canvas) return;
    
    const newIndex = historyIndex - 1;
    canvas.loadFromJSON(history[newIndex], () => {
      canvas.renderAll();
      updateLayers();
      setHistoryIndex(newIndex);
    });
  }, [canvas, history, historyIndex, updateLayers]);

  const redo = useCallback(() => {
    if (historyIndex >= history.length - 1 || !canvas) return;
    
    const newIndex = historyIndex + 1;
    canvas.loadFromJSON(history[newIndex], () => {
      canvas.renderAll();
      updateLayers();
      setHistoryIndex(newIndex);
    });
  }, [canvas, history, historyIndex, updateLayers]);

  const copy = useCallback(() => {
    if (!selectedObject) return;
    selectedObject.clone((cloned) => {
      setClipboard(cloned);
    });
  }, [selectedObject]);

  const paste = useCallback(() => {
    if (!clipboard || !canvas) return;
    
    clipboard.clone((cloned) => {
      cloned.set({
        left: cloned.left + 20,
        top: cloned.top + 20,
        id: `el_${Date.now()}`,
      });
      canvas.add(cloned);
      canvas.setActiveObject(cloned);
      canvas.requestRenderAll();
    });
  }, [canvas, clipboard]);

  const duplicate = useCallback(() => {
    if (!selectedObject || !canvas) return;
    
    selectedObject.clone((cloned) => {
      cloned.set({
        left: selectedObject.left + 20,
        top: selectedObject.top + 20,
        id: `el_${Date.now()}`,
      });
      canvas.add(cloned);
      canvas.setActiveObject(cloned);
      canvas.requestRenderAll();
    });
  }, [canvas, selectedObject]);

  const deleteSelected = useCallback(() => {
    if (!selectedObject || !canvas) return;
    canvas.remove(selectedObject);
    canvas.requestRenderAll();
    setSelectedObject(null);
  }, [canvas, selectedObject]);

  const selectAll = useCallback(() => {
    if (!canvas) return;
    canvas.discardActiveObject();
    const selection = new fabric.ActiveSelection(
      canvas.getObjects().filter(obj => obj.type !== 'alignmentGuideLine'),
      { canvas }
    );
    canvas.setActiveObject(selection);
    canvas.requestRenderAll();
  }, [canvas]);

  const handleSave = useCallback(() => {
    if (!canvas || !onSave) return;
    
    const json = canvas.toJSON(['id', 'name']);
    onSave(json);
  }, [canvas, onSave]);

  const handleExport = useCallback((format = 'png', quality = 1) => {
    if (!canvas) return;
    
    const dataUrl = canvas.toDataURL({
      format,
      quality,
      multiplier: 2, // 2x for retina
    });
    
    if (onExport) {
      onExport(dataUrl, format);
    } else {
      // Default download behavior
      const link = document.createElement('a');
      link.download = `design.${format}`;
      link.href = dataUrl;
      link.click();
    }
  }, [canvas, onExport]);

  // Add elements
  const addText = useCallback((preset = 'heading') => {
    if (!canvas) return;
    
    const presets = {
      heading: { text: 'Heading', fontSize: 64, fontWeight: 'bold' },
      subheading: { text: 'Subheading', fontSize: 36, fontWeight: '600' },
      body: { text: 'Body text goes here', fontSize: 18, fontWeight: 'normal' },
      caption: { text: 'Caption', fontSize: 14, fontWeight: 'normal' },
    };
    
    const config = presets[preset] || presets.heading;
    
    const text = new fabric.Textbox(config.text, {
      left: canvas.width / 2 - 100,
      top: canvas.height / 2 - 30,
      width: 400,
      fontSize: config.fontSize,
      fontFamily: 'Inter',
      fontWeight: config.fontWeight,
      fill: '#1e293b',
      textAlign: 'center',
      id: `text_${Date.now()}`,
    });
    
    canvas.add(text);
    canvas.setActiveObject(text);
    canvas.requestRenderAll();
  }, [canvas]);

  const addShape = useCallback((type) => {
    if (!canvas) return;
    
    let shape;
    const centerX = canvas.width / 2;
    const centerY = canvas.height / 2;
    
    switch (type) {
      case 'rect':
        shape = new fabric.Rect({
          left: centerX - 75,
          top: centerY - 50,
          width: 150,
          height: 100,
          fill: '#8b5cf6',
          rx: 8,
          ry: 8,
        });
        break;
        
      case 'circle':
        shape = new fabric.Circle({
          left: centerX - 50,
          top: centerY - 50,
          radius: 50,
          fill: '#06b6d4',
        });
        break;
        
      case 'triangle':
        shape = new fabric.Triangle({
          left: centerX - 50,
          top: centerY - 50,
          width: 100,
          height: 100,
          fill: '#10b981',
        });
        break;
        
      case 'line':
        shape = new fabric.Line([0, 0, 200, 0], {
          left: centerX - 100,
          top: centerY,
          stroke: '#1e293b',
          strokeWidth: 2,
        });
        break;
        
      default:
        return;
    }
    
    shape.id = `${type}_${Date.now()}`;
    canvas.add(shape);
    canvas.setActiveObject(shape);
    canvas.requestRenderAll();
  }, [canvas]);

  const addImage = useCallback((url) => {
    if (!canvas) return;
    
    fabric.Image.fromURL(url, (img) => {
      const scale = Math.min(
        (canvas.width * 0.5) / img.width,
        (canvas.height * 0.5) / img.height
      );
      
      img.set({
        left: canvas.width / 2 - (img.width * scale) / 2,
        top: canvas.height / 2 - (img.height * scale) / 2,
        scaleX: scale,
        scaleY: scale,
        id: `img_${Date.now()}`,
      });
      
      canvas.add(img);
      canvas.setActiveObject(img);
      canvas.requestRenderAll();
    }, { crossOrigin: 'anonymous' });
  }, [canvas]);

  // Zoom controls
  const zoomIn = useCallback(() => {
    setZoom((prev) => Math.min(prev + 0.1, 3));
  }, []);

  const zoomOut = useCallback(() => {
    setZoom((prev) => Math.max(prev - 0.1, 0.25));
  }, []);

  const resetZoom = useCallback(() => {
    setZoom(1);
  }, []);

  // Layer actions
  const handleLayerSelect = useCallback((layerId) => {
    if (!canvas) return;
    
    const obj = canvas.getObjects().find(o => o.id === layerId);
    if (obj) {
      canvas.setActiveObject(obj);
      canvas.requestRenderAll();
    }
  }, [canvas]);

  const handleLayerVisibility = useCallback((layerId, visible) => {
    if (!canvas) return;
    
    const obj = canvas.getObjects().find(o => o.id === layerId);
    if (obj) {
      obj.set('visible', visible);
      canvas.requestRenderAll();
      updateLayers();
    }
  }, [canvas, updateLayers]);

  const handleLayerLock = useCallback((layerId, locked) => {
    if (!canvas) return;
    
    const obj = canvas.getObjects().find(o => o.id === layerId);
    if (obj) {
      obj.set({
        selectable: !locked,
        evented: !locked,
      });
      canvas.requestRenderAll();
      updateLayers();
    }
  }, [canvas, updateLayers]);

  const handleLayerReorder = useCallback((fromIndex, toIndex) => {
    if (!canvas) return;
    
    const objects = canvas.getObjects().filter(obj => obj.type !== 'alignmentGuideLine');
    const reversedFrom = objects.length - 1 - fromIndex;
    const reversedTo = objects.length - 1 - toIndex;
    
    const obj = objects[reversedFrom];
    if (!obj) return;
    
    canvas.moveTo(obj, reversedTo);
    canvas.requestRenderAll();
    updateLayers();
  }, [canvas, updateLayers]);

  // Property updates
  const handlePropertyChange = useCallback((property, value) => {
    if (!selectedObject || !canvas) return;
    
    const propertyMap = {
      fill: 'fill',
      stroke: 'stroke',
      strokeWidth: 'strokeWidth',
      opacity: 'opacity',
      fontSize: 'fontSize',
      fontFamily: 'fontFamily',
      fontWeight: 'fontWeight',
      fontStyle: 'fontStyle',
      textAlign: 'textAlign',
      lineHeight: 'lineHeight',
      letterSpacing: 'charSpacing',
      text: 'text',
      rx: 'rx',
      ry: 'ry',
    };
    
    const fabricProp = propertyMap[property] || property;
    
    if (property === 'letterSpacing') {
      value = value * 10; // Fabric uses different scale
    }
    
    selectedObject.set(fabricProp, value);
    canvas.requestRenderAll();
  }, [canvas, selectedObject]);

  // Alignment functions
  const alignObjects = useCallback((alignment) => {
    if (!selectedObject || !canvas) return;
    
    const objBounds = selectedObject.getBoundingRect(true);
    
    switch (alignment) {
      case 'left':
        selectedObject.set('left', 0);
        break;
      case 'center':
        selectedObject.set('left', (canvas.width - objBounds.width) / 2);
        break;
      case 'right':
        selectedObject.set('left', canvas.width - objBounds.width);
        break;
      case 'top':
        selectedObject.set('top', 0);
        break;
      case 'middle':
        selectedObject.set('top', (canvas.height - objBounds.height) / 2);
        break;
      case 'bottom':
        selectedObject.set('top', canvas.height - objBounds.height);
        break;
      default:
        break;
    }
    
    canvas.requestRenderAll();
    saveToHistory();
  }, [canvas, selectedObject, saveToHistory]);

  // Bring to front/back
  const bringToFront = useCallback(() => {
    if (!selectedObject || !canvas) return;
    canvas.bringToFront(selectedObject);
    canvas.requestRenderAll();
    updateLayers();
  }, [canvas, selectedObject, updateLayers]);

  const sendToBack = useCallback(() => {
    if (!selectedObject || !canvas) return;
    canvas.sendToBack(selectedObject);
    canvas.requestRenderAll();
    updateLayers();
  }, [canvas, selectedObject, updateLayers]);

  return (
    <div className="professional-editor">
      {/* Toolbar */}
      <EditorToolbar
        activeTool={activeTool}
        onToolChange={setActiveTool}
        onAddText={addText}
        onAddShape={addShape}
        onAddImage={addImage}
        onUndo={undo}
        onRedo={redo}
        onZoomIn={zoomIn}
        onZoomOut={zoomOut}
        onResetZoom={resetZoom}
        zoom={zoom}
        canUndo={historyIndex > 0}
        canRedo={historyIndex < history.length - 1}
        showGrid={showGrid}
        onToggleGrid={() => setShowGrid(!showGrid)}
        snapToGrid={snapToGrid}
        onToggleSnap={() => setSnapToGrid(!snapToGrid)}
        onSave={handleSave}
        onExport={handleExport}
        onToggleAI={() => setShowAIAssistant(!showAIAssistant)}
      />

      <div className="editor-main">
        {/* Layers Panel */}
        <LayersPanel
          layers={layers}
          selectedId={selectedObject?.id}
          onSelect={handleLayerSelect}
          onVisibilityChange={handleLayerVisibility}
          onLockChange={handleLayerLock}
          onReorder={handleLayerReorder}
          onDelete={deleteSelected}
          onDuplicate={duplicate}
        />

        {/* Canvas Area */}
        <div className="canvas-area" ref={containerRef}>
          <div 
            className="canvas-wrapper"
            style={{
              transform: `scale(${zoom})`,
              transformOrigin: 'center center',
            }}
          >
            {showGrid && (
              <div 
                className="canvas-grid"
                style={{
                  width: canvasWidth,
                  height: canvasHeight,
                  backgroundSize: `${GRID_SIZE}px ${GRID_SIZE}px`,
                }}
              />
            )}
            <canvas ref={canvasRef} />
          </div>

          {/* Zoom indicator */}
          <div className="zoom-indicator">
            {Math.round(zoom * 100)}%
          </div>
        </div>

        {/* Properties Panel */}
        <PropertiesPanel
          selectedObject={selectedObject}
          onPropertyChange={handlePropertyChange}
          onAlign={alignObjects}
          onBringToFront={bringToFront}
          onSendToBack={sendToBack}
          onDelete={deleteSelected}
          onDuplicate={duplicate}
        />

        {/* AI Assistant */}
        {showAIAssistant && (
          <AIAssistant
            canvas={canvas}
            selectedObject={selectedObject}
            onClose={() => setShowAIAssistant(false)}
            onApplyDesign={(design) => {
              loadDesign(canvas, design);
            }}
          />
        )}
      </div>
    </div>
  );
};

export default ProfessionalEditor;
