import uvicorn as uvicorn
from fastapi import FastAPI, Body
from fastapi.middleware.cors import CORSMiddleware
import argparse
from cassandra.cluster import Cluster, Session
from cassandra.auth import PlainTextAuthProvider
from coin_server.database.database_executor import get_coin_status, update_coin_status

cassandra_session: Session

parser = argparse.ArgumentParser()
parser.add_argument('--cassandra_uri', default="127.0.0.1")
parser.add_argument('--cassandra_port', default=9042)
parser.add_argument('--cassandra_user', default='cassandra')
parser.add_argument('--cassandra_passwd', default='cassandra')
args = vars(parser.parse_args())

app = FastAPI()

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/get_coin")
async def get_coin(username: str = Body(embed=True)):
    return get_coin_status(username=username, cassandra_session=cassandra_session)


@app.put("/update_coin")
async def update_coin(username: str = Body(embed=True),
                      addition: int = Body(embed=True)):
    return update_coin_status(username=username, add_coin=addition, cassandra_session=cassandra_session)


def connect_cassandra_database(uri: str, port: int, username: str = "cassandra_executor", password: str = "cassandra_executor",):
    global cassandra_session
    print(uri, port, username, password)
    auth_provider = PlainTextAuthProvider(username=username, password=password)
    cluster = Cluster([uri], port=port, auth_provider=auth_provider)
    cassandra_session = cluster.connect('blockscrape')


connect_cassandra_database(uri=str(args['cassandra_uri']), port=int(args['cassandra_port']),
                           username=str(args['cassandra_user']), password=str(args['cassandra_passwd']))


uvicorn.run(app, host="0.0.0.0", port=1337)
