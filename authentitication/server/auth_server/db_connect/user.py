from fastapi import status
from fastapi.responses import JSONResponse
from cassandra.cluster import Session
from datetime import datetime


def create_user(username: str, first_name: str, last_name: str, passwd: str, email: str, birth_date: int,
                session: Session):
    date_stamp = datetime.fromtimestamp(birth_date).strftime('%Y-%m-%d')

    if get_user(username, session) is None:
        try:
            session.execute("INSERT INTO user_data (username, first_name, last_name, passwd, email, birthdate)"
                            "VALUES (%(username)s, %(first_name)s, %(last_name)s, %(passwd)s, %(email)s, %(birthdate)s)",
                            {'username': username, 'first_name': first_name, 'last_name': last_name,
                             'passwd': passwd, 'email': email, 'birthdate': date_stamp})
            return JSONResponse(status_code=status.HTTP_201_CREATED, content="User created")
        except:
            return JSONResponse(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, content="Error in Database")
    else:
        return JSONResponse(status_code=status.HTTP_403_FORBIDDEN, content="username already exists")


def get_user(username: str, session: Session):
    rows = session.execute("SELECT username, passwd, first_name, last_name FROM user_data WHERE username=%s", [username])
    if len(rows.current_rows) == 1:
        user = {'username': rows.current_rows[0].username, 'passwd': rows.current_rows[0].passwd,
                'first_name': rows.current_rows[0].first_name, 'last_name': rows.current_rows[0].last_name}
        return user
    elif len(rows.current_rows) == 0:
        return None
