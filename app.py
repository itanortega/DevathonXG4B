import eventlet
eventlet.monkey_patch()

from flask import Flask, jsonify, request
from flask_socketio import SocketIO, emit, join_room, leave_room
from dotenv import load_dotenv   
import os  

load_dotenv() 

app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('FLASK_SECRET_KEY')

if os.getenv("FLASK_ENV") == "development":
    origins = "*"                      
else:
    origins = os.getenv("FRONTEND_URL").split(",")

socketio = SocketIO(
    app, 
    cors_allowed_origins=origins
    )  

rooms = {}
client_rooms = {}


@socketio.on('connect')
def handle_connect():
    print(f'Cliente conectado: {request.sid}',flush=True)

@socketio.on('disconnect')
def handle_disconnect():
    sid = request.sid
    print(f"🔌 Cliente desconectado: {sid}",flush=True)
    if sid in client_rooms:
        room_id = client_rooms[sid]
        print(f"   → Estaba en sala: {room_id}",flush=True)
        if room_id in rooms:
            players = rooms[room_id]['players']
            print(f"   → Jugadores antes: {players}",flush=True)
            if sid in players:
                players.remove(sid)
                print(f"   → Jugadores después: {players}",flush=True)
                if len(players) == 0:
                    print(f"   → Eliminando sala {room_id} (vacía)",flush=True)
                    del rooms[room_id]
                else:
                    emit('player_left', {'room_id': room_id}, room=room_id)
        del client_rooms[sid]
    else:
        print("   → No estaba en ninguna sala",flush=True)



if __name__ == '__main__':
    socketio.run(app, 
        host='0.0.0.0', 
        port=5000,
        debug=False,        
        use_reloader=False)