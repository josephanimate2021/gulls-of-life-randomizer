import os

from ..ap.patching.RomData import RomData
from .sym import sym
from ..data.items import ITEMS_DATA
from ..data.locations import *
from ..ap.patching.Util import simple_hex
from ..ap.patching.z80asm.Assembler import Z80Assembler, Z80Block, GameboyAddress
from ..ap.patching.z80asm.Util import value_to_byte_array

def apply_bugfixes(rom_data: RomData, parsed_sym: sym) -> None:
    """
    Applies bugfixes to the ROM data.
    """
    if os.path.exists("romhack_bugfixes.txt"):
        for line in open("romhack_bugfixes.txt").readlines():
            l = parsed_sym.find("label", line.strip().split(".")[0])
            if l is not None:
                rom_data.write_bytes(l.address_in_rom(), open(f"bugfixes/{line.strip()}", "rb").read())

def change_language_to_french(parsed_sym: sym, asm_code: dict):
    addr = parsed_sym.find("label", "saveFile")
    addr1 = parsed_sym.find("label", "initializeChildOnGameStart").__str__().split(":")[1]
    intFile_addr = GameboyAddress(addr.bank, addr.offset - 0x10)
    bank, offset = intFile_addr.__str__().split(":")
    asm_code[f"{bank}/{offset}/"] = "call changeLangToFrench"
    asm_code[f"{bank}//changeLangToFrench"] = (
        "ld a,$01\n"
        "ld (wActiveLanguage),a\n"
        f"ld hl,${addr1}\n"
        "ret"
    )
    
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
        # these first two trigger an unnecessary cutscene that we don't want. the rest of the segull interactions can stay without issue.
        ("group1MapaaObjectData", 0), ("group2Map9eObjectData", 0),
    ] if not patch_data["show_ballade_cutscenes"] else []
    if using_onedungeon_version(patch_data) and not patch_data["show_ballade_cutscenes"]: # we can only remove the segull interaction from room 7b if we're using an older version because newer versions since give you a check.
        groups.append(("group1Map7bObjectData", 0))
    for group, n in groups:
        l = parsed_sym.find("label", group)
        if l is not None: # Place all INTERAC_97 interactions in the same group.
            rom_data.write_bytes(l.address_in_rom() + n, [0x97, 0x67, 0xff, 0xff])

def add_warp_to_start(parsed_sym: sym, asm_code: dict):
    menuFadeAddr = parsed_sym.find("label", "menuStateFadeIntoMenu")
    bank, offset = menuFadeAddr.__str__().split(":")
    offsetAsInt = int(f"0x{offset}", 0)
    asm_code[f"{bank}/{simple_hex(offsetAsInt + 26, 4)}/"] = "call checkWarpToStart"
    asm_code[f"{bank}//checkWarpToStart"] = (
        "ld a,(wKeysPressed)\n"
        "and BTN_B | BTN_A\n"
        "cp BTN_B | BTN_A\n"
        "jr nz,@done\n"
        
        "ld a,$01\n"
        "set 7,a\n"
        "ld (wWarpDestGroup),a\n"
        "ld a,$aa        ; room ID\n"
        "ld (wWarpDestRoom),a\n"
        "ld a,$42         ; Position in a room\n"
        "ld (wWarpDestPos),a\n"
        "ld a,$05\n"
        "ld (wWarpTransition),a\n"
        "ld a,$03\n"
        "ld (wWarpTransition2),a\n"
        "ld a,$ff\n"
        "ld (wDisabledObjects),a\n"
        
        "call clearStaticObjects\n"
        
        "ld a,$d0\n"
        "ld (wLinkObjectIndex),a\n"
        
        "ld a,$03\n"
        "ld (wMenuLoadState),a\n"
        "pop af      ; pop return addr from stack\n"
        "ret\n"
        
        "@done:\n"
        f"jp menuStateFadeIntoMenu@openMenu"
    )

def modify_dream_timer(patch_data: dict, parsed_sym: sym, asm_code: dict):
    # Create variables for the loop.
    code_array = [
        "call $0000\n",
        "call $0010\n",
        "call $0020\n",
        "ld hl,$0030\n",
        "ldi a,(hl)\n",
        "or (hl)\n",
        "jr nz,$0050\n",
    ]
    code = ""
    if patch_data["romhack_version"] not in ["1.0_2", "1.0_1.1", "1.0_1"]:
        code_array[3] = (
            "ld e,$00\n"
            "ld a,(de)\n"
            "cp $02\n"
            "jr z,$0040\n"
            f"{code_array[3]}"
        )
    for c in code_array:
        code += c
    frames = 60 * int(patch_data["dream_timer"])
    interactionCodee9State0Addr = parsed_sym.find("label", "interactionCodee9@state0")
    bank = interactionCodee9State0Addr.__str__().split(":")[0]
    frame_array = [0, 0] if patch_data["disable_dream_timer"] else [
        simple_hex(0xff), simple_hex(0xff)
    ] if patch_data["max_out_dream_timer"] else [
        simple_hex(i) for i in reversed(value_to_byte_array(frames, 2))
    ]

    # Loop the way to adding code.
    for i in range(len(frame_array)):
        # Convert the asm code into bytes with the assembler.
        fake_assembler = Z80Assembler([0x0], {}, rando.rom)
        fake_assembler.add_block(Z80Block("00/0000/", code))
        fake_assembler.compile_all()

        # create variables for modifying the dream timer using the compiled code bytes.
        addr = GameboyAddress(interactionCodee9State0Addr.bank, interactionCodee9State0Addr.offset + len(fake_assembler.blocks[0].byte_array))
        offset = addr.__str__().split(":")[1]

        # Modify the asm code before preparing for the next iteration.
        asm_code[f"{bank}/{offset}/"] = f"ld (hl),${frame_array[i]}"
        code += asm_code[f"{bank}/{offset}/"] + "\n" + ("dec l\n" if i == 0 else "")