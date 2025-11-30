import React, { useState, useEffect, useRef } from 'react';
import { useQuery, useMutation } from 'react-query';
import { generateDesign, getDesigns } from '../services/api';
import { fabric } from 'fabric';

const DesignStudioPage = () => {
  const [prompt, setPrompt] = useState('');
  const [platform, setPlatform] = useState('meta');
  const [format, setFormat] = useState('square');
  const [selectedDesign, setSelectedDesign] = useState(null);
  const canvasRef = useRef(null);
  const fabricCanvasRef = useRef(null);

  const { data: designs, refetch } = useQuery('designs', getDesigns);

  const generateMutation = useMutation(generateDesign, {
    onSuccess: (data) => {
      refetch();
      setPrompt('');
      setSelectedDesign(data);
    },
  });

  const handleGenerate = () => {
    if (prompt.trim()) {
      generateMutation.mutate({
        prompt,
        platform,
        format,
      });
    }
  };

  const handleDesignClick = (design) => {
    setSelectedDesign(design);
  };

  const handleExport = () => {
    if (selectedDesign) {
      window.open(`${process.env.REACT_APP_API_URL}/designs/${selectedDesign.id}/export?format=png`, '_blank');
    }
  };

  const handleEdit = () => {
    if (selectedDesign && fabricCanvasRef.current) {
      // Enable editing mode
      fabricCanvasRef.current.isDrawingMode = false;
      fabricCanvasRef.current.selection = true;
      fabricCanvasRef.current.forEachObject((obj) => {
        obj.selectable = true;
        obj.evented = true;
      });
    }
  };

  // Initialize Fabric.js canvas
  useEffect(() => {
    if (canvasRef.current && !fabricCanvasRef.current) {
      const canvas = new fabric.Canvas(canvasRef.current, {
        width: 600,
        height: 600,
        backgroundColor: '#ffffff',
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

  // Load design into canvas when selected
  useEffect(() => {
    if (selectedDesign && fabricCanvasRef.current) {
      try {
        fabricCanvasRef.current.clear();
        if (selectedDesign.canvas_data) {
          fabricCanvasRef.current.loadFromJSON(selectedDesign.canvas_data, () => {
            fabricCanvasRef.current.renderAll();
          });
        }
      } catch (error) {
        console.error('Error loading canvas data:', error);
      }
    }
  }, [selectedDesign]);

  return (
    <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
      <h1 className="text-3xl font-bold text-gray-900 mb-8">Design Studio</h1>

      <div className="grid lg:grid-cols-2 gap-8">
        {/* Left Panel - Controls */}
        <div className="space-y-6">
          <div className="bg-white p-6 rounded-lg shadow">
          {/* Recent Designs */}
          <div className="bg-white p-6 rounded-lg shadow">
            <h2 className="text-xl font-semibold mb-4">Recent Designs</h2>
            <div className="space-y-2">
              {designs?.length > 0 ? (
                designs.slice(0, 5).map((design) => (
                  <div
                    key={design.id}
                    onClick={() => handleDesignClick(design)}
                    className={`p-3 border rounded hover:bg-gray-50 cursor-pointer ${
                      selectedDesign?.id === design.id ? 'border-primary-500 bg-primary-50' : 'border-gray-200'
                    }`}
                  >
                    <p className="text-sm font-medium">{design.prompt}</p>
                    <p className="text-xs text-gray-500">
                      {design.platform} • {design.format}
                    </p>
                  </div>
                ))
              ) : (
                <p className="text-gray-500 text-sm">No designs yet. Create your first one!</p>
              )}
            </div>
          </div><select
                  className="w-full px-3 py-2 border border-gray-300 rounded-md focus:ring-primary-500 focus:border-primary-500"
                  value={platform}
                  onChange={(e) => setPlatform(e.target.value)}
                >
                  <option value="meta">Meta (Facebook/Instagram)</option>
                  <option value="google">Google Ads</option>
                  <option value="linkedin">LinkedIn</option>
                </select>
              </div>

              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  Format
                </label>
                <select
                  className="w-full px-3 py-2 border border-gray-300 rounded-md focus:ring-primary-500 focus:border-primary-500"
                  value={format}
                  onChange={(e) => setFormat(e.target.value)}
                >
                  <option value="square">Square (1:1)</option>
                  <option value="landscape">Landscape (16:9)</option>
                  <option value="portrait">Portrait (9:16)</option>
                  <option value="story">Story (9:16)</option>
                </select>
              </div>

              <button
                onClick={handleGenerate}
                disabled={generateMutation.isLoading || !prompt.trim()}
                className="w-full bg-primary-600 text-white px-4 py-3 rounded-md font-semibold hover:bg-primary-700 disabled:bg-gray-400 disabled:cursor-not-allowed"
              >
                {generateMutation.isLoading ? 'Generating...' : 'Generate Design'}
              </button>
            </div>
          </div>

          {/* Recent Designs */}
          <div className="bg-white p-6 rounded-lg shadow">
            <h2 className="text-xl font-semibold mb-4">Recent Designs</h2>
            <div className="space-y-2">
              {designs?.length > 0 ? (
                designs.slice(0, 5).map((design) => (
                  <div
                    key={design.id}
                    className="p-3 border border-gray-200 rounded hover:bg-gray-50 cursor-pointer"
                  >
                    <p className="text-sm font-medium">{design.prompt}</p>
                    <p className="text-xs text-gray-500">
                      {design.platform} • {design.format}
                    </p>
                  </div>
                ))
              ) : (
                <p className="text-gray-500 text-sm">No designs yet. Create your first one!</p>
              )}
            </div>
        {/* Right Panel - Canvas Preview */}
        <div className="bg-white p-6 rounded-lg shadow">
          <h2 className="text-xl font-semibold mb-4">
            {selectedDesign ? 'Design Preview' : 'Preview'}
          </h2>
          <div className="bg-gray-100 rounded-lg flex items-center justify-center overflow-hidden">
            {selectedDesign ? (
              <canvas ref={canvasRef} id="design-canvas" />
            ) : (
              <div className="aspect-square flex items-center justify-center">
                <p className="text-gray-400">Select or generate a design to preview</p>
              </div>
            )}
          </div>
          {selectedDesign && (
            <div className="mt-4">
              <div className="mb-3 p-3 bg-gray-50 rounded">
                <p className="text-sm text-gray-600">
                  <strong>Prompt:</strong> {selectedDesign.prompt}
                </p>
                <p className="text-xs text-gray-500 mt-1">
                  {selectedDesign.platform} • {selectedDesign.format}
                </p>
              </div>
              <div className="flex space-x-2">
                <button 
                  onClick={handleEdit}
                  className="flex-1 bg-gray-200 text-gray-700 px-4 py-2 rounded hover:bg-gray-300 font-medium"
                >
                  Edit
                </button>
                <button 
                  onClick={handleExport}
                  className="flex-1 bg-primary-600 text-white px-4 py-2 rounded hover:bg-primary-700 font-medium"
                >
                  Export
                </button>
              </div>
            </div>
          )}
        </div>
      </div>
    </div>
  );
};

export default DesignStudioPage;
