import os

from ..ap.patching.RomData import RomData
from .sym import sym

def apply_bugfixes(rom_data: RomData, parsed_sym: sym) -> None:
    """
    Applies bugfixes to the ROM data.
    """
    if os.path.exists("romhack_bugfixes.txt"):
        for line in open("romhack_bugfixes.txt").readlines():
            l = parsed_sym.find("label", line.strip().split(".")[0])
            if l is not None:
                rom_data.write_bytes(l.address_in_rom(), open(f"bugfixes/{line.strip()}", "rb").read())

def apply_randomized_locations(rom_data: RomData, patch_data: dict, parsed_sym: sym) -> None:
    """
    Applies randomized locations to the ROM data.
    """
    if patch_data["shuffle_items"]:
        pass

def remove_unneccessary_cutscenes(rom_data: RomData, parsed_sym: sym) -> None:
    """
    Removes unnecessary cutscenes and interactions from the ROM data.
    """
    groups: list[tuple[str, int]] = [
        ("group1MapaaObjectData", 0), ("group1Map7bObjectData", 0), ("group2Map9eObjectData", 0)
        #("group1Map9bObjectData", 4 * 2), ("group1Map9cObjectData", 4 * 2),
        #("group1MapabObjectData", 4), ("group3Map9eObjectData", 4), ("group4Map13ObjectData", 4 * 3)
    ]
    for group, n in groups:
        l = parsed_sym.find("label", group)
        if l is not None:
            rom_data.write_bytes(l.address_in_rom() + n, [0x0b, 0x00, 0xf8, 0xf8])