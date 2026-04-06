from fastapi import APIRouter, HTTPException
from backend.models.user import LoginRequest
from backend.repository.user_repository import UserRepository
from backend.utils.auth import create_access_token
from datetime import timedelta

router = APIRouter()

# Instantiate repository per request to avoid stale state in unit tests

def get_repo():
    return UserRepository()

@router.post("/login", response_model=dict)
def login(login_data: LoginRequest):
    """
    Authenticate a user and return an access token.
    Automatically validates email format via Pydantic (EmailStr).
    Verifies user exists and password is correct.
    """
    try:
        repo = get_repo()
        user = repo.authenticate_user(login_data.email, login_data.password)
        access_token_expires = timedelta(minutes=30)
        access_token = create_access_token(
            data={"sub": str(user["_id"])}, expires_delta=access_token_expires
        )
        return {"access_token": access_token, "token_type": "bearer"}
    except ValueError as e:
        # Email not found or invalid password
        raise HTTPException(status_code=401, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=503, detail=f"Service unavailable: {str(e)}")

@router.post("/logout", response_model=dict)
def logout():
    """
    Logout a user. In a stateless JWT setup, this is handled client-side.
    """
    return {"message": "Logged out successfully"}