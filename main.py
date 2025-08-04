from fastapi import FastAPI, HTTPException, Form
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, EmailStr
from passlib.context import CryptContext
from jose import jwt
from datetime import datetime, timedelta

app = FastAPI()

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Em produção, troque por ["https://refugiartstudio-blip.github.io"]
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# "Banco de dados" temporário em memória
usuarios_db = {}

# Segurança
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
SECRET_KEY = "chave-secreta-refugiart"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60 * 24  # 1 dia

# Modelos
class UsuarioCadastro(BaseModel):
    email: EmailStr
    senha: str

class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"

# Função para criar token JWT
def criar_token(email: str):
    expira = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    payload = {"sub": email, "exp": expira}
    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)

# Verifica se o usuário já existe
def verificar_usuario_existente(email: str):
    return email in usuarios_db

# Rota de boas-vindas
@app.get("/")
def home():
    return {"message": "Backend Refugiart ativo!"}

# Rota de cadastro
@app.post("/cadastro", response_model=Token)
def cadastrar(usuario: UsuarioCadastro):
    if verificar_usuario_existente(usuario.email):
        raise HTTPException(status_code=400, detail="Usuário já existe.")

    senha_criptografada = pwd_context.hash(usuario.senha)
    usuarios_db[usuario.email] = {"senha": senha_criptografada}

    token = criar_token(usuario.email)
    return {"access_token": token}

# Rota de login
@app.post("/login", response_model=Token)
def login(email: EmailStr = Form(...), senha: str = Form(...)):
    usuario = usuarios_db.get(email)
    if not usuario or not pwd_context.verify(senha, usuario["senha"]):
        raise HTTPException(status_code=401, detail="Credenciais inválidas")

    token = criar_token(email)
    return {"access_token": token}