from .constants import *
from .logic.logic_predicates import *

# Setup in gameplay order.
locations_data = {
    #"Mist Island (Real World): Hardhat Worker": { Leaving this guy alone for now.
        #"vanila_item": "Sword",
        #"requirements": None, # None indicates that the location is always accessible from the last point, which is why we start from the top of the list and work our way down. If a location is not always accessible, we will need to add requirements for it.
        #"shortName": "mistWorker",
        #"treasure_spawn_mode": TREASURE_SPAWN_INSTANT
    #},
    #"Mist Island (Real World): Shop": { TODO
        #"vanila_item": "Potion",
        #"requirements": None, # None indicates that the location is always accessible from the last point, which is why we start from the top of the list and work our way down. If a location is not always accessible, we will need to add requirements for it.
        #"shortName": "mistShop",
        #"treasure_spawn_mode": TREASURE_SPAWN_INSTANT
    #},
    "Dark Lighthouse: Chest By Blue Statue": {
        "vanila_item": "Rupees (30)",
        "requirements": None,
        "room": 0x041f,
        "not_compatiable_versions": ["1.0_1", "0.3.1", "0.3", "0.2", "0.1"],
        "treasure_spawn_mode": TREASURE_SPAWN_CHEST,
        "dungeon": 1
    },
    "Dark Lighthouse: Chest With Pots And a Zol": {
        "vanila_item": "Small Key (Dark Lighthouse)",
        "requirements": None,
        "compatiable_versions": ["1.0_1", "0.3.1", "0.3", "0.2", "0.1"],
        "room": 0x041b,
        "treasure_spawn_mode": TREASURE_SPAWN_CHEST,
        "dungeon": 1
    },
    "Dark Lighthouse: Chest Around Armos": {
        "vanila_item": "Small Key (Dark Lighthouse)",
        "requirements": require_kill_normal_enemy(True),
        "not_compatiable_versions": ["1.0_1", "0.3.1", "0.3", "0.2", "0.1"],
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
        "not_compatiable_versions": ["1.0_1", "0.3.1", "0.3", "0.2", "0.1"],
        "room": 0x041D,
        "treasure_spawn_mode": TREASURE_SPAWN_CHEST,
        "dungeon": 1
    },
    "Dark Lighthouse: Chest Across Holes": {
        "vanila_item": "Small Key (Dark Lighthouse)",
        "requirements": None,
        "not_compatiable_versions": ["1.0_1", "0.3.1", "0.3", "0.2", "0.1"],
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
        }, # If we don't require one small key here, we will encounter a softlock because the creator chose to place a keydoor in a spot where it's easy to get around it without the need of a small key.
        "room": 0x0415,
        "treasure_spawn_mode": TREASURE_SPAWN_CHEST,
        "dungeon": 1
    },
    "Dark Lighthouse: Boss Key Chest": {
        "vanila_item": "Boss Key (Dark Lighthouse)",
        "requirements": {
            "all": [
                has_small_keys(1, 1)
            ]
        },
        "compatiable_versions": ["0.3.1", "0.3", "0.2", "0.1"],
        "room": 0x041C,
        "treasure_spawn_mode": TREASURE_SPAWN_CHEST,
        "dungeon": 1
    },
    "Dark Lighthouse: Light All Torches": {
        "vanila_item": "Small Key (Dark Lighthouse)",
        "requirements": {
            "all": [
                has_small_keys(1, 2), 
                require_generic_boss_and_miniboss_kill(True)
            ]
        },
        "not_compatiable_versions": ["0.3.1", "0.3", "0.2", "0.1"],
        "room": 0x0417,
        "treasure_spawn_mode": TREASURE_SPAWN_CHEST,
        "dungeon": 1
    },
    "Dark Lighthouse: Chest Near Armos And Block": {
        "vanila_item": "Rupees (100)",
        "not_compatiable_versions": ["0.3.1", "0.3", "0.2", "0.1"],
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
        "not_compatiable_versions": ["1.0_1", "0.3.1", "0.3", "0.2", "0.1"],
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
        "shortName": "d1Boss",
        "treasure_spawn_mode": TREASURE_SPAWN_POOF,
        "dungeon": 1
    },
    #TODO: Essence check (d1).
     #"Mist Island (Real World): D1 Ending Cutscene": { TODO
     #  "vanila_item": "Dream Notebook",
      # "requirements": None,
        #"treasure_spawn_mode": TREASURE_SPAWN_INSTANT,
        #"shortName": "dreamNotebookCheck"
        #"compatiable_versions": ["1.0_2", "dev"],
    #}
    #"Jingle Island (Real World): Shop": { TODO
     #  "vanila_item": "Bombs (10)",
      # "requirements": None,
        #"treasure_spawn_mode": TREASURE_SPAWN_INSTANT,
        #"shortName": "jingleIslandShop"
        #"compatiable_versions": ["1.0_2", "dev"],
    #}
    "Jingle Island (Real World): Chest On Seperate Island": {
        "vanila_item": "Rupees (50)",
        "requirements": None,
        "room": 0x0113,
        "treasure_spawn_mode": TREASURE_SPAWN_CHEST,
        "compatiable_versions": ["dev"],
    },
    "Jingle Island (Real World): Chest Across Pit": {
        "vanila_item": "Sir Cork",
        "requirements": {
            "all": [
                ("Bombs (10)", 1)
            ]
        },
        "room": 0x05b0,
        "treasure_spawn_mode": TREASURE_SPAWN_CHEST,
        "compatiable_versions": ["1.0_2", "dev"],
    },
    "Toy Chest: Compass Chest": {
        "vanila_item": "Compass (Toy Chest)",
        "requirements": None,
        "room": 0x043a,
        "dungeon": 2,
        "treasure_spawn_mode": TREASURE_SPAWN_CHEST,
        "compatiable_versions": ["1.0_2", "dev"],
    },
    "Toy Chest: Map Chest": {
        "vanila_item": "Dungeon Map (Toy Chest)",
        "requirements": None,
        "room": 0x043b,
        "dungeon": 2,
        "treasure_spawn_mode": TREASURE_SPAWN_CHEST,
        "compatiable_versions": ["1.0_2", "dev"],
    },
    #"Toy Chest: Small Key Drop": { TODO
        #"vanila_item": "Small Key (Toy Chest)",
        #"requirements": require_kill_normal_enemy(True),
        #"room": 0x0437,
        #"dungeon": 2,
        #"treasure_spawn_mode": TREASURE_SPAWN_DROP,
        #"compatiable_versions": ["1.0_2", "dev"],
    #},
    "Toy Chest: Chest Across Pit": {
        "vanila_item": "Small Key (Toy Chest)",
        "requirements": {
            "all": [
                has_small_keys(2, 1)
            ]
        },
        "dungeon": 2,
        "room": 0x0434,
        "treasure_spawn_mode": TREASURE_SPAWN_CHEST,
        "compatiable_versions": ["1.0_2", "dev"],
    },
    "Toy Chest: Bommorang Chest": {
        "vanila_item": "Spinning Boomerang",
        "requirements": None,
        "room": 0x0431,
        "dungeon": 2,
        "treasure_spawn_mode": TREASURE_SPAWN_CHEST,
        "compatiable_versions": ["1.0_2", "dev"],
    },
    "Toy Chest: Miniboss": {
        "vanila_item": "Boss Key (Toy Chest)",
        "requirements": {
            "all": [
                require_generic_boss_and_miniboss_kill(True),
                has_small_keys(2, 2),
                ("Spinning Boomerang", 1)
            ]
        },
        "room": 0x042c,
        "dungeon": 2,
        "treasure_spawn_mode": TREASURE_SPAWN_CHEST,
        "compatiable_versions": ["1.0_2", "dev"],
    },
    "Toy Chest: Boss": {
        "vanila_item": "Heart Container",
        "requirements": {
            "all": [
                has_boss_key(2)
            ]
        },
        "shortName": "d2Boss",
        "treasure_spawn_mode": TREASURE_SPAWN_POOF,
        "dungeon": 2,
        "compatiable_versions": ["1.0_2", "dev"],
    },
    # TODO: Essence check (D2)
    "Lagoon Island (Real World): Chest Inside Cave": {
        "vanila_item": "Rupees (20)",
        "requirements": None,
        "room": 0x05b1,
        "treasure_spawn_mode": TREASURE_SPAWN_CHEST,
        "compatiable_versions": ["dev"],
    },
    #"Lagoon Island (Real World): Bottle Check": { TODO
        #"vanila_item": "Letter In a Bottle",
        #"requirements": None,
        #"room": 0x0115,
        #"treasure_spawn_mode": TREASURE_SPAWN_INSTANT,
        #"compatiable_versions": ["dev"],
    #},
    #"Lagoon Island (Real World): Trade In Bottle": {
        #"vanila_item": "Progressive Flippers",
        #"requirements": {
            #"all": [
                #("Letter In a Bottle", 1)
            #]
        #},
        #"shortName": "bottleTrade",
        #"treasure_spawn_mode": TREASURE_SPAWN_INSTANT,
        #"compatiable_versions": ["dev"],
    #},
    "Murmuring Reef: Dungeon Map Chest": {
        "vanila_item": "Dungeon Map (Murmuring Reef)",
        "requirements": None,
        "room": 0x0540,
        "treasure_spawn_mode": TREASURE_SPAWN_CHEST,
        "dungeon": 3,
        "compatiable_versions": ["dev"],
    },
    #"Murmuring Reef: Small Key Drop": {
        #"vanila_item": "Small Key (Murmuring Reef)",
        #"requirements": None,
        #"room": 0x053e,
        #"treasure_spawn_mode": TREASURE_SPAWN_DROP,
        #"compatiable_versions": ["dev"],
    #},
    "Murmuring Reef: Compass Chest": {
        "vanila_item": "Compass (Murmuring Reef)",
        "requirements": None,
        "room": 0x053a,
        "dungeon": 3,
        "treasure_spawn_mode": TREASURE_SPAWN_CHEST,
        "compatiable_versions": ["dev"],
    },
    "Murmuring Reef: Miniboss": {
        "vanila_item": "Mermaid Suit",
        "requirements": {
            "all": [
                has_small_keys(3, 1)
            ]
        },
        "room": 0x0537,
        "dungeon": 3,
        "treasure_spawn_mode": TREASURE_SPAWN_CHEST,
        "compatiable_versions": ["dev"],
    },
    "Murmuring Reef: Surfaced Rupee Chest": {
        "vanila_item": "Rupees (30)",
        "requirements": {
            "all": [
                ("Mermaid Suit", 1)
            ]
        },
        "room": 0x053d,
        "dungeon": 3,
        "treasure_spawn_mode": TREASURE_SPAWN_CHEST,
        "compatiable_versions": ["dev"],
    },
    "Murmuring Reef: Shells Puzzle": {
        "vanila_item": "Boss Key (Murmuring Reef)",
        "requirements": None,
        "room": 0x0539,
        "dungeon": 3,
        "treasure_spawn_mode": TREASURE_SPAWN_CHEST,
        "compatiable_versions": ["dev"],
    },
    "Murmuring Reef: Boss": {
        "vanila_item": "Heart Container",
        "requirements": {
            "all": [
                has_boss_key(3)
            ]
        },
        "shortName": "d3Boss",
        "dungeon": 3,
        "treasure_spawn_mode": TREASURE_SPAWN_POOF,
        "compatiable_versions": ["dev"],
    },
}