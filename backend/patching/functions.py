import os

from ..ap.patching.RomData import RomData
from .sym import sym
from ..data.items import ITEMS_DATA
from ..data.locations import *
from ..ap.patching.Util import simple_hex

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

def using_onedungeon_version(patch_data: dict) -> bool:
    return patch_data["romhack_version"] in ["1.0_1.1", "1.0_1"]

def remove_unneccessary_cutscenes(rom_data: RomData, parsed_sym: sym, patch_data: dict) -> None:
    """
    Removes unnecessary cutscenes and interactions from the ROM data.
    """
    groups: list[tuple[str, int]] = [
        # these first three trigger an unnecessary cutscene that we don't want. the rest of the segull interactions can stay without issue.
        ("group1MapaaObjectData", 0), ("group2Map9eObjectData", 0),
    ] if not patch_data["show_ballade_cutscenes"] else []
    if using_onedungeon_version(patch_data) and not patch_data["show_ballade_cutscenes"]: # we can only remove the segull interaction from room 7b if we're using an older version because newer versions since give you a check.
        groups.append(("group1Map7bObjectData", 0))
    for group, n in groups:
        l = parsed_sym.find("label", group)
        if l is not None: # Place all mask salesman interactions in the same group.
            rom_data.write_bytes(l.address_in_rom() + n, [0x97, 0x67, 0xff, 0xff])

def add_warp_to_start(patch_data: dict, parsed_sym: sym, asm_code: dict):
    menuFadeAddr = parsed_sym.find("label", "menuStateFadeIntoMenu")
    bank, offset = menuFadeAddr.__str__().split(":")
    offsetAsInt = int(f"0x{offset}", 0)
    asm_code[f"{bank}/{simple_hex(offsetAsInt + 26, 4)}/"] = "call checkWarpToStart"
    clearStaticObjectsAddr = parsed_sym.find("label", "clearStaticObjects").__str__().split(":")[1]
    menuFadeOpenMenuAddr = parsed_sym.find("label", "menuStateFadeIntoMenu@openMenu").__str__().split(":")[1]
    asm_code[f"{bank}//checkWarpToStart"] = (
        "ld a,($c481)\n"
        "and $02 | $01\n"
        "cp $02 | $01\n"
        "jr nz,@done\n"
        
        "ld a,$01\n"
        "set 7,a\n"
        "ld ($cc47),a\n"
        "ld a,$aa        ; room ID\n"
        "ld ($cc48),a\n"
        "ld a,$42         ; Position in a room\n"
        "ld ($cc4a),a\n"
        "ld a,$05\n"
        "ld ($cc49),a\n"
        "ld a,$03\n"
        "ld ($cc4b),a\n"
        "ld a,$ff\n"
        "ld ($cc8a),a\n"
        
        f"call ${clearStaticObjectsAddr}\n"
        
        "ld a,$d0\n"
        "ld ($cc2c),a\n"
        
        "ld a,$03\n"
        "ld ($cbcc),a\n"
        "pop af      ; pop return addr from stack\n"
        "ret\n"
        
        "@done:\n"
        f"jp ${menuFadeOpenMenuAddr}"
    )