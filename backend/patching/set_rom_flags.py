from .sym import sym
from ..ap.patching.z80asm.Assembler import GameboyAddress

class RomGlobalFlags():
    def __init__(self, parsed_sym: sym, asm_code: dict):
        self.asm_code = asm_code
        addr = parsed_sym.find("label", "saveFile")[1]
        addr1 = parsed_sym.find("label", "initializeChildOnGameStart")[0].__str__().split(":")[1]
        intFile_addr = GameboyAddress(addr.bank, addr.offset - 0x10)
        self.bank, offset = intFile_addr.__str__().split(":")
        self.asm_code[f"{self.bank}/{offset}/"] = "call setInitFlags"
        self.asm_code[f"{self.bank}//setInitFlags"] = (
            f"ld hl,${addr1}\n"
            "ret"
        )
    def insert_code(self, new_code: str):
        self.asm_code[f"{self.bank}//setInitFlags"] = f"{new_code}\n" + self.asm_code[f"{self.bank}//setInitFlags"]