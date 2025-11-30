import React, { useCallback, useState } from 'react';
import { useDropzone } from 'react-dropzone';
import { useMutation, useQuery } from 'react-query';
import { uploadGuideline, getGuidelines } from '../services/api';

const GuidelinesPage = () => {
  const [uploadStatus, setUploadStatus] = useState('');

  const { data: guidelines, refetch } = useQuery('guidelines', getGuidelines);

  const uploadMutation = useMutation(uploadGuideline, {
    onSuccess: () => {
      setUploadStatus('Upload successful! Processing guidelines...');
      refetch();
      setTimeout(() => setUploadStatus(''), 3000);
    },
    onError: (error) => {
      setUploadStatus(`Error: ${error.message}`);
      setTimeout(() => setUploadStatus(''), 3000);
    },
  });

  const onDrop = useCallback((acceptedFiles) => {
    if (acceptedFiles.length > 0) {
      const file = acceptedFiles[0];
      const formData = new FormData();
      formData.append('file', file);
      uploadMutation.mutate(formData);
    }
  }, [uploadMutation]);

  const { getRootProps, getInputProps, isDragActive } = useDropzone({
    onDrop,
    accept: {
      'application/pdf': ['.pdf'],
      'image/*': ['.png', '.jpg', '.jpeg'],
    },
    maxFiles: 1,
  });

  return (
    <div className="max-w-5xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
      <h1 className="text-3xl font-bold text-gray-900 mb-8">Brand Guidelines</h1>

      {/* Upload Section */}
      <div className="bg-white p-8 rounded-lg shadow mb-8">
        <h2 className="text-xl font-semibold mb-4">Upload Brand Guidelines</h2>
        <div
          {...getRootProps()}
          className={`border-2 border-dashed rounded-lg p-12 text-center cursor-pointer transition ${
            isDragActive
              ? 'border-primary-600 bg-primary-50'
              : 'border-gray-300 hover:border-primary-400'
          }`}
        >
          <input {...getInputProps()} />
          <div className="text-gray-600">
            <svg
              className="mx-auto h-12 w-12 text-gray-400 mb-4"
              stroke="currentColor"
              fill="none"
              viewBox="0 0 48 48"
            >
              <path
                d="M28 8H12a4 4 0 00-4 4v20m32-12v8m0 0v8a4 4 0 01-4 4H12a4 4 0 01-4-4v-4m32-4l-3.172-3.172a4 4 0 00-5.656 0L28 28M8 32l9.172-9.172a4 4 0 015.656 0L28 28m0 0l4 4m4-24h8m-4-4v8m-12 4h.02"
                strokeWidth="2"
                strokeLinecap="round"
                strokeLinejoin="round"
              />
            </svg>
            {isDragActive ? (
              <p className="text-lg">Drop the file here...</p>
            ) : (
              <div>
                <p className="text-lg mb-2">
                  Drag & drop your brand guidelines PDF, or click to select
                </p>
                <p className="text-sm text-gray-500">
                  Supports PDF, PNG, JPG (max 10MB)
                </p>
              </div>
            )}
          </div>
        </div>
        {uploadStatus && (
          <div className="mt-4 p-3 rounded bg-primary-100 text-primary-800">
            {uploadStatus}
          </div>
        )}
      </div>

      {/* Extracted Guidelines */}
      <div className="bg-white p-8 rounded-lg shadow">
        <h2 className="text-xl font-semibold mb-4">Extracted Guidelines</h2>
        {guidelines?.length > 0 ? (
          <div className="space-y-4">
            {guidelines.map((guideline) => (
              <div key={guideline.id} className="border border-gray-200 rounded-lg p-4">
                <div className="flex justify-between items-start mb-2">
                  <h3 className="font-medium text-lg">{guideline.name}</h3>
                  <span className="text-xs text-gray-500">
                    {new Date(guideline.created_at).toLocaleDateString()}
                  </span>
                </div>
                <div className="grid grid-cols-2 gap-4 mt-4">
                  <div>
                    <p className="text-sm font-medium text-gray-700 mb-2">Colors</p>
                    <div className="flex space-x-2">
                      {guideline.colors?.slice(0, 5).map((color, idx) => (
                        <div
                          key={idx}
                          className="w-8 h-8 rounded border border-gray-300"
                          style={{ backgroundColor: color }}
                          title={color}
                        />
                      ))}
                    </div>
                  </div>
                  <div>
                    <p className="text-sm font-medium text-gray-700 mb-2">Fonts</p>
                    <div className="text-sm text-gray-600">
                      {guideline.fonts?.join(', ') || 'None extracted'}
                    </div>
                  </div>
                </div>
              </div>
            ))}
          </div>
        ) : (
          <p className="text-gray-500">
            No guidelines uploaded yet. Upload your brand guidelines to get started.
          </p>
        )}
      </div>
    </div>
  );
};

export default GuidelinesPage;
