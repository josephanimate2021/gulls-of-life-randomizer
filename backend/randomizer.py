import random
import hashlib
import json
import base64
import os

from .data.locations import locations_data, ROM_HASH
from .generation.logic_predates import *
from .ap.patching.RomData import RomData
from .patching.bps.patch import *
from .patching.sym import sym
from tkinter.filedialog import askopenfilename

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
        rom_data = RomData(apply_bps_patch(open("romhack.bps", "rb"), self.rom))
        # TODO: Change locations of items inside the ROM.
        parsed_sym = sym()
        if os.path.exists("romhack_bugfixes.txt"):
            for line in open("romhack_bugfixes.txt").readlines():
                l = parsed_sym.find("label", line.strip())
                if l is not None:
                    rom_data.write_bytes(l.address_in_rom(), open(f"bugfixes/{line.strip()}", "rb").read())
        rom_data.update_header_checksum()
        rom_data.update_checksum(0x14e)
        open("romhack.gbc", "wb").write(rom_data.output())
        return json.dumps({
            "seed": base64.b64encode(str(patch_data).encode("ascii")).decode("ascii"),
            "patched": True
        })

    def ask_for_rom(self, lang_index) -> tuple[bool, str]:
        title = ('Sélectionner un fichier ROM', 'Select a ROM file')
        file_name = "The Legend of Zelda - Oracle of Ages.gbc"
        if not os.path.exists(file_name):
            file_name = askopenfilename(
                title=('Sélectionner un fichier ROM', 'Select a ROM file')[lang_index],
                filetypes=(("Game Boy Color ROM", "*.gbc"), ("All files", "*.*"))
            ) 
        if not file_name or not os.path.exists(file_name):
            return None, "Oracle of Ages (US) ROM was not found or selected."
        self.base_rom_bytes = bytes(open(file_name, "rb").read())

        basemd5 = hashlib.md5()
        basemd5.update(self.base_rom_bytes)
        if ROM_HASH == basemd5.hexdigest():
            return True, file_name
        else:
            return False, ("Supplied ROM does not match known MD5 for Oracle of Ages US version."
                                "Get the correct game and version, then dump it.")

rando = Randomizer()