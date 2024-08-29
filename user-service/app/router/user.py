#router/user.py
from typing import Optional
from fastapi import APIRouter, Depends, HTTPException, status
from app.models import Register_User, Token, User, Teacher, UserType
from fastapi.security import OAuth2PasswordRequestForm
from sqlmodel import Session, select
from app.auth import hash_password, get_current_user, authenticate_user, create_access_token
from app.db_engine import get_session
from app.utils import send_whatsapp_message


user_router = APIRouter(
    prefix="/user",
    tags=["user"]
)


@user_router.post("/register", response_model=User)
async def register_user(new_user: Register_User, session: Session = Depends(get_session)):
    db_user = session.exec(select(User).where(
        User.email == new_user.email)).first()
    if db_user:
        raise HTTPException(
            status_code=409, detail="User with these credentials already exists")

    user = User(
        full_name=new_user.full_name,
        email=new_user.email,
        phone=new_user.phone,
        affiliation=new_user.affiliation,
        is_verified=new_user.is_verified,
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
        whatsapp_response = send_whatsapp_message(
            new_user.phone, f"Welcome {new_user.full_name} to Panaversity!")
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


@user_router.post("/logout")
async def logout_user(access_token: str, refresh_token: Optional[str] = None):
    return {"status": "success", "message": "Logout successful. The token has been invalidated."}


@user_router.patch("/profile")
async def update_user_profile(profile_data: dict, current_user: User = Depends(get_current_user), session: Session = Depends(get_session)):
    for key, value in profile_data.items():
        setattr(current_user, key, value)
    session.add(current_user)
    session.commit()
    return {"status": "success", "message": "Profile updated successfully."}


@user_router.get("/me", response_model=User)
async def get_profile(current_user: User = Depends(get_current_user)):
    return current_user
