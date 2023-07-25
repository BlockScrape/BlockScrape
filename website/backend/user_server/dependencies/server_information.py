
server_con_string: str


def set_server_con_string(uri: str):
    global server_con_string
    server_con_string = uri


async def get_server_con_string():
    return server_con_string
