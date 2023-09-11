import argparse
import asyncio
import threading
import time

import redis.asyncio as redis
import socketio as socketio
import uvicorn
from socketio import AsyncRedisManager

parser = argparse.ArgumentParser()
parser.add_argument('--redis_uri', default="127.0.0.1")
parser.add_argument('--redis_port', default=6379)
parser.add_argument('--task_db_number', default=0)
parser.add_argument('--socketio_db_numer', default=1)
args = vars(parser.parse_args())

conn_pool = redis.ConnectionPool(host=args["redis_uri"], port=args["redis_port"], db=args["redis_db_number"])
red = redis.Redis(connection_pool=conn_pool)

job_map = {}  # key: socket id, value: user id
job_map_rlt = {}
sio = socketio.AsyncServer(client_manager=AsyncRedisManager(f"redis://{args['redis_uri']}:{args['redis_port']}/{args['socketio_db_numer']}"),
                           async_mode='asgi',
                           cors_allowed_origins='*')
red_pubsub = red.pubsub()


@sio.event
async def connect(sid, environ):
    print("connect ", sid)


@sio.on("set_job")
async def set_job(sid, job_id):
    # add to user map if not already there
    job_map[sid] = job_id
    job_map_rlt[job_id] = sid
    print("set_user ")
    print(job_id)


@sio.event
async def disconnect(sid):
    print("disconnect ", sid)
    # remove sid from user map, clear pending tasks
    if sid in job_map.keys():
        job_id = job_map[sid]
        del job_map[sid]
        del job_map_rlt[job_id]
    else:
        print("sid not in job_map:", sid)


app = socketio.ASGIApp(sio)


def run():
    # socketio.AsyncServer class
    config = uvicorn.Config("blockscrape_result_server.__main__:app", host="0.0.0.0",
                            log_level="info")
    server = uvicorn.Server(config=config)
    server.run()


async def main():
    thread = None
    try:
        thread = threading.Thread(target=run)
        thread.start()
        await red_pubsub.psubscribe("*")
        proxy_sio = socketio.AsyncServer(client_manager=AsyncRedisManager(
            f"redis://{args['redis_uri']}:{args['redis_port']}/{args['socketio_db_numer']}",
            write_only=True))
        while True:
            message = await red_pubsub.get_message(timeout=8.0)
            print("message")
            print(message)
            if message:
                print("emit task_result")
                await proxy_sio.emit("task_result", message["data"], room=job_map_rlt[message["channel"]])
            else:
                time.sleep(1)
    except KeyboardInterrupt:
        pass
    finally:
        await red.close()
        thread.join()


if __name__ == '__main__':
    asyncio.run(main())
