"""
Synchronized playback room state manager for WebSocket video players.
"""
from dataclasses import dataclass
import time

@dataclass
class PlaybackState:
    is_playing: bool
    current_seconds: float
    updated_at: float
    controller_user_id: str

class RoomManager:
    def __init__(self, drift_tolerance_s: float = 1.0):
        self.drift_tolerance = drift_tolerance_s
        self.rooms: dict[str, PlaybackState] = {}
        self.participants: dict[str, set[str]] = {}

    def create_or_join(self, room_id: str, user_id: str) -> PlaybackState:
        self.participants.setdefault(room_id, set()).add(user_id)
        if room_id not in self.rooms:
            self.rooms[room_id] = PlaybackState(
                is_playing=False,
                current_seconds=0.0,
                updated_at=time.time(),
                controller_user_id=user_id,
            )
        return self.get_state(room_id)

    def get_state(self, room_id: str) -> PlaybackState:
        state = self.rooms[room_id]
        if state.is_playing:
            # Extrapolate current time
            elapsed = time.time() - state.updated_at
            now_sec = state.current_seconds + elapsed
        else:
            now_sec = state.current_seconds
        return PlaybackState(state.is_playing, now_sec, time.time(), state.controller_user_id)

    def update_action(self, room_id: str, user_id: str, action: str, seconds: float) -> PlaybackState:
        is_playing = (action == "play")
        self.rooms[room_id] = PlaybackState(
            is_playing=is_playing,
            current_seconds=seconds,
            updated_at=time.time(),
            controller_user_id=user_id,
        )
        return self.rooms[room_id]
