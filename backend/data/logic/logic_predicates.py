from ..constants import DUNGEON_NAMES

import os
import json

def has_small_keys(dungeon_id: int, amount: int = 1):
    return (f"Small Key ({DUNGEON_NAMES[dungeon_id]})", amount)

def has_boss_key(dungeon_id: int):
    return (f"Boss Key ({DUNGEON_NAMES[dungeon_id]})", 1)

def has_first_version():
    if os.path.exists("rando_settings.json"):
        rando_settings = json.loads(open("rando_settings.json").read())
        return rando_settings["romhack_version"] in ["1.0_1", "0.3", "0.2", "0.1"]
    else:
        return False