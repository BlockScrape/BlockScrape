import time
from uuid import uuid4, UUID
import random
from cassandra.cluster import Session
from fastapi import status
from fastapi.responses import JSONResponse


def create_order(username: str, name: str, scraping_url, start_timestamp: int, repetitions: int, intervall: int,
                 request_method: str, request_header: str, request_body: str, session: Session):
    create_statement = "INSERT INTO order_list (uuid, creator_username, name, scraping_url, request_method, request_header, request_body, start_timestamp, next_scrape, last_updated, intervall, repetitions, finished, scheduler_number) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)"
    create_data = session.prepare(create_statement).bind({'uuid': uuid4(),
                                                          'creator_username': username,
                                                          'name': name,
                                                          'scraping_url': scraping_url,
                                                          'request_method': request_method,
                                                          'request_header': request_header,
                                                          'request_body': request_body,
                                                          'start_timestamp': int(start_timestamp / 1000),
                                                          'next_scrape': int(start_timestamp / 1000),
                                                          'last_updated': int(time.time()),
                                                          'intervall': intervall,
                                                          'repetitions': repetitions,
                                                          'finished': False,
                                                          'scheduler_number': random.randint(1, 10)
                                                          })
    session.execute(create_data)
    return JSONResponse(status_code=status.HTTP_201_CREATED, content="Order created")


def get_orders(username: str, session: Session):
    try:
        rows = session.execute(
            "SELECT * FROM order_list "
            "WHERE creator_username=%s ALLOW FILTERING", [username])
        return get_data_list_with_keys(rows.current_rows)
    except:
        return JSONResponse(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, content="Error in Database")


def get_order(uuid: str, session: Session):
    casted_uuid = UUID(uuid)
    rows = session.execute(
        "SELECT * FROM order_list WHERE uuid=%s",
        [casted_uuid])
    if len(rows.current_rows) == 1:
        return get_data_with_keys(rows.current_rows[0])
    else:
        return None


def delete_order(username: str, uuid: str, session: Session):
    order = get_order(uuid, session)
    if order is not None:
        if order['creator_username'] == username:
            casted_uuid = UUID(uuid)
            session.execute("DELETE FROM order_list WHERE uuid=%s", [casted_uuid])
            return JSONResponse(status_code=status.HTTP_200_OK, content="Order deleted")
        else:
            return JSONResponse(status_code=status.HTTP_403_FORBIDDEN, content="Nope")
    else:
        return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST, content="No Order")


def get_data_list_with_keys(rows):
    data = []
    for row in rows:
        data.append(get_data_with_keys(row))
    return data


def get_data_with_keys(row):
    return {'uuid': row.uuid, 'name': row.name, 'creator_username': row.creator_username,
            'scraping_url': row.scraping_url, 'start_timestamp': row.start_timestamp, 'repetitions': row.repetitions,
            'intervall': row.intervall, 'request_header': row.request_header, 'request_body': row.request_body,
            'request_method': row.request_method, 'next_scrape': row.next_scrape, 'last_updated': row.last_updated,
            'finished': row.finished}
