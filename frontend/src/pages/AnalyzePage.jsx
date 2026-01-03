/**
 * Analyze Design Page
 * Upload and analyze images to convert them into editable designs
 */

import React, { useState, useCallback, useRef } from 'react';
import { useNavigate } from 'react-router-dom';
import './AnalyzePage.css';

const API_BASE = process.env.REACT_APP_ML_SERVICE_URL || 'http://localhost:8001';

// Icons
const UploadIcon = () => (
  <svg width="48" height="48" viewBox="0 0 48 48" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round">
    <path d="M24 32V8M24 8L16 16M24 8L32 16" />
    <path d="M8 28V36C8 38.2 9.8 40 12 40H36C38.2 40 40 38.2 40 36V28" />
  </svg>
);

const SparklesIcon = () => (
  <svg width="20" height="20" viewBox="0 0 20 20" fill="currentColor">
    <path d="M10 2L11.5 6.5L16 8L11.5 9.5L10 14L8.5 9.5L4 8L8.5 6.5L10 2Z" />
  </svg>
);

const AnalyzePage = () => {
  const navigate = useNavigate();
  const [isDragging, setIsDragging] = useState(false);
  const [isAnalyzing, setIsAnalyzing] = useState(false);
  const [previewImage, setPreviewImage] = useState(null);
  const [error, setError] = useState(null);
  const [analysisResult, setAnalysisResult] = useState(null);
  const fileInputRef = useRef(null);

  const handleDragOver = useCallback((e) => {
    e.preventDefault();
    setIsDragging(true);
  }, []);

  const handleDragLeave = useCallback((e) => {
    e.preventDefault();
    setIsDragging(false);
  }, []);

  const handleDrop = useCallback((e) => {
    e.preventDefault();
    setIsDragging(false);
    
    const files = e.dataTransfer.files;
    if (files.length > 0) {
      processFile(files[0]);
    }
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, []);

  const handleFileSelect = useCallback((e) => {
    const files = e.target.files;
    if (files.length > 0) {
      processFile(files[0]);
    }
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, []);

  const processFile = async (file) => {
    if (!file.type.startsWith('image/')) {
      setError('Please upload an image file (PNG, JPG, WEBP)');
      return;
    }

    if (file.size > 10 * 1024 * 1024) {
      setError('File size must be less than 10MB');
      return;
    }

    setError(null);

    const reader = new FileReader();
    reader.onload = (e) => {
      setPreviewImage(e.target.result);
    };
    reader.readAsDataURL(file);

    await analyzeImage(file);
  };

  const analyzeImage = async (file) => {
    setIsAnalyzing(true);
    setError(null);

    try {
      const base64 = await fileToBase64(file);

      const response = await fetch(`${API_BASE}/analyze-image`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          image_data: base64,
          include_fabric_json: true,
          detect_text: true,
        }),
      });

      const result = await response.json();

      if (result.success) {
        setAnalysisResult(result);
      } else {
        setError(result.error || 'Failed to analyze image');
      }
    } catch (err) {
      console.error('Analysis error:', err);
      setError('Failed to connect to analysis service. Make sure ML service is running on port 8001.');
    } finally {
      setIsAnalyzing(false);
    }
  };

  const fileToBase64 = (file) => {
    return new Promise((resolve, reject) => {
      const reader = new FileReader();
      reader.onload = () => resolve(reader.result);
      reader.onerror = reject;
      reader.readAsDataURL(file);
    });
  };

  const handleOpenInEditor = () => {
    if (analysisResult && previewImage) {
      // Store the analysis result AND the original image in sessionStorage for the editor
      sessionStorage.setItem('importedDesign', JSON.stringify({
        blueprint: analysisResult.blueprint,
        fabricJson: analysisResult.fabric_json,
        layers: analysisResult.layers,
        colorPalette: analysisResult.color_palette,
        originalImage: previewImage, // Include the original image!
      }));
      navigate('/editor');
    }
  };

  const handleReset = () => {
    setPreviewImage(null);
    setAnalysisResult(null);
    setError(null);
    if (fileInputRef.current) {
      fileInputRef.current.value = '';
    }
  };

  return (
    <div className="analyze-page">
      <div className="analyze-header">
        <h1>
          <span className="header-icon">🔍</span>
          Design Reverse Engineering
        </h1>
        <p>Upload any design or poster to convert it into fully editable layers</p>
      </div>

      <div className="analyze-content">
        {!previewImage ? (
          <div
            className={`upload-zone ${isDragging ? 'dragging' : ''}`}
            onDragOver={handleDragOver}
            onDragLeave={handleDragLeave}
            onDrop={handleDrop}
            onClick={() => fileInputRef.current?.click()}
          >
            <div className="upload-zone-content">
              <div className="upload-icon">
                <UploadIcon />
              </div>
              <h3>Drop your design here</h3>
              <p>or click to browse files</p>
              <span className="file-types">PNG, JPG, WEBP • Max 10MB</span>
            </div>
            <input
              ref={fileInputRef}
              type="file"
              accept="image/*"
              onChange={handleFileSelect}
              style={{ display: 'none' }}
            />
          </div>
        ) : (
          <div className="analysis-container">
            <div className="preview-panel">
              <h4>Original Image</h4>
              <div className="preview-wrapper">
                <img src={previewImage} alt="Uploaded design" />
                {isAnalyzing && (
                  <div className="analyzing-overlay">
                    <div className="analyzing-spinner"></div>
                    <p>Analyzing design...</p>
                    <span>Detecting text, colors, and layout</span>
                  </div>
                )}
              </div>
            </div>

            {analysisResult && (
              <div className="results-panel">
                <h4>Analysis Results</h4>
                
                <div className="stats-grid">
                  <div className="stat-card">
                    <span className="stat-value">{analysisResult.layers?.length || 0}</span>
                    <span className="stat-label">Layers</span>
                  </div>
                  <div className="stat-card">
                    <span className="stat-value">{analysisResult.metadata?.text_regions_detected || 0}</span>
                    <span className="stat-label">Text Regions</span>
                  </div>
                  <div className="stat-card">
                    <span className="stat-value">{analysisResult.color_palette?.length || 0}</span>
                    <span className="stat-label">Colors</span>
                  </div>
                </div>

                {analysisResult.color_palette && (
                  <div className="palette-section">
                    <h5>Detected Colors</h5>
                    <div className="color-swatches">
                      {analysisResult.color_palette.slice(0, 6).map((color, i) => (
                        <div
                          key={i}
                          className="color-swatch"
                          style={{ backgroundColor: color }}
                          title={color}
                        />
                      ))}
                    </div>
                  </div>
                )}

                <div className="layers-section">
                  <h5>Detected Layers</h5>
                  <div className="layers-list">
                    {analysisResult.layers?.map((layer) => (
                      <div key={layer.id} className="layer-row">
                        <span className="layer-icon">
                          {layer.type === 'text' ? '📝' : 
                           layer.type === 'image' ? '🖼️' : 
                           layer.type === 'background' ? '🎨' : '▢'}
                        </span>
                        <span className="layer-content">
                          {layer.type === 'text' 
                            ? `"${layer.content?.substring(0, 40)}${layer.content?.length > 40 ? '...' : ''}"` 
                            : layer.type}
                        </span>
                        <span className={`layer-badge ${layer.role}`}>
                          {layer.role}
                        </span>
                      </div>
                    ))}
                  </div>
                </div>
              </div>
            )}
          </div>
        )}

        {error && (
          <div className="error-banner">
            <span>⚠️</span>
            {error}
          </div>
        )}

        <div className="action-buttons">
          {previewImage && (
            <button className="btn-secondary" onClick={handleReset}>
              Upload Different Image
            </button>
          )}
          {analysisResult && (
            <button className="btn-primary" onClick={handleOpenInEditor}>
              <SparklesIcon />
              Open in Editor
            </button>
          )}
        </div>
      </div>

      <div className="analyze-tips">
        <h4>💡 How to edit your design</h4>
        <ul>
          <li><strong>Edit text:</strong> Click on any text to select, double-click to edit</li>
          <li><strong>Change style:</strong> Use the right panel to change font, color, size</li>
          <li><strong>Delete:</strong> Select any element and press Delete key</li>
          <li><strong>Add new text:</strong> Use "Add Text" button in the left toolbar</li>
          <li><strong>Move elements:</strong> Drag any selected element to reposition</li>
          <li><strong>Resize:</strong> Drag corners of selected element to resize</li>
        </ul>
      </div>
    </div>
  );
};

export default AnalyzePage;
