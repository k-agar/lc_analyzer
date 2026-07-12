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

const API_BASE = process.env.REACT_APP_API_URL || 
  (process.env.NODE_ENV === 'development' ? 'http://localhost:8000' : 'https://lc-analyzer.onrender.com');

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
      const response = await fetch(`${API_BASE}/analyze/${username}`);
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

            <div className="card contest-card">
              <h3>Contest Performance</h3>
              {data.contest ? (
                <div className="contest-stats">
                  <div className="rating-display">
                    <span className="rating-value">{data.contest.rating}</span>
                    {data.contest.badge && (
                      <span className={`contest-badge ${data.contest.badge.toLowerCase()}`}>
                        {data.contest.badge}
                      </span>
                    )}
                  </div>
                  <div className="stats-grid">
                    <div className="contest-stat-item">
                      <span className="label">Global Rank</span>
                      <span className="value">
                        {data.contest.globalRanking.toLocaleString()} / {data.contest.totalParticipants.toLocaleString()}
                      </span>
                    </div>
                    <div className="contest-stat-item">
                      <span className="label">Percentile</span>
                      <span className="value">Top {data.contest.topPercentage}%</span>
                    </div>
                    <div className="contest-stat-item">
                      <span className="label">Attended</span>
                      <span className="value">{data.contest.attendedContestsCount} Contests</span>
                    </div>
                  </div>
                </div>
              ) : (
                <div className="contest-empty">
                  <div className="empty-icon">🏆</div>
                  <p>No contest history</p>
                  <span>Participate in LeetCode contests to get rated.</span>
                </div>
              )}
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

            <div className="card badges-card">
              <h3>Badges Earned ({data.badges ? data.badges.length : 0})</h3>
              {data.badges && data.badges.length > 0 ? (
                <div className="badges-grid-container">
                  <div className="badges-grid">
                    {data.badges.map((badge) => (
                      <div className="badge-item-wrapper" key={badge.id || badge.name}>
                        <div className="badge-icon-container">
                          <img
                            src={badge.icon}
                            alt={badge.displayName}
                            className="badge-icon-img"
                            onError={(e) => {
                              e.target.style.display = 'none';
                            }}
                          />
                        </div>
                        <div className="badge-tooltip">
                          <div className="tooltip-name">{badge.displayName}</div>
                          {badge.hoverText && <div className="tooltip-desc">{badge.hoverText}</div>}
                        </div>
                      </div>
                    ))}
                  </div>
                </div>
              ) : (
                <div className="badges-empty">
                  <div className="empty-icon">🏅</div>
                  <p>No badges earned yet</p>
                  <span>Solve daily challenges and study plans to earn badges!</span>
                </div>
              )}
            </div>

            {data.study_plan && (
              <div className="card study-plan-card">
                <h3>AI Study Plan</h3>
                <div className="study-plan-content">
                  {renderMarkdown(data.study_plan)}
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

const parseBold = (text) => {
  const parts = text.split(/(\*\*.*?\*\*)/g);
  return parts.map((part, i) => {
    if (part.startsWith('**') && part.endsWith('**')) {
      return <strong key={i}>{part.slice(2, -2)}</strong>;
    }
    return part;
  });
};

const renderMarkdown = (text) => {
  if (!text) return null;
  
  // Ensure any inline or list item starting with 'Day X' starts on a new line.
  let processedText = text;
  processedText = processedText.replace(/(?!^)\b(Day \d+)\b/g, '\n$1');
  
  const lines = processedText.split('\n');
  return lines.map((line, index) => {
    const trimmedLine = line.trim();
    if (trimmedLine === '') {
      return <div key={index} style={{ height: '0.5rem' }} />;
    }
    
    // Check if line is a Day X heading
    const isDayHeading = /^(Day \d+|### Day \d+|## Day \d+|# Day \d+)/i.test(trimmedLine);
    if (isDayHeading) {
      const cleanDay = trimmedLine.replace(/^(### |## |# )/i, '').trim();
      return (
        <h4 key={index} className="study-plan-day-heading">
          {parseBold(cleanDay)}
        </h4>
      );
    }
    
    if (trimmedLine.startsWith('### ')) {
      return <h4 key={index}>{parseBold(trimmedLine.replace('### ', ''))}</h4>;
    }
    if (trimmedLine.startsWith('## ')) {
      return <h3 key={index}>{parseBold(trimmedLine.replace('## ', ''))}</h3>;
    }
    if (trimmedLine.startsWith('# ')) {
      return <h2 key={index}>{parseBold(trimmedLine.replace('# ', ''))}</h2>;
    }
    
    const isListItem = trimmedLine.startsWith('- ') || trimmedLine.startsWith('* ');
    if (isListItem) {
      const cleanLine = trimmedLine.substring(2);
      return (
        <li key={index}>
          {parseBold(cleanLine)}
        </li>
      );
    }
    
    return <p key={index}>{parseBold(trimmedLine)}</p>;
  });
};

export default App;
