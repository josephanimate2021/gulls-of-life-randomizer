from ..constants import DUNGEON_NAMES

import os

def has_small_keys(dungeon_id: int, amount: int = 1):
    return (f"Small Key ({DUNGEON_NAMES[dungeon_id]})", amount)

def has_boss_key(dungeon_id: int):
    return (f"Boss Key ({DUNGEON_NAMES[dungeon_id]})", 1),

def has_first_version():
    if os.path.exists("rando_settings.py"):
        import rando_settings
        return rando_settings.get()["romhack_version"] == "1.0_1"
    else:
        return False