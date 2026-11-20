import os
from typing import Optional

from ..ap.patching.RomData import RomData
from .sym import sym
from ..data.items import ITEMS_DATA
from ..data.locations import *
from ..ap.patching.Util import simple_hex
from ..ap.patching.z80asm.Assembler import Z80Assembler, Z80Block, GameboyAddress
from ..ap.patching.z80asm.Util import value_to_byte_array
from .set_rom_flags import RomGlobalFlags

def apply_bugfixes(rom_data: RomData, parsed_sym: sym) -> None:
    """
    Applies bugfixes to the ROM data.
    """
    if os.path.exists("romhack_bugfixes.txt"):
        for line in open("romhack_bugfixes.txt").readlines():
            l = parsed_sym.find("label", line.strip().split(".")[0])
            if l is not None:
                rom_data.write_bytes(l[0].address_in_rom(), open(f"bugfixes/{line.strip()}", "rb").read())
    
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
                table_addr = parsed_sym.find("label", "chestDataGroupTable")[0]
                chest_addr = rom.get_chest_addr(location_data['room'], table_addr.bank, table_addr.offset)
                item_name = patch_data["locations"][location_name]
                item_ids = get_item_id_and_subid(item_name)
                if (
                    item_name.startswith("Small Key")
                    or item_name.startswith("Boss Key")
                ) and not patch_data["keysanity"]:
                    item_ids[1] = 0x03
                if (
                    item_name.startswith("Dungeon Map")
                    or item_name.startswith("Compass")
                ): # TODO: implement compass/map sanity.
                    item_ids[1] = 0x02
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
    return patch_data["romhack_version"] in ["1.0_1.1", "1.0_1", "0.3.1", "0.3", "0.2", "0.1"]

