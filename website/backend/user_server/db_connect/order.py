from fastapi import status
from fastapi.responses import JSONResponse
from cassandra.cluster import Session
from uuid import uuid4, UUID


def create_order(username: str, name: str, scraping_url, start_timestamp: int, repetitions: int, intervall: int,
                 session: Session):
    try:
        session.execute(
            "INSERT INTO order_list (uuid, creator_username, name, scraping_url, start_timestamp, repetitions, intervall)"
            "VALUES (%(id)s, %(creator_user)s, %(scrape_name)s, %(scrape_url)s, %(timestamp)s, %(repetit)s, %(interv)s)",
            {'id': uuid4(), 'creator_user': username, 'scrape_name': name, 'scrape_url': scraping_url,
             'timestamp': int(start_timestamp/1000), 'repetit': repetitions, 'interv': intervall})
        return JSONResponse(status_code=status.HTTP_201_CREATED, content="Order created")
    except:
        return JSONResponse(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, content="Error in Database")


def get_orders(username: str, session: Session):
    try:
        rows = session.execute(
            "SELECT uuid, name, creator_username, scraping_url, start_timestamp, repetitions, intervall FROM order_list "
            "WHERE creator_username=%s ALLOW FILTERING", [username])
        return get_data_list_with_keys(rows.current_rows)
    except:
        return JSONResponse(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, content="Error in Database")


def get_order(uuid: str, session: Session):
    casted_uuid = UUID(uuid)
    rows = session.execute(
        "SELECT uuid, name, creator_username, scraping_url, start_timestamp, repetitions, intervall FROM order_list WHERE uuid=%s",
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
            'intervall': row.intervall}
