import json

from fastapi import status
from fastapi.responses import JSONResponse
from cassandra.cluster import Session
from datetime import datetime
import pyotp as otp


def create_user(username: str, first_name: str, last_name: str, passwd: str, email: str, birth_date: int,
                session: Session):
    date_stamp = datetime.fromtimestamp(birth_date / 1000).strftime('%Y-%m-%d')
    pyotp_rand = otp.random_base32()
    if get_user(username, session) is None:

        query = "INSERT INTO user_data (username, first_name, last_name, passwd, email, birthdate, otp_secret, otp_verified) VALUES (?, ?, ?, ?, ?, ?, ?, ?)"

        insert_data = session.prepare(query).bind(
            {'username': username, 'first_name': first_name, 'last_name': last_name, 'passwd': passwd, 'email': email,
             'birthdate': date_stamp, 'otp_secret': pyotp_rand, 'otp_verified': False})
        session.execute(insert_data)
        content = {
            'otp_secret': pyotp_rand
        }
        return JSONResponse(status_code=status.HTTP_201_CREATED, content=content)
    else:
        return JSONResponse(status_code=status.HTTP_403_FORBIDDEN, content="username already exists")


def verify_otp_secret(username: str, mfa_key: str, session: Session):
    if get_user(username, session) is not None:
        query = "SELECT otp_secret, otp_verified FROM user_data WHERE username=?"
        get_otp_stmt = session.prepare(query).bind([username])
        rows = session.execute(get_otp_stmt)
        if len(rows.current_rows) == 1:
            if rows.current_rows[0].otp_verified is False:
                totp = otp.TOTP(rows.current_rows[0].otp_secret)
                result = totp.verify(mfa_key)
                print(result)
                if result is True:
                    update_query = "UPDATE user_data SET otp_verified = true WHERE username=?"
                    update_statement = session.prepare(update_query).bind([username])
                    session.execute(update_statement)
                    return JSONResponse(status_code=status.HTTP_200_OK, content={"result": True, "content": ""})
                return JSONResponse(status_code=status.HTTP_403_FORBIDDEN, content="Key couldn't validated")
            return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST, content="already Validated")
        return JSONResponse(status_code=status.HTTP_406_NOT_ACCEPTABLE, content="no user found")


def check_verified(username: str, session: Session):
    query = "SELECT otp_verified, otp_secret FROM user_data WHERE username=?"
    get_otp_stmt = session.prepare(query).bind([username])
    rows = session.execute(get_otp_stmt)
    if len(rows.current_rows) == 1:
        return {"verified": rows.current_rows[0].otp_verified, "key": rows.current_rows[0].otp_secret,
                "otp_google_auth": otp.totp.TOTP(rows.current_rows[0].otp_secret).provisioning_uri(
                    name=username, issuer_name='BlockScrape')}
    return None


def get_user(username: str, session: Session):
    query = "SELECT username, passwd, first_name, last_name, otp_secret FROM user_data WHERE username=?"
    get_otp_stmt = session.prepare(query).bind([username])
    rows = session.execute(get_otp_stmt)
    if len(rows.current_rows) == 1:
        user = {'username': rows.current_rows[0].username, 'passwd': rows.current_rows[0].passwd,
                'first_name': rows.current_rows[0].first_name, 'last_name': rows.current_rows[0].last_name,
                'otp_secret': rows.current_rows[0].otp_secret}
        return user
    elif len(rows.current_rows) == 0:
        return None
