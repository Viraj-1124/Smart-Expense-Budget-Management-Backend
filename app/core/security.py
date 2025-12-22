import hashlib
from passlib.context import CryptContext
from datetime import datetime,timedelta
from jose import jwt

pwd_context = CryptContext(schemes=["bcrypt"],deprecated="auto")

SECRET_KEY = "SECRET_KEY_CHANGE_LATER"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60

def hash_password(password: str) -> str:
    # Pre-hash to avoid bcrypt 72-byte limit
    sha256 = hashlib.sha256(password.encode("utf-8")).hexdigest()
    return pwd_context.hash(sha256)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    sha256 = hashlib.sha256(plain_password.encode("utf-8")).hexdigest()
    return pwd_context.verify(sha256, hashed_password)

def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp":expire})
    return jwt.encode(to_encode,SECRET_KEY,algorithm=ALGORITHM)