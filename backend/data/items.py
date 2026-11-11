from .items_classification import ItemClassification

ITEMS_DATA = {
    #   "No Item": {
    #   'classification': ItemClassification.filler,
    #   "",
    #    'id': 0x00,
    #    'subid': 0x00
    #    },
    "Shield": {
        'classification': ItemClassification.progression,
        'id': 0x01,
        'hidden': True
    },
    "Bombs (10)": {
        'classification': ItemClassification.progression,
        'id': 0x03
    },
    "Sword": {
        'classification': ItemClassification.progression,
        'id': 0x05,
        'hidden': True
    },
    "Boomerang": {
        'classification': ItemClassification.progression,
        'id': 0x06,
        'subid': 0x04
    },
    "Lantern Of Dreams": {
        'classification': ItemClassification.progression,
        'id': 0x11,
        'subid': 0x02                                                                                                          
    },
    "Switch Hook": {
        'classification': ItemClassification.progression,
        'id': 0x0a
    },
    "Cane of Somaria": {
        'classification': ItemClassification.progression,
        'id': 0x04
    },
    "Biggoron's Sword": {
        'classification': ItemClassification.progression,
        'id': 0x0c
    },
    "Bombchus (10)": {
        'classification': ItemClassification.progression,
        'id': 0x0d,
        'subid': 0x01
    },
    "Seed Shooter": {
        'classification': ItemClassification.progression,
        'id': 0x0f
    },
    "Shovel": {
        'classification': ItemClassification.progression,
        'id': 0x15,
        'hidden': True
    },
    "Power Glove": {
        'classification': ItemClassification.progression,
        'id': 0x16,
        'subid': 0x02
    },
    "Roc's Cape": {
        'classification': ItemClassification.progression,
        'id': 0x17,
        'subid': 0x03
    },
    "Seed Satchel": {
        'classification': ItemClassification.progression,
        'id': 0x19,
        'hidden': True
    },
    #"Ember Seeds": {
     #   'classification': ItemClassification.progression,
      #  'id': 0x20
    #},
    #"Scent Seeds": {
     #   'classification': ItemClassification.progression,
      #  'id': 0x21
    #},
    #"Pegasus Seeds": {
     #   'classification': ItemClassification.progression,
      #  'id': 0x22
    #},
    #"Gale Seeds": {
     #   'classification': ItemClassification.progression,
      #  'id': 0x23
    #},
    #"Mystery Seeds": {
     #   'classification': ItemClassification.progression,
      #  'id': 0x24
    #},
    "Rupees (1)": {
        'classification': ItemClassification.filler,
        'id': 0x28,
        'subid': 0x00
    },
    "Rupees (5)": {
        'classification': ItemClassification.filler,
        'id': 0x28,
        'subid': 0x01
    },
    "Rupees (10)": {
        'classification': ItemClassification.filler,
        'id': 0x28,
        'subid': 0x02
    },
    "Rupees (20)": {
        'classification': ItemClassification.filler,
        'id': 0x28,
        'subid': 0x03
    },
    "Rupees (30)": {
        'classification': ItemClassification.filler,
        'id': 0x28,
        'subid': 0x04
    },
    "Rupees (50)": {
        'classification': ItemClassification.filler,
        'id': 0x28,
        'subid': 0x05
    },
    "Rupees (100)": {
        'classification': ItemClassification.filler,
        'id': 0x28,
        'subid': 0x06
    },
    "Rupees (200)": {
        'classification': ItemClassification.filler,
        'id': 0x28,
        'subid': 0x08
    },
    "Heart Container": {
        'classification': ItemClassification.filler,
        'id': 0x2a,
        'subid': 0x01
    },
    "Piece of Heart": {
        'classification': ItemClassification.filler,
        'id': 0x2b,
        'subid': 0x01
    },
    "Progressive Flippers": {
        'classification': ItemClassification.progression,
        'id': 0x2e,
        'subid': 0x01,
        'hidden': True
    },
    "Potion": {
        'classification': ItemClassification.filler,
        'id': 0x2f,
        'hidden': True
    },

    #"Small Key (Maku Path)": {
     #   'classification': ItemClassification.progression,
      #  'id': 0x30,
       # 'subid': 0x00
    #},
    "Small Key (Dark Lighthouse)": {
        'classification': ItemClassification.progression,
        'id': 0x30,
        'subid': 0x01
    },
    "Small Key (Toy Chest)": {
        'classification': ItemClassification.progression,
        'id': 0x30,
        'subid': 0x02,
        'hidden': True
    },
    "Small Key (Murmuring Reef)": {
        'classification': ItemClassification.progression,
        'id': 0x30,
        'subid': 0x03,
        'hidden': True
    },
    "Small Key (Sleeping Forge)": {
        'classification': ItemClassification.progression,
        'id': 0x30,
        'subid': 0x04,
        'hidden': True
    },
    "Small Key (Echo Cathedral)": {
        'classification': ItemClassification.progression,
        'id': 0x30,
        'subid': 0x05,
        'hidden': True
    },
    "Small Key (Sky Spiral)": {
        'classification': ItemClassification.progression,
        'id': 0x30,
        'subid': 0x06,
        'hidden': True
    },
    "Small Key (Frost Palace)": {
        'classification': ItemClassification.progression,
        'id': 0x30,
        'subid': 0x07,
        'hidden': True
    },
    "Small Key (Sleepless Tower)": {
        'classification': ItemClassification.progression,
        'id': 0x30,
        'subid': 0x08,
        'hidden': True
    },
    "Small Key (The Snakes' Burrow)": {
        'classification': ItemClassification.progression,
        'id': 0x30,
        'subid': 0x0b,
        'hidden': True
    },
    "Master Key (Dark Lighthouse)": {
        'classification': ItemClassification.progression,
        'id': 0x30,
        'subid': 0x01,
        'hidden': True
    },
    "Master Key (Toy Chest)": {
        'classification': ItemClassification.progression,
        'id': 0x30,
        'subid': 0x02,
        'hidden': True
    },
    "Master Key (Murmuring Reef)": {
        'classification': ItemClassification.progression,
        'id': 0x30,
        'subid': 0x03,
        'hidden': True
    },
    "Master Key (Sleeping Forge)": {
        'classification': ItemClassification.progression,
        'id': 0x30,
        'subid': 0x04,
        'hidden': True
    },
    "Master Key (Echo Cathedral)": {
        'classification': ItemClassification.progression,
        'id': 0x30,
        'subid': 0x05,
        'hidden': True
    },
    "Master Key (Sky Spiral)": {
        'classification': ItemClassification.progression,
        'id': 0x30,
        'subid': 0x06,
        'hidden': True
    },
    "Master Key (Frost Palace)": {
        'classification': ItemClassification.progression,
        'id': 0x30,
        'subid': 0x07,
        'hidden': True
    },
    "Master Key (Sleepless Tower)": {
        'classification': ItemClassification.progression,
        'id': 0x30,
        'subid': 0x08,
        'hidden': True
    },
    "Master Key (The Snakes' Burrow)": {
        'classification': ItemClassification.progression,
        'id': 0x30,
        'subid': 0x0b,
        'hidden': True
    },
    "Boss Key (Dark Lighthouse)": {
        'classification': ItemClassification.progression,
        'id': 0x31,
        'subid': 0x01
    },
    "Boss Key (Toy Chest)": {
        'classification': ItemClassification.progression,
        'id': 0x31,
        'subid': 0x02
    },
    "Boss Key (Murmuring Reef)": {
        'classification': ItemClassification.progression,
        'id': 0x31,
        'subid': 0x03,
        'hidden': True
    },
    "Boss Key (Sleeping Forge)": {
        'classification': ItemClassification.progression,
        'id': 0x31,
        'subid': 0x04,
        'hidden': True
    },
    "Boss Key (Echo Cathedral)": {
        'classification': ItemClassification.progression,
        'id': 0x31,
        'subid': 0x05,
        'hidden': True
    },
    "Boss Key (Sky Spiral)": {
        'classification': ItemClassification.progression,
        'id': 0x31,
        'subid': 0x06,
        'hidden': True
    },
    "Boss Key (Frost Palace)": {
        'classification': ItemClassification.progression,
        'id': 0x31,
        'subid': 0x07,
        'hidden': True
    },
    "Boss Key (Sleepless Tower)": {
        'classification': ItemClassification.progression,
        'id': 0x31,
        'subid': 0x08,
        'hidden': True
    },
    "Compass (Dark Lighthouse)": {
        'classification': ItemClassification.filler,
        'id': 0x32,
        'subid': 0x01
    },
    "Compass (Toy Chest)": {
        'classification': ItemClassification.filler,
        'id': 0x32,
        'subid': 0x02
    },
    "Compass (Murmuring Reef)": {
        'classification': ItemClassification.filler,
        'id': 0x32,
        'subid': 0x03,
        'hidden': True
    },
    "Compass (Sleeping Forge)": {
        'classification': ItemClassification.filler,
        'id': 0x32,
        'subid': 0x04
    },
    "Compass (Echo Cathedral)": {
        'classification': ItemClassification.filler,
        'id': 0x32,
        'subid': 0x05,
        'hidden': True
    },
    "Compass (Sky Spiral)": {
        'classification': ItemClassification.filler,
        'id': 0x32,
        'subid': 0x06,
        'hidden': True
    },
    "Compass (Frost Palace)": {
        'classification': ItemClassification.filler,
        'id': 0x32,
        'subid': 0x07
    },
    "Compass (Sleepless Tower)": {
        'classification': ItemClassification.filler,
        'id': 0x32,
        'subid': 0x08
    },
    "Dungeon Map (Dark Lighthouse)": {
        'classification': ItemClassification.filler,
        'id': 0x33,
        'subid': 0x01
    },
    "Dungeon Map (Toy Chest)": {
        'classification': ItemClassification.filler,
        'id': 0x33,
        'subid': 0x02
    },
    "Dungeon Map (Murmuring Reef)": {
        'classification': ItemClassification.filler,
        'id': 0x33,
        'subid': 0x03
    },
    "Dungeon Map (Sleeping Forge)": {
        'classification': ItemClassification.filler,
        'id': 0x33,
        'subid': 0x04
    },
    "Dungeon Map (Echo Cathedral)": {
        'classification': ItemClassification.filler,
        'id': 0x33,
        'subid': 0x05
    },
    "Dungeon Map (Sky Spiral)": {
        'classification': ItemClassification.filler,
        'id': 0x33,
        'subid': 0x06
    },
    "Dungeon Map (Frost Palace)": {
        'classification': ItemClassification.filler,
        'id': 0x33,
        'subid': 0x07
    },
    "Dungeon Map (Sleepless Tower)": {
        'classification': ItemClassification.filler,
        'id': 0x33,
        'subid': 0x08
    },

    "Gasha Seed": {
        'classification': ItemClassification.filler,
        'id': 0x34,
        'subid': 0x01,
        'hidden': True
    },
    
    #     "Maku Seed": {
    #           'classification': ItemClassification.progression,
    #         'id': 0x36
    #     },

    # TODO: Trade Items (if any)
    "Poe Clock": {
        'classification': ItemClassification.progression_skip_balancing,
        'id': 0x3d,
        'hidden': True
    },
    "Stationery": {
        'classification': ItemClassification.progression_skip_balancing,
        'id': 0x3e,
        'hidden': True
    },
    "Stink Bag": {
        'classification': ItemClassification.progression_skip_balancing,
        'id': 0x3f,
        'hidden': True
    },
    "Tasty Meat": {
        'classification': ItemClassification.progression_skip_balancing,
        'id': 0x47,
        'hidden': True
    },
    "Doggie Mask": {
        'classification': ItemClassification.progression,
        'id': 0x56,
        'hidden': True
    },
    "Dumbbell": {
        'classification': ItemClassification.progression_skip_balancing,
        'id': 0x57,
        'hidden': True
    },
    "Cheesy Mustache": {
        'classification': ItemClassification.progression_skip_balancing,
        'id': 0x5f,
        'hidden': True
    },
    "Funny Joke": {
        'classification': ItemClassification.progression_skip_balancing,
        'id': 0x3c,
        'hidden': True
    },
    "Touching Book": {
        'classification': ItemClassification.progression_skip_balancing,
        'id': 0x35,
        'hidden': True
    },
    "Magic Oar": {
        'classification': ItemClassification.progression_skip_balancing,
        'id': 0x38,
        'hidden': True
    },
    "Sea Ukulele": {
        'classification': ItemClassification.progression_skip_balancing,
        'id': 0x39,
        'hidden': True
    },
    "Broken Sword": {
         'classification': ItemClassification.progression_skip_balancing,
         'id': 0x3a,
        'hidden': True
    },

    # Not sure we will be using these as well.
    "Bomb Flower": {
        'classification': ItemClassification.progression_skip_balancing,
        'id': 0x49,
        'hidden': True
    },
    "Book of Seals": {
        'classification': ItemClassification.progression,
        'id': 0x55,
        'hidden': True
    },
    "Brother Emblem": {
        'classification': ItemClassification.progression,
        'id': 0x5b,
        'hidden': True
    },
    "Cheval Rope": {
        'classification': ItemClassification.progression,
        'id': 0x52,
        'hidden': True
    },

    "Crown Key": {
        'classification': ItemClassification.progression,
        'id': 0x43,
        'hidden': True
    },
    "Fairy Powder": {
        'classification': ItemClassification.progression,
        'id': 0x51,
        'hidden': True
    },
    "Goron Vase": {
        'classification': ItemClassification.progression_skip_balancing,
        'id': 0x5c,
        'hidden': True
    },
    "Goronade": {
        'classification': ItemClassification.progression_skip_balancing,
        'id': 0x5d,
        'hidden': True
    },
    "Graveyard Key": {
        'classification': ItemClassification.progression,
        'id': 0x42,
        'hidden': True
    },
    "Island Chart": {
        'classification': ItemClassification.progression,
        'id': 0x54,
        'hidden': True
    },
    "Lava Juice": {
        'classification': ItemClassification.progression_skip_balancing,
        'id': 0x5a,
        'hidden': True
    },
    "Letter of Introduction": {
        'classification': ItemClassification.progression_skip_balancing,
        'id': 0x59,
        'hidden': True
    },
    "Library Key": {
        'classification': ItemClassification.progression,
        'id': 0x46,
        'hidden': True
    },
    "Mermaid Key": {
        'classification': ItemClassification.progression,
        'id': 0x44,
        'hidden': True
    },
    "Old Mermaid Key": {
        'classification': ItemClassification.progression,
        'id': 0x45,
        'hidden': True
    },
    "Rock Brisket": {
        'classification': ItemClassification.progression_skip_balancing,
        'id': 0x5e,
        'hidden': True
    },
    "Scent Seedling": {
        'classification': ItemClassification.progression_skip_balancing,
        'id': 0x4d,
        'hidden': True
    },
    "Slate": {
        'classification': ItemClassification.progression,
        'id': 0x4b
    },
    "Tokay Eyeball": {
        'classification': ItemClassification.progression,
        'id': 0x4f,
        'hidden': True
    },
    "Cracked Tuni Nut": {
        'classification': ItemClassification.progression_skip_balancing,
        'id': 0x4c,
        'hidden': True
    },
    "Tuni Nut": {
        'classification': ItemClassification.progression,
        'id': 0x3b,
        'hidden': True
    },
    "Zora Scale": {
        'classification': ItemClassification.progression,
        'id': 0x4e,
        'hidden': True
    },
    #   "Bomb Upgrade": {
    #   'classification': ItemClassification.progression,
    #   "",
    #        'id': 0x61
    #    },
    #   "Satchel Upgrade": {
    #   'classification': ItemClassification.progression,
    #   "",
    #        'id': 0x62)
}