from fastapi import APIRouter, HTTPException
from backend.models.user import UserCreate, UserUpdate
from backend.repository.user_repository import UserRepository

router = APIRouter()

user_repo = UserRepository()

@router.post("/users", response_model=dict)
def create_user(user: UserCreate):
    """
    Create a new user.
    """
    try:
        user_id = user_repo.create_user(user)
        return {"message": "User created successfully", "user_id": user_id}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/users", response_model=list)
def get_all_users():
    """
    Get all users.
    """
    try:
        users = user_repo.get_all_users()
        return users
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/users/{user_id}", response_model=dict)
def get_user(user_id: str):
    """
    Get a user by ID.
    """
    try:
        user = user_repo.get_user_by_id(user_id)
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        return user
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.put("/users/{user_id}", response_model=dict)
def update_user(user_id: str, update_data: UserUpdate):
    """
    Update a user by ID.
    """
    try:
        updated = user_repo.update_user(user_id, update_data)
        if not updated:
            raise HTTPException(status_code=404, detail="User not found or no changes made")
        return {"message": "User updated successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.delete("/users/{user_id}", response_model=dict)
def delete_user(user_id: str):
    """
    Soft delete a user by ID.
    """
    try:
        deleted = user_repo.delete_user(user_id)
        if not deleted:
            raise HTTPException(status_code=404, detail="User not found")
        return {"message": "User deleted successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
