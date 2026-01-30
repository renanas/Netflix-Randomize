# Validação de Email - Documentação

## 🔍 Resumo da Implementação

O projeto agora tem **validação de email em 3 níveis**:

### 1️⃣ **Validação Automática pelo Pydantic (EmailStr)**
- Feita automaticamente em todos os modelos que usam `EmailStr`
- Valida o formato básico de email
- **Onde funciona**: Criação de usuário e Login

### 2️⃣ **Validação de Email Duplicado (Banco de Dados)**
- Verifica se o email já está cadastrado no MongoDB
- Retorna erro específico: `"Email {email} já está cadastrado"`
- **Onde funciona**: Na criação de usuário (`POST /users`)

### 3️⃣ **Validação Adicional (Opcional)**
- Classe `EmailValidator` em `backend/utils/email_validator.py`
- Pode validar domínios descartáveis e formato mais rigoroso
- **Uso opcional** em endpoints conforme necessidade

---

## 📋 Como Funciona na Prática

### ✅ Criação de Usuário (`POST /users`)

```
1. Pydantic valida automaticamente o email (EmailStr)
   ❌ Se formato inválido → Erro 422
   
2. Repository valida se email já existe
   ❌ Se existe → Erro 400: "Email {email} já está cadastrado"
   
3. Se tudo ok → Usuário criado com sucesso ✓
```

### ✅ Login (`POST /login`)

```
1. Pydantic valida automaticamente o email (EmailStr)
   ❌ Se formato inválido → Erro 422
   
2. Repository valida se email existe
   ❌ Se não existe → Erro 401: "Email {email} não encontrado"
   
3. Repository valida se senha está correta
   ❌ Se incorreta → Erro 401: "Senha incorreta"
   
4. Se tudo ok → Token JWT retornado ✓
```

---

## 💻 Exemplos de Uso

### Criar Usuário (Válido)

```bash
curl -X POST http://localhost:8000/users \
  -H "Content-Type: application/json" \
  -d '{
    "email": "usuario@example.com",
    "senha": "senha123",
    "plano": "premium",
    "pais": "Brasil",
    "profile": {...},
    "user_behavior": {...}
  }'
```

**Resposta:**
```json
{
  "message": "User created successfully",
  "user_id": "507f1f77bcf86cd799439011"
}
```

---

### Criar Usuário (Email Inválido)

```bash
curl -X POST http://localhost:8000/users \
  -H "Content-Type: application/json" \
  -d '{
    "email": "email-invalido",
    ...
  }'
```

**Resposta:**
```json
{
  "detail": [
    {
      "type": "value_error",
      "loc": ["body", "email"],
      "msg": "value is not a valid email address: ..."
    }
  ]
}
```

---

### Criar Usuário (Email Duplicado)

```bash
curl -X POST http://localhost:8000/users \
  -H "Content-Type: application/json" \
  -d '{
    "email": "usuario@example.com",  # Email já existe
    ...
  }'
```

**Resposta:**
```json
{
  "detail": "Email usuario@example.com já está cadastrado"
}
```

---

### Login (Sucesso)

```bash
curl -X POST http://localhost:8000/login \
  -H "Content-Type: application/json" \
  -d '{
    "email": "usuario@example.com",
    "senha": "senha123"
  }'
```

**Resposta:**
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer"
}
```

---

### Login (Email Não Encontrado)

```bash
curl -X POST http://localhost:8000/login \
  -H "Content-Type: application/json" \
  -d '{
    "email": "naoexiste@example.com",
    "senha": "qualquer"
  }'
```

**Resposta:**
```json
{
  "detail": "Email naoexiste@example.com não encontrado"
}
```

---

### Login (Senha Incorreta)

```bash
curl -X POST http://localhost:8000/login \
  -H "Content-Type: application/json" \
  -d '{
    "email": "usuario@example.com",
    "senha": "senhaerrada"
  }'
```

**Resposta:**
```json
{
  "detail": "Senha incorreta"
}
```

---

## 🔧 Como Usar a Validação Adicional (Opcional)

### Importar e usar EmailValidator

```python
from backend.utils.email_validator import EmailValidator

# Validar formato
is_valid, error = EmailValidator.is_valid_format("usuario@example.com")

# Validar domínios descartáveis
is_disposable, msg = EmailValidator.is_disposable("user@tempmail.com")

# Validação completa
is_valid, error = EmailValidator.validate_email(
    "usuario@example.com",
    check_disposable=True  # Bloquear domínios descartáveis
)
```

### Integrar em um router (Exemplo)

```python
from backend.utils.email_validator import EmailValidator

@router.post("/users")
def create_user(user: UserCreate):
    # Validação adicional (além do Pydantic)
    is_valid, error = EmailValidator.validate_email(
        user.email,
        check_disposable=True
    )
    if not is_valid:
        raise HTTPException(status_code=400, detail=error)
    
    # ... resto do código
```

---

## 📊 Tabela de Códigos de Status HTTP

| Código | Situação | Mensagem |
|--------|----------|----------|
| **201** | ✅ Usuário criado | "User created successfully" |
| **400** | ❌ Email duplicado | "Email {email} já está cadastrado" |
| **400** | ❌ Formato inválido | Erro do Pydantic (EmailStr) |
| **401** | ❌ Email não existe | "Email {email} não encontrado" |
| **401** | ❌ Senha incorreta | "Senha incorreta" |
| **422** | ❌ Validação Pydantic | Erro de formato/tipo |

---

## 🎯 Arquivos Modificados

- `backend/repository/user_repository.py` - Validação de email duplicado
- `backend/routers/users_routers.py` - Tratamento de erros na criação
- `backend/routers/auth_routers.py` - Tratamento de erros no login
- `backend/utils/email_validator.py` - Novo utilitário (opcional)

---

## ⚠️ Notas Importantes

1. **EmailStr (Pydantic)** - Já vinha no projeto e é obrigatório em todos os endpoints
2. **Validação de Duplicado** - Funciona automaticamente na criação de usuário
3. **Mensagens de Erro** - São específicas para facilitar o debug no frontend
4. **EmailValidator** - É um utilitário adicional para validações mais rigorosas (pode ativar quando desejar)

---

## 📝 Para o Frontend

Tratar os seguintes casos:

```javascript
// Tentativa de criar usuário com email inválido
// Status: 422
// Mensagem: Erro de validação do Pydantic

// Tentativa de criar usuário com email duplicado
// Status: 400
// Mensagem: "Email {email} já está cadastrado"

// Tentativa de login com email inválido
// Status: 422
// Mensagem: Erro de validação do Pydantic

// Tentativa de login com email não registrado
// Status: 401
// Mensagem: "Email {email} não encontrado"

// Tentativa de login com senha incorreta
// Status: 401
// Mensagem: "Senha incorreta"
```
