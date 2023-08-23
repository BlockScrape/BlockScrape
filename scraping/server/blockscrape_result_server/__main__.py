import asyncio
import time
from json import JSONDecoder
from typing import List, Coroutine

import redis.asyncio as redis
import socketio as socketio

from blockscrape_mining_server.schema import TaskSchema, TaskResultSchema

conn_pool = redis.ConnectionPool(host="redis", port=6379, db=0)
red = redis.Redis(connection_pool=conn_pool)

job_map = {}  # key: socket id, value: user id
sio = socketio.AsyncServer(async_mode='asgi', cors_allowed_origins='*')


@sio.event("connect")
async def connect(sid, environ):
    print("connect ", sid)


@sio.event("set_job")
async def set_user(sid, job_id):
    # add to user map if not already there
    job_map[sid] = job_id


@sio.event("disconnect")
async def disconnect(sid):
    print("disconnect ", sid)
    # remove sid from user map, clear pending tasks
    del job_map[sid]