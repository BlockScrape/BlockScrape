from datetime import timedelta, datetime

from cassandra.cluster import Session
from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
from passlib.context import CryptContext
from starlette import status
from auth_server.dependencies.db_connector import get_database_session
from auth_server.schemas.authentification import TokenData
from auth_server.db_connect.user import get_user
import pyotp as otp


SECRET_KEY = "7e9e6bebb353971f53da617a44c9ac2a26b1f3e072ba532ad98ac75d7c557104"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 600

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


async def get_current_user(session: Session = Depends(get_database_session),
                           token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except JWTError:
        raise credentials_exception
    user = get_user(token_data.username, session)
    if user is None:
        raise credentials_exception
    return user


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def verify_mfa(mfa_key: str, otp_secret: str):
    mfa_checker = otp.TOTP(otp_secret)
    return mfa_checker.verify(mfa_key)


def check_user(username: str, plain_password: str, session: Session):
    user = get_user(username, session)
    if not user:
        return False
    if not verify_password(plain_password, user['passwd']):
        return False
    return user


def authenticate_user(username: str, plain_password: str, mfa_key: str, session: Session):
    user = get_user(username, session)
    if not user:
        return False
    if not verify_password(plain_password, user['passwd']):
        return False
    if not verify_mfa(mfa_key, user['otp_secret']):
        return False
    return user


def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def hash_password(password):
    return pwd_context.hash(password)
