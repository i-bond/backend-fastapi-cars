#Authenticate dependency, which will be injected into the routes to enforce authorizatiom
from auth.auth_handler import validate_access_token
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, HTTPBearer
from models.users import UsersPrivate
from fastapi.security import HTTPAuthorizationCredentials
from fastapi import Security


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/users/login", scheme_name="JWT")  #auth by login and password


token_auth_scheme = HTTPBearer() # auth by token
def auth_wrapper(auth: HTTPAuthorizationCredentials = Security(token_auth_scheme)):
    ''' Decode user token, return payload and get email'''
    user_email = validate_access_token(auth.credentials).get('user_email')
    return user_email

