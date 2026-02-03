from passlib.context import CryptContext
from datetime import datetime, timedelta
import jwt
from typing import Optional
from fastapi import HTTPException, Header

# JWT configuration
SECRET_KEY = "your-secret-key"  # TODO: Change to a secure key in production
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

pwd_context = CryptContext(schemes=["pbkdf2_sha256"], deprecated="auto")

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def decode_access_token(token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except jwt.ExpiredSignatureError:
        return None
    except jwt.InvalidTokenError:
        return None

def verify_token(authorization: Optional[str] = Header(None)) -> str:
    """
    Verify JWT token from Authorization header.
    Returns user_id if valid, raises HTTPException if invalid.
    
    Expected header format: "Authorization: Bearer <token>"
    """
    if not authorization:
        raise HTTPException(status_code=401, detail="Missing authorization header")
    
    # Expected format: "Bearer <token>"
    parts = authorization.split()
    if len(parts) != 2 or parts[0].lower() != "bearer":
        raise HTTPException(status_code=401, detail="Invalid authorization header format")
    
    token = parts[1]
    payload = decode_access_token(token)
    
    if not payload or "sub" not in payload:
        raise HTTPException(status_code=401, detail="Invalid or expired token")
    
    return payload["sub"]