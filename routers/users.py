from fastapi import APIRouter, Request, status, HTTPException, Depends
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from models.users import UsersPrivate, TokenResponse
from auth.auth_handler import create_access_token, validate_access_token, hash_password, verify_hash
from fastapi.encoders import jsonable_encoder
from fastapi.security import OAuth2PasswordRequestForm, HTTPBearer, HTTPAuthorizationCredentials
from typing import List, Optional
from pydantic import BaseModel




users_router = APIRouter(prefix="/users", tags=["users"])


@users_router.post("/register", status_code=201, response_description="Register new user", response_model=UsersPrivate)
async def register(new_user: UsersPrivate):
    #hash user password and check if email/username already exist collection
    email_exist = await UsersPrivate.find_one(UsersPrivate.email == new_user.email)
    username_exist = await UsersPrivate.find_one(UsersPrivate.username == new_user.username)
    if email_exist or username_exist:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT, detail=f"User with specified email/username already exists"
        )

    new_user.password = hash_password(new_user.password)
    await new_user.insert()
    created_user = await UsersPrivate.find_one(UsersPrivate.username == new_user.username)

    return created_user


@users_router.post("/login", response_description="User Login", response_model=TokenResponse)
async def login(formData: OAuth2PasswordRequestForm = Depends()):
    user_exist = await UsersPrivate.find_one(UsersPrivate.email == formData.username)

    if (user_exist is None) or (not verify_hash(formData.password, user_exist.password)):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Invalid email and/or password")

    token = create_access_token(user_exist.email)
    return {
        "access_token": token,
        "token_type": 'Bearer'
    }









# Secure route with token
# token_auth_scheme = HTTPBearer() # auth by token
#
# def auth_wrapper(auth: HTTPAuthorizationCredentials = Security(token_auth_scheme)):
#     ''' Decode user token, return payload and get email'''
#     user_email = validate_access_token(auth.credentials).get('user_email')
#     return user_email
#
#
# class ActionList(BaseModel):
#     day: str
#     todo_list: List
#     author: Optional[str]
#
#
# @users_router.post("/actionlist", response_description="Create todo list", response_model=ActionList)
# async def create_todo(todo_list: ActionList, user_email=Depends(auth_wrapper)):
#     """A valid access token is required to access this route"""
#     todo_list.author = user_email
#     print(todo_list)
#     # return todo_list
#     return todo_list





















