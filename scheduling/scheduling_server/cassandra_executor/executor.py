from cassandra.cluster import Session
import time


def get_next_data(session: Session, schedule_time: int):
    temp_time = int(time.time())
    next_scrape_time = temp_time + schedule_time
    last_updated_time = temp_time - schedule_time/2
    select_statement = "SELECT * FROM order_list WHERE finished=false AND next_scrape<%(timing_next)s AND last_updated>%(timing_last)s;"
    update_statement = "UPDATE order_list SET last_updated=%(current_time)s WHERE finished=false AND next_scrape<%(timing_next)s AND last_updated>%(timing_last)s;"
    statement = select_statement + update_statement
    data = session.execute(statement, {'timing_next': next_scrape_time,
                                       'timing_last': last_updated_time,
                                       'current_time': temp_time})
    print(data)
