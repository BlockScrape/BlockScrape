from datetime import timedelta
from cassandra.cluster import Session
import uvicorn as uvicorn
from fastapi import FastAPI, Depends, Body, HTTPException, status
from fastapi.responses import JSONResponse
from fastapi.security import OAuth2PasswordRequestForm
from fastapi.middleware.cors import CORSMiddleware
from auth_server.dependencies.db_connector import get_database_session, connect_database
from auth_server.dependencies.authentification import authenticate_user, ACCESS_TOKEN_EXPIRE_MINUTES, \
    create_access_token, get_current_user, hash_password
from auth_server.schemas.authentification import Token
import auth_server.db_connect.user
import argparse

parser = argparse.ArgumentParser()
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


@app.post("/token", response_model=Token)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(),
                                 session: Session = Depends(get_database_session)):
    user = authenticate_user(form_data.username, form_data.password, session)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user['username']}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}


@app.post("/user/create")
async def create_user(firstname: str = Body(embed=True),
                      lastname: str = Body(embed=True),
                      username: str = Body(embed=True),
                      passwd: str = Body(embed=True),
                      email: str = Body(embed=True),
                      birthdate: int = Body(embed=True),
                      session: Session = Depends(get_database_session)):
    return auth_server.db_connect.user.create_user(username=username, first_name=firstname, last_name=lastname,
                                                   passwd=hash_password(passwd), email=email, birth_date=birthdate, session=session)


@app.get("/user/get_by_token")
async def get_user_by_token(auth_user=Depends(get_current_user)):
    if auth_user is None:
        return JSONResponse(status_code=status.HTTP_401_UNAUTHORIZED, content="token unauthorized")
    else:
        return {'username': auth_user['username'], 'first_name': auth_user['first_name'],
                'last_name': auth_user['last_name']}

connect_database(uri=str(args['cassandra_uri']), port=int(args['cassandra_port']),
                 username=str(args['cassandra_user']), password=str(args['cassandra_passwd']))

uvicorn.run(app, host="0.0.0.0", port=7979)
