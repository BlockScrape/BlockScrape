import time
import schedule

import redis
from uuid import uuid4
from cassandra.cluster import Cluster, Session
from cassandra.auth import PlainTextAuthProvider
from cassandra_executor.executor import get_next_data
cassandra_session: Session
redis_session: redis.client


def connect_cassandra_database(uri: str, port: int, username: str = "cassandra_executor", password: str = "cassandra_executor",):
    global cassandra_session
    print(uri, port, username, password)
    auth_provider = PlainTextAuthProvider(username=username, password=password)
    cluster = Cluster([uri], port=port, auth_provider=auth_provider)
    cassandra_session = cluster.connect('blockscrape')


def connect_redis_database(uri: str, port: int):
    global redis_session
    redis_session = redis.Redis(host=uri, port=port, decode_responses=True)
    uuid_data = str(uuid4())

    redis_session.hset(uuid_data, mapping={
        'url': 'test',
        'method': 'POST'
    })
    print("HI")
    time.sleep(2)
    redis2 = redis.Redis(host=uri, port=port, decode_responses=True)
    print(redis2.hgetall(uuid_data))


connect_cassandra_database(uri="localhost", port=9042)

schedule.every(20).seconds.do(get_next_data, cassandra_session, 20)
