import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import HomePage from './pages/HomePage';
import DesignStudioPage from './pages/DesignStudioPage';
import GuidelinesPage from './pages/GuidelinesPage';
import ExportPage from './pages/ExportPage';
import Navbar from './components/Navbar';

function App() {
  return (
    <Router>
      <div className="min-h-screen bg-gray-50">
        <Navbar />
        <Routes>
          <Route path="/" element={<HomePage />} />
          <Route path="/studio" element={<DesignStudioPage />} />
          <Route path="/guidelines" element={<GuidelinesPage />} />
          <Route path="/export" element={<ExportPage />} />
        </Routes>
      </div>
    </Router>
  );
}

export default App;
