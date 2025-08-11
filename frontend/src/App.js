import React from 'react';
import { BrowserRouter as Router, Routes, Route, useNavigate } from 'react-router-dom';
import HealthForm from './pages/HealthForm';

function Dashboard() {
  const navigate = useNavigate();
  return (
    <div className="min-h-screen bg-gray-50">
      <nav className="bg-white shadow-lg">
        <div className="max-w-7xl mx-auto px-4">
          <div className="flex justify-between h-16">
            <div className="flex items-center">
              <h1 className="text-2xl font-bold text-blue-600">DiaLens Risk Intelligence</h1>
            </div>
          </div>
        </div>
      </nav>
      <div className="max-w-7xl mx-auto py-6 px-4">
        <div className="mb-8">
          <h1 className="text-3xl font-bold text-gray-900">Health Dashboard</h1>
          <p className="text-gray-600">Monitor your health metrics and risk factors</p>
        </div>
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-8">
          <div className="bg-green-100 text-green-800 border-green-200 border rounded-lg p-6">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-sm font-medium opacity-75">Diabetes Risk</p>
                <p className="text-2xl font-bold">Low</p>
                <p className="text-sm opacity-75">15%</p>
              </div>
            </div>
          </div>
          <div className="bg-yellow-100 text-yellow-800 border-yellow-200 border rounded-lg p-6">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-sm font-medium opacity-75">Heart Disease Risk</p>
                <p className="text-2xl font-bold">Medium</p>
                <p className="text-sm opacity-75">35%</p>
              </div>
            </div>
          </div>
          <div className="bg-blue-100 text-blue-800 border-blue-200 border rounded-lg p-6">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-sm font-medium opacity-75">BMI Status</p>
                <p className="text-2xl font-bold">Normal</p>
                <p className="text-sm opacity-75">23.5</p>
              </div>
            </div>
          </div>
        </div>
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          <div className="bg-white rounded-lg shadow p-6">
            <h3 className="text-lg font-semibold mb-4">Quick Health Check</h3>
            <button
              className="w-full bg-blue-600 text-white py-2 px-4 rounded hover:bg-blue-700"
              onClick={() => navigate('/assessment')}
            >
              Start Risk Assessment
            </button>
          </div>
          <div className="bg-white rounded-lg shadow p-6">
            <h3 className="text-lg font-semibold mb-4">AI Health Chat</h3>
            <button className="w-full bg-green-500 text-white py-2 px-4 rounded hover:bg-green-600">
              Ask Health Question
            </button>
          </div>
        </div>
      </div>
    </div>
  );
}

function App() {
  return (
    <Router>
      <Routes>
        <Route path="/" element={<Dashboard />} />
        <Route path="/assessment" element={<HealthForm />} />
      </Routes>
    </Router>
  );
}

export default App;