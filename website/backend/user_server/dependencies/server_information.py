
auth_server_con_string: str
coin_server_con_string: str


def set_server_con_string(auth_uri: str, coin_uri):
    global auth_server_con_string
    global coin_server_con_string
    auth_server_con_string = auth_uri
    coin_server_con_string = coin_uri


async def get_auth_server_con_string():
    return auth_server_con_string


async def get_coin_server_con_string():
    return coin_server_con_string
