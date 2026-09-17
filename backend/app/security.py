from datetime import datetime, timedelta, timezone

import bcrypt
import jwt

from app.database import settings

# hash_password: hasha a senha do usuario
# verify_password: verifica se a senha do usuario é valida
# create_access_token: cria o token de acesso
# decode_access_token: decodifica o token de acesso


def hash_password(password: str) -> str:
    return bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")

def verify_password(password: str, password_hash: str) -> bool:
    return bcrypt.checkpw(password.encode("utf-8"), password_hash.encode("utf-8"))

def create_access_token(user_id: int) -> str:
    expire = datetime.now(timezone.utc) + timedelta(minutes=settings.access_token_expire_minutes)
    payload = {"sub": str(user_id), "exp" : expire}

    return jwt.encode(payload, settings.secret_key, algorithm="HS256")

def decode_access_token(token: str) -> int:
    payload = jwt.decode(token, settings.secret_key, algorithms=["HS256"])
    return int(payload["sub"])