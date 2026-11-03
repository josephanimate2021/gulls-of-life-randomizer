import random
import hashlib
import json
import base64
import os

from .data.locations import locations_data, ROM_HASH
from .generation.logic_predates import *
from .ap.patching.RomData import RomData
from .patching.functions import *
from .patching.sym import sym

class Randomizer():
    def __init__(self):
        self.rom = open("ages.gbc", "rb").read()

    def generate_seed(self, settings: dict):
        settings_copy = settings.copy()
        if settings["shuffle_all"]:
            for p, v in settings.items():
                if p == "shuffle_all":
                    continue
                if isinstance(v, bool):
                    settings_copy[p] = True

        if len(settings["locations"]) == 0:
            if not settings_copy["shuffle_items"]:
                print("Using Vanila Locations because item shuffling was not selected.")
                for location, info in locations_data.items():
                    settings["locations"][location] = info["vanila_item"]
        # TODO: item shuffler
        return json.dumps(settings)

    def patch_rom(self, patch_data: dict) -> dict[str, str]:
        rom_data = RomData(open("romhack.gbc", "rb").read())
        # TODO: Change locations of items inside the ROM.
        parsed_sym = sym()
        if os.path.exists("romhack_bugfixes.txt"):
            for line in open("romhack_bugfixes.txt").readlines():
                l = parsed_sym.find("label", line.strip().split(".")[0])
                if l is not None:
                    rom_data.write_bytes(l.address_in_rom(), open(f"bugfixes/{line.strip()}", "rb").read())
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