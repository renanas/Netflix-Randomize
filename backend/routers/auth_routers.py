from fastapi import APIRouter, HTTPException
from backend.models.user import LoginRequest
from backend.repository.user_repository import UserRepository
from backend.utils.auth import create_access_token
from datetime import timedelta

router = APIRouter()

user_repo = None

def get_repo():
    global user_repo
    if user_repo is None:
        user_repo = UserRepository()
    return user_repo

@router.post("/login", response_model=dict)
def login(login_data: LoginRequest):
    """
    Authenticate a user and return an access token.
    Valida automaticamente o email pelo Pydantic (EmailStr).
    Verifica se o usuário existe e se a senha está correta.
    """
    try:
        repo = get_repo()
        user = repo.authenticate_user(login_data.email, login_data.senha)
        access_token_expires = timedelta(minutes=30)
        access_token = create_access_token(
            data={"sub": str(user["_id"])}, expires_delta=access_token_expires
        )
        return {"access_token": access_token, "token_type": "bearer"}
    except ValueError as e:
        # Email não encontrado ou senha incorreta
        raise HTTPException(status_code=401, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=503, detail=f"Service unavailable: {str(e)}")

@router.post("/logout", response_model=dict)
def logout():
    """
    Logout a user. In a stateless JWT setup, this is handled client-side.
    """
    return {"message": "Logged out successfully"}