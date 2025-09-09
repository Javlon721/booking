from typing import Annotated

from fastapi import HTTPException, status, Depends
from fastapi.security import OAuth2PasswordBearer
from jwt import ExpiredSignatureError

from src.auth.models import TokenData, Token
from src.auth.utils import decode_token, create_access_token

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login", refreshUrl="auth/token/refresh")

credentials_exception = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Could not validate credentials",
    headers={"WWW-Authenticate": "Bearer"},
)


def authorize_user(token: Annotated[str, Depends(oauth2_scheme)]) -> TokenData:
    try:
        decoded_data = decode_token(token)
        sub = decoded_data.get("sub")

        if sub is None:
            raise credentials_exception

        token_data = TokenData(user_id=sub)

    except ExpiredSignatureError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token expired")
    except Exception:
        raise credentials_exception

    return token_data


def renew_access_token(token: Annotated[str, Depends(oauth2_scheme)]) -> Token:
    try:
        decoded_data = decode_token(token)
        sub = decoded_data.get("sub")
        is_refresh = decoded_data.get("refresh")

        if sub is None or not is_refresh:
            raise credentials_exception

        new_token_data = {"sub": sub, }
        new_access_token = create_access_token(new_token_data)

        return Token(access_token=new_access_token, token_type="bearer")
    except ExpiredSignatureError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Refresh token expired")
    except Exception:
        raise credentials_exception


AuthorizeUserDepends = Depends(authorize_user)
