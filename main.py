from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, EmailStr
from passlib.context import CryptContext
from jose import jwt
from datetime import datetime, timedelta
import databases
import sqlalchemy

DATABASE_URL = "sqlite:///./usuarios.db"

database = databases.Database(DATABASE_URL)
metadata = sqlalchemy.MetaData()

usuarios = sqlalchemy.Table(
    "usuarios",
    metadata,
    sqlalchemy.Column("email", sqlalchemy.String, primary_key=True),
    sqlalchemy.Column("senha", sqlalchemy.String),
)

engine = sqlalchemy.create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
metadata.create_all(engine)

app = FastAPI()

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Ajuste para produção
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
SECRET_KEY = "chave-secreta-refugiart"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60 * 24

class UsuarioCadastro(BaseModel):
    email: EmailStr
    senha: str

class UsuarioLogin(BaseModel):
    email: EmailStr
    senha: str

class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"

def criar_token(email: str):
    expira = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    payload = {"sub": email, "exp": expira}
    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)

async def verificar_usuario_existente(email: str):
    query = usuarios.select().where(usuarios.c.email == email)
    usuario = await database.fetch_one(query)
    return usuario is not None

@app.on_event("startup")
async def startup():
    await database.connect()

@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()

@app.post("/cadastro", response_model=Token)
async def cadastrar(usuario: UsuarioCadastro):
    if await verificar_usuario_existente(usuario.email):
        raise HTTPException(status_code=400, detail="Usuário já existe.")

    senha_criptografada = pwd_context.hash(usuario.senha)
    query = usuarios.insert().values(email=usuario.email, senha=senha_criptografada)
    await database.execute(query)

    token = criar_token(usuario.email)
    return {"access_token": token}

@app.post("/login", response_model=Token)
async def login(usuario: UsuarioLogin):
    query = usuarios.select().where(usuarios.c.email == usuario.email)
    usuario_db = await database.fetch_one(query)
    if not usuario_db or not pwd_context.verify(usuario.senha, usuario_db["senha"]):
        raise HTTPException(status_code=401, detail="Credenciais inválidas")

    token = criar_token(usuario.email)
    return {"access_token": token}

@app.get("/")
def read_root():
    return {"message": "Servidor FastAPI ativo com sucesso!"}