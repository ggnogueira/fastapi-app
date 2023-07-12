# Seguindo a documentação do FASTAPI

# Passo 1.
Criando virtual env
`python -m venv ./env`

# Passo 2.
Ativando virtual env (windows)
`./env/Scripts/activate`

# Passo 3.
Instalando dependencias
`pip install fastapi`
`pip install "uvicorn[standard]"`

# Passo 4.
Executando script
`uvicorn main:app --reload`

# Passo 5.
Acessando documentação
`http://127.0.0.1:8000/docs` ou `http://127.0.0.1:8000/redoc`

# Passo 6.
Autenticação usando JWT. Fazendo instalação das dependecias.
`pip install "python-jose[cryptography]"`

# Passo 7.
Instalando algoritmo para criptografia das senhas.
`pip install "passlib[bcrypt]"`

# Passo 8.
Para criar o banco de dados é necessário executar o seguinte comando dentro do python.
```py
import services
services.create_database()
```
