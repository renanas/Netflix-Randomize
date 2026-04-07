# 🎬 Netflix Randomize

Um sistema inteligente de recomendação de filmes com **Machine Learning (KNN)**, **carrossel animado de filmes aleatórios** e interface estilo **Netflix** em React!

## ✨ Funcionalidades Principais

### 🤖 **Recomendação com Machine Learning (KNN)**
- ✅ Modelo KNN treinado offline em filmes do TMDB
- ✅ Vetorização de features: gêneros (one-hot), popularidade, votos, log(vote_count)
- ✅ Recomendações personalizadas baseadas no histórico do usuário
- ✅ Cold-start handling: filmes populares para novos usuários
- ✅ Caching inteligente em MongoDB (atualização a cada geração)
- ✅ Batch refresh: script para pré-computar recomendações

### 🎲 **Carrossel de Filmes Aleatórios**
- ✅ Componente visual animado estilo "abertura de caixa" (passa filmes rapidamente e para em um)
- ✅ Seleciona aleatoriamente filmes das recomendações
- ✅ Exibe resultado em destaque com sinopse, classificação e banner
- ✅ Totalmente responsivo (desktop, tablet, mobile)

### 👤 **Autenticação e Gerenciamento de Usuários**
- ✅ Login/Registro com JWT
- ✅ Hash de senha com bcrypt
- ✅ Validação de email
- ✅ Perfil de usuário com preferências
- ✅ Histórico de visualização
- ✅ Sistema de avaliações (ratings)

### 📺 **Interface em React**
- ✅ Páginas: Login, Home (grid de filmes), My List (watchlist), Recommend Movie (carrossel)
- ✅ Navegação estilo Netflix com header fixo
- ✅ Grid interativo com filmes recomendados
- ✅ Integração com TMDB para posters e dados
- ✅ Dark theme Netflix

### 🎬 **Integração com TMDB**
- ✅ Fetch automático de filmes populares
- ✅ Armazenamento em MongoDB (sem duplicatas)
- ✅ Enriquecimento com dados detalhados
- ✅ Suporte a videos, créditos, reviews

### 📊 **Logs e Monitoramento**
- ✅ Logs detalhados de recomendações (cache hit/miss)
- ✅ Rastreamento de uso do KNN
- ✅ Cold-start detection
- ✅ Error tracking

### 🧪 **Testes Automatizados**
- ✅ 20 testes pytest (100% passando)
- ✅ Testes de: auth, users, movies, ratings, recommendations
- ✅ Cobertura de isolamento em testes via mocking
- ✅ Validação de serialização (ObjectId → string)

---

## 🏗️ Arquitetura

```
Netflix-Randomize/
├── backend/                          # 🔧 API FastAPI
│   ├── main.py                       # Aplicação principal
│   ├── config.py                     # Configurações
│   ├── database/
│   │   └── mongodb_connection.py     # Conexão MongoDB
│   ├── models/                       # Pydantic models
│   │   ├── user.py                   # User com preferences, behavior
│   │   ├── rating.py                 # Rating de filmes
│   │   ├── watchlist.py              # Watchlist
│   │   └── movie.py                  # Movie (TMDB)
│   ├── repository/                   # Data access layer
│   │   ├── user_repository.py        # CRUD users
│   │   ├── movie_repository.py       # CRUD movies (com sanitização)
│   │   ├── rating_repository.py      # CRUD ratings
│   │   └── recommendation_repository.py  # Cache de recomendações
│   ├── services/                     # Business logic
│   │   ├── user_service.py           # Lógica de usuários
│   │   ├── tmdb_service.py           # Fetch TMDB
│   │   ├── rating_service.py         # Cálculos de ratings
│   │   ├── playback_service.py       # Histórico de playback
│   │   ├── watchlist_service.py      # Gerenciamento de watchlist
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
│       └── email_validator.py        # Validação email
│
├── recommendation_system/             # 🤖 KNN Machine Learning
│   ├── train_model.py               # Treinamento offline do KNN
│   ├── recommend.py                 # Inference (predições)
│   ├── models/                       # Artifacts treinados
│   │   ├── knn_model.pkl            # Modelo KNN treinado
│   │   ├── scaler.pkl               # StandardScaler
│   │   └── movie_metadata.pkl       # Metadados (IDs, gêneros)
│   └── requirements.txt              # Deps: scikit-learn, joblib, numpy
│
├── scripts/                          # 🔄 Utilitários
│   ├── train_recommendations.py      # Entry point para treinamento
│   ├── refresh_all_recommendations.py # Batch refresh para todos os users
│   ├── hash_existing_password.py     # Migrate senhas
│   └── test_mongo_ping.py            # Verificar MongoDB
│
├── frontend/                         # 🎨 Interface Web React
│   ├── src/
│   │   ├── components/               # Componentes React
│   │   │   ├── Login.js              # Página de login
│   │   │   ├── Home.js               # Grid de filmes recomendados
│   │   │   ├── MyList.js             # Watchlist do usuário
│   │   │   ├── Recommend.js          # Carrossel animado
│   │   │   └── Header.js             # Navegação
│   │   ├── App.js                    # Roteamento
│   │   └── index.js                  # Entry point
│   ├── public/                       # Assets estáticos
│   ├── package.json                  # Dependências React
│   └── README.md                     # Docs frontend
│
├── tests/                            # ✅ Testes
│   ├── test_config.py
│   ├── test_users_and_auth_routers.py
│   ├── test_movies_router_errors.py
│   └── test_recommendation_router.py
│
├── .env                              # 🔐 Variáveis de ambiente
├── .gitignore
├── requirements.txt                  # Dependencies Python
├── pytest.ini
├── pyrightconfig.json
└── README.md                         # Este arquivo
```

