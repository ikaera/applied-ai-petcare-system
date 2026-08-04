import React, { useState } from 'react';
import axios from 'axios';
import './ABComparison.css';

function ABComparison({ pets, apiBase }) {
  const [input, setInput] = useState({
    pet: pets[0]?.name || '',
    recommendation: 'Feed with high-protein kibble'
  });
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);

  const handleCompare = (e) => {
    e.preventDefault();
    setLoading(true);

    axios.post(`${apiBase}/api/compare`, input)
      .then(res => setResult(res.data))
      .catch(err => {
        console.error('Error:', err);
        alert('Error comparing modes');
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
    <div className="ab-comparison">
      <h2>A/B Test: Heuristic vs Groq API</h2>
      <p className="subtitle">Compare keyword-based and semantic retrieval on the same recommendation</p>

      <form className="compare-form" onSubmit={handleCompare}>
        <div className="form-group">
          <label>Pet</label>
          <select
            value={input.pet}
            onChange={(e) => setInput({ ...input, pet: e.target.value })}
          >
            {pets.map(pet => (
              <option key={pet.name} value={pet.name}>
                {pet.name} ({pet.species})
              </option>
            ))}
          </select>
        </div>

        <div className="form-group">
          <label>Recommendation to Validate</label>
          <textarea
            value={input.recommendation}
            onChange={(e) => setInput({ ...input, recommendation: e.target.value })}
            rows="3"
          />
        </div>

        <button type="submit" disabled={loading}>
          {loading ? 'Comparing...' : 'Compare Modes'}
        </button>
      </form>

      {result && (
        <div className="comparison-results">
          <h3>Results for {result.pet}</h3>
          <p className="rec-text">"{result.recommendation}"</p>

          <div className="comparison-grid">
            <div className="mode-card heuristic">
              <h4>Heuristic (Keyword-based)</h4>
              <div className="mode-content">
                <div className="validation-item">
                  <span className="label">Status:</span>
                  <span
                    className="value"
                    style={{ color: getStatusColor(result.heuristic.validation.status) }}
                  >
                    {result.heuristic.validation.status}
                  </span>
                </div>

                <div className="validation-item">
                  <span className="label">Note:</span>
                  <span className="value">{result.heuristic.validation.note}</span>
                </div>

                <div className="confidence-item">
                  <span className="label">Confidence:</span>
                  <div className="confidence-bar">
                    <div
                      className="confidence-fill"
                      style={{ width: `${result.heuristic.confidence * 100}%` }}
                    />
                  </div>
                  <span className="confidence-text">
                    {Math.round(result.heuristic.confidence * 100)}%
                  </span>
                </div>

                {result.heuristic.retrieved_docs && (
                  <div className="docs-section">
                    <strong>Retrieved ({result.heuristic.retrieved_docs.length})</strong>
                    <ul>
                      {result.heuristic.retrieved_docs.slice(0, 2).map((doc, idx) => (
                        <li key={idx}>{doc}</li>
                      ))}
                    </ul>
                  </div>
                )}
              </div>
            </div>

            <div className="mode-card groq">
              <h4>Groq API (Semantic)</h4>
              <div className="mode-content">
                <div className="validation-item">
                  <span className="label">Status:</span>
                  <span
                    className="value"
                    style={{ color: getStatusColor(result.groq.validation.status) }}
                  >
                    {result.groq.validation.status}
                  </span>
                </div>

                <div className="validation-item">
                  <span className="label">Note:</span>
                  <span className="value">{result.groq.validation.note}</span>
                </div>

                <div className="confidence-item">
                  <span className="label">Confidence:</span>
                  <div className="confidence-bar">
                    <div
                      className="confidence-fill"
                      style={{ width: `${result.groq.confidence * 100}%` }}
                    />
                  </div>
                  <span className="confidence-text">
                    {Math.round(result.groq.confidence * 100)}%
                  </span>
                </div>

                {result.groq.retrieved_docs && (
                  <div className="docs-section">
                    <strong>Retrieved ({result.groq.retrieved_docs.length})</strong>
                    <ul>
                      {result.groq.retrieved_docs.slice(0, 2).map((doc, idx) => (
                        <li key={idx}>{doc}</li>
                      ))}
                    </ul>
                  </div>
                )}
              </div>
            </div>
          </div>

          <div className="comparison-summary">
            <h4>Summary</h4>
            <div className="summary-row">
              <span>Both modes agree:</span>
              <strong>{result.comparison.both_safe ? '✓ Yes' : '✗ No'}</strong>
            </div>
            <div className="summary-row">
              <span>Confidence difference:</span>
              <strong>{Math.round(result.comparison.confidence_difference * 100)}%</strong>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}

export default ABComparison;
