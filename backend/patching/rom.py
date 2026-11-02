from ..ap.patching.RomData import RomData
from .bps.patch import *
from .sym import sym

import base64
import json
import os

def patch_rom(patch_data: dict) -> dict[str, str]:
    rom_data = RomData(apply_bps_patch(open("romhack.bps", "rb"), rando.rom))
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