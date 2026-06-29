import React, { useState } from 'react';
import {
  Radar,
  RadarChart,
  PolarGrid,
  PolarAngleAxis,
  PolarRadiusAxis,
  ResponsiveContainer
} from 'recharts';
import CalendarHeatmap from 'react-calendar-heatmap';
import 'react-calendar-heatmap/dist/styles.css';
import './App.css';

function App() {
  const [username, setUsername] = useState('');
  const [loading, setLoading] = useState(false);
  const [status, setStatus] = useState({ type: '', message: '' });
  const [data, setData] = useState(null);

  const today = new Date();
  const oneYearAgo = new Date();
  oneYearAgo.setFullYear(today.getFullYear() - 1);

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!username.trim()) return;

    setLoading(true);
    setData(null);
    setStatus({ type: '', message: '' });
    console.log(`Sending request for username: ${username}`);

    try {
      const response = await fetch(`http://localhost:8000/analyze/${username}`);
      if (response.status === 404) {
        throw new Error('User not found');
      }
      if (!response.ok) {
        throw new Error(`HTTP error! Status: ${response.status}`);
      }
      const result = await response.json();
      console.log('Analysis Response:', result);
      setData(result);
      setStatus({ type: 'success', message: 'Analysis completed successfully!' });
    } catch (error) {
      console.error('Error calling analyze endpoint:', error);
      if (error.message === 'User not found') {
        setStatus({ type: 'error', message: 'Username not found. Please try again.' });
      } else {
        setStatus({ type: 'error', message: 'Failed to fetch analysis. Make sure the backend is running.' });
      }
    } finally {
      setLoading(false);
    }
  };

  const getHeatmapValues = (calendar) => {
    if (!calendar) return [];
    return Object.keys(calendar).map((timestampSec) => {
      const date = new Date(parseInt(timestampSec, 10) * 1000);
      const year = date.getFullYear();
      const month = String(date.getMonth() + 1).padStart(2, '0');
      const day = String(date.getDate()).padStart(2, '0');
      return {
        date: `${year}-${month}-${day}`,
        count: calendar[timestampSec],
      };
    });
  };

  return (
    <div className="App">
      <div className="content-wrapper">
        <header className="app-header">
          <div className="logo-icon">📊</div>
          <h1>LeetCode Profile Analyser</h1>
          <p className="subtitle">Discover your strengths, weaknesses, and custom study plans</p>
        </header>
        
        <div className="search-card">
          <form className="form-group" onSubmit={handleSubmit}>
            <div className="input-wrapper">
              <input
                type="text"
                placeholder="Enter LeetCode username"
                className="username-input"
                value={username}
                onChange={(e) => setUsername(e.target.value)}
                disabled={loading}
                required
              />
            </div>
            <button type="submit" className="submit-btn" disabled={loading}>
              {loading ? 'Analyzing...' : 'Analyze Profile'}
            </button>
          </form>
        </div>

        {loading && <div className="status-msg loading">Loading...</div>}

        {status.message && !loading && (
          <div className={`status-msg ${status.type}`}>
            {status.message}
          </div>
        )}

        {data && !loading && (
          <div className="dashboard-grid">
            <div className="card stats-card">
              <h3>Difficulty Stats</h3>
              <div className="stats-list">
                <div className="stat-item easy">
                  <span className="label">Easy</span>
                  <span className="value">{data.difficulty.Easy}</span>
                </div>
                <div className="stat-item medium">
                  <span className="label">Medium</span>
                  <span className="value">{data.difficulty.Medium}</span>
                </div>
                <div className="stat-item hard">
                  <span className="label">Hard</span>
                  <span className="value">{data.difficulty.Hard}</span>
                </div>
              </div>
            </div>

            {data.topics && data.topics.length > 0 && (
              <div className="card chart-card">
                <h3>Weakest Topics Profile</h3>
                <div className="chart-wrapper">
                  <ResponsiveContainer width="100%" height="100%">
                    <RadarChart cx="50%" cy="50%" outerRadius="70%" data={data.topics.slice(0, 8)}>
                      <PolarGrid stroke="#475569" />
                      <PolarAngleAxis dataKey="tagName" stroke="#94a3b8" tick={{ fill: '#94a3b8', fontSize: 11 }} />
                      <PolarRadiusAxis angle={30} domain={[0, 'auto']} stroke="#475569" tick={{ fill: '#94a3b8', fontSize: 9 }} />
                      <Radar
                        name="Solved"
                        dataKey="problemsSolved"
                        stroke="#818cf8"
                        fill="#818cf8"
                        fillOpacity={0.3}
                      />
                    </RadarChart>
                  </ResponsiveContainer>
                </div>
              </div>
            )}

            {data.calendar && (
              <div className="card heatmap-card">
                <h3>Submission Calendar (Past Year)</h3>
                <div className="heatmap-wrapper">
                  <CalendarHeatmap
                    startDate={oneYearAgo}
                    endDate={today}
                    values={getHeatmapValues(data.calendar)}
                    classForValue={(value) => {
                      if (!value || value.count === 0) {
                        return 'color-empty';
                      }
                      return `color-scale-${Math.min(value.count, 4)}`;
                    }}
                  />
                </div>
              </div>
            )}
          </div>
        )}
      </div>
    </div>
  );
}

export default App;
