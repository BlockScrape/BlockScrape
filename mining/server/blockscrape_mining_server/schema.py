import datetime
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
    headers: str
    content: bytes
    creator_user: str
    job_id: str


class TaskResultSchema(BaseModel):
    task_result_id: str
    task_id: str
    job_id: str
    headers: str
    content: str
    encoding: str
    status: int
    time: int
    elapsed: int
