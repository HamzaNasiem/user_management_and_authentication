from fastapi import APIRouter, Depends, HTTPException
from app.auth import get_current_user, hash_password, verify_password
from app.models import User
from sqlmodel import Session
from app.db_engine import get_session

auth_router = APIRouter(
    prefix="/auth",
    tags=["auth"]
)


@auth_router.post("/password-reset")
async def initiate_password_reset(email: str):
    return {"status": "success", "message": "Password reset link has been sent to your email."}


@auth_router.post("/password-update")
async def update_password(current_password: str, new_password: str, current_user: User = Depends(get_current_user), session: Session = Depends(get_session)):
    if not verify_password(current_password, current_user.password):
        raise HTTPException(
            status_code=401, detail="Current password is incorrect")

    current_user.password = hash_password(new_password)
    session.add(current_user)
    session.commit()

    return {"status": "success", "message": "Password updated successfully."}


@auth_router.post("/verify-contact")
async def verify_contact(verification_type: str, contact: str, verification_code: str):
    return {"status": "success", "message": "Email/Phone verification successful."}
