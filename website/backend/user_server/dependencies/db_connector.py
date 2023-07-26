from cassandra.cluster import Cluster, Session
from cassandra.auth import PlainTextAuthProvider

session: Session


def connect_database(uri: str, port: int, username: str = "cassandra", password: str = "cassandra"):
    global session
    print(uri, port, username, password)

    auth_provider = PlainTextAuthProvider(username=username, password=password)
    cluster = Cluster([uri], port=port, auth_provider=auth_provider)
    session = cluster.connect('blockscrape')


async def get_database_session():
    return session