---

## 🚀 Quick Start

### 1️⃣ **Pré-requisitos**

```bash
- Python 3.8+
- Node.js 16+
- MongoDB (Cloud ou Local)
- TMDB API Key
```

### 2️⃣ **Setup Backend**

```bash
# Clone
git clone <fork-url>
cd Netflix-Randomize

# Virtual env
python -m venv venv
venv\Scripts\activate  # Windows

# Install
pip install -r requirements.txt

# Criar .env
cat > .env << EOF
MONGO_URI=mongodb+srv://user:pass@cluster.mongodb.net/?appName=Cluster
DB_NAME=netflix
TMDB_BEARER_TOKEN=seu_token_tmdb
SECRET_KEY=sua_chave_secreta
API_PREFIX=/api
EOF
```

### 3️⃣ **Treinar Modelo KNN** (❗ OBRIGATÓRIO)

```bash
# Treina KNN com filmes do MongoDB
python scripts/train_recommendations.py
```

**Output:** `✅ Model, scaler, and metadata loaded successfully`

### 4️⃣ **Setup Frontend**

```bash
cd frontend
npm install
```

### 5️⃣ **Iniciar Aplicação**

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
- Docs API: http://localhost:8000/docs

### 6️⃣ **Login**

```
Email: teste@netflix.com
Senha: 123456
```

---

## 📡 Endpoints da API

### 🔐 **Autenticação**
```
POST   /api/auth/login
POST   /api/auth/register
```

### 👤 **Usuários**
```
GET    /api/users/me
PUT    /api/users/<user_id>/profile
```

### 🎬 **Filmes**
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

### 📺 **Recomendações** 🎯
```
GET    /api/recommendationMovie      # Lista de recomendações
GET    /api/randomMovie              # Filme aleatório
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
1. **Feature Extraction**: 32 features (gêneros one-hot, popularity, rating, log votes)
2. **Normalization**: StandardScaler
3. **Training**: KNN (n_neighbors=10, metric=cosine)
4. **Persistence**: joblib (.pkl files)
5. **Inference**: Similaridade cosseno entre filmes

### **Cold-Start**
- Novo usuário → filmes POPULARES
- Usuário com histórico → KNN
- Cache válido → retorna do MongoDB (~100ms)

---

## 🎨 Frontend React

### **Páginas**
- **Login**: Autenticação JWT
- **Home**: Grid de filmes recomendados
- **My List**: Watchlist do usuário
- **Recommend Movie**: Carrossel animado de filmes aleatórios

### **Features**
- 🎲 Carrossel animado estilo "abertura de caixa"
- 📺 Grid responsivo de filmes
- 📱 Dark theme Netflix
- 🔄 Navegação suave

---

## 🧪 Testes

```bash
# Todos os 20 testes
pytest -q

# Resultado:
# 20 passed, 2 warnings ✅
```

**Testes inclusos:**
- Auth (login, JWT, bcrypt)
- Users (CRUD, preferences)
- Movies (fetch, ObjectId sanitization)
- Ratings
- **Recommendations** (cache, cold-start, KNN)
- Playback & Watchlist

---

## 📊 Logs Automáticos

```
✅ Cache HIT: Retorna recomendações do MongoDB
❌ Cache MISS: Gera novas via KNN
✨ Cold-start: Retorna filmes populares
🤖 KNN invoked: Modelo em uso
```

---

## 🔐 Segurança

- JWT com expiração
- bcrypt password hashing
- Email validation
- CORS configuration
- ObjectId → string serialization
- Input validation (Pydantic)

---

## 📦 Dependências

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

## 🎯 Próximas Melhorias

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

| Problema | Solução |
|----------|---------|
| KNN unavailable | `python scripts/train_recommendations.py` |
| No MONGO_URI | Preencher `.env` |
| No recommendations | Usuário novo → filmes populares |
| CORS error | Proxy configurado no React |
| Frontend não carrega | `npm install` e `npm start` |

---

## 📝 Licença

MIT License

---

## 🤝 Contribuir

1. Fork
2. Branch (`git checkout -b feature/X`)
3. Commit (`git commit -m 'Add X'`)
4. Push (`git push origin feature/X`)
5. PR

---

**Made with ❤️ • v1.0.0 • Abril de 2026 • ✅ Production Ready**