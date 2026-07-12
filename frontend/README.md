# 🧠 LeetCode Profile Analyser

A full-stack analytics platform that processes your LeetCode profile data and generates a personalized AI-powered study plan to help you improve your coding skills.

> Enter any LeetCode username → Get deep insights → Receive a 7-day AI study plan

![Tech Stack](https://img.shields.io/badge/Frontend-React-61DAFB?style=flat&logo=react)
![Tech Stack](https://img.shields.io/badge/Backend-FastAPI-009688?style=flat&logo=fastapi)
![Tech Stack](https://img.shields.io/badge/AI-Gemini-4285F4?style=flat&logo=google)
![Tech Stack](https://img.shields.io/badge/Deployed-Render%20%2B%20Vercel-black?style=flat)

---

## 🌐 Live Demo

- **Frontend:** [https://lc-analyzer.vercel.app](https://lc-analyzer.vercel.app/)
- **Backend API:** [https://lc-analyzer.onrender.com](https://lc-analyzer.onrender.com)

---

## ✨ Features

- **Topic-wise Analysis** — See exactly how many problems you've solved per DSA topic (Arrays, Trees, Dynamic Programming, Graphs, and more)
- **Difficulty Breakdown** — Visual stats for Easy, Medium, and Hard problems solved
- **Submission Heatmap** — GitHub-style heatmap showing your coding activity over 365 days
- **Radar Chart** — Instantly see your strongest and weakest topics at a glance
- **AI Study Plan** — Powered by Google Gemini, generates a personalized 7-day practice plan targeting your weakest areas
- **Real-time Data** — Fetches live data directly from LeetCode's GraphQL API

---

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────┐
│                    React Frontend                        │
│         (Input → Charts → Heatmap → Study Plan)         │
└─────────────────────┬───────────────────────────────────┘
                      │ HTTP GET /analyze/{username}
┌─────────────────────▼───────────────────────────────────┐
│                   FastAPI Backend                        │
│  ┌─────────────┐  ┌──────────────┐  ┌───────────────┐  │
│  │ leetcode.py │  │ analytics.py │  │recommender.py │  │
│  │  GraphQL    │→ │  Processing  │→ │  Gemini AI    │  │
│  │  Fetcher    │  │  & Analytics │  │  Study Plan   │  │
│  └─────────────┘  └──────────────┘  └───────────────┘  │
└──────────┬──────────────────────────────────┬───────────┘
           │                                  │
┌──────────▼──────────┐          ┌────────────▼──────────┐
│  LeetCode GraphQL   │          │    Google Gemini API   │
│  leetcode.com/      │          │    (Study Plan LLM)    │
│  graphql            │          │                        │
└─────────────────────┘          └───────────────────────┘
```

---

## 🛠️ Tech Stack

| Layer | Technology | Purpose |
|-------|-----------|---------|
| Frontend | React | UI and data visualization |
| Charts | Recharts | Radar chart for topic stats |
| Heatmap | react-calendar-heatmap | Submission frequency heatmap |
| Backend | FastAPI (Python) | REST API and business logic |
| HTTP Client | httpx | Async HTTP requests |
| AI | Google Gemini (`google-genai`) | Personalized study plan generation |
| Deployment | Render | Backend hosting |
| Deployment | Vercel | Frontend hosting |

---

## 📁 Project Structure

```
lc_analyzer/
├── backend/
│   ├── main.py           # FastAPI app, CORS, endpoints
│   ├── leetcode.py       # LeetCode GraphQL API fetcher
│   ├── analytics.py      # Data processing & analytics engine
│   ├── recommender.py    # Gemini AI study plan generator
│   ├── requirements.txt  # Python dependencies
│   └── .env              # Environment variables (never commit this)
│
└── frontend/
    ├── src/
    │   ├── App.js         # Main React component
    │   └── App.css        # Styles
    └── package.json
```

---

## 🚀 Getting Started

### Prerequisites

- Python 3.10+
- Node.js 18+
- A Google Gemini API key from [Google AI Studio](https://aistudio.google.com/apikey)

### 1. Clone the repository

```bash
git clone https://github.com/your-username/lc_analyzer.git
cd lc_analyzer
```

### 2. Set up the Backend

```bash
cd backend
python3 -m venv venv
source venv/bin/activate        # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

Create a `.env` file in the `backend/` folder:

```env
Gemini_api_key=your_gemini_api_key_here
```

Start the backend server:

```bash
uvicorn main:app --reload
```

Backend will be running at `http://localhost:8000`

### 3. Set up the Frontend

Open a new terminal:

```bash
cd frontend
npm install
npm start
```

Frontend will be running at `http://localhost:3000`

---

## 🔌 API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET` | `/health` | Health check |
| `GET` | `/analyze/{username}` | Full profile analysis + study plan |
| `GET` | `/docs` | Auto-generated API documentation |

### Example Response

```json
{
  "difficulty": {
    "Easy": 120,
    "Medium": 85,
    "Hard": 23
  },
  "topics": [
    { "tagName": "Dynamic Programming", "problemsSolved": 12 },
    { "tagName": "Graph", "problemsSolved": 8 },
    ...
  ],
  "study_plan": "Day 1: Focus on Dynamic Programming...\nDay 2: ..."
}
```

---

## 🧩 How It Works

### 1. Data Fetching (`leetcode.py`)
Queries LeetCode's internal GraphQL API at `https://leetcode.com/graphql` to fetch:
- Problems solved by difficulty (Easy/Medium/Hard)
- Topic tag counts (Arrays, Trees, DP, etc.)

LeetCode doesn't have an official public API, so this reverse-engineers their GraphQL endpoint used by their own website.

### 2. Analytics Engine (`analytics.py`)
Processes raw data to compute:
- **Difficulty stats** — counts per difficulty level
- **Topic stats** — filters to important DSA topics only, sorts from weakest to strongest
- **Summary** — combines all metrics into a single response

### 3. AI Recommendation Engine (`recommender.py`)
- Picks the **5 weakest topics** from the sorted topic list
- Identifies the **3 strongest topics** for context
- Sends a structured prompt to **Google Gemini**
- Returns a **7-day personalized study plan** with daily focus areas and problem types

### 4. Frontend (`App.js`)
Displays everything in an interactive dashboard:
- **RadarChart** — topic-wise performance overview
- **Calendar Heatmap** — 365-day submission activity
- **Difficulty cards** — Easy/Medium/Hard breakdown
- **Study plan card** — AI-generated recommendations

---

## 🔐 Environment Variables

| Variable | Description |
|----------|-------------|
| `Gemini_api_key` | Your Google Gemini API key |

> ⚠️ Never commit your `.env` file. It's listed in `.gitignore`.

For production (Render), add environment variables in the dashboard under **Environment → Environment Variables**.

---

## 🚢 Deployment

### Backend (Render)

1. Push code to GitHub
2. Go to [render.com](https://render.com) → New Web Service
3. Connect your GitHub repo
4. Set:
   - **Root Directory:** `backend`
   - **Build Command:** `pip install -r requirements.txt`
   - **Start Command:** `uvicorn main:app --host 0.0.0.0 --port 10000`
5. Add `Gemini_api_key` in Environment Variables
6. Deploy

### Frontend (Vercel)

1. Go to [vercel.com](https://vercel.com) → New Project
2. Import your GitHub repo
3. Set **Root Directory** to `frontend`
4. Deploy

---

## ⚠️ Known Limitations

- **LeetCode API** — Uses an unofficial GraphQL endpoint. May break if LeetCode changes their internal API
- **Submission history** — Detailed submission history requires LeetCode session authentication (not implemented)
- **Gemini free tier** — Limited to 1500 requests/day on the free tier. The app handles rate limits gracefully

---

## 🔮 Future Improvements

- [ ] User authentication to save progress over time
- [ ] LeetCode session cookie support for full submission history
- [ ] Specific problem recommendations with direct links
- [ ] Difficulty trend chart showing improvement over time
- [ ] Response caching to reduce API calls for repeated lookups
- [ ] Contest performance analysis

---

## 🧠 What I Learned

- How to reverse-engineer GraphQL APIs using browser DevTools
- Building async Python backends with FastAPI
- Integrating LLMs into production applications
- Handling API keys securely with environment variables
- Deploying full-stack apps with Render + Vercel
- Managing CORS between separate frontend and backend deployments

---

## 📄 License

MIT License — feel free to use this project for learning or as a template.

---

## 🙋 Author

**Krishna Agarwal**
- GitHub: [@k-agar](https://github.com/k-agar)
- Project: [lc_analyzer](https://github.com/k-agar/lc_analyzer)

---

> Built with ❤️ to make LeetCode practice smarter, not harder.