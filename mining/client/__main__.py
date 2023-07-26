import socketio
sio = socketio.AsyncClient()
@sio.event()

if __name__ == '__main__':
    get_and_run_task_bundle()
