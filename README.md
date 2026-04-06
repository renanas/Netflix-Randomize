# 🎬 Netflix Randomize

Um sistema inteligente de recomendação de filmes com **Machine Learning (KNN)**, **roleta aleatória** e interface estilo **Netflix**!

## ✨ Funcionalidades Principais

### 🤖 **Recomendação com Machine Learning (KNN)**
- ✅ Modelo KNN treinado offline em filmes do TMDB
- ✅ Vetorização de features: gêneros (one-hot), popularidade, votos, log(vote_count)
- ✅ Recomendações personalizadas baseadas no histórico do usuário
- ✅ Cold-start handling: filmes populares para novos usuários
- ✅ Caching inteligente em MongoDB (atualização a cada geração)
- ✅ Batch refresh: script para pré-computar recomendações

### 🎲 **Roleta de Filmes Aleatória**
- ✅ Componente visual animado (4 segundos de girada)
- ✅ Seleciona aleatoriamente 1 filme das recomendações
- ✅ Exibe resultado em destaque com sinopse completa
- ✅ Totalmente responsivo (desktop, tablet, mobile)

### 👤 **Autenticação e Gerenciamento de Usuários**
- ✅ Login/Registro com JWT
- ✅ Hash de senha com bcrypt
- ✅ Validação de email
- ✅ Perfil de usuário com preferências
- ✅ Histórico de visualização
- ✅ Sistema de avaliações (ratings)

### 📺 **Recomendações de Filmes**
- ✅ Grid interativo com 20 filmes recomendados
- ✅ Baseado em histórico do usuário via KNN
- ✅ Atualização de cache com botão "Refresh"
- ✅ Integração com TMDB para dados de filmes
- ✅ Exibição de metadados: título, avaliação, gêneros, popularidade

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
├── frontend/                         # 🎨 Interface Web
│   ├── index.html                    # 🔐 Página de Login
│   ├── home.html                     # 🏠 Página Principal (Roleta + Grid)
│   ├── config.js                     # ⚙️  Configuração API
│   ├── style.css                     # 💅 Estilos (Netflix Dark Theme)
│   ├── script-login.js               # 📝 Lógica de Login
│   ├── script-home.js                # 🎲 Lógica da Roleta & Filmes
│   └── README.md                     # 📖 Docs frontend
│
├── tests/                            # ✅ Testes
│   ├── test_config.py
│   ├── test_users_and_auth_routers.py
│   ├── test_movies_router_errors.py
│   └── test_recommendation_router.py
│
├── .env                              # 🔐 Variáveis de ambiente
├── .gitignore
├── requirements.txt                  # Dependencies
├── pytest.ini
├── pyrightconfig.json
└── README.md                         # Este arquivo
```

---

## 🚀 Quick Start

### 1️⃣ **Pré-requisitos**

```bash
- Python 3.8+
- MongoDB (Cloud ou Local)
- TMDB API Key
```

### 2️⃣ **Setup**

```bash
# Clone
git clone <fork-url>
cd Netflix-Randomize

# Virtual env
python -m venv venv
venv\Scripts\activate  # Windows
# or source venv/bin/activate  # Linux/Mac

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

# Ou agendar via cron (Linux/Mac):
# 0 2 * * * /path/to/venv/bin/python /path/to/scripts/train_recommendations.py
```

**Output:** `✅ Model, scaler, and metadata loaded successfully`

### 4️⃣ **Iniciar Backend**

```bash
python -m uvicorn backend.main:app --reload

# Backend roda em: http://localhost:8000
# Docs: http://localhost:8000/docs (Swagger)
```

### 5️⃣ **Abrir Frontend**

```bash
# Opção 1: Live Server (VS Code)
# Clique direito em frontend/index.html → Open with Live Server

# Opção 2: Python HTTP Server
cd frontend
python -m http.server 8080
# Acesse: http://localhost:8080
```

### 6️⃣ **Login**

```
Email: teste@netflix.com
Senha: 123456
```

---

## 📡 Endpoints da API

### 🔐 **Autenticação**
```
POST   /api/login
POST   /api/register
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
GET    /api/popular
```

### ⭐ **Ratings**
```
POST   /api/ratings
GET    /api/ratings
```

### 📺 **Recomendações** 🎯
```
GET    /api/recommendationMovie      # ✅ Cache HIT ou ❌ Cache MISS
POST   /api/recommendationMovie/refresh
GET    /api/randomMovie              # Filme aleatório
```

### 📋 **Watchlist & Playback**
```
POST   /api/watchlist
GET    /api/watchlist
DELETE /api/watchlist/<movie_id>

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

## 🎨 Frontend

