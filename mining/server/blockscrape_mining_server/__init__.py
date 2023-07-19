import asyncio
import time
from typing import List

import redis.asyncio as redis
from fastapi import FastAPI
from starlette.background import BackgroundTasks

from mining.server.blockscrape_mining_server.schema import TaskSchema, TaskResultSchema

app = FastAPI()

conn_pool = redis.ConnectionPool(host="redis", port=6379, db=0)
red = redis.Redis(connection_pool=conn_pool)


async def _post_process_tasks(tasks: List[str], user_id: str):
    deserialized_tasks = [TaskSchema.model_validate(task) for task in tasks]

    # add dispatching information
    edited_tasks = [_add_dispatching_information(task, user_id) for task in deserialized_tasks]

    await red.lpush("pending_tasks", *edited_tasks)


def _add_dispatching_information(task: dict, user_id: str):
    task["dispatched_to"].append((user_id, int(time.time())))
    return task

async def _process_task_result(task_result: TaskResultSchema):

    pass



@app.post("/task_bundle")
async def get_new_task_bundle(background_tasks: BackgroundTasks, nr_of_tasks: int = 10) -> List[TaskSchema]:
    # TODO get from pending tasks first
    tasks = await asyncio.gather(*
                                 [red.brpop("tasks") for i in range(nr_of_tasks)]
                                 )
    user_id = "abc123"  # TODO user auth
    background_tasks.add_task(_post_process_tasks, tasks, user_id)
    return tasks

@app.post("/submit_task_bundle")
async def submit_task_bundle(task_results: List[TaskResultSchema]):
    await asyncio.gather(*
                         [_process_task_result(x) for x in task_results]
                         )
