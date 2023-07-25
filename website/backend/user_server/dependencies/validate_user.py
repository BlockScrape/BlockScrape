from fastapi import APIRouter, Depends, Body, status
from fastapi.responses import JSONResponse
from fastapi.security import OAuth2PasswordBearer
from user_server.dependencies.server_information import get_server_con_string
from user_server.config import create_user, get_user_by_token
import requests
import json

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


async def get_current_user(token: str = Depends(oauth2_scheme), server_url: str = Depends(get_server_con_string)):
    server_path = server_url + get_user_by_token
    token_data = "Bearer " + token
    header = {'Authorization': token_data}
    user = requests.get(url=server_path, headers=header).json()
    if "username" in user:
        return user
    else:
        return None
