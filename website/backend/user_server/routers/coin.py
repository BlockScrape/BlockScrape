from fastapi import APIRouter, Depends, Body, status
from fastapi.responses import JSONResponse
import random

router = APIRouter(
    prefix="/coin",
    tags=["coin"],
    dependencies=[],
    responses={404: {"description": "Not found"}},
)


@router.get("/info")
async def getCoins():
    return {"coin": round(random.random()*200, 2)}
