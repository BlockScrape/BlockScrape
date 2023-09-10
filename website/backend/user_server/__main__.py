import uvicorn as uvicorn
from fastapi import FastAPI, Depends, status
from fastapi.security import OAuth2PasswordRequestForm
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import argparse
from routers import coin, order, user
from user_server.config import validate_user_credentials, check_credential
from user_server.dependencies.db_connector import connect_database, get_database_session
from user_server.dependencies.server_information import set_server_con_string, get_auth_server_con_string
import requests

parser = argparse.ArgumentParser()
parser.add_argument('--authentication_uri', default="http://127.0.0.1:7979")
parser.add_argument('--coinservice_uri', default="http://127.0.0.1:1337")
parser.add_argument('--cassandra_uri', default="127.0.0.1")
parser.add_argument('--cassandra_port', default=9042)
parser.add_argument('--cassandra_user', default='cassandra')
parser.add_argument('--cassandra_passwd', default='cassandra')
args = vars(parser.parse_args())

app = FastAPI()

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.post("/token")
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(),
                                 server_url: str = Depends(get_auth_server_con_string)):
    server_path: str = server_url + validate_user_credentials
    request_form_data = {'username': form_data.username, 'password': form_data.password,
                         'client_secret': form_data.client_secret}
    try:
        request = requests.post(url=server_path, data=request_form_data)
    except requests.exceptions.ConnectionError:
        return JSONResponse(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            content="Internal Server not reachable, try later")
    if request.status_code == 200:
        return JSONResponse(status_code=status.HTTP_200_OK, content=request.json())
    elif request.status_code == 401:
        return JSONResponse(status_code=status.HTTP_403_FORBIDDEN, content="Incorrect username or password")
    else:
        return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST, content="Could not validate Credentials")


@app.post("/check_credentials")
async def check_credentials(form_data: OAuth2PasswordRequestForm = Depends(),
                            server_url: str = Depends(get_auth_server_con_string)):
    server_path: str = server_url + check_credential
    request_form_data = {'username': form_data.username, 'password': form_data.password}
    try:
        request = requests.post(url=server_path, data=request_form_data)
    except requests.exceptions.ConnectionError:
        return JSONResponse(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            content="Internal Server not reachable, try later")
    if request.status_code == 200:
        return JSONResponse(status_code=status.HTTP_200_OK, content=request.json())
    elif request.status_code == 401:
        return JSONResponse(status_code=status.HTTP_401_UNAUTHORIZED, content="Incorrect username or password")
    elif request.status_code == 403:
        return JSONResponse(status_code=status.HTTP_403_FORBIDDEN, content="Something went wrong")
    else:
        return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST, content="Could not validate Credentials")




for router in [coin.router, order.router, user.router]:
    app.include_router(router)

connect_database(uri=str(args['cassandra_uri']), port=int(args['cassandra_port']),
                 username=str(args['cassandra_user']), password=str(args['cassandra_passwd']))

set_server_con_string(auth_uri=str(args['authentication_uri']), coin_uri=str(args['coinservice_uri']))

uvicorn.run(app, host="0.0.0.0", port=6543)
