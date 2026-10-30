import random
from .data.locations import locations_data, ROM_HASH
from .generation.logic_predates import *
import hashlib

class Randomizer():
    def __init__(self):
        self.rom = bytes(open("ages.gbc", "rb").read())

    def generate_seed(self, arr):
        if not self.seed:
            self.seed = hash(tuple(arr))

    def validate_rom(self) -> bool:
        """
        Validates the ROM by checking its hash against the expected hash.
        Returns:
            bool: True if the ROM is valid, False otherwise.
        """
        rom_hash = hashlib.md5(self.rom).hexdigest()
        return rom_hash == ROM_HASH

rando = Randomizer()