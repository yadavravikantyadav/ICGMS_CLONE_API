from fastapi.security import HTTPBearer,HTTPAuthorizationCredentials
from fastapi import Depends, HTTPException, status
from Token import verify_token
from typing import Annotated
from sqlalchemy.orm import Session
from database import get_db
from models import TokenModel

# OAuth2 password flow with token URL
oauth2_scheme = HTTPBearer()


def get_current_user(db:Session=Depends(get_db),token:HTTPAuthorizationCredentials = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid or expired token"
        )
    
   
    print("Token received:", token.credentials)

    token_obj=db.query(TokenModel).filter(TokenModel.token==token.credentials).first()
    if not token_obj:
        raise credentials_exception

    token = token.credentials
    user_data = verify_token(token, credentials_exception)
    print("_______________________________________________________--User data:", user_data)
    return user_data


user_dependency =Annotated[Session,Depends(get_current_user)]