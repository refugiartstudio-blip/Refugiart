from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from jose import JWTError, jwt
from datetime import datetime, timedelta
import bcrypt
import sqlite3
import os

app = FastAPI()

# Liberação do frontend (CORS)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # depois pode restringir para seu domínio
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Conexão com banco SQLite
conn = sqlite3.connect("usuarios.db", check_same_thread=False)
cursor = conn.cursor()

# Criação da tabela
cursor.execute("""
    CREATE TABLE IF NOT EXISTS usuarios (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nome TEXT NOT NULL,
        email TEXT NOT NULL UNIQUE,
        usuario TEXT NOT NULL,
        senha BLOB NOT NULL
    )
""")
conn.commit()

# Modelos
class Usuario(BaseModel):
    nome: str
    email: str
    usuario: str
    senha: str

class LoginData(BaseModel):
    email: str
    senha: str

# Configurações JWT
SECRET_KEY = "CHAVE_SUPER_SECRETA_DO_REFUGIART"  # troque por algo mais seguro
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60

# Rota raiz
@app.get("/")
def root():
    return {"mensagem": "API do Refugiart no ar. Acesse /docs para usar."}

# Cadastro de usuários
@app.post("/cadastro")
def cadastro(usuario: Usuario):
    cursor.execute("SELECT * FROM usuarios WHERE email = ?", (usuario.email,))
    if cursor.fetchone():
        raise HTTPException(status_code=400, detail="E-mail já cadastrado.")

    senha_hash = bcrypt.hashpw(usuario.senha.encode('utf-8'), bcrypt.gensalt())
    cursor.execute(
        "INSERT INTO usuarios (nome, email, usuario, senha) VALUES (?, ?, ?, ?)",
        (usuario.nome, usuario.email, usuario.usuario, senha_hash)
    )
    conn.commit()
    return {"mensagem": "Usuário cadastrado com sucesso!"}

# Login de usuário
@app.post("/login")
def login(data: LoginData):
    cursor.execute("SELECT * FROM usuarios WHERE email = ?", (data.email,))
    usuario = cursor.fetchone()

    if not usuario:
        raise HTTPException(status_code=401, detail="Credenciais inválidas")

    senha_hash = usuario[4]
    if not bcrypt.checkpw(data.senha.encode('utf-8'), senha_hash):
        raise HTTPException(status_code=401, detail="Credenciais inválidas")

    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    payload = {
        "sub": data.email,
        "exp": expire
    }
    token = jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)

    return {"access_token": token, "token_type": "bearer"}