import argparse
import asyncio
import queue
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
parser.add_argument('--socketio_db_number', default=1)
args = vars(parser.parse_args())

conn_pool = redis.ConnectionPool(host=args["redis_uri"], port=args["redis_port"], db=args["task_db_number"])
red = redis.Redis(connection_pool=conn_pool)

job_map = {}  # key: socket id, value: user id
job_map_rlt = {}

red_pubsub = red.pubsub()
job_sid_queue = queue.Queue()


def run(job_sid_queue):
    sio = socketio.AsyncServer(client_manager=AsyncRedisManager(
        f"redis://{args['redis_uri']}:{args['redis_port']}/{args['socketio_db_number']}"),
        async_mode='asgi',
        cors_allowed_origins='*')

    @sio.event
    async def connect(sid, environ):
        print("connect ", sid)

    @sio.on("set_job")
    async def set_job(sid, job_id):
        # add to user map if not already there
        job_sid_queue.put(("a", sid, job_id))
        print("add to queue")

    @sio.event
    async def disconnect(sid):
        print("disconnect ", sid)
        # remove sid from user map, clear pending tasks
        job_sid_queue.put(("d", sid, None))
        print("delete to queue")

    app = socketio.ASGIApp(sio)

    uvicorn.run(app=app, host="0.0.0.0", log_level="info")


async def main():
    thread = None
    try:
        thread = threading.Thread(target=run, args=(job_sid_queue,))
        thread.start()
        print("Jegger ist ein Andy")
        proxy_sio = socketio.AsyncServer(client_manager=AsyncRedisManager(
            f"redis://{args['redis_uri']}:{args['redis_port']}/{args['socketio_db_number']}",
            write_only=True))
        while True:
            #print("Jegger ist ein noch größerer Andy")
            for i in range(job_sid_queue.qsize()):
                print("hi")
                action, sid, job_id = job_sid_queue.get()
                print("hi2")
                print(action)
                if action == "a":
                    job_map[sid] = job_id
                    job_map_rlt[job_id] = sid
                    print("set_job ")
                    print(job_map_rlt)
                    print(job_id)
                    await red_pubsub.subscribe(job_id)
                elif action == "d":
                    if sid in job_map.keys():
                        print("job removing started")
                        await red_pubsub.unsubscribe(job_id)
                        print("job removed middle test")
                        job_id = job_map[sid]
                        del job_map[sid]
                        del job_map_rlt[job_id]
                        print("job removed")
                    else:
                        print("sid not in job_map:", sid)
            if len(job_map.keys()) > 0:
                print("hilfe ich bin dumm")
                message = await red_pubsub.get_message(timeout=8.0)
                print("message")
                print(message)
                if message and message["type"] == "message":
                    print("emit task_result")
                    print(message["channel"].decode('utf-8'))
                    print(job_map_rlt.keys())
                    if message["channel"].decode('utf-8') in job_map_rlt.keys():
                        print("hallo test")
                        await proxy_sio.emit("task_result", message["data"], room=job_map_rlt[message["channel"].decode('utf-8')])
                        print("hallo test test test")
                    print("hallo 123")
                else:
                    time.sleep(1)
            else:
                time.sleep(1)
    except KeyboardInterrupt:
        pass
    finally:
        await red.close()
        thread.join()


if __name__ == '__main__':
    asyncio.run(main())
