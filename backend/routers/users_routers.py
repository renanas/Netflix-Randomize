from fastapi import APIRouter, HTTPException
from backend.models.user import UserCreate, UserUpdate
from backend.repository.user_repository import UserRepository

router = APIRouter()

user_repo = None

def get_repo():
    global user_repo
    if user_repo is None:
        user_repo = UserRepository()
    return user_repo

@router.post("/users", response_model=dict)
def create_user(user: UserCreate):
    """
    Create a new user.
    Automatically validates email format via Pydantic (EmailStr).
    Checks if email is already registered.
    """
    try:
        repo = get_repo()
        user_id = repo.create_user(user)
        return {"message": "User created successfully", "user_id": user_id}
    except ValueError as e:
        # Email already registered error
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=503, detail=f"Service unavailable: {str(e)}")

@router.get("/users", response_model=list)
def get_all_users():
    """
    Get all users.
    """
    try:
        repo = get_repo()
        users = repo.get_all_users()
        return users
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=503, detail=str(e))

@router.get("/users/{user_id}", response_model=dict)
def get_user(user_id: str):
    """
    Get a user by ID.
    """
    try:
        repo = get_repo()
        user = repo.get_user_by_id(user_id)
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        return user
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=503, detail=str(e))

@router.put("/users/{user_id}", response_model=dict)
def update_user(user_id: str, update_data: UserUpdate):
    """
    Update a user by ID.
    """
    try:
        repo = get_repo()
        updated = repo.update_user(user_id, update_data)
        if not updated:
            raise HTTPException(status_code=404, detail="User not found or no changes made")
        return {"message": "User updated successfully"}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=503, detail=str(e))

@router.delete("/users/{user_id}", response_model=dict)
def delete_user(user_id: str):
    """
    Soft delete a user by ID.
    """
    try:
        repo = get_repo()
        deleted = repo.delete_user(user_id)
        if not deleted:
            raise HTTPException(status_code=404, detail="User not found")
        return {"message": "User deleted successfully"}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=503, detail=str(e))
