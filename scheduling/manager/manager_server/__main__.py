import socketio
import eventlet

sio = socketio.Server(cors_allowed_origins='*')
app = socketio.WSGIApp(sio)

connected_clients = []

def update_client_numbers():
    total_clients = len(connected_clients)
    for i, client in enumerate(connected_clients, start=1):
        sio.emit('client_number', i, room=client['sid'])
        sio.emit('total_clients', total_clients, room=client['sid'])

@sio.event
def connect(sid, environ):
    global connected_clients
    connected_clients.append({'sid': sid})
    update_client_numbers()  # Aktualisierte Nummern und Gesamtanzahl an alle Clients senden
    print(f"Client {sid} connected. Current client count: {len(connected_clients)}")

@sio.event
def disconnect(sid):
    global connected_clients
    connected_clients = [client for client in connected_clients if client['sid'] != sid]
    update_client_numbers()  # Aktualisierte Nummern und Gesamtanzahl an alle Clients senden
    print(f"Client {sid} disconnected. Current client count: {len(connected_clients)}")

if __name__ == '__main__':
    eventlet.wsgi.server(eventlet.listen(('', 666)), app)
