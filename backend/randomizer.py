import random
import hashlib
import json
import base64

from .data.locations import locations_data, ROM_HASH
from .data.constants import DUNGEON_NAMES
#from .data.items import ITEMS_DATA
from .ap.patching.RomData import RomData
from .ap.patching.z80asm.Assembler import *
from .patching.functions import *
from .patching.sym import sym
from .patching.defines import DEFINES

class Randomizer():
    def __init__(self):
        self.rom = open("ages.gbc", "rb").read()
        self.location_data = {}

    def generate_seed(self, settings: dict):
        # Check to see if the shuffle_all setting is checked. If so, check all other items assosiated with it.
        settings_copy = settings.copy()
        excempt_settings = ["guarentee_sword", "show_ballade_cutscenes"]
        if settings["shuffle_all"]:
            for p, v in settings.items():
                if p == "shuffle_all":
                    continue
                if isinstance(v, bool) and p not in excempt_settings:
                    settings_copy[p] = True

        # Shuffle locations if the seed dosen't contain any.
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
            else: # Run the randomizer if shuffle items or shuffle_all is enabled.
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
        # Define variables
        rom = open("romhack.gbc", "rb").read()
        rom_data = RomData(rom)
        settings_copy = json.loads(open("settings_copy.json", "r").read())
        parsed_sym = sym("romhack.sym")
        asm_code = {}

        # define assembler things inside the Randomizer class.
        bank_caves = [int(i, 0) for i in json.loads(open("romhack.json").read())]
        bank_caves[0x14] = 0x3c99 # Manually modifying bank 14 because the size of a function in there is oversized.
        
        ringMenuBeg = parsed_sym.find("label", "runRingMenu")
        ringMenuEnd = parsed_sym.find("label", "saveQuitMenu_checkIsGameOver")
        bank_caves[0x02] = [
            [ringMenuBeg.offset, ringMenuEnd.offset], # Using the ring menu since this hack dosen't use rings. (Gives us lots of space here)
            bank_caves[0x02] # end of bank
        ]
        for p, v in parsed_sym.get_labels(as_defines=True).items():
            DEFINES[p] = v

        assembler = Z80Assembler(bank_caves, DEFINES, rom)

        # Call all functions for rom patching.
        apply_bugfixes(rom_data, parsed_sym)
        apply_randomized_locations(rom_data, patch_data, settings_copy, parsed_sym)
        remove_unneccessary_cutscenes(rom_data, parsed_sym, patch_data)
        add_warp_to_start(patch_data, parsed_sym, asm_code)
        modify_dream_timer(patch_data, parsed_sym, asm_code)

        # Compile ASM code.
        print(f"Compiling ASM files...")
        print(asm_code)
        for metalabel, contents in asm_code.items():
            assembler.add_block(Z80Block(metalabel, contents))
        assembler.compile_all()
        for block in assembler.blocks:
            rom_data.write_bytes(block.addr.address_in_rom(), block.byte_array)

        # Update checksums
        rom_data.update_header_checksum()
        rom_data.update_checksum(0x14e)

        # Write the ROM result and then return the infomation.
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

    def stringify_locations(self):
        return json.dumps(locations_data)

    def stringify_items(self):
        return json.dumps(ITEMS_DATA)

rando = Randomizer()