from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import sqlite3

app = FastAPI()

# Liberar o acesso do frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # pode colocar seu domínio aqui depois
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Conexão com banco de dados SQLite
conn = sqlite3.connect("usuarios.db", check_same_thread=False)
cursor = conn.cursor()

# Criar tabela se não existir
cursor.execute("""
    CREATE TABLE IF NOT EXISTS usuarios (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nome TEXT NOT NULL,
        email TEXT NOT NULL UNIQUE,
        usuario TEXT NOT NULL,
        senha TEXT NOT NULL
    )
""")
conn.commit()

# Modelo de entrada via JSON (Pydantic)
class Usuario(BaseModel):
    nome: str
    email: str
    usuario: str
    senha: str

@app.post("/cadastro")
def cadastro(usuario: Usuario):
    # Verificar se e-mail já existe
    cursor.execute("SELECT * FROM usuarios WHERE email = ?", (usuario.email,))
    if cursor.fetchone():
        raise HTTPException(status_code=400, detail="E-mail já cadastrado.")

    # Inserir usuário
    cursor.execute(
        "INSERT INTO usuarios (nome, email, usuario, senha) VALUES (?, ?, ?, ?)",
        (usuario.nome, usuario.email, usuario.usuario, usuario.senha)
    )
    conn.commit()
    return {"mensagem": "Usuário cadastrado com sucesso!"}
