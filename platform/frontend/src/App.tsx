import React, { useState, useEffect } from 'react';
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import { QueryClient, QueryClientProvider } from 'react-query';
import { Toaster } from 'react-hot-toast';
import { motion } from 'framer-motion';

// Components
import Sidebar from './components/Sidebar';
import Dashboard from './pages/Dashboard';
import FileUpload from './pages/FileUpload';
import AnalysisResults from './pages/AnalysisResults';
import ConsciousnessMonitor from './pages/ConsciousnessMonitor';
import AutomationConsole from './pages/AutomationConsole';
import SettingsPage from './pages/SettingsPage';

// Hooks and utilities
import { useApi } from './hooks/useApi';
import './App.css';

// React Query client
const queryClient = new QueryClient({
  defaultOptions: {
    queries: {
      retry: 1,
      refetchOnWindowFocus: false,
    },
  },
});

function App() {
  const [sidebarOpen, setSidebarOpen] = useState(true);
  const [darkMode, setDarkMode] = useState(true);
  const { data: platformStatus } = useApi('/api/status');

  useEffect(() => {
    // Apply dark mode class to document
    if (darkMode) {
      document.documentElement.classList.add('dark');
    } else {
      document.documentElement.classList.remove('dark');
    }
  }, [darkMode]);

  return (
    <QueryClientProvider client={queryClient}>
      <div className={`min-h-screen transition-colors duration-300 ${
        darkMode ? 'bg-gray-900 text-white' : 'bg-gray-50 text-gray-900'
      }`}>
        <Router>
          <div className="flex h-screen overflow-hidden">
            {/* Sidebar */}
            <Sidebar 
              open={sidebarOpen} 
              onClose={() => setSidebarOpen(false)}
              darkMode={darkMode}
              onToggleDarkMode={() => setDarkMode(!darkMode)}
            />
            
            {/* Main Content */}
            <div className="flex-1 flex flex-col overflow-hidden">
              {/* Header */}
              <header className={`shadow-sm border-b transition-colors ${
                darkMode ? 'bg-gray-800 border-gray-700' : 'bg-white border-gray-200'
              }`}>
                <div className="px-4 sm:px-6 lg:px-8">
                  <div className="flex items-center justify-between h-16">
                    {/* Toggle Sidebar */}
                    <button
                      onClick={() => setSidebarOpen(!sidebarOpen)}
                      className="p-2 rounded-md text-gray-400 hover:text-gray-500 hover:bg-gray-100 dark:hover:bg-gray-700 focus:outline-none focus:ring-2 focus:ring-blue-500"
                    >
                      <svg className="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 6h16M4 12h16M4 18h16" />
                      </svg>
                    </button>
                    
                    {/* Platform Title */}
                    <div className="flex items-center space-x-3">
                      <div className="text-2xl">🧠</div>
                      <div>
                        <h1 className="text-xl font-bold text-transparent bg-clip-text bg-gradient-to-r from-blue-500 to-purple-600">
                          Quantum Consciousness Platform
                        </h1>
                        {platformStatus && (
                          <p className="text-sm text-gray-500 dark:text-gray-400">
                            Status: <span className="text-green-500">Active</span> • 
                            Version: {platformStatus.version}
                          </p>
                        )}
                      </div>
                    </div>
                    
                    {/* Status Indicators */}
                    <div className="flex items-center space-x-4">
                      {platformStatus && (
                        <div className="flex space-x-2">
                          <div className="flex items-center space-x-1">
                            <div className="w-2 h-2 bg-green-500 rounded-full animate-pulse"></div>
                            <span className="text-xs text-gray-500 dark:text-gray-400">API</span>
                          </div>
                          <div className="flex items-center space-x-1">
                            <div className="w-2 h-2 bg-green-500 rounded-full animate-pulse"></div>
                            <span className="text-xs text-gray-500 dark:text-gray-400">AI</span>
                          </div>
                          <div className="flex items-center space-x-1">
                            <div className="w-2 h-2 bg-green-500 rounded-full animate-pulse"></div>
                            <span className="text-xs text-gray-500 dark:text-gray-400">Queue</span>
                          </div>
                        </div>
                      )}
                    </div>
                  </div>
                </div>
              </header>
              
              {/* Main Content Area */}
              <main className="flex-1 overflow-auto">
                <motion.div 
                  className="p-6"
                  initial={{ opacity: 0, y: 20 }}
                  animate={{ opacity: 1, y: 0 }}
                  transition={{ duration: 0.5 }}
                >
                  <Routes>
                    <Route path="/" element={<Navigate to="/dashboard" replace />} />
                    <Route path="/dashboard" element={<Dashboard />} />
                    <Route path="/upload" element={<FileUpload />} />
                    <Route path="/results" element={<AnalysisResults />} />
                    <Route path="/consciousness" element={<ConsciousnessMonitor />} />
                    <Route path="/automation" element={<AutomationConsole />} />
                    <Route path="/settings" element={<SettingsPage />} />
                  </Routes>
                </motion.div>
              </main>
            </div>
          </div>
        </Router>
        
        {/* Toast Notifications */}
        <Toaster
          position="top-right"
          toastOptions={{
            duration: 4000,
            style: {
              background: darkMode ? '#374151' : '#fff',
              color: darkMode ? '#fff' : '#000',
            },
            success: {
              iconTheme: {
                primary: '#10B981',
                secondary: '#fff',
              },
            },
            error: {
              iconTheme: {
                primary: '#EF4444',
                secondary: '#fff',
              },
            },
          }}
        />
      </div>
    </QueryClientProvider>
  );
}

export default App;