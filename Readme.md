# 🧠 LeetCode Profile Analyser

A full-stack analytics platform that analyzes LeetCode profiles and generates personalized AI-powered 7-day study plans.

> Enter a LeetCode username → Get insights → Get a personalized study plan

![React](https://img.shields.io/badge/Frontend-React-61DAFB?style=flat&logo=react)
![FastAPI](https://img.shields.io/badge/Backend-FastAPI-009688?style=flat&logo=fastapi)
![Hugging Face](https://img.shields.io/badge/AI-Hugging%20Face-FFD21E?style=flat&logo=huggingface)
![Deployment](https://img.shields.io/badge/Deployed-Vercel%20%2B%20Render-black?style=flat)

## 🌐 Live Demo

- Frontend: https://lc-analyzer.vercel.app/
- Backend API: https://lc-analyzer.onrender.com

## ✨ Features

- 📊 Topic-wise DSA analysis
- 🎯 Easy, Medium, and Hard difficulty breakdown
- 📅 365-day submission heatmap
- 🕸️ Radar chart for topic performance
- 🤖 AI-generated personalized 7-day study plan
- ⚡ Real-time LeetCode data using GraphQL

## 🛠️ Tech Stack

- **Frontend:** React, Recharts, react-calendar-heatmap
- **Backend:** FastAPI, Python, httpx
- **AI:** Hugging Face Inference API
- **Data:** LeetCode GraphQL API
- **Deployment:** Vercel + Render

## 🏗️ Architecture

    React Frontend
          │
          │ GET /analyze/{username}
          ▼
    FastAPI Backend
          │
          ├── LeetCode GraphQL API
          │        ↓
          │   Profile Data
          │        ↓
          ├── Analytics Engine
          │        ↓
          │   Weakest Topics
          │        ↓
          └── Hugging Face API
                   ↓
            7-Day Study Plan
                   ↓
             React Dashboard

## 📁 Project Structure

    lc_analyzer/
    ├── backend/
    │   ├── main.py
    │   ├── leetcode.py
    │   ├── analytics.py
    │   ├── recommender.py
    │   ├── requirements.txt
    │   └── .env
    │
    └── frontend/
        ├── src/
        │   ├── App.js
        │   └── App.css
        └── package.json

## 🚀 Run Locally

### Backend

    cd backend
    python3 -m venv venv
    source venv/bin/activate
    pip install -r requirements.txt

Create `.env`:

    HF_API_KEY=your_huggingface_api_key

Run:

    uvicorn main:app --reload

### Frontend

    cd frontend
    npm install
    npm start

## 🔌 API

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/health` | Health check |
| GET | `/analyze/{username}` | Analyze profile and generate study plan |
| GET | `/docs` | API documentation |

## 🧩 How It Works

1. Fetches LeetCode profile data through its GraphQL API.
2. Processes difficulty and topic statistics.
3. Identifies the user's weakest and strongest DSA topics.
4. Sends the analysis to a Hugging Face model.
5. Generates a personalized 7-day study plan.
6. Displays the results through the React dashboard.

## 🔐 Environment Variables

| Variable | Description |
|----------|-------------|
| `HF_API_KEY` | Hugging Face API token |

> Never commit your `.env` file.

## ⚠️ Limitations

- LeetCode GraphQL API is unofficial and may change.
- Detailed submission history requires authentication.
- Hugging Face API limits depend on the selected model and plan.

## 🔮 Future Improvements

- User authentication and progress tracking
- Specific problem recommendations
- Difficulty progress tracking
- Contest performance analysis
- Response caching
