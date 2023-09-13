import argparse
import asyncio
import time
import uuid
from json import JSONDecoder, JSONEncoder
from typing import List, Coroutine
import httpx
import socketio

from schema import TaskResultSchema, TaskSchema

parser = argparse.ArgumentParser()
parser.add_argument("--mining_server_url", type=str, default="localhost")
parser.add_argument("--user", type=str, required=True)
parsed_args = parser.parse_args()
mining_server_url: str = parsed_args.mining_server_url
user_id: str = parsed_args.user

sio = socketio.Client()


@sio.event
def connect():
    sio.emit("set_user", user_id)


@sio.on("task_bundle")
def compute_task_bundle(data: List[TaskSchema]):
    print("task_bundle", data)
    print("task_bundle_type", type(data))
    task_results: List[TaskResultSchema] = [scrape(TaskSchema.model_validate(task)) for task in data]
    json_encoded = JSONEncoder().encode([task_result.model_dump() for task_result in task_results])
    sio.emit("task_results", json_encoded)
    print("task_results", json_encoded)


def scrape(task: TaskSchema):
    with httpx.Client() as client:
        res: httpx.Response = client.request(method=task.method.value,
                                                         url=task.url,
                                                         headers=task.headers,
                                                         content=task.content,
                                             timeout=5.0
                                                             )
        return TaskResultSchema(task_id=task.id,
                                task_result_id=str(uuid.uuid4()),
                                job_id=task.job_id,
                                headers=str(res.headers),
                                time=int(time.time()),
                                content=res.content,
                                encoding=res.encoding,
                                status=res.status_code,
                                elapsed=res.elapsed)


sio.connect(mining_server_url)
