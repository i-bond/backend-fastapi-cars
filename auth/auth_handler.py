# This script is responsible for signing , encoding , decoding and returning JWTs
import time
from typing import Dict
import jwt
from decouple import config
from fastapi import HTTPException, status
from datetime import datetime, timedelta
from passlib.context import CryptContext


JWT_SECRET = config("secret", default='scrt')
JWT_ALGORITHM = config("algorithm", default='HS256')




# Class
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
def hash_password(password:str):
    return pwd_context.hash(password)


def verify_hash(plain_password: str, hashed_password: str):
    return pwd_context.verify(plain_password, hashed_password)


def create_access_token(user_email: str) -> str:
    payload = {
        "user_email": user_email,
        "expire_time": time.time() + 3600 #sec
        # "expire_time": datetime.utcnow() + timedelta(days=0, minutes=60),
    }

    token = jwt.encode(payload, JWT_SECRET, algorithm="HS256")
    return token


def validate_access_token(token: str):
    try:
        payload = jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
        if time.time() > payload['expire_time']:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Token expired!"
            )

        return payload

    except jwt.InvalidTokenError as e:
        raise HTTPException(status_code=401, detail="Invalid token")




if __name__ == '__main__':
    password_hash = hash_password('password123')
    # print(password_hash)
    # res1 = verify_hash('password1233', password_hash)
    # print(res1)

    result = validate_access_token('eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2VtYWlsIjoiamFja0BtYWlsLmNvbSIsImV4cGlyZV90aW1lIjoxNjcyMzgyNTUzLjY5NzU4Mzd9.B0yjnTkKGas9oPFjCY1tx3MVctd1ZdqHNnxi4irqHE0')
    print(result)



