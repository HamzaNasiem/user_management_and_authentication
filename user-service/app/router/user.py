#router/user.py
from typing import Optional
from fastapi import APIRouter, Depends, HTTPException, status, Request
from app.models import Register_User, Token, User, Teacher, UserType
from fastapi.security import OAuth2PasswordRequestForm
from sqlmodel import Session, select
from app.auth import hash_password, get_current_user, authenticate_user, create_access_token, create_and_send_magic_link
from app.db_engine import get_session
from app.utils import send_whatsapp_message
from datetime import datetime, timedelta
from jose import JWTError, jwt
from app.settings import SECRET_KEY, ALGORITHM

user_router = APIRouter(
    # prefix="/user",
    tags=["user"]
)


@user_router.post("/register", response_model=User)
async def register_user(new_user: Register_User, session: Session = Depends(get_session)):
    db_user = session.exec(select(User).where(
        (User.email == new_user.email) | (User.phone == new_user.phone)
    )).first()
    
    if db_user:
        raise HTTPException(
            status_code=409, detail="User with these credentials already exists")

    user = User(
        full_name=new_user.full_name,
        email=new_user.email,
        phone=new_user.phone,
        affiliation=new_user.affiliation,
        is_verified=False,
        password=hash_password(new_user.password),
        user_type=new_user.user_type
    )

    session.add(user)
    session.commit()
    session.refresh(user)

    if new_user.user_type == UserType.TEACHER:
        teacher = Teacher(user_id=user.id, department="Unassigned")
        session.add(teacher)
        session.commit()

    if new_user.phone:
        # Use the helper function to create and send the magic link
        whatsapp_response = await create_and_send_magic_link(user, new_user.phone)
        
        if whatsapp_response["status"] != "success":
            raise HTTPException(
                status_code=500, detail="User registered but failed to send WhatsApp message")

    return user


@user_router.post("/login", response_model=Token)
async def login_for_access_token(
    form_data: OAuth2PasswordRequestForm = Depends(),
    session: Session = Depends(get_session)
):
    user = authenticate_user(session, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token = create_access_token(data={"sub": user.email})
    return {"access_token": access_token, "token_type": "bearer"}

#resend link
@user_router.post("/resend-link")
async def resend_verification_link(
    form_data: OAuth2PasswordRequestForm = Depends(),
    session: Session = Depends(get_session)
):
    user = authenticate_user(session, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    if user.is_verified:
        raise HTTPException(status_code=400, detail="User is already verified")

    # Use the helper function to create and send the magic link
    whatsapp_response = await create_and_send_magic_link(user, user.phone)
    if whatsapp_response["status"] != "success":
        raise HTTPException(
            status_code=500, detail="Failed to send WhatsApp message")

    return {"msg": "Verification link resent successfully"}



@user_router.get("/verify")
async def verify_user(token: str, request: Request, session: Session = Depends(get_session)):
    try:
        # Decode the token
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email = payload.get("sub")
        phone = payload.get("phone")
        if email is None or phone is None:
            raise HTTPException(status_code=400, detail="Invalid token")
    except jwt.JWTError:
        raise HTTPException(status_code=400, detail="Invalid token")

    # Find the user
    user = session.exec(select(User).where(User.email == email, User.phone == phone)).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    # Verify user
    user.is_verified = True
    session.add(user)
    session.commit()

    return {"msg": "Phone number verified successfully"}



# logout 
@user_router.post("/logout")
async def logout_user(access_token: str, refresh_token: Optional[str] = None):
    return {"status": "success", "message": "Logout successful. The token has been invalidated."}


# profile section
@user_router.patch("/profile")
async def update_user_profile(profile_data: dict, current_user: User = Depends(get_current_user), session: Session = Depends(get_session)):
    for key, value in profile_data.items():
        setattr(current_user, key, value)
    session.add(current_user)
    session.commit()
    return {"status": "success", "message": "Profile updated successfully."}


@user_router.get("/profile", response_model=User)
async def get_profile(current_user: User = Depends(get_current_user)):
    return current_user
