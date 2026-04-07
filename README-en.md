# 🎬 Netflix Randomize

An intelligent movie recommendation system with **Machine Learning (KNN)**, **animated random movie carousel** and **Netflix-style interface** in React!

## ✨ Main Features

### 🤖 **Machine Learning Recommendation (KNN)**
- ✅ KNN model trained offline on TMDB movies
- ✅ Feature vectorization: genres (one-hot), popularity, votes, log(vote_count)
- ✅ Personalized recommendations based on user history
- ✅ Cold-start handling: popular movies for new users
- ✅ Smart caching in MongoDB (updated on each generation)
- ✅ Batch refresh: script to pre-compute recommendations

### 🎲 **Random Movie Carousel**
- ✅ Animated visual component like "case opening" (quickly passes movies and stops on one)
- ✅ Randomly selects movies from recommendations
- ✅ Displays result prominently with synopsis, rating, and banner
- ✅ Fully responsive (desktop, tablet, mobile)

### 👤 **Authentication and User Management**
- ✅ Login/Register with JWT
- ✅ Password hashing with bcrypt
- ✅ Email validation
- ✅ User profile with preferences
- ✅ Viewing history
- ✅ Rating system

### 📺 **React Interface**
- ✅ Pages: Login, Home (movie grid), My List (watchlist), Recommend Movie (carousel)
- ✅ Netflix-style navigation with fixed header
- ✅ Interactive grid with recommended movies
- ✅ TMDB integration for posters and data
- ✅ Netflix dark theme

### 🎬 **TMDB Integration**
- ✅ Automatic fetch of popular movies
- ✅ Storage in MongoDB (no duplicates)
- ✅ Enrichment with detailed data
- ✅ Support for videos, credits, reviews

### 📊 **Logs and Monitoring**
- ✅ Detailed recommendation logs (cache hit/miss)
- ✅ KNN usage tracking
- ✅ Cold-start detection
- ✅ Error tracking

### 🧪 **Automated Tests**
- ✅ 20 pytest tests (100% passing)
- ✅ Tests for: auth, users, movies, ratings, recommendations
- ✅ Isolation coverage in tests via mocking
- ✅ Serialization validation (ObjectId → string)

---

## 🏗️ Architecture

```
Netflix-Randomize/
├── backend/                          # 🔧 FastAPI API
│   ├── main.py                       # Main application
│   ├── config.py                     # Configurations
│   ├── database/
│   │   └── mongodb_connection.py     # MongoDB connection
│   ├── models/                       # Pydantic models
│   │   ├── user.py                   # User with preferences, behavior
│   │   ├── rating.py                 # Movie rating
│   │   ├── watchlist.py              # Watchlist
│   │   └── movie.py                  # Movie (TMDB)
│   ├── repository/                   # Data access layer
│   │   ├── user_repository.py        # CRUD users
│   │   ├── movie_repository.py       # CRUD movies (with sanitization)
│   │   ├── rating_repository.py      # CRUD ratings
│   │   └── recommendation_repository.py  # Recommendation cache
│   ├── services/                     # Business logic
│   │   ├── user_service.py           # User logic
│   │   ├── tmdb_service.py           # Fetch TMDB
│   │   ├── rating_service.py         # Rating calculations
│   │   ├── playback_service.py       # Playback history
│   │   ├── watchlist_service.py      # Watchlist management
│   │   └── recommendation_service.py # 🤖 KNN + Cache (CORE)
│   ├── routers/                      # API endpoints
│   │   ├── auth_routers.py          # /login, /register
│   │   ├── users_routers.py         # /users
│   │   ├── movies_routers.py        # /movies, /popular
│   │   ├── rating_routers.py        # /ratings
│   │   ├── playback_routers.py      # /playback
│   │   ├── watchlist_routers.py     # /watchlist
│   │   └── recommendation_routers.py # 🎯 /recommendationMovie, /randomMovie
│   └── utils/
│       ├── auth.py                   # JWT auth
│       └── email_validator.py        # Email validation
│
├── recommendation_system/             # 🤖 KNN Machine Learning
│   ├── train_model.py               # Offline KNN training
│   ├── recommend.py                 # Inference (predictions)
│   ├── models/                       # Trained artifacts
│   │   ├── knn_model.pkl            # Trained KNN model
│   │   ├── scaler.pkl               # StandardScaler
│   │   └── movie_metadata.pkl       # Metadata (IDs, genres)
│   └── requirements.txt              # Deps: scikit-learn, joblib, numpy
│
├── scripts/                          # 🔄 Utilities
│   ├── train_recommendations.py      # Entry point for training
│   ├── refresh_all_recommendations.py # Batch refresh for all users
│   ├── hash_existing_password.py     # Migrate passwords
│   └── test_mongo_ping.py            # Check MongoDB
│
├── frontend/                         # 🎨 React Web Interface
│   ├── src/
│   │   ├── components/               # React Components
│   │   │   ├── Login.js              # Login page
│   │   │   ├── Home.js               # Recommended movies grid
│   │   │   ├── MyList.js             # User watchlist
│   │   │   ├── Recommend.js          # Animated carousel
│   │   │   └── Header.js             # Navigation
│   │   ├── App.js                    # Routing
│   │   └── index.js                  # Entry point
│   ├── public/                       # Static assets
│   ├── package.json                  # React dependencies
│   └── README.md                     # Frontend docs
│
├── tests/                            # ✅ Tests
│   ├── test_config.py
│   ├── test_users_and_auth_routers.py
│   ├── test_movies_router_errors.py
│   └── test_recommendation_router.py
│
├── .env                              # 🔐 Environment variables
├── .gitignore
├── requirements.txt                  # Python dependencies
├── pytest.ini
├── pyrightconfig.json
└── README.md                         # This file
```

