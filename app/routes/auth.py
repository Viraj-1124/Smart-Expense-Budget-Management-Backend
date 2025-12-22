from fastapi import APIRouter, HTTPException, status, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.user import User
from app.schemas.user import UserCreate, UserLogin, Token
from app.core.security import hash_password, verify_password, create_access_token

router = APIRouter(prefix="/auth", tags = ["/Authentication"])


@router.post("/signup", status_code=201)
def  signup(user: UserCreate, db:Session =Depends(get_db)):
    existing_user = db.query(User).filter(User.email == user.email).first()

    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    
    new_user = User(
        email = user.email,
        hashed_password = hash_password(user.password)
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return {"message": "User Created Seccessfully"}


@router.post("/login",response_model=Token)
def login(user:UserLogin, db:Session = Depends(get_db)):
    db_user = db.query(User).filter(User.email==user.email).first()

    if not db_user or not verify_password(user.password, db_user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail = "Invalid Credentials"
        )
    
    token = create_access_token({"sub": db_user.email})

    return {
        "access_token" : token,
        "token_type" : "bearer"
    }