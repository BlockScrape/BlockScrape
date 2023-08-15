import json

import requests
from fastapi import APIRouter, Depends, Body, status
from fastapi.responses import JSONResponse

from user_server.dependencies.server_information import get_coin_server_con_string
from user_server.dependencies.validate_user import get_current_user

router = APIRouter(
    prefix="/coin",
    tags=["coin"],
    dependencies=[],
    responses={404: {"description": "Not found"}},
)


@router.get("/info")
async def get_coins(server_url: str = Depends(get_coin_server_con_string),
                    auth_user=Depends(get_current_user)):
    data = requests.get(url=server_url + "/get_coin", data=json.dumps({'username': auth_user['username']}))
    if data.status_code == 200:
        return JSONResponse(status_code=status.HTTP_200_OK, content=data.json())
    else:
        return JSONResponse(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, content="Backend Error")


@router.put("/update_coin")
async def update_coins(addition: int = Body(embed=True),
                       server_url: str = Depends(get_coin_server_con_string),
                       auth_user=Depends(get_current_user)):
    data = requests.put(url=server_url + "/update_coin",
                        data=json.dumps({'username': auth_user['username'], "addition": addition}))
    if data.status_code == 200:
        return JSONResponse(status_code=status.HTTP_200_OK, content="Okay")
    else:
        return JSONResponse(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, content="Backend Error")
