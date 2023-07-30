from fastapi import APIRouter, Depends, Body, status
from fastapi.responses import JSONResponse
from fastapi.security import OAuth2PasswordBearer
from user_server.dependencies.server_information import get_server_con_string
from user_server.config import create_user, get_user_by_token
from user_server.dependencies.validate_user import get_current_user
import requests
import json

router = APIRouter(
    prefix="/user",
    tags=["user"],
    dependencies=[],
    responses={404: {"description": "Not found"}},
)

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


@router.post("/create")
async def create(firstname: str = Body(embed=True),
                 lastname: str = Body(embed=True),
                 username: str = Body(embed=True),
                 passwd: str = Body(embed=True),
                 email: str = Body(embed=True),
                 birthdate: int = Body(embed=True),
                 server_url: str = Depends(get_server_con_string)):
    server_path: str = server_url + create_user
    user_data = {'firstname': firstname, 'lastname': lastname, 'username': username, 'passwd': passwd, 'email': email,
                 'birthdate': birthdate}
    try:
        request = requests.post(url=server_path, data=json.dumps(user_data))
    except requests.exceptions.ConnectionError:
        return JSONResponse(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            content="Internal Server not reachable, try later")
    if request.status_code == 201:
        return JSONResponse(status_code=status.HTTP_201_CREATED, content=request.json())
    elif request.status_code == 403:
        return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST, content="username already exists")
    else:
        return JSONResponse(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, content="Error for user Creation")


@router.get("/me")
async def get_user(auth_user=Depends(get_current_user)):
    return auth_user
