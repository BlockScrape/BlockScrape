from datetime import timedelta, datetime

import uvicorn as uvicorn
from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from routers import coin, order, user
from schemas.authentification import Token

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
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    return {"access_token": "1234", "token_type": "bearer"}


for router in [coin.router, order.router, user.router]:
    app.include_router(router)

app.mount("/", StaticFiles(directory="./static", html=True), name="static")

uvicorn.run(app, host="0.0.0.0", port=8000)
