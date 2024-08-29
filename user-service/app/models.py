#models.py
from sqlmodel import SQLModel, Field, Relationship, Column
from sqlalchemy import Enum as SQLAEnum, JSON
from typing import Optional, List
from enum import Enum


class UserType(str, Enum):
    ADMIN = "admin"
    STUDENT = "student"
    VISITOR = "visitor"
    TEACHER = "teacher"


class User(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    full_name: str
    email: str
    phone: Optional[str] = None
    affiliation: Optional[str] = None
    is_verified: Optional[bool] = False
    password: str
    user_type: UserType = Field(sa_column=Column(SQLAEnum(UserType)))

    teacher: Optional["Teacher"] = Relationship(back_populates="user")


class Teacher(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: int = Field(foreign_key="user.id")
    department: str
    courses: Optional[List[str]] = Field(
        sa_column=Column(JSON))  # Use JSON column for list[str]

    user: Optional[User] = Relationship(back_populates="teacher")



class Register_User(SQLModel):
    full_name: str
    email: str
    password: str
    phone: Optional[str] = None
    affiliation: Optional[str] = None
    is_verified: Optional[bool] = False
    user_type: UserType



class Token(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    access_token: str
    token_type: str
