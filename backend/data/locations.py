from .constants import *
from .logic.logic_predicates import *

locations_data = {
    #"Mist Island (Real World): Hardhat Worker": { Leaving this guy alone for now.
        #"vanila_item": "Sword",
        #"requirements": None, # None indicates that the location is always accessible from the last point, which is why we start from the top of the list and work our way down. If a location is not always accessible, we will need to add requirements for it.
        #"npc_itemGiveScript_addr": 0x000a + "+balladeNpc01Script@loop",
        #"treasure_spawn_mode": TREASURE_SPAWN_INSTANT
    #},
    "Dark Lighthouse: Chest By Blue Statue": {
        "vanila_item": "Rupees (30)",
        "requirements": None,
        "room": 0x041f,
        "not_compatiable_versions": ["1.0_1"],
        "treasure_spawn_mode": TREASURE_SPAWN_CHEST,
        "dungeon": 1
    },
    "Dark Lighthouse: Chest With Pots And a Zol": {
        "vanila_item": "Small Key (Dark Lighthouse)",
        "requirements": None,
        "compatiable_versions": ["1.0_1"],
        "room": 0x041b,
        "treasure_spawn_mode": TREASURE_SPAWN_CHEST,
        "dungeon": 1
    },
    "Dark Lighthouse: Chest Around Armos": {
        "vanila_item": "Small Key (Dark Lighthouse)",
        "requirements": {
            "all": [
                ("Sword", 1)
            ]
        },
        "not_compatiable_versions": ["1.0_1"],
        "room": 0x041e,
        "treasure_spawn_mode": TREASURE_SPAWN_CHEST,
        "dungeon": 1
    },
    "Dark Lighthouse: Chest With Lever": {
        "vanila_item": "Rupees (50)",
        "requirements": {
            "all": [
                ("Lantern Of Dreams", 1)
            ]
        },
        "not_compatiable_versions": ["1.0_1"],
        "room": 0x041D,
        "treasure_spawn_mode": TREASURE_SPAWN_CHEST,
        "dungeon": 1
    },
     "Dark Lighthouse: Chest Across Holes": {
        "vanila_item": "Small Key (Dark Lighthouse)",
        "requirements": None,
        "not_compatiable_versions": ["1.0_1"],
        "room": 0x041C,
        "treasure_spawn_mode": TREASURE_SPAWN_CHEST,
        "dungeon": 1
    },
    "Dark Lighthouse: Lantern Chest": {
        "vanila_item": "Lantern Of Dreams",
        "requirements": {
            "any": [
                ("conditional", has_first_version()),
                has_small_keys(1, 1)
            ]
        }, # If we don't require one small key here, we will encounter a softlock because the creator chose to place a keydoor in a room where you can access it after going through other rooms.
        "room": 0x0415,
        "treasure_spawn_mode": TREASURE_SPAWN_CHEST,
        "dungeon": 1
    },
    "Dark Lighthouse: Light All Torches": {
        "vanila_item": "Small Key (Dark Lighthouse)",
        "requirements": {
            "all": [
                has_small_keys(1, 2), # Keeping this in despite the oldest version being present to prevent softlocks.
            ]
        },
        "room": 0x0417,
        "treasure_spawn_mode": TREASURE_SPAWN_CHEST,
        "dungeon": 1
    },
    "Dark Lighthouse: Chest Near Armos And Block": {
        "vanila_item": "Rupees (100)",
        "requirements": None,
        "room": 0x041A,
        "treasure_spawn_mode": TREASURE_SPAWN_CHEST,
        "dungeon": 1
    },
    "Dark Lighthouse: Chest Near Blue Statue And Pots": {
        "vanila_item": "Boss Key (Dark Lighthouse)",
        "requirements": {
            "all": [
                has_small_keys(1, 3)
            ]
        },
        "not_compatiable_versions": ["1.0_1"],
        "room": 0x0419,
        "treasure_spawn_mode": TREASURE_SPAWN_CHEST,
        "dungeon": 1
    },
    "Dark Lighthouse: Boss": {
        "vanila_item": "Heart Container",
        "requirements": {
            "all": [
                has_boss_key(1)
            ]
        },
        "room": 0x0413,
        "treasure_spawn_mode": TREASURE_SPAWN_POOF,
        "dungeon": 1
    },
    #TODO: Essence checks (soon) and others once D1 checks and logic is fully stable.
}