def remove_unneccessary_cutscenes(rom_data: RomData, parsed_sym: sym, patch_data: dict, rom_flags: RomGlobalFlags | None, asm_code: dict) -> None:
    """
    Removes unnecessary cutscenes and interactions from the ROM data.
    """
    groups: list[list[str | int | list[int]]] = [["group1MapaaObjectData", 0]] if not patch_data["show_ballade_cutscenes"] else []
    if not patch_data["show_ballade_cutscenes"]:
        rooms_for_applyflag40 = [] # for cutscenes with INTERAC_MARINE (and a few others)
        if using_onedungeon_version(patch_data):
            groups.append(["group1Map7bObjectData", 0])
        # Change the condition to check for an always set global flag instead of a room flag for the first time marin interaction in a dream.
        marineHumanScriptAddr = parsed_sym.find("label", "marineHumanScript")[0]
        bank, offset = marineHumanScriptAddr.__str__().split(":")
        asm_code[f"{bank}/{simple_hex(int(offset, 16) + 1, 4)}/"] = "db jumpifglobalflagset,$58"
        if patch_data["romhack_version"] not in ["0.1", "0.2"]:
            if not using_onedungeon_version(patch_data):
                # D1
                groups[0].append([0xe7, 0x05]) # Give the ending script to the starting bird (May change depending on what happens in the future).

                # Interaction removal for any calls to all blocks listed inside the arr variable because those aren't needed in rando context.
                # (Gives us some space here and to set flags, and fixes the bridge apearing on it's own in one of the d2 rooms for some reason)
                arr = ["arrivalTalk"]
                if patch_data["romhack_version"] in ["dev"]:
                    arr.append("praise")
                for s in arr: # Same thing with the praise block
                    praiseAddr = parsed_sym.find("label", s)[0]
                    bank, offset = praiseAddr.__str__().split(":")
                    asm_code[f"{bank}/{offset}/"] = "jp interactionDelete"

                # Give the user the dream notebook without a cutscene sequence.
                marineToBeContinuedScriptGoAddr = parsed_sym.find("label", "marineToBeContinuedScript@go")[0]
                bank, offset = marineToBeContinuedScriptGoAddr.__str__().split(":")
                offsetAsInt = int(offset, 16)
                asm_code[f"{bank}/{simple_hex(offsetAsInt + 4, 4)}/"] = ( # TODO: dream notebook check
                    f"db giveitem,$12,$00"
                )
                asm_code[f"{bank}/{simple_hex(offsetAsInt + 11, 4)}/"] = f"db $02" # Modify the ending to be 2 so that the modified beach script is called.
                asm_code[f"{bank}/{simple_hex(offsetAsInt + 15, 4)}/"] = f"db $aa" # TODO (wWarpDestRoom For the upcoming Starting Islands feature)
                asm_code[f"{bank}/{simple_hex(offsetAsInt + 23, 4)}/"] = f"db $42" # (wWarpDestPos) Same thing here.
                asm_code[f"{bank}/{simple_hex(offsetAsInt + 31, 4)}/"] = f"db $81" # (wWarpDestGroup) And here.

                # Skips the text and sets some flags for jingle island ontop of the marin ending beach script.
                marinEndingBeachAddr = parsed_sym.find("label", "marineEndingScript@beach")[0]
                bank, offset = marinEndingBeachAddr.__str__().split(":")
                offsetAsInt = int(offset, 16)
                asm_code[f"{bank}/{offset}/"] = (
                    "db setglobalflag,$50\n" # GLOBALFLAG_BALLADE_RAFT
                    "db setglobalflag,$51\n" # GLOBALFLAG_BALLADE_ISLAND2
                    "db writememory\n"
                    "dw wBalladeEnding\n"
                    "db $00\n"
                    "db enablemenu\n"
                    "db enableinput\n"
                    "db scriptend"
                )

                # D2
                # Start with modifying the d2 portion of the endings block before going down the line.
                chapterEndingAddr = parsed_sym.find("label", "chapterEnding@endings")[0]
                bank, offset = chapterEndingAddr.__str__().split(":")
                offsetAsInt = int(offset, 16) + 4
                asm_code[f"{bank}/{simple_hex(offsetAsInt, 4)}/"] = "dw setEndFlagsD2beg"
                asm_code[f"{bank}//setEndFlagsD2beg"] = (
                    f"db $0{ENDINGS_ENUM.index('END_SOUND')},$d0\n"
                    f"db $0{ENDINGS_ENUM.index('END_FLAG')},$52\n"
                    f"db $0{ENDINGS_ENUM.index('END_STEP')},$11"
                )
                offsetAsInt += 6
                asm_code[f"{bank}/{simple_hex(offsetAsInt, 4)}/"] = "dw setEndFlagsD2End"
                asm_code[f"{bank}//setEndFlagsD2End"] = (
                    f"db $0{ENDINGS_ENUM.index('END_STEP')},$00\n"
                    f"db $0{ENDINGS_ENUM.index('END_DONE')}"
                )

                if patch_data["romhack_version"] in ["dev"]:
                    # D3-D7

                    # Sounds indicator to tell the user what dungeon they just finished. The starting number for this list is 3.
                    snds = ["SND_TELEPORT", "SND_SOLVEPUZZLE", "SND_TUNE_OF_ECHOES", "MUS_BALLADE_TEMPETES", "SND_SOLVEPUZZLE_2"]

                    # Loop until all of the code is inserted into the appropriate places.
                    for i in range(3, 8):
                        offsetAsInt += 6
                        asm_code[f"{bank}/{simple_hex(offsetAsInt, 4)}/"] = f"dw setEndFlagsD{i}"
                        asm_code[f"{bank}//setEndFlagsD{i}"] = f"db $0{ENDINGS_ENUM.index('END_SOUND')},{snds[i - 3]}\ndb $0{ENDINGS_ENUM.index('END_FLAG')},$5{i}\ndb $0{ENDINGS_ENUM.index('END_DONE')}"
                        if i == 3: # Special case for d3.
                            offsetAsInt += 6

            if patch_data["romhack_version"] not in ["0.3.1", "0.3"]: # Remove the jack dialog from the game.
                marineHumanScriptAddr = parsed_sym.find("label", "marineJackScript")[0]
                bank, offset = marineHumanScriptAddr.__str__().split(":")
                asm_code[f"{bank}/{simple_hex(int(offset, 16) + 1, 4)}/"] = "db scriptend"
            set_room_flags(0x40, rooms_for_applyflag40, rom_flags)
        for info in groups:
            l = parsed_sym.find("label", info[0])
            if l is not None: # Places set interactions inside a room.
                rom_data.write_bytes(l[0].address_in_rom() + find_address_for_param_helper(info[1], -1), [0xff] if not value_in_index(info, 2) else info[2])

