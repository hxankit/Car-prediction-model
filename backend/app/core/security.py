from passlib.context import CryptContext
from jose import jwt
from datetime import datetime, timedelta
import hashlib
SECRET_KEY = "supersecret"
ALGORITHM = "HS256"

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(password: str):
    sha_hash = hashlib.sha256(password.encode()).hexdigest()
    return pwd_context.hash(sha_hash)

def verify_password(plain, hashed):
    sha_hash = hashlib.sha256(plain.encode()).hexdigest()
    return pwd_context.verify(sha_hash, hashed)


def create_token(data: dict, expires_delta: timedelta = None):
    to_encode = data.copy()

    expire = datetime.utcnow() + (expires_delta or timedelta(hours=24))
    to_encode.update({
        "exp": expire,
        "iat": datetime.utcnow()  # issued at
    })

    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


from jose import JWTError

def decode_token(token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except JWTError:
        return None