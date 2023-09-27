import time
import uuid
from json import JSONEncoder
from pydantic import BaseModel
import redis
from cassandra.cluster import Session
from enum import Enum


class RequestMethod(Enum):
    get = "GET"
    options = "OPTIONS"
    head = "HEAD"
    post = "POST"
    put = "PUT"
    patch = "PATCH"
    delete = "DELETE"


class TaskSchema(BaseModel):
    id: str
    method: RequestMethod
    url: str
    headers: str
    content: bytes
    creator_user: str
    job_id: str


def get_next_data(session: Session, redis_session: redis.client, schedule_time: int, client_number, client_count):
    if client_number != -10 or client_count != -10:
        temp_time = int(time.time())
        next_scrape_time = temp_time + schedule_time
        last_updated_time = int(temp_time - (schedule_time / 2))
        select_statement = "SELECT * FROM order_list WHERE finished=false AND next_scrape<? AND last_updated<? ALLOW FILTERING;"
        update_statement = "UPDATE order_list SET repetitions=%(repetit)s, finished=%(finish)s, next_scrape=%(timing_next)s, last_updated=%(current_time)s WHERE uuid=%(ident)s;"
        select_data = session.prepare(select_statement).bind({'next_scrape': next_scrape_time,
                                                              'last_updated': last_updated_time})
        data = session.execute(select_data)
        for row in data.current_rows:
            if row.scheduler_number % client_count == client_number:
                print(row)
                repetitions = row.repetitions - 1
                finished = False
                if repetitions == 0:
                    finished = True
                next_scrape_time = row.next_scrape + row.intervall

                session.execute(update_statement, {'repetit': repetitions,
                                                   'finish': finished,
                                                   'timing_next': next_scrape_time,
                                                   'current_time': temp_time,
                                                   'ident': row.uuid})
                redis_session.lpush('tasks',
                                    TaskSchema(id=str(uuid.uuid4()), method=row.request_method, url=row.scraping_url,
                                               headers=row.request_header, content=bytes(row.request_body, 'utf-8'),
                                               creator_user=row.creator_username,
                                               job_id=str(row.uuid)).model_dump_json()
                                    )
    else:
        print("Client Number not set")
