from fastapi import APIRouter, Depends, Body, status
from fastapi.responses import JSONResponse

router = APIRouter(
    prefix="/user",
    tags=["user"],
    dependencies=[],
    responses={404: {"description": "Not found"}},
)


@router.post("/create")
async def create(firstname: str = Body(embed=True),
                 lastname: str = Body(embed=True),
                 username: str = Body(embed=True),
                 passwd: str = Body(embed=True),
                 email: str = Body(embed=True)):
    return JSONResponse(status_code=status.HTTP_201_CREATED, content="new user created")

