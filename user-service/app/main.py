#main.py
from fastapi import FastAPI
from app.router.user import user_router
from app.router.student_router import student_router
from app.router.oauth_router import oauth_router
from app.router.auth_router import auth_router
from app.db_engine import create_db_and_tables
from app.db_engine import create_db_and_tables
from app.router.teacher import teacher_router
app = FastAPI(title="Panaversity User Management and Authentication")


@app.on_event("startup")
def on_startup():
    try:
        create_db_and_tables()
    except Exception as e:
        print(f"Error during startup: {e}")


app.include_router(user_router, prefix="/api/v1/user")
app.include_router(teacher_router, prefix="/api/v1/teacher")
app.include_router(student_router, prefix="/api/v1/student")
app.include_router(oauth_router, prefix="/api/v1/oauth")
app.include_router(auth_router, prefix="/api/v1/auth")
