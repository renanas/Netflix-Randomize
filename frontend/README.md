# Netflix Randomize - Frontend

Frontend completo para o sistema de recomendação de filmes Netflix Randomize com roleta de seleção aleatória!

## 🎬 Funcionalidades

✅ **Login com JWT** - Autenticação segura  
✅ **Filmes Recomendados** - Grid interativo com recomendações personalizadas via KNN  
✅ **Roleta Aleatória** - Componente visual com animação de girar e selecionar filme aleatório  
✅ **Atualizar Recomendações** - Botão para reforçar o cache com novas recomendações  
✅ **Design Netflix** - Interface escura estilo Netflix com cores vibrantes  
✅ **Responsivo** - Funciona em desktop, tablet e mobile  

## 📋 Arquivos

```
frontend/
├── index.html           # Página de login
├── home.html            # Página principal com roleta e filmes
├── style.css            # Estilos CSS (dark theme, animações)
├── config.js            # Configuração da API e helper functions
├── script-login.js      # Lógica de login
├── script-home.js       # Lógica da roleta e carregamento de filmes
└── README.md            # Este arquivo
```

## 🚀 Como Usar

### 1. Pré-requisitos

- Backend FastAPI rodando em `http://localhost:8000`
- Modelo KNN já treinado (`python scripts/train_recommendations.py`)
- Usuário no banco de dados para login

### 2. Abrir o Frontend

Abra `index.html` no navegador:

```bash
# Opção 1: Abrir direto no navegador
# Navegue até: file:///seu/path/netflix-randomize/frontend/index.html

# Opção 2: Usar Live Server (recomendado)
# No VS Code: Clique com botão direito → "Open with Live Server"

# Opção 3: Usar Python server
cd frontend
python -m http.server 8080
# Acesse: http://localhost:8080
```

### 3. Login

Use as credenciais de teste:

```
Email: teste@netflix.com
Senha: 123456
```

Ou use credenciais de qualquer usuário cadastrado no MongoDB.

### 4. Usar o Sistema

#### 📺 Página Home

- **Grid de Filmes**: Mostra 20 filmes recomendados baseado no histórico do usuário
- **Botão Girar**: Centro da página - clique para girar a roleta e descubrir um filme aleatório
- **Botão Atualizar**: Força recálculo de recomendações via KNN

#### 🎲 Roleta de Filmes

1. Clique no botão **"🎲 GIRAR & DESCOBRIR"**
2. A roleta gira com animação (4 segundos)
3. O sistema chama `/randomMovie` da API
4. Resultado aparece em destaque com detalhes do filme

## 🔧 Configuração da API

Edite `config.js` para mudar a URL da API:

```javascript
const API_BASE_URL = 'http://localhost:8000';
```

## 📡 Endpoints Utilizados

O frontend usa os seguintes endpoints do backend:

```
POST   /login                      # Login (recebe email/senha, retorna JWT)
GET    /recommendationMovie        # Lista 20 filmes recomendados
GET    /randomMovie                # 1 filme aleatório dos recomendados
POST   /recommendationMovie/refresh # Força atualizar recomendações
```

## 🎨 Customização

### Cores

Edite `:root` no `style.css`:

```css
:root {
    --primary-color: #e50914;      /* Vermelho Netflix */
    --dark-bg: #141414;            /* Fundo escuro */
    --accent-color: #ffd700;       /* Dourado */
    --success-color: #4caf50;      /* Verde */
    --error-color: #f44336;        /* Vermelho erro */
}
```

### Animação da Roleta

Altere a duração em `script-home.js`:

```javascript
await new Promise(resolve => setTimeout(resolve, 4000)); // 4 segundos
```

Or no CSS:

```css
animation: spin 4s cubic-bezier(0.25, 0.46, 0.45, 0.94); /* Duração */
```

## 📱 Responsividade

- **Desktop** (>768px): Grid 5+ colunas, roleta grande
- **Tablet** (480px-768px): Grid 3-4 colunas, roleta média
- **Mobile** (<480px): Grid 2 colunas, roleta pequena

## 🔐 Segurança

- Token JWT armazenado em `localStorage`
- Token incluído em todas as requisições (header `Authorization: Bearer token`)
- Redirecionamento automático se token expirar
- Logout limpa dados locais

## 🐛 Troubleshooting

**"Failed to fetch recommendations"**
- Verifique se backend está rodando em `http://localhost:8000`
- Verifique CORS no backend
- Verifique se token está válido

**"No recommendations available"**
- Usuário não tem histórico de visualização
- Execute `/recommendationMovie/refresh` para forçar recálculo
- Verifique se modelo KNN está treinado

**Roleta não funciona**
- Verifique console (F12) para erros
- Verifique se endpoint `/randomMovie` existe
- Verifique se atualmente há recomendações carregadas

## 📊 Fluxo de Dados

```
LOGIN
  ↓
Token JWT → localStorage
  ↓
HOME (verificar autenticação)
  ↓
GET /recommendationMovie → 20 filmes
  ↓
Exibir grid + roleta ativa
  ↓
Usuário clica GIRAR
  ↓
GET /randomMovie (usa token)
  ↓
Exibir resultado em destaque
```

## 🎯 Próximas Melhorias

- [ ] Adicionar aba "Meus Filmes Assistidos"
- [ ] Integrar com player de vídeo
- [ ] Notificações push para novos filmes
- [ ] Histórico de filmes girados
- [ ] Social sharing
- [ ] Dark/Light mode toggle
- [ ] Busca e filtros avançados

## 📝 Notas

- O frontend é agnóstico sobre quantos filmes são recomendados
- Cada logout limpa automaticamente o token
- A roleta sempre tira um filme dos recomendados atuais
- Recomendações são cacheadas no backend por 24h (configurável)

---

Desenvolvido com ❤️ para Netflix Randomize
