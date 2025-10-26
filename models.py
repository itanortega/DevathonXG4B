from typing import Optional, List
from pydantic import BaseModel, Field

class RoomCreatedData(BaseModel):
    room_id: str = Field(..., description="Unique room ID")


class RoomInfo(BaseModel):
    room_id: str = Field(..., example="ABC123")
    player_count: int = Field(..., ge=1, le=2, example=1)


class RoomListData(BaseModel):
    __root__: List[RoomInfo]


class RoomListUpdateData(BaseModel):
    __root__: List[RoomInfo]


class PlayerLeftData(BaseModel):
    room_id: str = Field(..., description="ID of the affected room")


class GameStateData(BaseModel):
    board: List[List[str]] = Field(
        ...,
        description="Current 3x3 game board state",
        example=[["X", "", "O"], ["", "X", ""], ["", "", "O"]]
    )
    current_turn: str = Field(..., example="O")
    winner: Optional[str] = Field(None, example="X")
    game_over: bool = Field(..., example=False)


class JoinRoomRequest(BaseModel):
    room_id: str = Field(..., description="ID of the room to join", example="ABC123")


class JoinErrorData(BaseModel):
    error: str = Field(..., description="Error message", example="Room not found")


class GameStartData(BaseModel):
    room_id: str = Field(..., description="Room ID", example="ABC123")
    you_are: str = Field(..., description="Your symbol in the game ('X' or 'O')", example="X")


class RoomJoinedData(BaseModel):
    room_id: str = Field(..., description="ID of the joined room", example="ABC123")


class MakeMoveRequest(BaseModel):
    room_id: str = Field(..., description="Room ID", example="ABC123")
    row: int = Field(..., ge=0, le=2, description="Board row (0-2)", example=1)
    col: int = Field(..., ge=0, le=2, description="Board column (0-2)", example=0)
    player: str = Field(..., pattern="^[XO]$", description="Player symbol ('X' or 'O')", example="X")


class InvalidMoveData(BaseModel):
    error: str = Field(..., description="Error message", example="Invalid move")