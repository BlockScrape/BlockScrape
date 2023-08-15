from cassandra.cluster import Cluster, Session
from fastapi.responses import JSONResponse
from fastapi import status


create_statement = "INSERT INTO coin_data (username, coin_value) VALUES (%(usern)s, %(coin)s)"
select_statement = "SELECT * FROM coin_data WHERE username=%(usern)s"


def get_coin_status(username: str, cassandra_session: Session):
    data = select(username, cassandra_session)
    if len(data.current_rows) > 0:
        return int(data.current_rows[0].coin_value)
    else:
        cassandra_session.execute(create_statement, {'usern': username, 'coin': 0})
        return 0


def update_coin_status(username: str, add_coin: int, cassandra_session: Session):
    coins = get_coin_status(username, cassandra_session)
    if coins + add_coin >= 0:
        update_statement = "UPDATE coin_data SET coin_value=%(new_value)s WHERE username=%(usern)s"
        new_value = coins + add_coin
        cassandra_session.execute(update_statement, {'usern': username,
                                                     'new_value': new_value})
        return JSONResponse(status_code=status.HTTP_200_OK, content="Updated")
    else:
        return JSONResponse(status_code=status.HTTP_409_CONFLICT, content="Not enough coins")


def select(username: str, cassandra_session: Session):
    return cassandra_session.execute(select_statement, {'usern': username})
