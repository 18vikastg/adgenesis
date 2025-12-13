/**
 * Projects Page - User's saved designs with localStorage
 */

import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import './Projects.css';

const ImageIcon = () => (
  <svg width="48" height="48" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
    <rect x="3" y="3" width="18" height="18" rx="2" />
    <circle cx="8.5" cy="8.5" r="1.5" />
    <path d="M21 15l-5-5L5 21" />
  </svg>
);

const PlusIcon = () => (
  <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
    <line x1="12" y1="5" x2="12" y2="19" />
    <line x1="5" y1="12" x2="19" y2="12" />
  </svg>
);

const DeleteIcon = () => (
  <svg width="18" height="18" viewBox="0 0 18 18" fill="none" stroke="currentColor" strokeWidth="2">
    <path d="M3 5h12M6 5V3a1 1 0 011-1h4a1 1 0 011 1v2" />
    <path d="M14 5v10a1 1 0 01-1 1H5a1 1 0 01-1-1V5" />
  </svg>
);

const DuplicateIcon = () => (
  <svg width="18" height="18" viewBox="0 0 18 18" fill="none" stroke="currentColor" strokeWidth="2">
    <rect x="6" y="6" width="10" height="10" rx="1" />
    <path d="M4 12H3a1 1 0 01-1-1V3a1 1 0 011-1h8a1 1 0 011 1v1" />
  </svg>
);

const FolderIcon = () => (
  <svg width="20" height="20" viewBox="0 0 20 20" fill="none" stroke="currentColor" strokeWidth="2">
    <path d="M2 5a2 2 0 012-2h4l2 2h6a2 2 0 012 2v8a2 2 0 01-2 2H4a2 2 0 01-2-2V5z" />
  </svg>
);

const GridIcon = () => (
  <svg width="20" height="20" viewBox="0 0 20 20" fill="none" stroke="currentColor" strokeWidth="2">
    <rect x="3" y="3" width="6" height="6" rx="1" />
    <rect x="11" y="3" width="6" height="6" rx="1" />
    <rect x="3" y="11" width="6" height="6" rx="1" />
    <rect x="11" y="11" width="6" height="6" rx="1" />
  </svg>
);

const ListIcon = () => (
  <svg width="20" height="20" viewBox="0 0 20 20" fill="none" stroke="currentColor" strokeWidth="2">
    <line x1="4" y1="6" x2="16" y2="6" />
    <line x1="4" y1="10" x2="16" y2="10" />
    <line x1="4" y1="14" x2="16" y2="14" />
  </svg>
);

// localStorage keys
const PROJECTS_KEY = 'adgenesis_projects';

// Get projects from localStorage
const getLocalProjects = () => {
  try {
    const projects = localStorage.getItem(PROJECTS_KEY);
    return projects ? JSON.parse(projects) : [];
  } catch {
    return [];
  }
};

// Save projects to localStorage
const saveLocalProjects = (projects) => {
  localStorage.setItem(PROJECTS_KEY, JSON.stringify(projects));
};

