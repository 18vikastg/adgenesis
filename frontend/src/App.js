/**
 * AdGenesis - Premium AI Design Platform
 * Canva-inspired SaaS Application
 * Developed by Vikas TG
 */

import React from 'react';
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import { QueryClient, QueryClientProvider } from 'react-query';
import './styles/design-system.css';
import './index.css';

// Layouts
import DashboardLayout from './layouts/DashboardLayout';

// Pages
import LandingPage from './pages/LandingPage';
import AboutPage from './pages/AboutPage';
import Dashboard from './pages/Dashboard';
import Editor from './pages/Editor';
import Templates from './pages/Templates';
import Projects from './pages/Projects';
import BrandKit from './pages/BrandKit';
import AnalyzePage from './pages/AnalyzePage';

// Create React Query client
const queryClient = new QueryClient({
  defaultOptions: {
    queries: {
      refetchOnWindowFocus: false,
      retry: 1,
      staleTime: 5 * 60 * 1000,
    },
  },
});

function App() {
  return (
    <QueryClientProvider client={queryClient}>
      <Router>
        <Routes>
          {/* Public Pages */}
          <Route path="/" element={<LandingPage />} />
          <Route path="/about" element={<AboutPage />} />
          
          {/* Dashboard routes */}
          <Route path="/dashboard" element={<DashboardLayout />}>
            <Route index element={<Dashboard />} />
            <Route path="templates" element={<Templates />} />
            <Route path="projects" element={<Projects />} />
            <Route path="brand-kit" element={<BrandKit />} />
            <Route path="analyze" element={<AnalyzePage />} />
          </Route>
          
          {/* Editor - Full screen */}
          <Route path="/editor" element={<Editor />} />
          <Route path="/editor/:projectId" element={<Editor />} />
          
          {/* Fallback */}
          <Route path="*" element={<Navigate to="/" replace />} />
        </Routes>
      </Router>
    </QueryClientProvider>
  );
}

export default App;
