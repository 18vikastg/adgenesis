import React, { useState, useEffect, useRef } from 'react';
import { useQuery, useMutation } from 'react-query';
import { generateDesign, getDesigns } from '../services/api';
import { fabric } from 'fabric';
import AdvancedEditor from '../components/AdvancedEditor';
import TemplateGallery from '../components/TemplateGallery';

const ML_SERVICE_URL = process.env.REACT_APP_ML_URL || 'http://localhost:8001';

const DesignStudioPage = () => {
  // State
  const [prompt, setPrompt] = useState('');
  const [platform, setPlatform] = useState('meta');
  const [format, setFormat] = useState('square');
  const [selectedDesign, setSelectedDesign] = useState(null);
  const [showEditor, setShowEditor] = useState(false);
  const [showTemplates, setShowTemplates] = useState(false);
  const [generating, setGenerating] = useState(false);
  
  const canvasRef = useRef(null);
  const fabricCanvasRef = useRef(null);

  const { data: designs, refetch } = useQuery('designs', getDesigns);

  // Platform specs
  const platformSpecs = {
    meta: {
      square: { width: 1080, height: 1080, label: 'Square (1:1)' },
      landscape: { width: 1200, height: 628, label: 'Landscape (1.91:1)' },
      portrait: { width: 1080, height: 1350, label: 'Portrait (4:5)' },
      story: { width: 1080, height: 1920, label: 'Story (9:16)' },
    },
    google: {
      square: { width: 1200, height: 1200, label: 'Square' },
      landscape: { width: 1200, height: 628, label: 'Landscape' },
      portrait: { width: 900, height: 1600, label: 'Portrait' },
    },
    linkedin: {
      square: { width: 1200, height: 1200, label: 'Square' },
      landscape: { width: 1200, height: 627, label: 'Landscape' },
    },
  };

  // Quick prompts
  const quickPrompts = [
    { label: '🚀 Tech Startup', prompt: 'Create a modern tech startup ad with innovation theme' },
    { label: '🛍️ Fashion Sale', prompt: 'Create a trendy fashion sale poster with 50% off' },
    { label: '🍔 Food Delivery', prompt: 'Create a food delivery ad with appetizing colors' },
    { label: '💼 Business', prompt: 'Create a professional business consulting ad' },
    { label: '🎉 Event', prompt: 'Create an exciting event announcement poster' },
    { label: '✨ Minimal', prompt: 'Create a clean minimal design with elegant typography' },
  ];

  // Generate design
  const handleGenerate = async () => {
    if (!prompt.trim()) return;
    
    setGenerating(true);
    try {
      // Call ML service directly for professional generation
      const response = await fetch(`${ML_SERVICE_URL}/generate`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ prompt, platform, format }),
      });
      
      if (!response.ok) throw new Error('Generation failed');
      
      const designSpec = await response.json();
      
      // Save to backend
      const savedDesign = await generateDesign({ prompt, platform, format });
      
      // Merge ML-generated design with saved design
      const fullDesign = {
        ...savedDesign,
        canvas_data: {
          ...designSpec,
          objects: designSpec.elements,
          background: designSpec.background_color,
          width: platformSpecs[platform]?.[format]?.width || 1080,
          height: platformSpecs[platform]?.[format]?.height || 1080,
        },
      };
      
      setSelectedDesign(fullDesign);
      refetch();
    } catch (error) {
      console.error('Generation error:', error);
      alert('Failed to generate design. Please try again.');
    } finally {
      setGenerating(false);
    }
  };

  // Handle template selection
  const handleTemplateSelect = async (template) => {
    setShowTemplates(false);
    setGenerating(true);
    
    try {
      const response = await fetch(`${ML_SERVICE_URL}/generate`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          prompt: template.preview_prompt || `Create a ${template.name} design`,
          platform,
          format,
          template_id: template.id,
        }),
      });
      
      if (!response.ok) throw new Error('Generation failed');
      
      const designSpec = await response.json();
      
      // Save to backend
      const savedDesign = await generateDesign({
        prompt: template.name,
        platform,
        format,
      });
      
      const fullDesign = {
        ...savedDesign,
        canvas_data: {
          ...designSpec,
          objects: designSpec.elements,
          background: designSpec.background_color,
          width: platformSpecs[platform]?.[format]?.width || 1080,
          height: platformSpecs[platform]?.[format]?.height || 1080,
        },
      };
      
      setSelectedDesign(fullDesign);
      refetch();
    } catch (error) {
      console.error('Template error:', error);
      alert('Failed to load template. Please try again.');
    } finally {
      setGenerating(false);
    }
  };

  // Initialize canvas
  useEffect(() => {
    if (canvasRef.current && !fabricCanvasRef.current) {
      const canvas = new fabric.Canvas(canvasRef.current, {
        width: 500,
        height: 500,
        backgroundColor: '#f3f4f6',
        preserveObjectStacking: true,
      });
      fabricCanvasRef.current = canvas;
    }

    return () => {
      if (fabricCanvasRef.current) {
        fabricCanvasRef.current.dispose();
        fabricCanvasRef.current = null;
      }
    };
  }, []);

  // Render design to canvas
  useEffect(() => {
    if (!selectedDesign?.canvas_data || !fabricCanvasRef.current) return;
    
    const canvas = fabricCanvasRef.current;
    canvas.clear();
    
    const data = selectedDesign.canvas_data;
    const bgColor = data.background || data.background_color || '#ffffff';
    canvas.setBackgroundColor(bgColor, canvas.renderAll.bind(canvas));
    
    // Calculate scale
    const designWidth = data.width || 1080;
    const designHeight = data.height || 1080;
    const scale = Math.min(500 / designWidth, 500 / designHeight);
    
    // Render elements
    const objects = data.objects || data.elements || [];
    objects.forEach((obj, index) => {
      let fabricObj = null;
      
      const x = (obj.left || obj.x || 0) * scale;
      const y = (obj.top || obj.y || 0) * scale;
      
      if (obj.type === 'textbox' || obj.type === 'text') {
        fabricObj = new fabric.Textbox(obj.text || '', {
          left: x,
          top: y,
          width: obj.width ? obj.width * scale : 300,
          fontSize: (obj.fontSize || 24) * scale,
          fill: obj.fill || obj.color || '#000000',
          fontFamily: obj.fontFamily || 'Arial',
          fontWeight: obj.fontWeight || 'normal',
          fontStyle: obj.fontStyle || 'normal',
          textAlign: obj.textAlign || 'left',
          lineHeight: obj.lineHeight || 1.2,
          opacity: obj.opacity || 1,
          selectable: false,
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
          opacity: obj.opacity || 1,
          selectable: false,
        });
      } else if (obj.type === 'circle') {
        fabricObj = new fabric.Circle({
          left: x,
          top: y,
          radius: ((obj.width || 100) / 2) * scale,
          fill: obj.fill || obj.color || '#22c55e',
          opacity: obj.opacity || 1,
          selectable: false,
        });
      }
      
      if (fabricObj) {
        canvas.add(fabricObj);
      }
    });
    
    canvas.renderAll();
  }, [selectedDesign]);

  // Export design
  const handleExport = () => {
    if (!fabricCanvasRef.current) return;
    
    const dataURL = fabricCanvasRef.current.toDataURL({
      format: 'png',
      multiplier: 2,
    });
    
    const link = document.createElement('a');
    link.download = `design-${Date.now()}.png`;
    link.href = dataURL;
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
  };

  // Save edited design
  const handleSaveDesign = async (updatedDesign) => {
    try {
      setSelectedDesign(updatedDesign);
      refetch();
    } catch (error) {
      console.error('Save failed:', error);
    }
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-gray-50 to-gray-100">
      {/* Header */}
      <div className="bg-white border-b shadow-sm sticky top-0 z-40">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-4">
          <div className="flex items-center justify-between">
            <div>
              <h1 className="text-2xl font-bold text-gray-900">Design Studio</h1>
              <p className="text-sm text-gray-500 mt-1">Create professional posters with AI</p>
            </div>
            <div className="flex items-center space-x-3">
              <button
                onClick={() => setShowTemplates(true)}
                className="px-4 py-2 bg-gray-100 text-gray-700 rounded-lg hover:bg-gray-200 font-medium flex items-center space-x-2"
              >
                <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 5a1 1 0 011-1h14a1 1 0 011 1v2a1 1 0 01-1 1H5a1 1 0 01-1-1V5zM4 13a1 1 0 011-1h6a1 1 0 011 1v6a1 1 0 01-1 1H5a1 1 0 01-1-1v-6zM16 13a1 1 0 011-1h2a1 1 0 011 1v6a1 1 0 01-1 1h-2a1 1 0 01-1-1v-6z" />
                </svg>
                <span>Templates</span>
              </button>
            </div>
          </div>
        </div>
      </div>

      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        <div className="grid lg:grid-cols-5 gap-8">
          {/* Left Panel - Controls */}
          <div className="lg:col-span-2 space-y-6">
            {/* Prompt Input Card */}
            <div className="bg-white rounded-2xl shadow-lg overflow-hidden">
              <div className="p-6">
                <h2 className="text-lg font-semibold text-gray-900 mb-4">Create Your Design</h2>
                
                {/* Prompt textarea */}
                <div className="mb-4">
                  <label className="block text-sm font-medium text-gray-700 mb-2">
                    Describe your poster
                  </label>
                  <textarea
                    className="w-full px-4 py-3 border border-gray-200 rounded-xl focus:ring-2 focus:ring-blue-500 focus:border-transparent resize-none transition-all"
                    rows="4"
                    placeholder="E.g., Create a modern tech startup poster with bold typography and gradient background..."
                    value={prompt}
                    onChange={(e) => setPrompt(e.target.value)}
                  />
                </div>

                {/* Quick prompts */}
                <div className="mb-4">
                  <label className="block text-xs font-medium text-gray-500 uppercase mb-2">
                    Quick Start
                  </label>
                  <div className="flex flex-wrap gap-2">
                    {quickPrompts.map((qp, i) => (
                      <button
                        key={i}
                        onClick={() => setPrompt(qp.prompt)}
                        className="px-3 py-1.5 bg-gray-100 text-gray-700 text-sm rounded-full hover:bg-gray-200 transition-colors"
                      >
                        {qp.label}
                      </button>
                    ))}
                  </div>
                </div>

                {/* Platform & Format */}
                <div className="grid grid-cols-2 gap-4 mb-4">
                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-2">
                      Platform
                    </label>
                    <select
                      className="w-full px-3 py-2.5 border border-gray-200 rounded-xl focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                      value={platform}
                      onChange={(e) => {
                        setPlatform(e.target.value);
                        setFormat('square');
                      }}
                    >
                      <option value="meta">Meta (FB/IG)</option>
                      <option value="google">Google Ads</option>
                      <option value="linkedin">LinkedIn</option>
                    </select>
                  </div>

                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-2">
                      Format
                    </label>
                    <select
                      className="w-full px-3 py-2.5 border border-gray-200 rounded-xl focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                      value={format}
                      onChange={(e) => setFormat(e.target.value)}
                    >
                      {Object.entries(platformSpecs[platform] || {}).map(([key, spec]) => (
                        <option key={key} value={key}>{spec.label}</option>
                      ))}
                    </select>
                  </div>
                </div>

                {/* Generate Button */}
                <button
                  onClick={handleGenerate}
                  disabled={generating || !prompt.trim()}
                  className="w-full py-3.5 bg-gradient-to-r from-blue-600 to-indigo-600 text-white rounded-xl font-semibold hover:from-blue-700 hover:to-indigo-700 disabled:from-gray-400 disabled:to-gray-400 disabled:cursor-not-allowed transition-all flex items-center justify-center space-x-2 shadow-lg shadow-blue-500/25"
                >
                  {generating ? (
                    <>
                      <svg className="animate-spin h-5 w-5" viewBox="0 0 24 24">
                        <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4" fill="none" />
                        <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4z" />
                      </svg>
                      <span>Creating Magic...</span>
                    </>
                  ) : (
                    <>
                      <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M13 10V3L4 14h7v7l9-11h-7z" />
                      </svg>
                      <span>Generate Design</span>
                    </>
                  )}
                </button>
              </div>
            </div>

            {/* Recent Designs */}
            <div className="bg-white rounded-2xl shadow-lg p-6">
              <div className="flex items-center justify-between mb-4">
                <h2 className="text-lg font-semibold text-gray-900">Recent Designs</h2>
                <span className="text-sm text-gray-500">{designs?.length || 0} designs</span>
              </div>
              
              <div className="space-y-2 max-h-[300px] overflow-y-auto">
                {designs?.length > 0 ? (
                  designs.slice(0, 10).map((design) => (
                    <div
                      key={design.id}
                      onClick={() => setSelectedDesign(design)}
                      className={`p-3 rounded-xl cursor-pointer transition-all ${
                        selectedDesign?.id === design.id
                          ? 'bg-blue-50 border-2 border-blue-500'
                          : 'bg-gray-50 hover:bg-gray-100 border-2 border-transparent'
                      }`}
                    >
                      <p className="text-sm font-medium text-gray-900 line-clamp-1">
                        {design.prompt}
                      </p>
                      <p className="text-xs text-gray-500 mt-1">
                        {design.platform} • {design.format}
                      </p>
                    </div>
                  ))
                ) : (
                  <div className="text-center py-8">
                    <div className="w-12 h-12 bg-gray-100 rounded-full flex items-center justify-center mx-auto mb-3">
                      <svg className="w-6 h-6 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 16l4.586-4.586a2 2 0 012.828 0L16 16m-2-2l1.586-1.586a2 2 0 012.828 0L20 14m-6-6h.01M6 20h12a2 2 0 002-2V6a2 2 0 00-2-2H6a2 2 0 00-2 2v12a2 2 0 002 2z" />
                      </svg>
                    </div>
                    <p className="text-gray-500 text-sm">No designs yet</p>
                    <p className="text-gray-400 text-xs mt-1">Create your first one!</p>
                  </div>
                )}
              </div>
            </div>
          </div>

          {/* Right Panel - Canvas Preview */}
          <div className="lg:col-span-3">
            <div className="bg-white rounded-2xl shadow-lg overflow-hidden sticky top-24">
              {/* Preview Header */}
              <div className="px-6 py-4 border-b flex items-center justify-between">
                <h2 className="font-semibold text-gray-900">
                  {selectedDesign ? 'Design Preview' : 'Preview'}
                </h2>
                {selectedDesign && (
                  <div className="flex items-center space-x-2">
                    <button
                      onClick={() => setShowEditor(true)}
                      className="px-4 py-2 bg-gray-100 text-gray-700 rounded-lg hover:bg-gray-200 font-medium flex items-center space-x-2"
                    >
                      <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M11 5H6a2 2 0 00-2 2v11a2 2 0 002 2h11a2 2 0 002-2v-5m-1.414-9.414a2 2 0 112.828 2.828L11.828 15H9v-2.828l8.586-8.586z" />
                      </svg>
                      <span>Edit</span>
                    </button>
                    <button
                      onClick={handleExport}
                      className="px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 font-medium flex items-center space-x-2"
                    >
                      <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 16v1a3 3 0 003 3h10a3 3 0 003-3v-1m-4-4l-4 4m0 0l-4-4m4 4V4" />
                      </svg>
                      <span>Export</span>
                    </button>
                  </div>
                )}
              </div>

              {/* Canvas */}
              <div className="p-8 bg-gradient-to-br from-gray-100 to-gray-200 min-h-[550px] flex items-center justify-center">
                {selectedDesign ? (
                  <div className="bg-white shadow-2xl rounded-lg overflow-hidden">
                    <canvas ref={canvasRef} id="design-canvas" />
                  </div>
                ) : (
                  <div className="text-center">
                    <div className="w-24 h-24 bg-white rounded-2xl flex items-center justify-center mx-auto mb-4 shadow-lg">
                      <svg className="w-12 h-12 text-gray-300" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={1.5} d="M4 16l4.586-4.586a2 2 0 012.828 0L16 16m-2-2l1.586-1.586a2 2 0 012.828 0L20 14m-6-6h.01M6 20h12a2 2 0 002-2V6a2 2 0 00-2-2H6a2 2 0 00-2 2v12a2 2 0 002 2z" />
                      </svg>
                    </div>
                    <p className="text-gray-500 font-medium">No design selected</p>
                    <p className="text-gray-400 text-sm mt-1">Generate or select a design to preview</p>
                    
                    <button
                      onClick={() => setShowTemplates(true)}
                      className="mt-4 px-6 py-2.5 bg-blue-600 text-white rounded-lg hover:bg-blue-700 font-medium inline-flex items-center space-x-2"
                    >
                      <span>Browse Templates</span>
                      <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 5l7 7-7 7" />
                      </svg>
                    </button>
                  </div>
                )}
              </div>

              {/* Design Info */}
              {selectedDesign && (
                <div className="px-6 py-4 border-t bg-gray-50">
                  <div className="flex items-start justify-between">
                    <div>
                      <p className="text-sm font-medium text-gray-900">{selectedDesign.prompt}</p>
                      <p className="text-xs text-gray-500 mt-1">
                        {selectedDesign.platform} • {selectedDesign.format} • 
                        {platformSpecs[selectedDesign.platform]?.[selectedDesign.format]?.width || 1080}x
                        {platformSpecs[selectedDesign.platform]?.[selectedDesign.format]?.height || 1080}px
                      </p>
                    </div>
                    <span className="px-2.5 py-1 bg-green-100 text-green-700 text-xs font-medium rounded-full">
                      Ready
                    </span>
                  </div>
                </div>
              )}
            </div>
          </div>
        </div>
      </div>

      {/* Advanced Editor Modal */}
      {showEditor && selectedDesign && (
        <AdvancedEditor
          design={selectedDesign}
          onSave={handleSaveDesign}
          onClose={() => setShowEditor(false)}
        />
      )}

      {/* Template Gallery Modal */}
      {showTemplates && (
        <TemplateGallery
          onSelectTemplate={handleTemplateSelect}
          onClose={() => setShowTemplates(false)}
        />
      )}
    </div>
  );
};

export default DesignStudioPage;
