from pydantic import BaseModel, EmailStr
from typing import List, Dict

class Profile(BaseModel):
    nome_perfil: str
    avatar: str
    classificacao_etaria: str
    idioma_preferido: str
    minha_lista: List[int]  # IDs de filmes

class UserBehavior(BaseModel):
    historico_visualizacao: List[int]  # IDs de filmes assistidos
    status_reproducao: Dict[str, int]  # ID do filme (string): tempo parado (em segundos)
    avaliacao: Dict[str, int]  # ID do filme (string): 0 (dislike) ou 1 (like)
    generos_favoritos: List[str]

class User(BaseModel):
    email: EmailStr
    senha: str  # Senha hasheada
    plano: str
    pais: str
    profile: Profile
    user_behavior: UserBehavior

class UserCreate(BaseModel):
    email: EmailStr
    senha: str
    plano: str
    pais: str
    profile: Profile
    user_behavior: UserBehavior

class UserUpdate(BaseModel):
    email: EmailStr = None
    senha: str = None
    plano: str = None
    pais: str = None
    profile: Profile = None
    user_behavior: UserBehavior = None

class LoginRequest(BaseModel):
    email: EmailStr
    senha: str