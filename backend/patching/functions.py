import os

from ..ap.patching.RomData import RomData
from .sym import sym
from ..data.items import ITEMS_DATA
from ..data.locations import *

def apply_bugfixes(rom_data: RomData, parsed_sym: sym) -> None:
    """
    Applies bugfixes to the ROM data.
    """
    if os.path.exists("romhack_bugfixes.txt"):
        for line in open("romhack_bugfixes.txt").readlines():
            l = parsed_sym.find("label", line.strip().split(".")[0])
            if l is not None:
                rom_data.write_bytes(l.address_in_rom(), open(f"bugfixes/{line.strip()}", "rb").read())

# helper function that adds param2 to i unless stopped by my base case, which is helpful for finding the right rom address for a certain param in a table despite changes in the disasm code.
def find_address_for_param_helper(lineNumber, param, param2 = 4, i=0,c=0) -> int:
    return i - param if c == lineNumber else find_address_for_param_helper(lineNumber, param, param2, i + param2, c + 1)

def apply_randomized_locations(rom: RomData, patch_data: dict, settings_copy: dict, parsed_sym: sym) -> None:
    """
    Applies randomized locations to the ROM data.
    """
    print(patch_data, settings_copy)
    if settings_copy["shuffle_items"]:
        for location_name, location_data in locations_data.items():
            if (
                'treasure_spawn_mode' not in location_data 
                or location_name not in patch_data["locations"]
            ):
                continue
            if location_data['treasure_spawn_mode'] == TREASURE_SPAWN_CHEST and "room" in location_data:
                table_addr = parsed_sym.find("label", "chestDataGroupTable")
                chest_addr = rom.get_chest_addr(location_data['room'], table_addr.bank, table_addr.offset)
                item_name = patch_data["locations"][location_name]
                item_ids = get_item_id_and_subid(item_name)
                if (
                    item_name.startswith("Small Key")
                    or item_name.startswith("Boss Key")
                ) and not patch_data["keysanity"]:
                    item_ids[1] = 0x03
                print(item_name, item_ids)
                rom.write_bytes(chest_addr, item_ids)
            else:
                pass # TODO: collect mode on nonchest items.

def get_item_id_and_subid(item_name: str) -> list[int]:
    """
    Returns the item ID and sub-ID for the given item name.
    """
    if item_name not in ITEMS_DATA:
        raise ValueError(f"Item '{item_name}' not found in ITEMS_DATA.")
    item_data = ITEMS_DATA[item_name]
    return [item_data["id"], 0x00 if "subid" not in item_data else item_data["subid"]]

def remove_unneccessary_cutscenes(rom_data: RomData, parsed_sym: sym) -> None:
    """
    Removes unnecessary cutscenes and interactions from the ROM data.
    """
    groups: list[tuple[str, int]] = [
        # these first three trigger an unnecessary cutscene that we don't want. the rest of the segull interactions can stay without issue.
        ("group1MapaaObjectData", 0), ("group1Map7bObjectData", 0), ("group2Map9eObjectData", 0),
    ]
    for group, n in groups:
        l = parsed_sym.find("label", group)
        if l is not None: # Place all mask salesman interactions in the same group.
            rom_data.write_bytes(l.address_in_rom() + n, [0x97, 0x67, 0xf8, 0xf8])