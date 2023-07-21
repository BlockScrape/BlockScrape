from fastapi import APIRouter, Depends, Body, status
from fastapi.responses import JSONResponse

router = APIRouter(
    prefix="/order",
    tags=["order"],
    dependencies=[],
    responses={404: {"description": "Not found"}},
)


@router.get("/info")
async def getOrders():
    return {"name": "test", "url": "test", "starting_time": 1690702340, "intervall_time": 30, "repetitions": 5}


@router.post("/create")
async def create(name: str = Body(embed=True),
                 url: str = Body(embed=True),
                 starting_time: int = Body(embed=True),
                 intervall_time: int = Body(embed=True),
                 repetitions: int = Body(embed=True)):
    return JSONResponse(status_code=status.HTTP_201_CREATED, content="new order created")
