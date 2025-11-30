import React from 'react';
import { Link } from 'react-router-dom';

const HomePage = () => {
  return (
    <div className="min-h-screen bg-gradient-to-b from-primary-50 to-white">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-20">
        <div className="text-center">
          <h1 className="text-5xl font-extrabold text-gray-900 mb-6">
            AI-Powered Ad Design
            <span className="text-primary-600"> in Seconds</span>
          </h1>
          <p className="text-xl text-gray-600 mb-8 max-w-3xl mx-auto">
            Upload your brand guidelines, describe your ad concept, and let AI generate
            platform-compliant designs for Meta, Google, and LinkedIn.
          </p>
          <div className="flex justify-center space-x-4">
            <Link
              to="/studio"
              className="bg-primary-600 text-white px-8 py-3 rounded-lg text-lg font-semibold hover:bg-primary-700 transition"
            >
              Start Creating
            </Link>
            <Link
              to="/guidelines"
              className="bg-white text-primary-600 border-2 border-primary-600 px-8 py-3 rounded-lg text-lg font-semibold hover:bg-primary-50 transition"
            >
              Upload Guidelines
            </Link>
          </div>
        </div>

        <div className="mt-20 grid md:grid-cols-3 gap-8">
          <div className="bg-white p-6 rounded-lg shadow-lg">
            <div className="text-primary-600 text-3xl mb-4">🎨</div>
            <h3 className="text-xl font-bold mb-2">AI Generation</h3>
            <p className="text-gray-600">
              Generate professional ad designs from simple text prompts using advanced AI.
            </p>
          </div>
          <div className="bg-white p-6 rounded-lg shadow-lg">
            <div className="text-primary-600 text-3xl mb-4">✅</div>
            <h3 className="text-xl font-bold mb-2">Platform Compliance</h3>
            <p className="text-gray-600">
              Automatically check designs against Meta, Google, and LinkedIn requirements.
            </p>
          </div>
          <div className="bg-white p-6 rounded-lg shadow-lg">
            <div className="text-primary-600 text-3xl mb-4">📦</div>
            <h3 className="text-xl font-bold mb-2">Batch Export</h3>
            <p className="text-gray-600">
              Export designs in multiple formats (PNG, JPG, SVG, PDF) with one click.
            </p>
          </div>
        </div>
      </div>
    </div>
  );
};

export default HomePage;
