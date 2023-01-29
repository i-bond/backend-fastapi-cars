from enum import Enum
from typing import Optional, List
from beanie import Document
from pydantic import Field, EmailStr, BaseModel


class Role(str, Enum):
    SALESMAN = "SALESMAN"
    USER = "USER"
    ADMIN = "ADMIN"

# class Users(Document):
#     username: str = Field(..., min_length=3, max_length=30)
#     email: EmailStr = Field(...)
#     password: str = Field(...)
#     role: Role = Role.USER
#
#     class Settings:
#         '''Set DB collection'''
#         name = 'users'
#
#     class Config:
#         '''Payload example'''
#         schema_extra = {
#             "example": {
#                 "username": "Jack",
#                 "email": "jack@mail.com",
#                 "password": "123",
#                 "role": "USER",
#             }
#         }



class UsersPublic(Document):
    username: str = Field(..., min_length=3, max_length=30)
    email: EmailStr = Field(...)
    role: Role = Role.USER

    class Settings:
        '''Set DB collection'''
        name = 'users'

    class Config:
        '''Payload example'''
        schema_extra = {
            "example": {
                "username": "Jack",
                "email": "jack@mail.com",
                "password": "123",
                "role": "USER",
            }
        }


class UsersPrivate(UsersPublic):
    password: str = Field(...)


class TokenResponse(BaseModel):
    access_token: str
    token_type: str


# Forms
class UserLoginForm(BaseModel):
    email: EmailStr = Field(...)
    password: str = Field(...)

