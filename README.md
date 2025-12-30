# Netflix-Randomize

## Description
This project is a Netflix clone API that allows fetching movie data from TMDB (The Movie Database) and storing it in a MongoDB Atlas database. It provides endpoints to retrieve popular movies and detailed information about specific movies, with automatic saving to avoid duplicates.

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
