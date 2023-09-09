import time
import schedule
import redis
from cassandra.cluster import Cluster, Session
from cassandra.auth import PlainTextAuthProvider
from cassandra_executor.executor import get_next_data
import argparse

cassandra_session: Session
redis_session: redis.client


parser = argparse.ArgumentParser()
parser.add_argument('--cassandra_uri', default="127.0.0.1")
parser.add_argument('--cassandra_port', default=9042)
parser.add_argument('--cassandra_user', default='cassandra')
parser.add_argument('--cassandra_passwd', default='cassandra')
parser.add_argument('--redis_uri', default="127.0.0.1")
parser.add_argument('--redis_port', default=9042)
args = vars(parser.parse_args())




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

schedule.every(10).seconds.do(get_next_data, cassandra_session, redis_session, 10)

print("Scheduling Service started")
while True:
    schedule.run_pending()
    time.sleep(1)
