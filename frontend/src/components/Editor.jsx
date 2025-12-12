import React, { useState, useEffect, useRef, useCallback } from 'react';
import { fabric } from 'fabric';
import axios from 'axios';

const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000';

/**
 * Design Editor Component
 * Implements full editing workflow with autosave, compliance checking, and export
 */
const Editor = ({ designId, onClose }) => {
  const [design, setDesign] = useState(null);
  const [selectedElement, setSelectedElement] = useState(null);
  const [loading, setLoading] = useState(true);
  const [saveStatus, setSaveStatus] = useState('saved'); // saved, saving, unsaved
  const [compliance, setCompliance] = useState(null);
  const [history, setHistory] = useState([]);
  const [historyIndex, setHistoryIndex] = useState(-1);
  
  const canvasRef = useRef(null);
  const fabricCanvasRef = useRef(null);
  const saveTimeoutRef = useRef(null);
  const complianceTimeoutRef = useRef(null);

  // Fetch design from API
  const fetchDesign = useCallback(async (id) => {
    try {
      setLoading(true);
      const response = await axios.get(`${API_BASE_URL}/api/designs/${id}`);
      const designData = response.data;
      setDesign(designData);
      setHistory([designData]);
      setHistoryIndex(0);
      return designData;
    } catch (error) {
      console.error('Failed to fetch design:', error);
      alert('Failed to load design');
    } finally {
      setLoading(false);
    }
  }, []);

  // Save design to API (debounced)
  const saveDesign = useCallback(async (designData) => {
    try {
      setSaveStatus('saving');
      await axios.put(`${API_BASE_URL}/api/designs/${designId}`, designData);
      setSaveStatus('saved');
      
      // Add to history
      setHistory(prev => [...prev.slice(0, historyIndex + 1), designData]);
      setHistoryIndex(prev => prev + 1);
    } catch (error) {
      console.error('Failed to save design:', error);
      setSaveStatus('unsaved');
    }
  }, [designId, historyIndex]);

  // Debounced autosave
  const debouncedSave = useCallback((designData) => {
    setSaveStatus('unsaved');
    clearTimeout(saveTimeoutRef.current);
    saveTimeoutRef.current = setTimeout(() => {
      saveDesign(designData);
    }, 1000);
  }, [saveDesign]);

  // Check compliance (debounced)
  const checkCompliance = useCallback(async (designData) => {
    clearTimeout(complianceTimeoutRef.current);
    complianceTimeoutRef.current = setTimeout(async () => {
      try {
        const response = await axios.post(`${API_BASE_URL}/api/compliance/check`, {
          design_id: designId,
          platform: designData.platform
        });
        setCompliance(response.data);
      } catch (error) {
        console.error('Compliance check failed:', error);
      }
    }, 1500);
  }, [designId]);

  // Initialize Fabric.js canvas
  useEffect(() => {
    if (!canvasRef.current || fabricCanvasRef.current) return;

    const canvas = new fabric.Canvas(canvasRef.current, {
      width: 800,
      height: 800,
      backgroundColor: '#ffffff',
      preserveObjectStacking: true
    });

    fabricCanvasRef.current = canvas;

    // Handle object selection
    canvas.on('selection:created', (e) => {
      if (e.selected && e.selected[0]) {
        setSelectedElement(e.selected[0]);
      }
    });

    canvas.on('selection:updated', (e) => {
      if (e.selected && e.selected[0]) {
        setSelectedElement(e.selected[0]);
      }
    });

    canvas.on('selection:cleared', () => {
      setSelectedElement(null);
    });

    // Handle object modifications
    canvas.on('object:modified', () => {
      handleCanvasChange();
    });

    return () => {
      canvas.dispose();
      fabricCanvasRef.current = null;
    };
  }, []);

  // Load design into canvas
  useEffect(() => {
    if (design && fabricCanvasRef.current && design.canvas_data) {
      fabricCanvasRef.current.loadFromJSON(design.canvas_data, () => {
        fabricCanvasRef.current.renderAll();
      });
    }
  }, [design]);

  // Fetch design on mount
  useEffect(() => {
    if (designId) {
      fetchDesign(designId);
    }
  }, [designId, fetchDesign]);

  // Handle canvas changes
  const handleCanvasChange = useCallback(() => {
    if (!fabricCanvasRef.current || !design) return;

    const updatedDesign = {
      ...design,
      canvas_data: fabricCanvasRef.current.toJSON(),
      metadata: {
        ...design.metadata,
        updatedAt: new Date().toISOString(),
        version: (design.metadata?.version || 1) + 1
      }
    };

    setDesign(updatedDesign);
    debouncedSave(updatedDesign);
    checkCompliance(updatedDesign);
  }, [design, debouncedSave, checkCompliance]);

  // Update selected element property
  const updateElementProperty = (property, value) => {
    if (!selectedElement) return;

    selectedElement.set(property, value);
    fabricCanvasRef.current.renderAll();
    handleCanvasChange();
  };

  // Add text element
  const addText = () => {
    const text = new fabric.IText('New Text', {
      left: 100,
      top: 100,
      fontFamily: 'Arial',
      fontSize: 24,
      fill: '#000000',
      editable: true
    });
    fabricCanvasRef.current.add(text);
    fabricCanvasRef.current.setActiveObject(text);
    handleCanvasChange();
  };

  // Add shape
  const addShape = (type) => {
    let shape;
    if (type === 'rectangle') {
      shape = new fabric.Rect({
        left: 100,
        top: 100,
        width: 150,
        height: 100,
        fill: '#0066FF'
      });
    } else if (type === 'circle') {
      shape = new fabric.Circle({
        left: 100,
        top: 100,
        radius: 50,
        fill: '#00CC66'
      });
    }
    
    if (shape) {
      fabricCanvasRef.current.add(shape);
      fabricCanvasRef.current.setActiveObject(shape);
      handleCanvasChange();
    }
  };

  // Delete selected element
  const deleteElement = () => {
    if (!selectedElement) return;
    fabricCanvasRef.current.remove(selectedElement);
    setSelectedElement(null);
    handleCanvasChange();
  };

  // Undo/Redo
  const undo = () => {
    if (historyIndex > 0) {
      const prevDesign = history[historyIndex - 1];
      setDesign(prevDesign);
      setHistoryIndex(historyIndex - 1);
      if (fabricCanvasRef.current && prevDesign.canvas_data) {
        fabricCanvasRef.current.loadFromJSON(prevDesign.canvas_data, () => {
          fabricCanvasRef.current.renderAll();
        });
      }
    }
  };

  const redo = () => {
    if (historyIndex < history.length - 1) {
      const nextDesign = history[historyIndex + 1];
      setDesign(nextDesign);
      setHistoryIndex(historyIndex + 1);
      if (fabricCanvasRef.current && nextDesign.canvas_data) {
        fabricCanvasRef.current.loadFromJSON(nextDesign.canvas_data, () => {
          fabricCanvasRef.current.renderAll();
        });
      }
    }
  };

  // Export design
  const exportDesign = async (format = 'png') => {
    try {
      const response = await axios.get(
        `${API_BASE_URL}/api/designs/${designId}/export?format=${format}`,
        { responseType: 'blob' }
      );
      
      const url = window.URL.createObjectURL(new Blob([response.data]));
      const link = document.createElement('a');
      link.href = url;
      link.setAttribute('download', `design-${designId}.${format}`);
      document.body.appendChild(link);
      link.click();
      link.remove();
    } catch (error) {
      console.error('Export failed:', error);
      alert('Export failed');
    }
  };

  // Keyboard shortcuts
  useEffect(() => {
    const handleKeyDown = (e) => {
      // Cmd/Ctrl + S: Save
      if ((e.metaKey || e.ctrlKey) && e.key === 's') {
        e.preventDefault();
        saveDesign(design);
      }
      // Cmd/Ctrl + Z: Undo
      if ((e.metaKey || e.ctrlKey) && e.key === 'z' && !e.shiftKey) {
        e.preventDefault();
        undo();
      }
      // Cmd/Ctrl + Shift + Z: Redo
      if ((e.metaKey || e.ctrlKey) && e.key === 'z' && e.shiftKey) {
        e.preventDefault();
        redo();
      }
      // Delete/Backspace: Delete element
      if ((e.key === 'Delete' || e.key === 'Backspace') && selectedElement) {
        e.preventDefault();
        deleteElement();
      }
    };

    window.addEventListener('keydown', handleKeyDown);
    return () => window.removeEventListener('keydown', handleKeyDown);
  }, [design, selectedElement, historyIndex]);

  if (loading) {
    return (
      <div className="flex items-center justify-center h-screen">
        <div className="text-lg">Loading editor...</div>
      </div>
    );
  }

  return (
    <div className="editor-container h-screen flex flex-col bg-gray-50">
      {/* Header Toolbar */}
      <div className="bg-white border-b border-gray-200 px-4 py-3 flex items-center justify-between">
        <div className="flex items-center space-x-4">
          <button
            onClick={onClose}
            className="text-gray-600 hover:text-gray-900"
          >
            ← Back
          </button>
          <h1 className="text-lg font-semibold">{design?.prompt || 'Design Editor'}</h1>
          
          {/* Save Status */}
          <div className="flex items-center space-x-2">
            {saveStatus === 'saved' && (
              <span className="text-sm text-green-600 flex items-center">
                <svg className="w-4 h-4 mr-1" fill="currentColor" viewBox="0 0 20 20">
                  <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clipRule="evenodd" />
                </svg>
                Saved
              </span>
            )}
            {saveStatus === 'saving' && (
              <span className="text-sm text-blue-600">Saving...</span>
            )}
            {saveStatus === 'unsaved' && (
              <span className="text-sm text-orange-600">Unsaved changes</span>
            )}
          </div>

          {/* Compliance Badge */}
          {compliance && (
            <div className={`px-3 py-1 rounded-full text-xs font-medium ${
              compliance.compliant 
                ? 'bg-green-100 text-green-800' 
                : 'bg-red-100 text-red-800'
            }`}>
              {compliance.compliant ? '✓ Compliant' : '⚠ Issues found'}
            </div>
          )}
        </div>

        <div className="flex items-center space-x-2">
          {/* History Controls */}
          <button
            onClick={undo}
            disabled={historyIndex <= 0}
            className="px-3 py-1 text-sm bg-gray-100 rounded hover:bg-gray-200 disabled:opacity-50 disabled:cursor-not-allowed"
            title="Undo (Ctrl+Z)"
          >
            ↶ Undo
          </button>
          <button
            onClick={redo}
            disabled={historyIndex >= history.length - 1}
            className="px-3 py-1 text-sm bg-gray-100 rounded hover:bg-gray-200 disabled:opacity-50 disabled:cursor-not-allowed"
            title="Redo (Ctrl+Shift+Z)"
          >
            ↷ Redo
          </button>

          {/* Export */}
          <select
            onChange={(e) => exportDesign(e.target.value)}
            className="px-3 py-1 text-sm border border-gray-300 rounded"
            defaultValue=""
          >
            <option value="" disabled>Export as...</option>
            <option value="png">PNG</option>
            <option value="jpg">JPG</option>
            <option value="svg">SVG</option>
            <option value="pdf">PDF</option>
          </select>
        </div>
      </div>

      {/* Main Content */}
      <div className="flex flex-1 overflow-hidden">
        {/* Left Toolbar */}
        <div className="w-16 bg-white border-r border-gray-200 flex flex-col items-center py-4 space-y-4">
          <button
            onClick={addText}
            className="p-3 hover:bg-gray-100 rounded"
            title="Add Text"
          >
            <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M11 5H6a2 2 0 00-2 2v11a2 2 0 002 2h11a2 2 0 002-2v-5m-1.414-9.414a2 2 0 112.828 2.828L11.828 15H9v-2.828l8.586-8.586z" />
            </svg>
          </button>
          <button
            onClick={() => addShape('rectangle')}
            className="p-3 hover:bg-gray-100 rounded"
            title="Add Rectangle"
          >
            <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <rect x="4" y="4" width="16" height="16" strokeWidth={2} />
            </svg>
          </button>
          <button
            onClick={() => addShape('circle')}
            className="p-3 hover:bg-gray-100 rounded"
            title="Add Circle"
          >
            <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <circle cx="12" cy="12" r="8" strokeWidth={2} />
            </svg>
          </button>
          <button
            onClick={deleteElement}
            disabled={!selectedElement}
            className="p-3 hover:bg-gray-100 rounded disabled:opacity-50 disabled:cursor-not-allowed"
            title="Delete (Del)"
          >
            <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16" />
            </svg>
          </button>
        </div>

        {/* Canvas Area */}
        <div className="flex-1 flex items-center justify-center bg-gray-100 p-8 overflow-auto">
          <div className="bg-white shadow-lg">
            <canvas ref={canvasRef} />
          </div>
        </div>

        {/* Right Properties Panel */}
        <div className="w-80 bg-white border-l border-gray-200 overflow-y-auto">
          {selectedElement ? (
            <div className="p-4 space-y-4">
              <h3 className="font-semibold text-lg">Properties</h3>
              
              {/* Position */}
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">Position</label>
                <div className="grid grid-cols-2 gap-2">
                  <div>
                    <label className="text-xs text-gray-500">X</label>
                    <input
                      type="number"
                      value={Math.round(selectedElement.left || 0)}
                      onChange={(e) => updateElementProperty('left', parseFloat(e.target.value))}
                      className="w-full px-2 py-1 border border-gray-300 rounded text-sm"
                    />
                  </div>
                  <div>
                    <label className="text-xs text-gray-500">Y</label>
                    <input
                      type="number"
                      value={Math.round(selectedElement.top || 0)}
                      onChange={(e) => updateElementProperty('top', parseFloat(e.target.value))}
                      className="w-full px-2 py-1 border border-gray-300 rounded text-sm"
                    />
                  </div>
                </div>
              </div>

              {/* Size */}
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">Size</label>
                <div className="grid grid-cols-2 gap-2">
                  <div>
                    <label className="text-xs text-gray-500">Width</label>
                    <input
                      type="number"
                      value={Math.round(selectedElement.width * (selectedElement.scaleX || 1))}
                      onChange={(e) => updateElementProperty('width', parseFloat(e.target.value))}
                      className="w-full px-2 py-1 border border-gray-300 rounded text-sm"
                    />
                  </div>
                  <div>
                    <label className="text-xs text-gray-500">Height</label>
                    <input
                      type="number"
                      value={Math.round(selectedElement.height * (selectedElement.scaleY || 1))}
                      onChange={(e) => updateElementProperty('height', parseFloat(e.target.value))}
                      className="w-full px-2 py-1 border border-gray-300 rounded text-sm"
                    />
                  </div>
                </div>
              </div>

              {/* Rotation */}
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">
                  Rotation: {Math.round(selectedElement.angle || 0)}°
                </label>
                <input
                  type="range"
                  min="0"
                  max="360"
                  value={selectedElement.angle || 0}
                  onChange={(e) => updateElementProperty('angle', parseFloat(e.target.value))}
                  className="w-full"
                />
              </div>

              {/* Text Properties */}
              {selectedElement.type === 'i-text' && (
                <>
                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-1">Font Family</label>
                    <select
                      value={selectedElement.fontFamily || 'Arial'}
                      onChange={(e) => updateElementProperty('fontFamily', e.target.value)}
                      className="w-full px-2 py-1 border border-gray-300 rounded text-sm"
                    >
                      <option value="Arial">Arial</option>
                      <option value="Helvetica">Helvetica</option>
                      <option value="Times New Roman">Times New Roman</option>
                      <option value="Georgia">Georgia</option>
                      <option value="Courier New">Courier New</option>
                    </select>
                  </div>

                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-1">Font Size</label>
                    <input
                      type="number"
                      value={selectedElement.fontSize || 24}
                      onChange={(e) => updateElementProperty('fontSize', parseFloat(e.target.value))}
                      className="w-full px-2 py-1 border border-gray-300 rounded text-sm"
                    />
                  </div>

                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-1">Color</label>
                    <input
                      type="color"
                      value={selectedElement.fill || '#000000'}
                      onChange={(e) => updateElementProperty('fill', e.target.value)}
                      className="w-full h-10 border border-gray-300 rounded"
                    />
                  </div>

                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-1">Font Weight</label>
                    <select
                      value={selectedElement.fontWeight || 'normal'}
                      onChange={(e) => updateElementProperty('fontWeight', e.target.value)}
                      className="w-full px-2 py-1 border border-gray-300 rounded text-sm"
                    >
                      <option value="normal">Normal</option>
                      <option value="bold">Bold</option>
                      <option value="700">700</option>
                      <option value="800">800</option>
                    </select>
                  </div>
                </>
              )}

              {/* Shape Properties */}
              {(selectedElement.type === 'rect' || selectedElement.type === 'circle') && (
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">Fill Color</label>
                  <input
                    type="color"
                    value={selectedElement.fill || '#0066FF'}
                    onChange={(e) => updateElementProperty('fill', e.target.value)}
                    className="w-full h-10 border border-gray-300 rounded"
                  />
                </div>
              )}

              {/* Opacity */}
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">
                  Opacity: {Math.round((selectedElement.opacity || 1) * 100)}%
                </label>
                <input
                  type="range"
                  min="0"
                  max="1"
                  step="0.01"
                  value={selectedElement.opacity || 1}
                  onChange={(e) => updateElementProperty('opacity', parseFloat(e.target.value))}
                  className="w-full"
                />
              </div>
            </div>
          ) : (
            <div className="p-4 text-center text-gray-500">
              <p>Select an element to edit its properties</p>
            </div>
          )}

          {/* Compliance Results */}
          {compliance && !compliance.compliant && (
            <div className="p-4 border-t border-gray-200">
              <h3 className="font-semibold text-sm text-red-700 mb-2">Compliance Issues</h3>
              <ul className="space-y-2 text-sm">
                {compliance.violations?.map((violation, idx) => (
                  <li key={idx} className="text-red-600">• {violation}</li>
                ))}
              </ul>
              {compliance.suggested_fixes && (
                <div className="mt-3">
                  <h4 className="font-medium text-sm mb-1">Suggested Fixes:</h4>
                  <ul className="space-y-1 text-xs text-gray-600">
                    {compliance.suggested_fixes.map((fix, idx) => (
                      <li key={idx}>• {fix.issue}: {fix.fix}</li>
                    ))}
                  </ul>
                </div>
              )}
            </div>
          )}
        </div>
      </div>
    </div>
  );
};

export default Editor;
