from fastapi import APIRouter, Depends, Body, status
from fastapi.responses import JSONResponse

router = APIRouter(
    prefix="/coin",
    tags=["coin"],
    dependencies=[],
    responses={404: {"description": "Not found"}},
)


@router.get("/info")
async def getCoins():
    return {"coin": 132.451346}
