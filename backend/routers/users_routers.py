from fastapi import APIRouter, HTTPException
from backend.models.user import UserCreate, UserUpdate
from backend.services.user_service import UserService

router = APIRouter()

# Instantiate a new service per request to avoid stale global state across tests
# and ensure test-time monkeypatching of repository modules is applied.

def get_service():
    return UserService()

@router.post("/users", response_model=dict)
def create_user(user: UserCreate):
    """
    Create a new user.
    Automatically validates email format via Pydantic (EmailStr).
    Checks if email is already registered.
    """
    try:
        service = get_service()
        user_id = service.create_user(user)
        return {"message": "User created successfully", "user_id": user_id}
    except ValueError as e:
        # Email already registered error
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        print('users router error create_user', repr(e))
        raise HTTPException(status_code=503, detail=f"Service unavailable: {str(e)}")

@router.get("/users", response_model=list)
def get_all_users():
    """
    Get all users.
    """
    try:
        service = get_service()
        users = service.get_all_users()
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
        service = get_service()
        user = service.get_user_by_id(user_id)
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
        service = get_service()
        updated = service.update_user(user_id, update_data)
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
        service = get_service()
        deleted = service.delete_user(user_id)
        if not deleted:
            raise HTTPException(status_code=404, detail="User not found")
        return {"message": "User deleted successfully"}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=503, detail=str(e))
