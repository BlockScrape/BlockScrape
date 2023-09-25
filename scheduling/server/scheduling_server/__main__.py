import time
from schedule import every, repeat, run_pending
import redis
from cassandra.cluster import Cluster, Session
from cassandra.auth import PlainTextAuthProvider
from cassandra_executor.executor import get_next_data
import argparse
import socketio


cassandra_session: Session
redis_session: redis.client


parser = argparse.ArgumentParser()
parser.add_argument('--cassandra_uri', default="127.0.0.1")
parser.add_argument('--cassandra_port', default=9042)
parser.add_argument('--cassandra_user', default='cassandra')
parser.add_argument('--cassandra_passwd', default='cassandra')
parser.add_argument('--redis_uri', default="127.0.0.1")
parser.add_argument('--redis_port', default=9042)
parser.add_argument('--manager_uri', default="127.0.0.1")
parser.add_argument('--manager_port', default=666)
args = vars(parser.parse_args())

number = -10
count = -10
schedule_time = 15


def connect_cassandra_database(uri: str, port: int, username: str = "cassandra_executor", password: str = "cassandra_executor",):
    global cassandra_session
    print(uri, port, username, password)
    auth_provider = PlainTextAuthProvider(username=username, password=password)
    cluster = Cluster([uri], port=port, auth_provider=auth_provider)
    cassandra_session = cluster.connect('blockscrape')


def connect_redis_database(uri: str, port: int):
    global redis_session
    redis_session = redis.Redis(host=uri, port=port, decode_responses=True)


connect_cassandra_database(uri=str(args['cassandra_uri']), port=int(args['cassandra_port']),
                           username=str(args['cassandra_user']), password=str(args['cassandra_passwd']))
connect_redis_database(uri=str(args['redis_uri']), port=int(args['redis_port']))

sio = socketio.Client()

@repeat(every(schedule_time).seconds)
def job():
    get_next_data(cassandra_session, redis_session, schedule_time - 5, number - 1, count)

@sio.event
def connect():
    print('Verbunden zum Socket.io-Server')


@sio.on('client_number')
def receive_client_number(client_number):
    global number
    number = client_number
    print(f'Client-Number is: {client_number}')


@sio.on('total_clients')
def receive_total_clients(total_clients):
    global count
    count = total_clients
    print(f'Client-Count is: {total_clients}')


@sio.event
def disconnect():
    print('Verbindung zum Socket.io-Server getrennt')


if __name__ == '__main__':
    sio.connect(args['manager_uri']+":"+args['manager_port'])
    print("Scheduling Service started")
    while True:
        time.sleep(1)
        run_pending()
