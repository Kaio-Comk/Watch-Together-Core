import time
from watchtogether import RoomManager

def test_room_synchronization():
    mgr = RoomManager()
    state = mgr.create_or_join("room1", "userA")
    assert not state.is_playing
    assert state.current_seconds == 0.0
    
    # Play at second 10.0
    mgr.update_action("room1", "userA", "play", 10.0)
    time.sleep(0.05)
    
    current = mgr.get_state("room1")
    assert current.is_playing
    assert current.current_seconds >= 10.0
