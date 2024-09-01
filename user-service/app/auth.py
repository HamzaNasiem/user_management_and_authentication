#auth.py
from datetime import datetime, timedelta
from jose import JWTError, jwt
from passlib.context import CryptContext
from sqlmodel import Session, select
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from app.models import User
from app.db_engine import get_session
from app.settings import SECRET_KEY, ALGORITHM, ACCESS_TOKEN_EXPIRE_MINUTES
from app.utils import send_whatsapp_message

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/user/login")



def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def hash_password(password):
    return pwd_context.hash(password)


def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def authenticate_user(session: Session, email: str, password: str):
    user = session.exec(select(User).where(User.email == email)).first()
    if not user or not verify_password(password, user.password):
        return False
    return user


async def get_current_user(token: str = Depends(oauth2_scheme), session: Session = Depends(get_session)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    user = session.exec(select(User).where(User.email == email)).first()
    if user is None:
        raise credentials_exception
    return user


async def create_and_send_magic_link(user, phone: str):
    # Generate token with phone number and email
    expire = datetime.utcnow() + timedelta(minutes=15)  # Token expires in 15 minutes
    token_data = {"sub": user.email, "phone": user.phone, "exp": expire}
    token = jwt.encode(token_data, SECRET_KEY, algorithm=ALGORITHM)
    
    # Generate the verification URL
    url = f"http://localhost:8000/api/v1/user/verify?token={token}"
    
    # Message to be sent
    sms_message = f"Click the link to verify your phone number: {url}. The link expires in 15 minutes."
    
    # Send the WhatsApp message
    whatsapp_response = send_whatsapp_message(phone, sms_message)
    return whatsapp_response