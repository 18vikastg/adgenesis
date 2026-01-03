/**
 * ImageUploader Component
 * Upload and analyze images to convert them into editable designs
 * 
 * Part of the Design Reverse-Engineering Engine
 */

import React, { useState, useCallback, useRef } from 'react';
import './ImageUploader.css';

const API_BASE = process.env.REACT_APP_ML_SERVICE_URL || 'http://localhost:8001';

const ImageUploader = ({ onDesignExtracted, onClose }) => {
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
  }, []);

  const handleFileSelect = useCallback((e) => {
    const files = e.target.files;
    if (files.length > 0) {
      processFile(files[0]);
    }
  }, []);

  const processFile = async (file) => {
    // Validate file type
    if (!file.type.startsWith('image/')) {
      setError('Please upload an image file (PNG, JPG, WEBP)');
      return;
    }

    // Validate file size (max 10MB)
    if (file.size > 10 * 1024 * 1024) {
      setError('File size must be less than 10MB');
      return;
    }

    setError(null);

    // Create preview
    const reader = new FileReader();
    reader.onload = (e) => {
      setPreviewImage(e.target.result);
    };
    reader.readAsDataURL(file);

    // Analyze image
    await analyzeImage(file);
  };

  const analyzeImage = async (file) => {
    setIsAnalyzing(true);
    setError(null);

    try {
      // Convert to base64
      const base64 = await fileToBase64(file);

      // Call the analyze-image endpoint
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
        console.log('Analysis result:', result);
      } else {
        setError(result.error || 'Failed to analyze image');
      }
    } catch (err) {
      console.error('Analysis error:', err);
      setError('Failed to connect to analysis service. Make sure ML service is running.');
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

  const handleUseDesign = () => {
    if (analysisResult && onDesignExtracted) {
      onDesignExtracted({
        blueprint: analysisResult.blueprint,
        fabricJson: analysisResult.fabric_json,
        layers: analysisResult.layers,
        colorPalette: analysisResult.color_palette,
      });
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
    <div className="image-uploader-overlay">
      <div className="image-uploader-modal">
        <div className="image-uploader-header">
          <h2>🔍 Design Reverse Engineering</h2>
          <p className="subtitle">
            Upload an image to convert it into editable layers
          </p>
          <button className="close-button" onClick={onClose}>
            ✕
          </button>
        </div>

        <div className="image-uploader-content">
          {!previewImage ? (
            <div
              className={`drop-zone ${isDragging ? 'dragging' : ''}`}
              onDragOver={handleDragOver}
              onDragLeave={handleDragLeave}
              onDrop={handleDrop}
              onClick={() => fileInputRef.current?.click()}
            >
              <div className="drop-zone-content">
                <div className="drop-icon">📁</div>
                <h3>Drop your design here</h3>
                <p>or click to browse files</p>
                <span className="file-types">PNG, JPG, WEBP (max 10MB)</span>
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
            <div className="preview-container">
              <div className="preview-section">
                <h4>Original Image</h4>
                <div className="preview-image-wrapper">
                  <img src={previewImage} alt="Uploaded design" />
                </div>
              </div>

              {isAnalyzing && (
                <div className="analyzing-overlay">
                  <div className="analyzing-spinner"></div>
                  <p>Analyzing design...</p>
                  <span className="analyzing-sub">
                    Detecting text, colors, and layout
                  </span>
                </div>
              )}

              {analysisResult && (
                <div className="analysis-section">
                  <h4>Analysis Result</h4>
                  
                  <div className="analysis-stats">
                    <div className="stat">
                      <span className="stat-value">{analysisResult.layers?.length || 0}</span>
                      <span className="stat-label">Layers</span>
                    </div>
                    <div className="stat">
                      <span className="stat-value">
                        {analysisResult.metadata?.text_regions_detected || 0}
                      </span>
                      <span className="stat-label">Text Regions</span>
                    </div>
                    <div className="stat">
                      <span className="stat-value">
                        {analysisResult.color_palette?.length || 0}
                      </span>
                      <span className="stat-label">Colors</span>
                    </div>
                  </div>

                  {/* Color Palette */}
                  {analysisResult.color_palette && (
                    <div className="color-palette">
                      <h5>Detected Colors</h5>
                      <div className="colors">
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

                  {/* Layers Preview */}
                  <div className="layers-preview">
                    <h5>Detected Layers</h5>
                    <div className="layers-list">
                      {analysisResult.layers?.map((layer) => (
                        <div key={layer.id} className="layer-item">
                          <span className="layer-icon">
                            {layer.type === 'text' ? '📝' : 
                             layer.type === 'image' ? '🖼️' : 
                             layer.type === 'background' ? '🎨' : '▢'}
                          </span>
                          <span className="layer-name">
                            {layer.type === 'text' 
                              ? `"${layer.content?.substring(0, 30)}${layer.content?.length > 30 ? '...' : ''}"` 
                              : layer.type}
                          </span>
                          <span className={`layer-role ${layer.role}`}>
                            {layer.role}
                          </span>
                          {layer.confidence && layer.confidence < 1 && (
                            <span className="confidence-badge">
                              {Math.round(layer.confidence * 100)}%
                            </span>
                          )}
                        </div>
                      ))}
                    </div>
                  </div>
                </div>
              )}
            </div>
          )}

          {error && (
            <div className="error-message">
              <span className="error-icon">⚠️</span>
              {error}
            </div>
          )}
        </div>

        <div className="image-uploader-actions">
          {previewImage && (
            <>
              <button className="btn-secondary" onClick={handleReset}>
                Upload Different Image
              </button>
              {analysisResult && (
                <button className="btn-primary" onClick={handleUseDesign}>
                  ✨ Open in Editor
                </button>
              )}
            </>
          )}
          {!previewImage && (
            <button className="btn-secondary" onClick={onClose}>
              Cancel
            </button>
          )}
        </div>
      </div>
    </div>
  );
};

export default ImageUploader;
