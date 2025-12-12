import React, { useState } from 'react';
import { useQuery } from 'react-query';
import { getDesigns } from '../services/api';
import Editor from '../components/Editor';

/**
 * EditorPage - Integrates the Editor component with design selection
 * 
 * This page shows how to use the Editor component:
 * 1. List designs
 * 2. Click to open in editor
 * 3. Editor handles all editing, autosave, compliance
 */
const EditorPage = () => {
  const [editingDesignId, setEditingDesignId] = useState(null);
  const { data: designs } = useQuery('designs', getDesigns);

  // If a design is being edited, show the full-screen editor
  if (editingDesignId) {
    return (
      <Editor
        designId={editingDesignId}
        onClose={() => setEditingDesignId(null)}
      />
    );
  }

  // Otherwise, show the design list
  return (
    <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
      <div className="flex justify-between items-center mb-8">
        <h1 className="text-3xl font-bold text-gray-900">Advanced Editor</h1>
        <p className="text-sm text-gray-500">
          Select a design to edit with full canvas controls
        </p>
      </div>

      <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-6">
        {designs?.length > 0 ? (
          designs.map((design) => (
            <div
              key={design.id}
              className="bg-white rounded-lg shadow hover:shadow-lg transition cursor-pointer"
              onClick={() => setEditingDesignId(design.id)}
            >
              <div className="aspect-square bg-gray-100 rounded-t-lg flex items-center justify-center">
                <p className="text-gray-400">Design Preview</p>
              </div>
              <div className="p-4">
                <h3 className="font-semibold text-lg mb-2 truncate">{design.prompt}</h3>
                <div className="flex justify-between items-center text-sm text-gray-500">
                  <span>{design.platform}</span>
                  <span>{design.format}</span>
                </div>
                <button
                  onClick={(e) => {
                    e.stopPropagation();
                    setEditingDesignId(design.id);
                  }}
                  className="mt-3 w-full bg-primary-600 text-white px-4 py-2 rounded hover:bg-primary-700 font-medium"
                >
                  Edit in Advanced Editor
                </button>
              </div>
            </div>
          ))
        ) : (
          <div className="col-span-full text-center py-12">
            <p className="text-gray-500">
              No designs available. Create some designs first.
            </p>
          </div>
        )}
      </div>

      {/* Feature List */}
      <div className="mt-12 bg-blue-50 rounded-lg p-6">
        <h2 className="text-xl font-semibold mb-4">Advanced Editor Features</h2>
        <div className="grid md:grid-cols-2 gap-4">
          <div>
            <h3 className="font-medium mb-2">✏️ Editing</h3>
            <ul className="text-sm text-gray-700 space-y-1">
              <li>• Add text, shapes, and images</li>
              <li>• Move, resize, rotate elements</li>
              <li>• Full properties panel</li>
              <li>• Delete with keyboard shortcuts</li>
            </ul>
          </div>
          <div>
            <h3 className="font-medium mb-2">💾 Auto-Save</h3>
            <ul className="text-sm text-gray-700 space-y-1">
              <li>• Automatic saving (1s delay)</li>
              <li>• Save status indicator</li>
              <li>• Manual save: Ctrl+S</li>
              <li>• Version tracking</li>
            </ul>
          </div>
          <div>
            <h3 className="font-medium mb-2">↩️ History</h3>
            <ul className="text-sm text-gray-700 space-y-1">
              <li>• Full undo/redo support</li>
              <li>• Ctrl+Z to undo</li>
              <li>• Ctrl+Shift+Z to redo</li>
              <li>• Rollback to any version</li>
            </ul>
          </div>
          <div>
            <h3 className="font-medium mb-2">✅ Compliance</h3>
            <ul className="text-sm text-gray-700 space-y-1">
              <li>• Real-time validation</li>
              <li>• Platform-specific rules</li>
              <li>• Visual compliance badge</li>
              <li>• Suggested fixes</li>
            </ul>
          </div>
        </div>
      </div>
    </div>
  );
};

export default EditorPage;
