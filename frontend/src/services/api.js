import axios from 'axios';

const API_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000';

const api = axios.create({
  baseURL: API_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Design APIs
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

// Guidelines APIs
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

// Compliance APIs
export const checkCompliance = async (designId, platform) => {
  const response = await api.post('/api/compliance/check', {
    design_id: designId,
    platform,
  });
  return response.data;
};

export default api;
