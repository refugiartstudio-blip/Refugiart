from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from database import SessionLocal, engine, Base
from models import Usuario
from passlib.context import CryptContext
from jose import JWTError, jwt
from pydantic import BaseModel
from datetime import datetime, timedelta

# Criar tabelas
Base.metadata.create_all(bind=engine)

app = FastAPI()

# Configurações de segurança
SECRET_KEY = "sua_chave_secreta_muito_forte"  # Troque para algo seguro!
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Schemas para requisições
class UsuarioCreate(BaseModel):
    email: str
    username: str
    senha: str

class Token(BaseModel):
    access_token: str
    token_type: str

# Dependência para DB
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Funções auxiliares
def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password):
    return pwd_context.hash(password)

def get_user_by_email(db: Session, email: str):
    return db.query(Usuario).filter(Usuario.email == email).first()

def get_user_by_username(db: Session, username: str):
    return db.query(Usuario).filter(Usuario.username == username).first()

def authenticate_user(db: Session, username: str, password: str):
    user = get_user_by_username(db, username)
    if not user:
        return False
    if not verify_password(password, user.hashed_password):
        return False
    return user

def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta if expires_delta else timedelta(minutes=15))
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

# Rota cadastro
@app.post("/cadastro", status_code=201)
def cadastro(user: UsuarioCreate, db: Session = Depends(get_db)):
    db_user_email = get_user_by_email(db, user.email)
    db_user_username = get_user_by_username(db, user.username)
    if db_user_email or db_user_username:
        raise HTTPException(status_code=400, detail="Email ou nome de usuário já cadastrado")
    
    hashed_password = get_password_hash(user.senha)
    novo_usuario = Usuario(email=user.email, username=user.username, hashed_password=hashed_password)
    db.add(novo_usuario)
    db.commit()
    db.refresh(novo_usuario)
    return {"msg": "Usuário criado com sucesso"}

# Rota login
@app.post("/login", response_model=Token)
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(status_code=401, detail="Usuário ou senha incorretos", headers={"WWW-Authenticate": "Bearer"})
    
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(data={"sub": user.username}, expires_delta=access_token_expires)

    return {"access_token": access_token, "token_type": "bearer"}