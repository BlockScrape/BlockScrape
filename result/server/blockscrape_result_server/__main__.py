import argparse
import asyncio
import queue
import threading
import time
import pika
import redis.asyncio as redis
import socketio as socketio
import uvicorn
from socketio import RedisManager, AsyncRedisManager
import json
import eventlet



parser = argparse.ArgumentParser()
parser.add_argument('--redis_uri', default="127.0.0.1")
parser.add_argument('--redis_port', default=6379)
parser.add_argument('--task_db_number', default=0)
parser.add_argument('--socketio_db_number', default=1)
parser.add_argument('--rabbitMQ_uri', default="localhost")
parser.add_argument('--rabbitMQ_user', default="user")
parser.add_argument('--rabbitMQ_passwd', default="user")
args = vars(parser.parse_args())

conn_pool = redis.ConnectionPool(host=args["redis_uri"], port=args["redis_port"], db=args["task_db_number"])
red = redis.Redis(connection_pool=conn_pool)

job_map = {}  # key: socket id, value: user id
job_map_rlt = {}

red_pubsub = red.pubsub()
job_sid_queue = queue.Queue()

credentials = pika.PlainCredentials(args["rabbitMQ_user"], args["rabbitMQ_passwd"])
connection = pika.BlockingConnection(pika.ConnectionParameters(args["rabbitMQ_uri"], credentials=credentials))
channel = connection.channel()
exchange_name = 'results'
connection.channel().exchange_declare(exchange=exchange_name, exchange_type='fanout')
# Name des Exchanges (Fanout Exchange)
exchange_name = 'results'

# Temporäre Warteschlange erstellen
result = channel.queue_declare(queue='', exclusive=True)
queue_name = result.method.queue

# Binden Sie die Warteschlange an das Exchange
channel.queue_bind(exchange=exchange_name, queue=queue_name)
# Nachrichten empfangen


print(' [*] Consumer 1 is waiting for messages. To exit, press CTRL+C')
channel.start_consuming()


def run(job_sid_queue):
    sio = socketio.Server(client_manager=RedisManager(
        f"redis://{args['redis_uri']}:{args['redis_port']}/{args['socketio_db_number']}"),
        cors_allowed_origins='*')

    @sio.event
    def connect(sid, environ):
        print("connect ", sid)

    @sio.on("set_job")
    def set_job(sid, job_id):
        # add to user map if not already there
        job_sid_queue.put(("a", sid, job_id))
        print("add to queue")

    @sio.event
    def disconnect(sid):
        print("disconnect ", sid)
        # remove sid from user map, clear pending tasks
        job_sid_queue.put(("d", sid, None))
        print("delete to queue")

    app = socketio.WSGIApp(sio)
    eventlet.monkey_patch()
    eventlet.wsgi.server(eventlet.listen(('', 8000)), app)


def callback(ch, method, properties, body):
    for i in range(job_sid_queue.qsize()):
        action, sid, job_id = job_sid_queue.get()
        if action == "a":
            job_map[sid] = job_id
            job_map_rlt[job_id] = sid
            print("set_job ")
            print(job_map_rlt)
            print(job_id)
        elif action == "d":
            if sid in job_map.keys():
                print("job removing started")
                job_id = job_map[sid]
                del job_map[sid]
                del job_map_rlt[job_id]
                print("job removed")
            else:
                print("sid not in job_map:", sid)
    if len(job_map.keys()) > 0:
        message = json.loads(body)
        job_id = message.get('job_id')
        ergebnis = json.loads(message.get('result'))
        if ergebnis is not None:
            print("emit task_result")
            print(job_id)
            print(job_map_rlt.keys())
            if job_id in job_map_rlt.keys():
                print(job_map_rlt[job_id])
                proxy_sio.emit("task_result", ergebnis,
                               room=job_map_rlt[job_id])
        print(f" [x] Consumer 1 received '{ergebnis}' for Job ID {job_id}")


if __name__ == '__main__':
    thread = threading.Thread(target=run, args=(job_sid_queue,))
    thread.start()
    proxy_sio = socketio.Server(client_manager=RedisManager(
        f"redis://{args['redis_uri']}:{args['redis_port']}/{args['socketio_db_number']}",
        write_only=True))
    channel.basic_consume(queue=queue_name, on_message_callback=callback, auto_ack=True)
    print("run Consumer")
    channel.start_consuming()
