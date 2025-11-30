import React, { useState } from 'react';
import { useQuery, useMutation } from 'react-query';
import { generateDesign, getDesigns } from '../services/api';

const DesignStudioPage = () => {
  const [prompt, setPrompt] = useState('');
  const [platform, setPlatform] = useState('meta');
  const [format, setFormat] = useState('square');

  const { data: designs, refetch } = useQuery('designs', getDesigns);

  const generateMutation = useMutation(generateDesign, {
    onSuccess: () => {
      refetch();
      setPrompt('');
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

  return (
    <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
      <h1 className="text-3xl font-bold text-gray-900 mb-8">Design Studio</h1>

      <div className="grid lg:grid-cols-2 gap-8">
        {/* Left Panel - Controls */}
        <div className="space-y-6">
          <div className="bg-white p-6 rounded-lg shadow">
            <h2 className="text-xl font-semibold mb-4">Generate New Design</h2>

            <div className="space-y-4">
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  Describe your ad
                </label>
                <textarea
                  className="w-full px-3 py-2 border border-gray-300 rounded-md focus:ring-primary-500 focus:border-primary-500"
                  rows="4"
                  placeholder="E.g., Create a summer sale ad with beach theme, 50% off text, and call-to-action button"
                  value={prompt}
                  onChange={(e) => setPrompt(e.target.value)}
                />
              </div>

              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  Platform
                </label>
                <select
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
          </div>
        </div>

        {/* Right Panel - Canvas Preview */}
        <div className="bg-white p-6 rounded-lg shadow">
          <h2 className="text-xl font-semibold mb-4">Preview</h2>
          <div className="aspect-square bg-gray-100 rounded-lg flex items-center justify-center">
            <p className="text-gray-400">Canvas preview will appear here</p>
          </div>
          <div className="mt-4 flex space-x-2">
            <button className="flex-1 bg-gray-200 text-gray-700 px-4 py-2 rounded hover:bg-gray-300">
              Edit
            </button>
            <button className="flex-1 bg-primary-600 text-white px-4 py-2 rounded hover:bg-primary-700">
              Export
            </button>
          </div>
        </div>
      </div>
    </div>
  );
};

export default DesignStudioPage;
