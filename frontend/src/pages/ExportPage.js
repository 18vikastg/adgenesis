import React, { useState, useEffect, useRef } from 'react';
import { useQuery } from 'react-query';
import { getDesigns, exportDesign } from '../services/api';
import { fabric } from 'fabric';

const ExportPage = () => {
  const [selectedDesigns, setSelectedDesigns] = useState([]);
  const [exportFormat, setExportFormat] = useState('png');
  const [previewData, setPreviewData] = useState({});

  const { data: designs } = useQuery('designs', getDesigns);

  const toggleDesign = (designId) => {
    setSelectedDesigns((prev) =>
      prev.includes(designId)
        ? prev.filter((id) => id !== designId)
        : [...prev, designId]
    );
  };

  const handleExport = async () => {
    if (selectedDesigns.length === 0) {
      alert('Please select at least one design to export');
      return;
    }

    for (const designId of selectedDesigns) {
      try {
        await exportDesign(designId, exportFormat);
      } catch (error) {
        console.error('Export failed:', error);
        alert('Export failed. Please check if you have an active OpenAI API key with credits.');
      }
    }
  };

  // Generate canvas previews for designs
  useEffect(() => {
    if (designs && designs.length > 0) {
      designs.forEach((design) => {
        if (design.canvas_data && !previewData[design.id]) {
          try {
            const tempCanvas = document.createElement('canvas');
            tempCanvas.width = 200;
            tempCanvas.height = 200;
            const fabricCanvas = new fabric.Canvas(tempCanvas);
            
            fabricCanvas.loadFromJSON(design.canvas_data, () => {
              fabricCanvas.renderAll();
              const dataURL = fabricCanvas.toDataURL({ format: 'png' });
              setPreviewData(prev => ({ ...prev, [design.id]: dataURL }));
              fabricCanvas.dispose();
            });
          } catch (error) {
            console.error('Error generating preview:', error);
          }
        }
      });
    }
  }, [designs]);

  return (
    <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
      <h1 className="text-3xl font-bold text-gray-900 mb-8">Export Designs</h1>

      <div className="bg-white p-6 rounded-lg shadow mb-8">
        <div className="flex items-center justify-between">
          <div className="flex items-center space-x-4">
            <label className="text-sm font-medium text-gray-700">Export Format:</label>
            <select
              className="px-3 py-2 border border-gray-300 rounded-md focus:ring-primary-500 focus:border-primary-500"
              value={exportFormat}
              onChange={(e) => setExportFormat(e.target.value)}
            >
              <option value="png">PNG</option>
              <option value="jpg">JPG</option>
              <div className="aspect-square bg-gray-100 flex items-center justify-center">
                {previewData[design.id] ? (
                  <img
                    src={previewData[design.id]}
                    alt={design.prompt}
                    className="w-full h-full object-cover"
                  />
                ) : design.preview_url ? (
                  <img
                    src={design.preview_url}
                    alt={design.prompt}
                    className="w-full h-full object-cover"
                  />
                ) : (
                  <div className="flex items-center justify-center h-full">
                    <p className="text-gray-400">Loading preview...</p>
                  </div>
                )} Selected ({selectedDesigns.length})
          </button>
        </div>
      </div>

      <div className="grid md:grid-cols-3 lg:grid-cols-4 gap-6">
        {designs?.length > 0 ? (
          designs.map((design) => (
            <div
              key={design.id}
              className={`bg-white rounded-lg shadow overflow-hidden cursor-pointer transition ${
                selectedDesigns.includes(design.id)
                  ? 'ring-4 ring-primary-600'
                  : 'hover:shadow-lg'
              }`}
              onClick={() => toggleDesign(design.id)}
            >
              <div className="aspect-square bg-gray-100 flex items-center justify-center">
                {design.preview_url ? (
                  <img
                    src={design.preview_url}
                    alt={design.prompt}
                    className="w-full h-full object-cover"
                  />
                ) : (
                  <p className="text-gray-400">No preview</p>
                )}
              </div>
              <div className="p-4">
                <p className="text-sm font-medium truncate">{design.prompt}</p>
                <div className="flex justify-between items-center mt-2">
                  <span className="text-xs text-gray-500">{design.platform}</span>
                  <input
                    type="checkbox"
                    checked={selectedDesigns.includes(design.id)}
                    onChange={() => toggleDesign(design.id)}
                    className="h-4 w-4 text-primary-600 focus:ring-primary-500 border-gray-300 rounded"
                  />
                </div>
              </div>
            </div>
          ))
        ) : (
          <div className="col-span-full text-center py-12">
            <p className="text-gray-500">
              No designs available. Create some designs in the Design Studio first.
            </p>
          </div>
        )}
      </div>
    </div>
  );
};

export default ExportPage;