const Projects = () => {
  const navigate = useNavigate();
  const [projects, setProjects] = useState([]);
  const [isLoading, setIsLoading] = useState(true);
  const [viewMode, setViewMode] = useState('grid');
  const [searchQuery, setSearchQuery] = useState('');
  const [sortBy, setSortBy] = useState('recent');

  // Load projects on mount
  useEffect(() => {
    setIsLoading(true);
    setTimeout(() => {
      const localProjects = getLocalProjects();
      setProjects(localProjects);
      setIsLoading(false);
    }, 300);
  }, []);

  // Filter and sort projects
  const filteredProjects = projects
    .filter(p => 
      p.name?.toLowerCase().includes(searchQuery.toLowerCase()) ||
      p.prompt?.toLowerCase().includes(searchQuery.toLowerCase())
    )
    .sort((a, b) => {
      if (sortBy === 'recent') {
        return new Date(b.updatedAt) - new Date(a.updatedAt);
      } else if (sortBy === 'name') {
        return (a.name || '').localeCompare(b.name || '');
      } else if (sortBy === 'oldest') {
        return new Date(a.createdAt) - new Date(b.createdAt);
      }
      return 0;
    });

  const handleOpenDesign = (projectId) => {
    const project = projects.find(p => p.id === projectId);
    if (project) {
      navigate('/editor', { 
        state: { 
          projectId: project.id,
          name: project.name,
          width: project.width || 1080,
          height: project.height || 1080,
          canvasData: project.canvasData,
        } 
      });
    }
  };

  const handleDeleteProject = (e, projectId) => {
    e.stopPropagation();
    if (window.confirm('Are you sure you want to delete this project?')) {
      const updated = projects.filter(p => p.id !== projectId);
      setProjects(updated);
      saveLocalProjects(updated);
    }
  };

  const handleDuplicateProject = (e, projectId) => {
    e.stopPropagation();
    const project = projects.find(p => p.id === projectId);
    if (project) {
      const duplicated = {
        ...project,
        id: `project-${Date.now()}`,
        name: `${project.name} (Copy)`,
        createdAt: new Date().toISOString(),
        updatedAt: new Date().toISOString(),
      };
      const updated = [duplicated, ...projects];
      setProjects(updated);
      saveLocalProjects(updated);
    }
  };

  const handleCreateNew = () => {
    navigate('/editor');
  };

  const formatDate = (dateStr) => {
    const date = new Date(dateStr);
    const now = new Date();
    const diff = now - date;
    
    if (diff < 60000) return 'Just now';
    if (diff < 3600000) return `${Math.floor(diff / 60000)} min ago`;
    if (diff < 86400000) return `${Math.floor(diff / 3600000)} hours ago`;
    if (diff < 604800000) return `${Math.floor(diff / 86400000)} days ago`;
    return date.toLocaleDateString();
  };

  return (
    <div className="projects-page">
      <div className="projects-header">
        <div className="header-content">
          <h1>Your Projects</h1>
          <p>All your designs in one place</p>
        </div>
        <button className="create-new-btn" onClick={handleCreateNew}>
          <PlusIcon />
          <span>Create New</span>
        </button>
      </div>

      {/* Toolbar */}
      <div className="projects-toolbar">
        <div className="search-box">
          <input 
            type="text"
            placeholder="Search projects..."
            value={searchQuery}
            onChange={(e) => setSearchQuery(e.target.value)}
          />
        </div>
        
        <div className="toolbar-right">
          <select 
            className="sort-select"
            value={sortBy}
            onChange={(e) => setSortBy(e.target.value)}
          >
            <option value="recent">Most Recent</option>
            <option value="oldest">Oldest First</option>
            <option value="name">Name A-Z</option>
          </select>
          
          <div className="view-toggle">
            <button 
              className={viewMode === 'grid' ? 'active' : ''}
              onClick={() => setViewMode('grid')}
              title="Grid view"
            >
              <GridIcon />
            </button>
            <button 
              className={viewMode === 'list' ? 'active' : ''}
              onClick={() => setViewMode('list')}
              title="List view"
            >
              <ListIcon />
            </button>
          </div>
        </div>
      </div>

      {/* Projects Count */}
      <div className="projects-count">
        {filteredProjects.length} {filteredProjects.length === 1 ? 'project' : 'projects'}
      </div>

      {/* Projects Grid/List */}
      <div className={`projects-container ${viewMode}`}>
        {isLoading ? (
          Array.from({ length: 6 }).map((_, i) => (
            <div key={i} className="project-card skeleton">
              <div className="project-thumbnail skeleton" />
              <div className="project-info">
                <div className="skeleton" style={{ width: '60%', height: '16px' }} />
                <div className="skeleton" style={{ width: '40%', height: '12px', marginTop: '8px' }} />
              </div>
            </div>
          ))
        ) : filteredProjects.length > 0 ? (
          filteredProjects.map((project) => (
            <div
              key={project.id}
              className="project-card"
              onClick={() => handleOpenDesign(project.id)}
            >
              <div className="project-thumbnail">
                {project.thumbnail ? (
                  <img src={project.thumbnail} alt={project.name} />
                ) : (
                  <div className="project-placeholder">
                    <ImageIcon />
                  </div>
                )}
                <div className="project-actions">
                  <button 
                    className="project-action-btn"
                    onClick={(e) => handleDuplicateProject(e, project.id)}
                    title="Duplicate"
                  >
                    <DuplicateIcon />
                  </button>
                  <button 
                    className="project-action-btn delete"
                    onClick={(e) => handleDeleteProject(e, project.id)}
                    title="Delete"
                  >
                    <DeleteIcon />
                  </button>
                </div>
              </div>
              <div className="project-info">
                <h3>{project.name || 'Untitled Design'}</h3>
                <div className="project-meta">
                  <span className="project-size">{project.width} × {project.height}</span>
                  <span className="project-date">{formatDate(project.updatedAt)}</span>
                </div>
              </div>
            </div>
          ))
        ) : (
          <div className="empty-state">
            <div className="empty-icon">
              <FolderIcon />
            </div>
            <h3>No projects yet</h3>
            <p>Create your first design to get started</p>
            <button className="empty-cta" onClick={handleCreateNew}>
              <PlusIcon />
              Create New Design
            </button>
          </div>
        )}
      </div>
    </div>
  );
};

export default Projects;
