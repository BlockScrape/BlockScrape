import argparse
import asyncio
import time
from json import JSONDecoder
from typing import List, Coroutine

import uvicorn
import redis.asyncio as redis
import socketio as socketio

from blockscrape_mining_server.schema import TaskSchema, TaskResultSchema

parser = argparse.ArgumentParser()
parser.add_argument('--redis_uri', default="127.0.0.1")
parser.add_argument('--redis_port', default=6379)
args = vars(parser.parse_args())

conn_pool = redis.ConnectionPool(host=args["redis_uri"], port=args["redis_port"], db=0)
red = redis.Redis(connection_pool=conn_pool)
red_pubsub = red.pubsub()
user_map = {}  # key: socket id, value: user id


def _add_dispatching_information(task: TaskSchema, user_id: str):
    task.pending_users.append((user_id, int(time.time())))
    return task


async def get_new_task_bundle(user_id, nr_of_tasks: int = 10):
    # TODO get from pending tasks first
    tasks = await asyncio.gather(*
                                 [red.brpop("tasks") for i in range(nr_of_tasks)]
                                 )
    yield tasks
    deserialized_tasks = [TaskSchema.model_validate(task) for task in tasks]

    # add dispatching information
    edited_tasks = [_add_dispatching_information(task, user_id) for task in deserialized_tasks]

    await red.lpush("pending_tasks", *edited_tasks)

    return


async def _process_task_result(task_result: TaskResultSchema, user_id: str):
    return task_result


sio = socketio.AsyncServer(async_mode='asgi', cors_allowed_origins='*')


@sio.event
async def connect(sid, environ):
    print("connect ", sid)


@sio.on("set_user")
async def set_user(sid, user_id):
    # add to user map if not already there
    user_map[sid] = user_id
    print("set user", user_id)

    # send first task bundle
    await sio.emit("task_bundle", await get_new_task_bundle(10), room=sid)


@sio.on("task_results")
async def task_result(sid, data):
    """
    :param sid: socket id
    :param data: json_data encoded list of json_data encoded TaskResultSchema
    :return:
    """
    print("task_results", data)
    task_results = [TaskResultSchema.model_validate(x) for x in JSONDecoder().decode(data)]
    processed_results = await asyncio.gather(*
                                             [_process_task_result(x, user_map[sid]) for x in task_results]
                                             )
    # write results to redis
    await sio.emit("task_bundle", await get_new_task_bundle(10), room=sid)
    [await red.publish(result.job_id, result) for result in processed_results]


@sio.event
async def disconnect(sid):
    print("disconnect ", sid)
    # remove sid from user map, clear pending tasks
    del user_map[sid]


app = socketio.ASGIApp(sio)
uvicorn.run(app, host="0.0.0.0", port=8000, log_level="info")
