from flask import request
from flask_socketio import emit, join_room
from pydantic import BaseModel
from typing import List

from game import TicTacToe
from models import (
    RoomCreatedData, RoomListUpdateData, PlayerLeftData, JoinErrorData,
    JoinRoomRequest, GameStartData, GameStateData, RoomJoinedData,
    InvalidMoveData, MakeMoveRequest, RoomListData
)
import random
import string

rooms = {}
client_rooms = {}

def get_waiting_rooms() -> List[dict]:
    return [
        {"room_id": rid, "player_count": len(r["players"])}
        for rid, r in rooms.items()
        if r["status"] == "waiting"
    ]

def generate_room_id(length=6):
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=length))

def register_handlers(socketio):

    @socketio.doc_emit("player_left", PlayerLeftData)
    def _emit_player_left(room_id: str):
        emit("player_left", {"room_id": room_id}, room=room_id)

    @socketio.doc_emit("room_created", RoomCreatedData)
    def _emit_room_created(room_id: str, to_sid: str):
        emit("room_created", {"room_id": room_id}, room=to_sid)
    
    @socketio.doc_emit("room_list_update", RoomListUpdateData)
    def _emit_room_list_update():
        emit("room_list_update", get_waiting_rooms(), broadcast=True)
    
    @socketio.doc_emit("join_error", JoinErrorData)
    def _emit_join_error(error_msg: str, to_sid: str):
        emit("join_error", {"error": error_msg}, room=to_sid)

    @socketio.doc_emit("game_start", GameStartData)
    def _emit_game_start(room_id: str, player_symbol: str, to_sid: str):
        emit("game_start", {"room_id": room_id, "you_are": player_symbol}, room=to_sid)

    @socketio.doc_emit("game_state", GameStateData)  
    def _emit_game_state(game_state: dict, room_id: str):
        emit("game_state", game_state, room=room_id)

    @socketio.doc_emit("room_joined", RoomJoinedData)
    def _emit_room_joined(room_id: str, to_sid: str):
        emit("room_joined", {"room_id": room_id}, room=to_sid)

    @socketio.doc_emit("invalid_move", InvalidMoveData)
    def _emit_invalid_move(error_msg: str, to_sid: str):
        emit("invalid_move", {"error": error_msg}, room=to_sid)
    
    @socketio.doc_emit("room_list", RoomListData)
    def _emit_room_list(to_sid: str):
        emit("room_list", get_waiting_rooms(), room=to_sid)


    @socketio.on("connect")
    def handle_connect():
        print(f"Client connected: {request.sid}", flush=True)

    @socketio.on("disconnect")
    def handle_disconnect():
        sid = request.sid
        print(f"🔌 Client disconnected: {sid}", flush=True)
        if sid in client_rooms:
            room_id = client_rooms[sid]
            if room_id in rooms:
                players = rooms[room_id]["players"]
                if sid in players:
                    players.remove(sid)
                    if len(players) == 0:
                        del rooms[room_id]
                    else:
                        _emit_player_left(room_id)
            del client_rooms[sid]

    @socketio.on('create_room')
    def handle_create_room(data):
        room_name = data.get('room_name')
        if not room_name:
            room_name = generate_room_id()

        while room_name in rooms:
            room_name = generate_room_id()

        rooms[room_name] = {
            'game': TicTacToe(),
            'players': [request.sid],
            'status': 'waiting',
            'creator': request.sid
        }
        client_rooms[request.sid] = room_name
        join_room(room_name)

        emit('room_created', {'room_id': room_name}, room=request.sid)
        emit('room_list_update', get_waiting_rooms(), broadcast=True)

    @socketio.on("join_room_request", get_from_typehint=True)
    def handle_join_room(data: JoinRoomRequest):
        room_id = data.room_id
        if not room_id or room_id not in rooms:
            _emit_join_error("Room not found", request.sid)
            return

        room = rooms[room_id]
        if room["status"] != "waiting":
            _emit_join_error("Room is full or already in progress", request.sid)
            return

        room["players"].append(request.sid)
        client_rooms[request.sid] = room_id
        join_room(room_id)

        if len(room["players"]) == 2:
            room["status"] = "full"
            p1, p2 = room["players"]
            _emit_game_start(room_id, "X", p1)
            _emit_game_start(room_id, "O", p2)
            _emit_game_state(room["game"].get_state(), room_id)

        _emit_room_joined(room_id, request.sid)
        _emit_room_list_update()
    
    @socketio.on("make_move", get_from_typehint=True)
    def handle_move(data: MakeMoveRequest):
        room_id = data.room_id
        if room_id not in rooms:
            _emit_invalid_move("Room not found", request.sid)
            return

        room = rooms[room_id]
        game = room["game"]

        if game.make_move(data.row, data.col, data.player):
            _emit_game_state(game.get_state(), room_id)
        else:
            _emit_invalid_move("Invalid move", request.sid)

    @socketio.on("get_room_list")
    def handle_get_room_list():
        _emit_room_list(request.sid)