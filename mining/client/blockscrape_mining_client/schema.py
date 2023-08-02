from datetime import timedelta
from enum import Enum
from typing import List, Tuple

from pydantic import BaseModel


class RequestMethod(Enum):
    get = "GET"
    options = "OPTIONS"
    head = "HEAD"
    post = "POST"
    put = "PUT"
    patch = "PATCH"
    delete = "DELETE"


class TaskSchema(BaseModel):
    id: str
    method: RequestMethod
    url: str
    params: str | dict
    headers: str
    content: bytes
    data: dict
    files: dict
    json_data: str
    headers: dict
    cookies: dict

    validated: bool = False
    pending_users: List[Tuple[str, int]]
    finished_users: List[Tuple[str, int]]


class TaskResultSchema(BaseModel):
    task_result_id: str
    task_id: str
    headers: str
    content: bytes
    encoding: str
    status: int
    elapsed: timedelta
