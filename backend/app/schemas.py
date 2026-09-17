from pydantic import BaseModel, EmailStr

class UserCreate(BaseModel):
    # EmailStr valida se é um email valido
    email: EmailStr 
    password: str

class UserLogin(BaseModel):
    # EmailStr valida se é um email valido
    email: EmailStr
    password: str

# model_config = {"from_attributes": True} para que o pydantic use os nomes dos campos do banco de dados
class UserRead(BaseModel):
    id: int
    email: EmailStr

    model_config = {"from_attributes": True}

# Token é o token de acesso que o usuario recebe apos login
# token_type é o tipo de token, neste caso, bearer
class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"
