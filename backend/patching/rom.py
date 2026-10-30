from ..ap.patching.RomData import RomData
from .bps.patch import *

import base64

def patch_rom():
    rom_data = RomData(apply_bps_patch("romhack.bps", rando.rom))
    return {
        "seed": base64.b64encode(rando.rando_settings).decode(),
        "rom": base64.b64encode(rom_data.output()).decode()
    }