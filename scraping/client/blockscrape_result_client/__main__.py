import argparse
import asyncio
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

sio = socketio.AsyncClient()
sio.connect(mining_server_url)


@sio.event
async def connect():
    sio.emit("set_user", user_id)


@sio.on("task_bundle")
async def compute_task_bundle(data: List[TaskSchema]):
    task_results: List[TaskSchema] = asyncio.gather(*[scrape(task) for task in data])
    json_encoded = JSONEncoder().encode([task_result.model_dump_json() for task_result in task_results])
    sio.emit("task_results", task_results)


async def scrape(task: TaskSchema) -> Coroutine[TaskResultSchema]:
    async with httpx.AsyncClient() as client:
        res: httpx.Response = await client.request(method=task.method.value,
                                                   url=task.url,
                                                   params=task.params,
                                                   headers=task.headers,
                                                   content=task.content,
                                                   data=task.data,
                                                   files=task.files,
                                                   json=task.json_data,
                                                   cookies=task.cookies,
                                                   )
        return TaskResultSchema(task_id=task.id,
                                headers=res.headers,
                                content=res.content,
                                encoding=res.encoding,
                                status=res.status_code,
                                elapsed=res.elapsed,
                                )