---

## 🚀 Quick Start

### 1️⃣ **Prerequisites**

```bash
- Python 3.8+
- Node.js 16+
- MongoDB (Cloud or Local)
- TMDB API Key
```

### 2️⃣ **Backend Setup**

```bash
# Clone
git clone <fork-url>
cd Netflix-Randomize

# Virtual env
python -m venv venv
venv\Scripts\activate  # Windows

# Install
pip install -r requirements.txt

# Create .env
cat > .env << EOF
MONGO_URI=mongodb+srv://user:pass@cluster.mongodb.net/?appName=Cluster
DB_NAME=netflix
TMDB_BEARER_TOKEN=your_tmdb_token
SECRET_KEY=your_secret_key
API_PREFIX=/api
EOF
```

### 3️⃣ **Train KNN Model** (❗ REQUIRED)

```bash
# Train KNN with MongoDB movies
python scripts/train_recommendations.py
```

**Output:** `✅ Model, scaler, and metadata loaded successfully`

### 4️⃣ **Frontend Setup**

```bash
cd frontend
npm install
```

### 5️⃣ **Start Application**

```bash
# Terminal 1: Backend
cd Netflix-Randomize
venv\Scripts\activate
uvicorn backend.main:app --reload --host 0.0.0.0 --port 8000

# Terminal 2: Frontend
cd frontend
npm start
```

- Backend: http://localhost:8000
- Frontend: http://localhost:3000
- API Docs: http://localhost:8000/docs

### 6️⃣ **Login**

```
Email: teste@netflix.com
Password: 123456
```

---

## 📡 API Endpoints

### 🔐 **Authentication**
```
POST   /api/auth/login
POST   /api/auth/register
```

### 👤 **Users**
```
GET    /api/users/me
PUT    /api/users/<user_id>/profile
```

### 🎬 **Movies**
```
GET    /api/movies
GET    /api/movies/<movie_id>
GET    /api/fetch-popular
```

### ⭐ **Ratings**
```
POST   /api/ratings
GET    /api/ratings
```

### 📺 **Recommendations** 🎯
```
GET    /api/recommendationMovie      # List of recommendations
GET    /api/randomMovie              # Random movie
```

### 📋 **Watchlist & Playback**
```
POST   /api/watchlist/add
GET    /api/watchlist/detailed
DELETE /api/watchlist/remove/<movie_id>

POST   /api/playback
GET    /api/playback
```

---

## 🤖 Machine Learning (KNN)

### **Pipeline**
1. **Feature Extraction**: 32 features (one-hot genres, popularity, rating, log votes)
2. **Normalization**: StandardScaler
3. **Training**: KNN (n_neighbors=10, metric=cosine)
4. **Persistence**: joblib (.pkl files)
5. **Inference**: Cosine similarity between movies

### **Cold-Start**
- New user → POPULAR movies
- User with history → KNN
- Valid cache → return from MongoDB (~100ms)

---

## 🎨 React Frontend

### **Pages**
- **Login**: JWT authentication
- **Home**: Recommended movies grid
- **My List**: User watchlist
- **Recommend Movie**: Animated carousel

### **Features**
- 🎲 Animated carousel like "case opening"
- 📺 Responsive movie grid
- 📱 Netflix dark theme
- 🔄 Smooth navigation

---

## 🧪 Tests

```bash
# All 20 tests
pytest -q

# Result:
# 20 passed, 2 warnings ✅
```

**Included tests:**
- Auth (login, JWT, bcrypt)
- Users (CRUD, preferences)
- Movies (fetch, ObjectId sanitization)
- Ratings
- **Recommendations** (cache, cold-start, KNN)
- Playback & Watchlist

---

## 📊 Automatic Logs

```
✅ Cache HIT: Return recommendations from MongoDB
❌ Cache MISS: Generate new via KNN
✨ Cold-start: Return popular movies
🤖 KNN invoked: Model in use
```

---

## 🔐 Security

- JWT with expiration
- bcrypt password hashing
- Email validation
- CORS configuration
- ObjectId → string serialization
- Input validation (Pydantic)

---

## 📦 Dependencies

**Backend:**
```
fastapi, uvicorn, pymongo, pydantic, python-jose, passlib, requests, python-dotenv
```

**Frontend:**
```
react, react-router-dom, axios, styled-components
```

**ML:**
```
scikit-learn, joblib, numpy, scipy
```

**Testing:**
```
pytest, httpx
```

---

## 🎯 Future Improvements

- [ ] Collaborative Filtering
- [ ] Deep Learning embeddings
- [ ] Hybrid approach (content + collab)
- [ ] Push notifications
- [ ] Mobile app (React Native)
- [ ] Docker & CI/CD
- [ ] Redis caching
- [ ] Social features

---

## 🆘 Troubleshooting

| Problem | Solution |
|----------|---------|
| KNN unavailable | `python scripts/train_recommendations.py` |
| No MONGO_URI | Fill .env |
| No recommendations | New user → popular movies |
| CORS error | Proxy configured in React |
| Frontend not loading | `npm install` and `npm start` |

---

## 📝 License

MIT License

---

## 🤝 Contribute

1. Fork
2. Branch (`git checkout -b feature/X`)
3. Commit (`git commit -m 'Add X'`)
4. Push (`git push origin feature/X`)
5. PR

---

**Made with ❤️ • v1.0.0 • April 2026 • ✅ Production Ready**