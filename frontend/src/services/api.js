import axios from 'axios';

const API_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000';
const ML_API_URL = process.env.REACT_APP_ML_API_URL || 'http://localhost:8001';

const api = axios.create({
  baseURL: API_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

const mlApi = axios.create({
  baseURL: ML_API_URL,
  headers: {
    'Content-Type': 'application/json',
  },
  timeout: 60000, // 60s timeout for AI generation
});

// ===========================================
// AI Design Blueprint Generation APIs
// ===========================================

/**
 * Generate a design blueprint using the local LLM
 * @param {Object} params - Generation parameters
 * @param {string} params.prompt - User's design request
 * @param {string} params.platform - Target platform (meta, google, linkedin, twitter, pinterest, tiktok)
 * @param {string} params.format - Design format (square, story, landscape, portrait)
 * @param {Object} params.brandRules - Brand rules including colors, fonts, logo
 * @returns {Object} Design blueprint with elements, colors, fonts, metadata
 */
export const generateDesignBlueprint = async ({ prompt, platform = 'meta', format = 'square', brandRules = {} }) => {
  try {
    const response = await mlApi.post('/generate', {
      prompt,
      platform,
      format,
      brand_rules: brandRules,
    });
    return response.data;
  } catch (error) {
    console.error('Design generation error:', error);
    throw error;
  }
};

/**
 * Check ML service health
 */
export const checkMLHealth = async () => {
  try {
    const response = await mlApi.get('/health');
    return response.data;
  } catch (error) {
    return { status: 'offline', error: error.message };
  }
};

/**
 * Get ML model info
 */
export const getMLModelInfo = async () => {
  try {
    const response = await mlApi.get('/model-info');
    return response.data;
  } catch (error) {
    return { model: 'unknown', error: error.message };
  }
};

// ===========================================
// Legacy Design APIs (Backend)
// ===========================================

export const generateDesign = async (data) => {
  const response = await api.post('/api/designs/generate', data);
  return response.data;
};

export const getDesigns = async () => {
  const response = await api.get('/api/designs');
  return response.data;
};

export const getDesign = async (id) => {
  const response = await api.get(`/api/designs/${id}`);
  return response.data;
};

export const saveDesign = async (design) => {
  const response = await api.post('/api/designs', design);
  return response.data;
};

export const updateDesign = async (id, design) => {
  const response = await api.put(`/api/designs/${id}`, design);
  return response.data;
};

export const deleteDesign = async (id) => {
  const response = await api.delete(`/api/designs/${id}`);
  return response.data;
};

export const exportDesign = async (id, format) => {
  const response = await api.get(`/api/designs/${id}/export?format=${format}`, {
    responseType: 'blob',
  });
  
  // Create download link
  const url = window.URL.createObjectURL(new Blob([response.data]));
  const link = document.createElement('a');
  link.href = url;
  link.setAttribute('download', `design_${id}.${format}`);
  document.body.appendChild(link);
  link.click();
  link.remove();
  
  return response.data;
};

// ===========================================
// Guidelines APIs
// ===========================================

export const uploadGuideline = async (formData) => {
  const response = await api.post('/api/guidelines/upload', formData, {
    headers: {
      'Content-Type': 'multipart/form-data',
    },
  });
  return response.data;
};

export const getGuidelines = async () => {
  const response = await api.get('/api/guidelines');
  return response.data;
};

export const getGuideline = async (id) => {
  const response = await api.get(`/api/guidelines/${id}`);
  return response.data;
};

// ===========================================
// Compliance APIs
// ===========================================

export const checkCompliance = async (designId, platform) => {
  const response = await api.post('/api/compliance/check', {
    design_id: designId,
    platform,
  });
  return response.data;
};

// ===========================================
// Brand Kit APIs
// ===========================================

export const getBrandKit = async () => {
  const response = await api.get('/api/brand-kit');
  return response.data;
};

export const saveBrandKit = async (brandKit) => {
  const response = await api.post('/api/brand-kit', brandKit);
  return response.data;
};

export const uploadLogo = async (formData) => {
  const response = await api.post('/api/brand-kit/logo', formData, {
    headers: {
      'Content-Type': 'multipart/form-data',
    },
  });
  return response.data;
};

export default api;
