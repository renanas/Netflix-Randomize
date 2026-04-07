# 🎬 Netflix Randomize

An intelligent movie recommendation system with **Machine Learning (KNN)**, **animated random movie carousel** and **Netflix-style interface** in React!

## 🌍 Languages

- [Portuguese (pt-BR)](README-ptbr.md)
- [English](README-en.md)

## ✨ Main Features

### 🤖 **Machine Learning Recommendation (KNN)**
- ✅ KNN model trained offline on TMDB movies
- ✅ Personalized recommendations based on user history
- ✅ Smart caching and cold-start handling

### 🎲 **Random Movie Carousel**
- ✅ Animated "case opening" style carousel
- ✅ Displays random movies with details

### 👤 **Authentication & User Management**
- ✅ JWT authentication
- ✅ User profiles and watchlists

### 📺 **React Interface**
- ✅ Netflix-style UI with multiple pages
- ✅ Responsive design

### 🎬 **TMDB Integration**
- ✅ Movie data fetching and storage

---

## 🚀 Quick Start

### Prerequisites
- Python 3.8+, Node.js 16+, MongoDB, TMDB API Key

### Setup
1. Clone and setup backend (Python venv, install deps, .env)
2. Train KNN model: `python scripts/train_recommendations.py`
3. Setup frontend: `cd frontend && npm install`
4. Start backend: `uvicorn backend.main:app --reload`
5. Start frontend: `npm start`

- Backend: http://localhost:8000
- Frontend: http://localhost:3000

### Login
Email: teste@netflix.com | Password: 123456

---

For detailed instructions, see [README-ptbr.md](README-ptbr.md) or [README-en.md](README-en.md).

**Made with ❤️ • v1.0.0 • April 2026 • ✅ Production Ready**
