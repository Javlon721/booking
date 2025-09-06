from typing import Annotated

import jwt
from fastapi import HTTPException, status, Depends
from fastapi.security import OAuth2PasswordBearer
from jwt import ExpiredSignatureError

from src.auth.models import TokenData
from src.config import JWT_CONFIG

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")


def authorize_user(token: Annotated[str, Depends(oauth2_scheme)]) -> TokenData:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        decoded_data = jwt.decode(token, JWT_CONFIG.secret_key, algorithms=[JWT_CONFIG.algorithm])
        sub = decoded_data.get("sub")
        user_id = decoded_data.get("user_id")

        if sub is None or user_id is None:
            raise credentials_exception

        token_data = TokenData(username=sub, user_id=user_id)

    except ExpiredSignatureError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token expired")
    except Exception:
        raise credentials_exception

    return token_data


AuthorizeUserDepends = Depends(authorize_user)
