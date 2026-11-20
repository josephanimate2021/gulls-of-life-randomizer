from ..constants import DUNGEON_NAMES

import os
import json
import random

def has_small_keys(dungeon_id: int, amount: int = 1):
    return (f"Small Key ({DUNGEON_NAMES[dungeon_id]})", amount)

def has_boss_key(dungeon_id: int):
    return (f"Boss Key ({DUNGEON_NAMES[dungeon_id]})", 1)

def has_first_version():
    rando_settings = get_rando_settings()
    return rando_settings["romhack_version"] in ["1.0_1", "0.3.1", "0.3", "0.2", "0.1"] if rando_settings is not None else False

def get_rando_settings():
    return json.loads(open("rando_settings.json").read()) if os.path.exists("rando_settings.json") else None

def require_kill_normal_enemy(can_kill_with_hook: bool = False, pit_available: bool = False):
    rando_settings = get_rando_settings()
    possible_items = ["Biggoron's Sword"]
    has_sword = rando_settings is None or rando_settings["guarentee_sword"]
    if has_sword:
        possible_items = ["conditional"]
    else:
        if pit_available:
            possible_items.append("Shield")
        if can_kill_with_hook:
            possible_items.append("Echo Hook")
        if rando_settings["logic"] == "medium":
            possible_items.extend(["Bombs (10)", "Cane of Dreams", "Bombchus (10)"])
    return {"all": [(random.choice(possible_items), True if has_sword else 1)]}

def require_generic_boss_and_miniboss_kill(can_use_bombs: bool = False):
    rando_settings = get_rando_settings()
    possible_items = []
    has_sword = rando_settings is None or rando_settings["guarentee_sword"]
    if not has_sword:
        possible_items.append("Biggoron's Sword")
        if can_use_bombs and rando_settings["logic"] == "medium":
            possible_items.append("Bombs (10)")
    else:
        possible_items.append("conditional")
    return {"all": [(random.choice(possible_items), True if has_sword else 1)]}

def pick_sword(): # TODO: Use this function when collect mode is implemented.
    return random.choice(["Biggoron's Sword", "Sword"])