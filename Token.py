from datetime import datetime, timedelta
import jwt
from schemas import TokenData
from fastapi import HTTPException

SECRET_KEY = "593919bc0c86c3b5c01e2531e939b95dc46ab6a9abc48f0029585c4b6abb19f0"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30


def Create_token(data: dict):
    to_encode = data.copy()
    expire = datetime.now() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def verify_token(data: str, credentials_exception):
    try:
        payload = jwt.decode(data,SECRET_KEY, algorithms=[ALGORITHM])
        email = payload.get("email")
        role = payload.get("role_id")
        if email is None or role is None:
            raise credentials_exception
        return TokenData(email=email, role_id=role, role_name=payload.get("user_role"))
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token has expired")
    except jwt.InvalidTokenError as e:
        raise HTTPException(status_code=401, detail=f"Invalid token: {str(e)}")