def set_room_flags(flag: int, rooms: int | list[int], rom_flags: RomGlobalFlags):
    if not isinstance(rooms, list) and isinstance(rooms, int):
        rooms = [rooms]
    if len(rooms) > 0:
        for room in rooms:
            startflag = 0xc300 if room >= 0x600 else 0xc500 if room >= 0x200 else 0xc700
            rom_flags.insert_code(f"ld (${simple_hex(startflag + room, 4)}),a")
        rom_flags.insert_code(f"ld a,${simple_hex(flag)}")

def value_in_index(arr: list, index: int):
    try:
        print("Yes, value is in index", arr[index])
        return True
    except:
        print("Things didn't go as expected.")
        return False

def add_warp_to_start(parsed_sym: sym, asm_code: dict):
    menuFadeAddr = parsed_sym.find("label", "menuStateFadeIntoMenu")[0]
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
        f"ld a,$aa        ; room ID\n"
        "ld (wWarpDestRoom),a\n"
        f"ld a,$42         ; Position in a room\n"
        "ld (wWarpDestPos),a\n"
        "ld a,$05\n"
        "ld (wWarpTransition),a\n"
        "ld a,$03\n"
        "ld (wWarpTransition2),a\n"
        "ld a,$ff\n"
        "ld (wDisabledObjects),a\n"

        "ld a,SND_TELEPORT\n"
        "call playSound\n"
    
        "ld a,$03\n"
        "call setMusicVolume\n"
        "call clearStaticObjects\n"
        
        "ld a,$d0\n"
        "ld (wLinkObjectIndex),a\n"
        
        "ld a,$03\n"
        "ld (wMenuLoadState),a\n"
        "pop af      ; pop return addr from stack\n"
        "ret\n"
        
        "@done:\n"
        "jp menuStateFadeIntoMenu@openMenu"
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
    if not using_onedungeon_version(patch_data):
        code_array[3] = (
            "ld e,$00\n"
            "ld a,(de)\n"
            "cp $02\n"
            "jr z,$0040\n"
            f"{code_array[3]}"
        ) if patch_data["romhack_version"] != "1.0_2" else code_array[3]
    for c in code_array:
        code += c
    frames = 60 * int(patch_data["dream_timer"])
    interactionCodee9State0Addr = parsed_sym.find("label", "interactionCodee9@state0")[0]
    bank = interactionCodee9State0Addr.__str__().split(":")[0]
    frame_array = [0, 0] if patch_data["disable_dream_timer"] else [
        simple_hex(0xff), simple_hex(0xff)
    ] if patch_data["max_out_dream_timer"] else [
        simple_hex(i) for i in reversed(value_to_byte_array(frames, 2))
    ]

    # Loop the way to adding code.
    for i in range(len(frame_array)):
        # Convert the asm code into bytes with the assembler.
        fake_assembler = Z80Assembler([0], {}, rando.rom)
        fake_assembler.add_block(Z80Block("00/0000/", code))
        fake_assembler.compile_all()

        # create variables for modifying the dream timer using the compiled code bytes.
        addr = GameboyAddress(interactionCodee9State0Addr.bank, interactionCodee9State0Addr.offset + len(fake_assembler.blocks[0].byte_array))
        offset = addr.__str__().split(":")[1]

        # Modify the asm code before preparing for the next iteration.
        asm_code[f"{bank}/{offset}/"] = f"ld (hl),${frame_array[i]}"
        code += asm_code[f"{bank}/{offset}/"] + "\n" + ("dec l\n" if i == 0 else "")