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
parser.add_argument("--mining_server_url", type=str, default="http://localhost:8001")
parser.add_argument("--server_path", type=str, default="")
parser.add_argument("--user", type=str, required=True, default="")
parsed_args = parser.parse_args()
mining_server_url: str = parsed_args.mining_server_url
server_path: str = parsed_args.server_path
user_id: str = parsed_args.user

sio = socketio.Client()


@sio.event
def connect():
    sio.emit("set_user", user_id)
    print("set user_id to: ", user_id)


@sio.on("task_bundle")
def compute_task_bundle(data: List[TaskSchema]):
    print("task_bundle", data)
    print("task_bundle_type", type(data))
    task_results: List[TaskResultSchema] = [scrape(TaskSchema.model_validate(task)) for task in data]
    dumped = []
    for task_result in task_results:
        dumped.append(task_result.model_dump())


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
        content = res.content.decode("utf-8")
        return TaskResultSchema(task_id=task.id,
                                task_result_id=str(uuid.uuid4()),
                                job_id=task.job_id,
                                headers=str(res.headers),
                                time=int(time.time()),
                                content=content,
                                encoding=res.encoding,
                                status=res.status_code,
                                elapsed=int(res.elapsed.seconds))


sio.connect(mining_server_url)
