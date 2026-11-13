import random
import hashlib
import json
import base64

from .data.locations import locations_data, ROM_HASH
from .data.constants import DUNGEON_NAMES
from .data.items import *
from .ap.patching.RomData import RomData
from .ap.patching.z80asm.Assembler import *
from .patching.functions import *
from .patching.sym import sym
from .patching.defines import DEFINES
from .patching.set_rom_flags import RomGlobalFlags

class Randomizer():
    def __init__(self):
        self.rom = open("ages.gbc", "rb").read()
        self.location_data = {}
        self.rando_settings = {}

    def get_filler_item(self, consider_dungeon):
        filler_items = []
        for p, vv in ITEMS_DATA.items():
            if vv["classification"] == ItemClassification.filler:
                if consider_dungeon is None or p not in DUNGEON_ITEM_NAMES or DUNGEON_NAMES.index(p.split("(")[1].split(")")[0]) == consider_dungeon:
                    filler_items.append(p)
        return random.choice(filler_items)

    def generate_seed(self, settings: dict):
        # Check to see if the shuffle_all setting is checked. If so, check all other items assosiated with it.
        self.settings_copy = settings.copy()
        open("rando_settings.json", "w").write(json.dumps(settings))
        excempt_settings = ["guarentee_sword", "show_ballade_cutscenes", "disable_dream_timer", "vanilaize_rom", "max_out_dream_timer"]
        if settings["shuffle_all"]:
            for p, v in settings.items():
                if p == "shuffle_all":
                    continue
                if isinstance(v, bool) and p not in excempt_settings:
                    self.settings_copy[p] = True

        # Shuffle locations if the seed dosen't contain any.
        if len(settings["locations"]) == 0:
            def shuffle_locations(fill_loc_data):
                van_items = []
                for location, info in locations_data.items():
                    if (
                        "not_compatiable_versions" in info and settings["romhack_version"] in info["not_compatiable_versions"]
                    ) or (
                        "compatiable_versions" in info and settings["romhack_version"] not in info["compatiable_versions"]
                    ): 
                        continue
                    if fill_loc_data:
                        self.location_data[location] = info
                    van_items.append(info["vanila_item"])
                    settings["locations"][location] = info["vanila_item"]
                if self.settings_copy["shuffle_items"]:
                    random.shuffle(van_items)
                    for i, location in enumerate(settings["locations"]):
                        settings["locations"][location] = van_items[i]
                print(settings["locations"])
            shuffle_locations(True)
            if not self.settings_copy["shuffle_items"]:
                print("Using Vanila Locations because item shuffling was not selected.")
            else: # Run the randomizer if shuffle items or shuffle_all is enabled.
                if settings["logic"] != "none": # Run the actual randomizer logic
                    locations_in_logic = {}
                    self.temp_locations = {}
                    in_dungeon = False
                    self.gen_attempts = 0
                    self.loc_count = 0
                    self.loc_array = list(self.location_data.keys())
                    print(self.location_data, self.loc_array)
                    self.modifed_locs = []
                    while self.loc_count != len(self.loc_array):
                        print(f"Generation #{self.loc_count}")
                        if self.loc_count == 0:
                            self.modifed_locs = []
                            self.temp_locations = {}
                        loic = self.loc_array[self.loc_count]
                        data = self.location_data[loic]
                        if not settings["keysanity"]:
                            if "dungeon" in data and not in_dungeon:
                                in_dungeon = True
                                self.temp_locations = {}
                            elif in_dungeon:
                                in_dungeon = False
                                self.temp_locations = {}
                        def append_loc():
                            self.temp_locations[loic] = settings["locations"][loic]
                            locations_in_logic[loic] = self.temp_locations[loic]
                            self.loc_count += 1
                            return True
                        if data["requirements"] is not None:
                            if len(locations_in_logic) == 0:
                                raise Exception("There needs to be at least one location in there that dosen't require logic in order to continue filling locations.")
                            def recuursive_loop(r: dict = {}):
                                for type, arr in r.items():
                                    for i in range(len(arr)):
                                        req = arr[i]
                                        print(req, locations_in_logic)
                                        if isinstance(req, dict) and recuursive_loop(req):
                                            if type == "any" or i == len(arr) - 1:
                                                return True
                                            continue
                                        item, req_ct = req
                                        if (
                                            item == "conditional" and req_ct
                                        ) or ("Sword" in item and settings["guarentee_sword"]):
                                            if type == "any" or i == len(arr) - 1:
                                                return append_loc()
                                            continue
                                        item_count = 0
                                        item_cLocs = []
                                        for h in locations_in_logic.keys():
                                            if locations_in_logic[h] == item:
                                                item_count += 1
                                                item_cLocs.append(h)

                                        for loc in settings["locations"].keys():
                                            if settings["locations"][loc] == item:
                                                settings["locations"][loc] = self.get_filler_item(data["dungeon"] if "dungeon" in data else None)
                                        print(item_count, req_ct, item_count == req_ct)
                                        if item_count < req_ct:
                                            # Attempt to find locations with junk items to replace with logical items relative to them.
                                            junk_locs = []
                                            for l in locations_in_logic.keys():
                                                if ITEMS_DATA[locations_in_logic[l]]['classification'] == ItemClassification.filler:
                                                    junk_locs.append(l)
                                            print(junk_locs)
                                            if len(junk_locs) == 0: # If nothing is found, use what we gathered so far.
                                                junk_locs = list(self.temp_locations.keys())
                                            for _ in range(item_count, req_ct):
                                                rando_loc = ""
                                                while True:
                                                    rando_loc = random.choice(junk_locs)
                                                    if rando_loc not in self.modifed_locs:
                                                        self.modifed_locs.append(rando_loc)
                                                        break
                                                locations_in_logic[rando_loc] = item
                                            self.temp_locations = {}
                                        elif item_count > req_ct:
                                            for i in range(req_ct, item_count):
                                                locations_in_logic[item_cLocs[i]] = self.get_filler_item(data["dungeon"] if "dungeon" in data else None)
                                        else:
                                            append_loc()

                                        # Return if the array iteration is done depending on the type.
                                        if type == "any" or i == len(arr) - 1:
                                            return True
                                            
                            recuursive_loop(data["requirements"])
                        else:
                            append_loc()

                    settings["locations"] = locations_in_logic
                    print(locations_in_logic)
                else:
                    while not settings["keysanity"]: # Ensure that small or boss keys are within their dungeons in no logic seeds.
                        for location in list(settings["locations"].keys()):
                            item = settings["locations"][location]
                            if (
                                item.startswith("Small Key")
                                or item.startswith("Boss Key")
                            ) and ("dungeon" not in self.location_data[location] or not item.endswith(f"({DUNGEON_NAMES[self.location_data[location]['dungeon']]})")):
                                settings["locations"] = {}
                                shuffle_locations(False)
                                break
                        if len(settings["locations"]) == len(self.location_data):
                            break
        open("settings_copy.json", "w").write(json.dumps(self.settings_copy))
        return open("rando_settings.json").read()

    def patch_rom(self, patch_data: dict) -> dict[str, str]:
        # Define variables
        rom = open("romhack.gbc", "rb").read()
        rom_data = RomData(rom)
        settings_copy = json.loads(open("settings_copy.json", "r").read())
        parsed_sym = sym("romhack.sym")
        asm_code = {}
        if patch_data["romhack_version"] not in ["0.1", "0.2", "0.3"]:
            init_flags = RomGlobalFlags(parsed_sym, asm_code)

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
        apply_randomized_locations(rom_data, patch_data, settings_copy, parsed_sym)
        if not patch_data["vanilaize_rom"]:
            apply_bugfixes(rom_data, parsed_sym)
            remove_unneccessary_cutscenes(rom_data, parsed_sym, patch_data)
            add_warp_to_start(parsed_sym, asm_code)
            if patch_data["romhack_version"] not in ["0.2", "0.1"]:
                modify_dream_timer(patch_data, parsed_sym, asm_code)
        if patch_data["apply_fr_lang"] and patch_data["romhack_version"] not in ["0.1", "0.2", "0.3"]:
            init_flags.insert_code("ld a,$01\nld (wActiveLanguage),a\n")

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