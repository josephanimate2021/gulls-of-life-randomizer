import random
from .data.locations import locations_data, ROM_HASH
from .generation.logic_predates import *
import hashlib
import json
from .patching.rom import patch_rom

class Randomizer():
    def __init__(self):
        self.rom = bytes(open("ages.gbc", "rb").read())

    def generate_seed(self, settings):
        self.rando_settings = json.loads(settings)
        self.settings = self.rando_settings.copy()
        if self.rando_settings["shuffle_all"]:
            for p, v in self.rando_settings.items():
                if p == "shuffle_all":
                    continue
                if isinstance(v, bool):
                    self.settings[p] = True

        if len(self.rando_settings["locations"]) == 0:
            if not self.settings["shuffle_items"]:
                print("Using Vanila Locations because item shuffling was not selected.")
                for location, info in locations_data.items():
                    self.rando_settings["locations"][location] = info["vanila_item"]
        # TODO: item shuffler
        return json.dumps(self.rando_settings)

    def validate_rom(self) -> bool:
        """
        Validates the ROM by checking its hash against the expected hash.
        Returns:
            bool: True if the ROM is valid, False otherwise.
        """
        rom_hash = hashlib.md5(self.rom).hexdigest()
        return rom_hash == ROM_HASH

rando = Randomizer()