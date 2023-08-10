from fastapi import APIRouter, Depends, Body, status
from fastapi.responses import JSONResponse
from user_server.dependencies.validate_user import get_current_user
from user_server.db_connect.order import get_orders, create_order, delete_order
from user_server.dependencies.db_connector import get_database_session
from cassandra.cluster import Session

router = APIRouter(
    prefix="/order",
    tags=["order"],
    dependencies=[],
    responses={404: {"description": "Not found"}},
)


@router.get("/info")
async def getOrders(auth_user=Depends(get_current_user), session: Session = Depends(get_database_session)):
    if auth_user is not None:
        return get_orders(auth_user['username'], session)
    else:
        return JSONResponse(status_code=status.HTTP_403_FORBIDDEN, content="Could not validate Credentials")


@router.post("/create")
async def create(name: str = Body(embed=True),
                 url: str = Body(embed=True),
                 starting_time: int = Body(embed=True),
                 intervall_time: int = Body(embed=True),
                 repetitions: int = Body(embed=True),
                 request_header: str = Body(embed=True),
                 request_body: str = Body(embed=True),
                 request_method: str = Body(embed=True),
                 auth_user=Depends(get_current_user),
                 session: Session = Depends(get_database_session)):
    if auth_user is not None:
        if repetitions is not None and intervall_time is not None and starting_time is not None \
                and url is not None and name is not None and session is not None and request_method is not None and \
                (request_method == "POST" or request_method == "PUT" or request_method == "GET"
                 or request_method == "PATCH" or request_method == "DELETE" or request_method == "OPTIONS"
                 or request_method == "HEAD") and request_header is not None and request_body is not None:
            return create_order(name=name, scraping_url=url, start_timestamp=starting_time, intervall=intervall_time,
                                repetitions=repetitions, username=auth_user['username'], session=session,
                                request_method=request_method, request_header=request_header, request_body=request_body)
        else:
            return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST, content="wrong Input")
    else:
        return JSONResponse(status_code=status.HTTP_403_FORBIDDEN, content="Could not validate Credentials")


@router.delete("/delete")
async def delete(uuid: str = Body(embed=True),
                 auth_user=Depends(get_current_user),
                 session: Session = Depends(get_database_session)):
    if auth_user is not None:
        return delete_order(username=auth_user['username'], uuid=uuid, session=session)
    else:
        return JSONResponse(status_code=status.HTTP_403_FORBIDDEN, content="Could not validate Credentials")
