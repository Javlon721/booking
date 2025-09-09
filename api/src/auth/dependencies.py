from typing import Annotated

from fastapi import HTTPException, status, Depends
from fastapi.security import OAuth2PasswordBearer
from jwt import ExpiredSignatureError

from src.auth.models import TokenData
from src.auth.utils import decode_token

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")


def authorize_user(token: Annotated[str, Depends(oauth2_scheme)]) -> TokenData:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
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


AuthorizeUserDepends = Depends(authorize_user)
