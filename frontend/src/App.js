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
      <div className="app-container">
        <div className="logo-icon">📊</div>
        <h1>LeetCode Analyzer</h1>
        <p className="subtitle">Discover your strengths, weaknesses, and custom study plans</p>
        
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

        {loading && <div className="status-msg">Loading...</div>}

        {status.message && !loading && (
          <div className={`status-msg ${status.type}`}>
            {status.message}
          </div>
        )}

        {data && data.difficulty && !loading && (
          <div className="stats-container" style={{ marginTop: '2rem', textAlign: 'left', width: '100%' }}>
            <h3 style={{ marginBottom: '1rem', color: '#c084fc' }}>Difficulty Stats:</h3>
            <p style={{ margin: '0.5rem 0' }}>Easy: {data.difficulty.Easy}</p>
            <p style={{ margin: '0.5rem 0' }}>Medium: {data.difficulty.Medium}</p>
            <p style={{ margin: '0.5rem 0' }}>Hard: {data.difficulty.Hard}</p>
          </div>
        )}

        {data && data.topics && data.topics.length > 0 && !loading && (
          <div className="chart-container" style={{ marginTop: '2.5rem', width: '100%', height: '320px', textAlign: 'left' }}>
            <h3 style={{ marginBottom: '1rem', color: '#c084fc' }}>Weakest Topics Profile:</h3>
            <ResponsiveContainer width="100%" height="90%">
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
        )}

        {data && data.calendar && !loading && (
          <div className="heatmap-container" style={{ marginTop: '2.5rem', width: '100%', textAlign: 'left' }}>
            <h3 style={{ marginBottom: '1.25rem', color: '#c084fc' }}>Submission Calendar:</h3>
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
        )}
      </div>
    </div>
  );
}

export default App;
