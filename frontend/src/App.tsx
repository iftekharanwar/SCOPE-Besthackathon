import React from 'react';
import { Routes, Route, Link } from 'react-router-dom';
import { ClipboardList, BarChart3 } from 'lucide-react';
import ClaimSubmissionPage from './pages/ClaimSubmissionPage';
import AdjusterDashboardPage from './pages/AdjusterDashboardPage';

const App: React.FC = () => {
  return (
    <div className="min-h-screen bg-gray-50">
      <header className="bg-blue-700 text-white shadow-md">
        <div className="container mx-auto px-4 py-4">
          <div className="flex justify-between items-center">
            <h1 className="text-2xl font-bold">Smart Insurance Claim Routing Assistant</h1>
            <nav className="flex space-x-4">
              <Link 
                to="/" 
                className="flex items-center space-x-1 px-3 py-2 rounded hover:bg-blue-600 transition-colors"
              >
                <ClipboardList size={18} />
                <span>Submit Claim</span>
              </Link>
              <Link 
                to="/dashboard" 
                className="flex items-center space-x-1 px-3 py-2 rounded hover:bg-blue-600 transition-colors"
              >
                <BarChart3 size={18} />
                <span>Adjuster Dashboard</span>
              </Link>
            </nav>
          </div>
        </div>
      </header>
      
      <main className="container mx-auto px-4 py-8">
        <Routes>
          <Route path="/" element={<ClaimSubmissionPage />} />
          <Route path="/dashboard" element={<AdjusterDashboardPage />} />
        </Routes>
      </main>
      
      <footer className="bg-gray-100 border-t mt-auto">
        <div className="container mx-auto px-4 py-6">
          <p className="text-center text-gray-600">
            &copy; 2025 Smart Claims Optimization and Prioritization Engine - Prototype for BEST Hackathon
          </p>
        </div>
      </footer>
    </div>
  );
};

export default App;
