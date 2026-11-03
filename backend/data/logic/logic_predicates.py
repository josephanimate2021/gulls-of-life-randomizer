from ..constants import DUNGEON_NAMES

def has_small_keys(dungeon_id: int, amount: int = 1):
    return (f"Small Key ({DUNGEON_NAMES[dungeon_id]})", amount)

def has_boss_key(dungeon_id: int):
    return (f"Boss Key ({DUNGEON_NAMES[dungeon_id]})", 1),