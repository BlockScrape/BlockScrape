import argparse
import asyncio
import threading
import time

import redis.asyncio as redis
import socketio as socketio
import uvicorn

parser = argparse.ArgumentParser()
parser.add_argument('--redis_uri', default="127.0.0.1")
parser.add_argument('--redis_port', default=6379)
args = vars(parser.parse_args())

conn_pool = redis.ConnectionPool(host=args["redis_uri"], port=args["redis_port"], db=0)
red = redis.Redis(connection_pool=conn_pool)

job_map = {}  # key: socket id, value: user id
job_map_rlt = {}
sio = socketio.AsyncServer(async_mode='asgi', cors_allowed_origins='*')
red_pubsub = red.pubsub()


@sio.event
async def connect(sid, environ):
    print("connect ", sid)


@sio.on("set_user")
async def set_user(sid, job_id):
    # add to user map if not already there
    job_map[sid] = job_id
    job_map_rlt[job_id] = sid
    await red_pubsub.subscribe(job_id)


@sio.event
async def disconnect(sid):
    print("disconnect ", sid)
    # remove sid from user map, clear pending tasks
    job_id = job_map[sid]
    del job_map[sid]
    del job_map_rlt[job_id]


app = socketio.ASGIApp(sio)


def run(self):
    config = uvicorn.Config("block_scrape_result_server.__main__:app", host="0.0.0.0",
                            log_level="info")
    server = uvicorn.Server(config=config)
    server.run()


thread = None
try:
    thread = threading.Thread(target=run)
    thread.start()
    while True:
        message = asyncio.run(red_pubsub.get_message())
        if message:
            sio.emit("task_result", message["data"], room=job_map_rlt[message["channel"]])
        else:
            time.sleep(1)
except KeyboardInterrupt:
    pass
finally:
    red_pubsub.unsubscribe()
    red_pubsub.close()
    red.close()
    thread.join()
