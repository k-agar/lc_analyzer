# 🧠 LeetCode Profile Analyser

A full-stack analytics platform that processes your LeetCode profile data and generates a personalized AI-powered study plan to help you improve your coding skills.

> Enter any LeetCode username → Get deep insights → Receive a 7-day AI study plan

![Tech Stack](https://img.shields.io/badge/Frontend-React-61DAFB?style=flat&logo=react)
![Tech Stack](https://img.shields.io/badge/Backend-FastAPI-009688?style=flat&logo=fastapi)
![Tech Stack](https://img.shields.io/badge/AI-Hugging%20Face-FFD21E?style=flat&logo=huggingface)
![Tech Stack](https://img.shields.io/badge/Deployed-Render%20%2B%20Vercel-black?style=flat)

---

## 🌐 Live Demo

- **Frontend:** https://lc-analyzer.vercel.app/
- **Backend API:** https://lc-analyzer.onrender.com

---

## ✨ Features

- **Topic-wise Analysis** — See exactly how many problems you've solved per DSA topic (Arrays, Trees, Dynamic Programming, Graphs, and more)
- **Difficulty Breakdown** — Visual stats for Easy, Medium, and Hard problems solved
- **Submission Heatmap** — GitHub-style heatmap showing your coding activity over 365 days
- **Radar Chart** — Instantly see your strongest and weakest topics at a glance
- **AI Study Plan** — Powered by Hugging Face, generates a personalized 7-day practice plan targeting your weakest areas
- **Real-time Data** — Fetches live data directly from LeetCode's GraphQL API

---

## 🏗️ Architecture

```text
┌─────────────────────────────────────────────────────────┐
│                    React Frontend                        │
│         (Input → Charts → Heatmap → Study Plan)         │
└─────────────────────┬───────────────────────────────────┘
                      │ HTTP GET /analyze/{username}
┌─────────────────────▼───────────────────────────────────┐
│                   FastAPI Backend                        │
│  ┌─────────────┐  ┌──────────────┐  ┌───────────────┐  │
│  │ leetcode.py │  │ analytics.py │  │ recommender.py │  │
│  │  GraphQL    │→ │  Processing  │→ │ Hugging Face  │  │
│  │  Fetcher    │  │ & Analytics  │  │  AI Planner   │  │
│  └─────────────┘  └──────────────┘  └───────────────┘  │
└──────────┬──────────────────────────────────┬───────────┘
           │                                  │
┌──────────▼──────────┐          ┌────────────▼──────────┐
│  LeetCode GraphQL   │          │ Hugging Face Inference │
│  leetcode.com/      │          │          API           │
│  graphql            │          │    (Study Plan LLM)    │
└─────────────────────┘          └────────────────────────┘
