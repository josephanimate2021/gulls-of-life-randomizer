import random
import hashlib
import json
import base64

from .data.locations import locations_data, ROM_HASH
from .data.constants import DUNGEON_NAMES
#from .data.items import ITEMS_DATA
from .ap.patching.RomData import RomData
from .patching.functions import *
from .patching.sym import sym

class Randomizer():
    def __init__(self):
        self.rom = open("ages.gbc", "rb").read()
        self.location_data = {}

    def generate_seed(self, settings: dict):
        settings_copy = settings.copy()
        if settings["shuffle_all"]:
            for p, v in settings.items():
                if p == "shuffle_all":
                    continue
                if isinstance(v, bool) and p != "guarentee_sword":
                    settings_copy[p] = True

        if len(settings["locations"]) == 0:
            def shuffle_locations():
                van_items = []
                for location, info in locations_data.items():
                    if (
                        "not_compatiable_versions" in info and settings["romhack_version"] in info["not_compatiable_versions"]
                    ) or (
                        "compatiable_versions" in info and settings["romhack_version"] not in info["compatiable_versions"]
                    ): 
                        continue
                    self.location_data[location] = info
                    van_items.append(info["vanila_item"])
                    settings["locations"][location] = info["vanila_item"]
                if settings_copy["shuffle_items"]:
                    random.shuffle(van_items)
                    for i, location in enumerate(settings["locations"]):
                        settings["locations"][location] = van_items[i]
                print(settings["locations"])
            shuffle_locations()
            if not settings_copy["shuffle_items"]:
                print("Using Vanila Locations because item shuffling was not selected.")
            else:
                while not settings["keysanity"]: # Ensure that small or boss keys are within their dungeons, even with no logic.
                    for location in list(settings["locations"].keys()):
                        item = settings["locations"][location]
                        if (
                            item.startswith("Small Key")
                            or item.startswith("Boss Key")
                        ) and ("dungeon" not in self.location_data[location] or not item.endswith(f"({DUNGEON_NAMES[self.location_data[location]['dungeon']]})")):
                            settings["locations"] = {}
                            shuffle_locations()
                            break
                    if len(settings["locations"]) == len(self.location_data):
                        break
                    

                if settings["logic"] != "none":
                    print("Using Randomized Locations because item shuffling was selected.")
        open("settings_copy.json", "w").write(json.dumps(settings_copy))
        return json.dumps(settings)

    def patch_rom(self, patch_data: dict) -> dict[str, str]:
        rom_data = RomData(open("romhack.gbc", "rb").read())
        settings_copy = json.loads(open("settings_copy.json", "r").read())
        # TODO: Change locations of items inside the ROM.
        parsed_sym = sym()

        # Call all functions for rom patching.
        apply_bugfixes(rom_data, parsed_sym)
        apply_randomized_locations(rom_data, patch_data, settings_copy, parsed_sym)
        remove_unneccessary_cutscenes(rom_data, parsed_sym)

        rom_data.update_header_checksum()
        rom_data.update_checksum(0x14e)
        open("romhack.gbc", "wb").write(rom_data.output())
        return json.dumps({
            "seed": base64.b64encode(str(patch_data).encode("ascii")).decode("ascii"),
            "patched": True
        })

    def validate_rom(self) -> bool:
        """
        Validates the ROM by checking its hash against the expected hash.
        Returns:
            bool: True if the ROM is valid, False otherwise.
        """
        rom_hash = hashlib.md5(self.rom).hexdigest()
        return rom_hash == ROM_HASH

rando = Randomizer()