### **Features**
- 🔐 Login seguro com JWT
- 🎲 Roleta animada com 4 segundos de girada
- 📺 Grid de 20 filmes recomendados
- 📱 Responsivo (5 cols desktop → 2 cols mobile)
- 🎨 Dark theme Netflix (vermelho #e50914)

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
| CORS error | Adicionar frontend URL no backend |

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

**Made with ❤️ • v1.0.0 • Abril de 2026 • ✅ Production Ready** It provides endpoints to retrieve popular movies and detailed information about specific movies, with automatic saving to avoid duplicates.

## Features
- Fetch popular movies from TMDB API
- Retrieve detailed movie information (including videos and credits)
- Store movie data in MongoDB Atlas
- Avoid duplicate entries based on TMDB ID
- RESTful API built with FastAPI
- Comprehensive test suite

## Installation

### Prerequisites
- Python 3.8+
- MongoDB Atlas account
- TMDB API key

### Setup
1. Clone the repository:
   ```
   git clone https://github.com/yourusername/netflix-randomize.git
   cd netflix-randomize
   ```

2. Create a virtual environment:
   ```
   python -m venv venv
   ```

3. Activate the virtual environment:
   - Windows: `venv\Scripts\activate`
   - Linux/Mac: `source venv/bin/activate`

4. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

5. Create a `.env` file in the root directory with your credentials:
   ```
   MONGO_URI=mongodb+srv://yourusername:yourpassword@cluster.mongodb.net/?appName=Cluster
   DB_NAME=netflix
   TMDB_BEARER_TOKEN=your_tmdb_bearer_token
   # Optional, prefix for all API routes. e.g. "/api" or "v1".
   # Do not end with '/'.
   API_PREFIX=/api
   ```

## Usage

### Running the Application
To start the FastAPI server:
```
uvicorn backend.main:app --reload --host 127.0.0.1 --port 8000
```

Or for debugging:
```
python venv\Scripts\python.exe -m uvicorn backend.main:app --reload --log-level debug --host 127.0.0.1 --port 8000
```

### API Endpoints

- **GET /**: Welcome message
- **GET /fetch-popular?page=1**: Fetch popular movies from TMDB and save to database
- **GET /movie/{movie_id}**: Fetch detailed movie information and save to database

### Testing
Run the test suite:
```
python -m pytest scripts/
```

Or run individual test files:
```
python scripts/test_movie_repository.py
```

## API Documentation
Once the server is running, visit `http://127.0.0.1:8000/docs` for interactive API documentation.

## Project Structure
```
netflix-randomize/
├── backend/
│   ├── database/
│   │   ├── mongodb_connection.py
│   │   └── __init__.py
│   ├── repository/
│   │   ├── movie_repository.py
│   │   └── __init__.py
│   ├── routes/
│   ├── services/
│   │   ├── tmdb_service.py
│   │   └── __init__.py
│   └── main.py
├── scripts/
│   ├── test_*.py
│   └── debug_env.py
├── frontend/
├── requirements.txt
├── .env
└── README.md
```

## Contributing
1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests
5. Submit a pull request

## License
This project is licensed under the MIT License.

---

# Netflix-Randomize

## Descrição
Este projeto é uma API clone da Netflix que permite buscar dados de filmes do TMDB (The Movie Database) e armazená-los em um banco de dados MongoDB Atlas. Ele fornece endpoints para recuperar filmes populares e informações detalhadas sobre filmes específicos, com salvamento automático para evitar duplicatas.

## Funcionalidades
- Buscar filmes populares da API TMDB
- Recuperar informações detalhadas de filmes (incluindo vídeos e créditos)
- Armazenar dados de filmes no MongoDB Atlas
- Evitar entradas duplicadas com base no ID do TMDB
- API RESTful construída com FastAPI
- Conjunto abrangente de testes

## Instalação

### Pré-requisitos
- Python 3.8+
- Conta MongoDB Atlas
- Chave da API TMDB

### Configuração
1. Clone o repositório:
   ```
   git clone https://github.com/yourusername/netflix-randomize.git
   cd netflix-randomize
   ```

2. Crie um ambiente virtual:
   ```
   python -m venv venv
   ```

3. Ative o ambiente virtual:
   - Windows: `venv\Scripts\activate`
   - Linux/Mac: `source venv/bin/activate`

4. Instale as dependências:
   ```
   pip install -r requirements.txt
   ```

5. Crie um arquivo `.env` no diretório raiz com suas credenciais:
   ```
   MONGO_URI=mongodb+srv://seuusuario:suasenha@cluster.mongodb.net/?appName=Cluster
   DB_NAME=netflix
   TMDB_BEARER_TOKEN=seu_token_tmdb
   ```

## Uso

### Executando a Aplicação
Para iniciar o servidor FastAPI:
```
uvicorn backend.main:app --reload --host 127.0.0.1 --port 8000
```

Ou para depuração:
```
python venv\Scripts\python.exe -m uvicorn backend.main:app --reload --log-level debug --host 127.0.0.1 --port 8000
```

### Endpoints da API

- **GET /**: Mensagem de boas-vindas
- **GET /fetch-popular?page=1**: Buscar filmes populares do TMDB e salvar no banco
- **GET /movie/{movie_id}**: Buscar informações detalhadas do filme e salvar no banco

### Testes
Execute o conjunto de testes:
```
python -m pytest scripts/
```

Ou execute arquivos de teste individuais:
```
python scripts/test_movie_repository.py
```

## Documentação da API
Após iniciar o servidor, visite `http://127.0.0.1:8000/docs` para documentação interativa da API.

## Estrutura do Projeto
```
netflix-randomize/
├── backend/
│   ├── database/
│   │   ├── mongodb_connection.py
│   │   └── __init__.py
│   ├── repository/
│   │   ├── movie_repository.py
│   │   └── __init__.py
│   ├── routes/
│   ├── services/
│   │   ├── tmdb_service.py
│   │   └── __init__.py
│   └── main.py
├── scripts/
│   ├── test_*.py
│   └── debug_env.py
├── frontend/
├── requirements.txt
├── .env
└── README.md
```

## Contribuição
1. Faça um fork do repositório
2. Crie uma branch de funcionalidade
3. Faça suas alterações
4. Adicione testes
5. Envie um pull request

## Licença
Este projeto está licenciado sob a Licença MIT.
