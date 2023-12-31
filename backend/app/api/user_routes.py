import uuid
from fastapi import Depends, HTTPException, status, APIRouter, Response
from fastapi.security import OAuth2PasswordRequestForm
from models.user import User, RefreshToken
from dependencies import get_db, SessionLocal
from schemas.users import UserCreate, UserResponse, UserUpdate, RefreshTokenRequest
from core.security import create_access_token, create_refresh_token, hash_password, verify_password, decode_token, extract_jti, REFRESH_TOKEN_EXPIRE_DAYS
from datetime import datetime, timedelta

from core.security import oauth2_scheme

router = APIRouter()



def authenticate_user(email: str, password: str, db):
    user = db.query(User).filter(User.email == email).first()
    if not user or not verify_password(password, user.hashed_password):
        return False
    return user


async def get_current_user(token: str = Depends(oauth2_scheme), db: SessionLocal = Depends(get_db)):
    token_data = decode_token(token)
    if token_data is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")
    user = db.query(User).filter(User.user_id == token_data["sub"]).first()
    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User not found")
    return user

@router.post("/register", status_code=status.HTTP_201_CREATED)
async def create_user(user: UserCreate, db: SessionLocal = Depends(get_db)):
    # Vérifier si l'utilisateur existe déjà
    db_user = db.query(User).filter(User.email == user.email).first()
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")

    # Hasher le mot de passe et créer un nouvel utilisateur
    hashed_password = hash_password(user.password)
    db_user = User(username=user.username, email=user.email, hashed_password=hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)

    # Retourner l'utilisateur créé (sans le mot de passe hashé)
    return {"id": db_user.user_id, "username": db_user.username, "email": db_user.email}


@router.post("/login")
async def login(form_data: OAuth2PasswordRequestForm = Depends(), db: SessionLocal = Depends(get_db)):
    user = authenticate_user(form_data.username, form_data.password, db)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token = create_access_token(data={"sub": user.user_id})
    jti = str(uuid.uuid4())
    refresh_token = create_refresh_token(data={"sub": user.user_id, "jti": jti})
    # Enregistrer le refresh_token dans la base de données
    db_refresh_token = RefreshToken(jti=jti, user_id=user.user_id, expires_at=datetime.utcnow() + timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS))
    db.add(db_refresh_token)
    db.commit()
    return {"access_token": access_token, "token_type": "bearer", "refresh_token": refresh_token}


@router.post("/refresh-token")
async def refresh_token(request: RefreshTokenRequest, db: SessionLocal = Depends(get_db)):
    refresh_token = request.refresh_token
    jti = extract_jti(refresh_token)

    if not jti:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid or expired token")

    stored_token = db.query(RefreshToken).filter(RefreshToken.jti == jti).first()
    
    if not stored_token or stored_token.revoked or stored_token.expires_at < datetime.utcnow():
        raise HTTPException(status_code=401, detail="Invalid or revoked refresh token")
    
    user = db.query(User).filter(User.user_id == stored_token.user_id).first()
    if not user:
        raise HTTPException(status_code=401, detail="User not found")

    new_access_token = create_access_token(data={"sub": user.user_id})
    return {"access_token": new_access_token}


@router.get("/{user_id}", response_model=UserResponse)
async def read_user(user_id: int, current_user: User = Depends(get_current_user), db: SessionLocal = Depends(get_db)):
    if current_user.user_id != user_id and not current_user.is_admin:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to access this user's information")

    db_user = db.query(User).filter(User.user_id == user_id).first()
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return UserResponse(**db_user.__dict__)


@router.put("/{user_id}")
async def update_user(user_id: int, user_update: UserUpdate, current_user: User = Depends(get_current_user), db: SessionLocal = Depends(get_db)):
    if current_user.user_id != user_id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to update this user")

    db_user = db.query(User).filter(User.user_id == user_id).first()
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")

    # Vérifier si la nouvelle adresse email existe déjà
    if user_update.email is not None and db.query(User).filter(User.email == user_update.email).first():
        raise HTTPException(status_code=400, detail="Email already in use")

    # Mettre à jour les champs autorisés
    if user_update.username is not None:
        db_user.username = user_update.username
    if user_update.email is not None:
        db_user.email = user_update.email
    if user_update.password is not None:
        hashed_password = hash_password(user_update.password)
        db_user.hashed_password = hashed_password

    db.add(db_user)
    db.commit()
    db.refresh(db_user)

    return {"msg": "User updated successfully"}


@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(user_id: int, current_user: User = Depends(get_current_user), db: SessionLocal = Depends(get_db)):
    if current_user.user_id != user_id and not current_user.is_admin:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to delete this user")

    db_user = db.query(User).filter(User.user_id == user_id).first()
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")

    db.delete(db_user)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)
