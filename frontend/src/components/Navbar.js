import React from 'react';
import { Link } from 'react-router-dom';

const Navbar = () => {
  return (
    <nav className="bg-white shadow-lg">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex justify-between h-16">
          <div className="flex items-center">
            <Link to="/" className="flex items-center">
              <span className="text-2xl font-bold text-primary-600">ADGENESIS</span>
            </Link>
            <div className="hidden md:ml-10 md:flex md:space-x-8">
              <Link
                to="/studio"
                className="text-gray-700 hover:text-primary-600 px-3 py-2 rounded-md text-sm font-medium"
              >
                Design Studio
              </Link>
              <Link
                to="/guidelines"
                className="text-gray-700 hover:text-primary-600 px-3 py-2 rounded-md text-sm font-medium"
              >
                Brand Guidelines
              </Link>
              <Link
                to="/export"
                className="text-gray-700 hover:text-primary-600 px-3 py-2 rounded-md text-sm font-medium"
              >
                Export
              </Link>
            </div>
          </div>
          <div className="flex items-center">
            <button className="bg-primary-600 text-white px-4 py-2 rounded-md text-sm font-medium hover:bg-primary-700">
              Demo User
            </button>
          </div>
        </div>
      </div>
    </nav>
  );
};

export default Navbar;
