import React, { useState, useEffect } from 'react';
import axios from 'axios';
import './App.css';
import TaskManager from './components/TaskManager';
import RecommendationEngine from './components/RecommendationEngine';
import ABComparison from './components/ABComparison';

const API_BASE = process.env.REACT_APP_API_URL || 'http://localhost:5000';

function App() {
  const [activeTab, setActiveTab] = useState('tasks');
  const [pets, setPets] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    // Fetch pets on load
    axios.get(`${API_BASE}/api/pets`)
      .then(res => setPets(res.data.pets))
      .catch(err => console.error('Error loading pets:', err))
      .finally(() => setLoading(false));
  }, []);

  return (
    <div className="app">
      <header className="header">
        <h1>🐾 PawPal+ AI System</h1>
        <p>Schedule tasks • Get recommendations • Compare AI modes</p>
      </header>

      <nav className="nav">
        <button
          className={`nav-btn ${activeTab === 'tasks' ? 'active' : ''}`}
          onClick={() => setActiveTab('tasks')}
        >
          Tasks
        </button>
        <button
          className={`nav-btn ${activeTab === 'recommend' ? 'active' : ''}`}
          onClick={() => setActiveTab('recommend')}
        >
          Recommendations
        </button>
        <button
          className={`nav-btn ${activeTab === 'compare' ? 'active' : ''}`}
          onClick={() => setActiveTab('compare')}
        >
          A/B Test
        </button>
      </nav>

      <main className="main">
        {loading ? (
          <div className="loading">Loading...</div>
        ) : (
          <>
            {activeTab === 'tasks' && <TaskManager pets={pets} apiBase={API_BASE} />}
            {activeTab === 'recommend' && <RecommendationEngine pets={pets} apiBase={API_BASE} />}
            {activeTab === 'compare' && <ABComparison pets={pets} apiBase={API_BASE} />}
          </>
        )}
      </main>

      <footer className="footer">
        <p>Flask API: {API_BASE}</p>
      </footer>
    </div>
  );
}

export default App;
