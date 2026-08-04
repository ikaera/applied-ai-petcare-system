import React, { useState } from 'react';
import axios from 'axios';
import './RecommendationEngine.css';

function RecommendationEngine({ pets, apiBase }) {
  const [input, setInput] = useState({
    pet: pets[0]?.name || '',
    recommendation: 'Feed with high-protein kibble',
    mode: 'heuristic'
  });
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);

  const handleGetRecommendation = (e) => {
    e.preventDefault();
    setLoading(true);

    axios.post(`${apiBase}/api/recommend`, input)
      .then(res => setResult(res.data))
      .catch(err => {
        console.error('Error:', err);
        alert('Error getting recommendation');
      })
      .finally(() => setLoading(false));
  };

  const getStatusColor = (status) => {
    const colors = {
      'PASS': '#4CAF50',
      'REVIEW': '#FF9800',
      'BIASED': '#f44336'
    };
    return colors[status] || '#666';
  };

  return (
    <div className="recommendation-engine">
      <h2>Get AI Recommendation</h2>

      <form className="rec-form" onSubmit={handleGetRecommendation}>
        <div className="form-group">
          <label>Select Pet</label>
          <select
            value={input.pet}
            onChange={(e) => setInput({ ...input, pet: e.target.value })}
          >
            {pets.map(pet => (
              <option key={pet.name} value={pet.name}>
                {pet.name} ({pet.species}, age {pet.age})
              </option>
            ))}
          </select>
        </div>

        <div className="form-group">
          <label>Recommendation Text</label>
          <textarea
            value={input.recommendation}
            onChange={(e) => setInput({ ...input, recommendation: e.target.value })}
            rows="3"
            placeholder="Enter the care recommendation..."
          />
        </div>

        <div className="form-group">
          <label>Retrieval Mode</label>
          <select
            value={input.mode}
            onChange={(e) => setInput({ ...input, mode: e.target.value })}
          >
            <option value="heuristic">Heuristic (Keyword)</option>
            <option value="groq">Groq API (Semantic)</option>
          </select>
        </div>

        <button type="submit" disabled={loading}>
          {loading ? 'Analyzing...' : 'Get Recommendation'}
        </button>
      </form>

      {result && (
        <div className="rec-result">
          <div className="result-header">
            <h3>{result.pet}'s Recommendation</h3>
            <span className="mode-badge">{result.mode.toUpperCase()}</span>
          </div>

          <div className="recommendation-text">
            <p>{result.recommendation}</p>
          </div>

          <div className="validation-box">
            <h4>Validation Result</h4>
            <div
              className="status"
              style={{ color: getStatusColor(result.validation.status) }}
            >
              Status: <strong>{result.validation.status}</strong>
            </div>
            <p className="note">{result.validation.note}</p>
            <div className="confidence">
              <span>Confidence:</span>
              <div className="confidence-bar">
                <div
                  className="confidence-fill"
                  style={{ width: `${result.confidence * 100}%` }}
                />
              </div>
              <span>{Math.round(result.confidence * 100)}%</span>
            </div>
          </div>

          {result.retrieved_docs && result.retrieved_docs.length > 0 && (
            <div className="docs-box">
              <h4>Retrieved Documents</h4>
              <ul>
                {result.retrieved_docs.slice(0, 3).map((doc, idx) => (
                  <li key={idx}>{doc}</li>
                ))}
              </ul>
            </div>
          )}
        </div>
      )}
    </div>
  );
}

export default RecommendationEngine;
