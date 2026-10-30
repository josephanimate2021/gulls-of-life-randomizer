from ..ap.patching.z80asm.Assembler import *
from typing import Any

def str_hex_to_int(h) -> int:
    return int("0x" + h, 0)

class sym():
    bank_limit = 0x0b
    def __init__(self):
        with open("romhack.sym", "rt") as f:
            self.array = []
            array = []
            code = f.readline()
            while code != "":
                array.append(code)
                self.array.append(code.splitlines()[0])
                code = f.readline()

    def browse_sym(self, property) -> List[str]:
        found_property = False
        info = []
        for stuff in self.array:
            if not stuff:
                continue
            if stuff.startswith("[") and "]" in stuff:
                if found_property:
                    break
                if not found_property and stuff == f"[{property}]":
                    found_property = True
            elif found_property:
                info.append(stuff)
        return info
    
    def get_labels(self, change_gbAddress_offset = True) -> Dict[str, GameboyAddress]:
        info = {}
        for stuff in self.browse_sym("labels"):
            address, label = stuff.split(" ")
            bank, addr = address.split(":")
            if str_hex_to_int(addr[:1]) > self.bank_limit:
                continue
            info[label] = GameboyAddress(str_hex_to_int(bank), str_hex_to_int(addr), change_gbAddress_offset)
        return info

    def get_defs(self) -> Dict[str, int]:
        info = {}
        for stuff in self.browse_sym("definitions"):
            address, label = stuff.split(" ")
            info[label] = str_hex_to_int(address)
        return info
    
    def get_sections(self) -> List[Dict[str, Any]]:
        array = []
        for stuff in self.browse_sym("sections"):
            full_address, bank_and_address, address, size, label = stuff.split(" ")
            addr = bank_and_address.split(":")[1]
            if str_hex_to_int(addr[:1]) > self.bank_limit:
                continue
            array.append({
                "full_address": str_hex_to_int(full_address),
                "bank_and_address": [str_hex_to_int(s) for s in bank_and_address.split(":")],
                "address": str_hex_to_int(address),
                "size": str_hex_to_int(size),
                "label": label
            })
        return array

    def find(self, type: str, label: str) -> None | Dict[str, Any] | GameboyAddress | str | int:
        if type == "section":
            for section in self.get_sections():
                for p, _ in section.items():
                    if section[p] == label:
                        return section
        elif type.startswith("label"):
            labels = self.get_labels("_noChangeToGbAddressOffset" not in type)
            defs = self.get_defs()
            if "_findFromBankAndAddr" in type:
                for lbl, l in labels.items():
                    if l.__str__() == label:
                        return lbl
            elif label in labels:
                return labels[label]
            elif label in defs:
                return defs[label]
            else:
                return None
        return None

    def find_addr_end(self, bank, offset) -> GameboyAddress | None:
        beginFindAddrEnd = False
        label = ""
        offsete = 0x00
        banke = 0x00
        for l, addr in self.get_labels().items():
            b, a = addr.__str__().split(":")
            if beginFindAddrEnd:
                return GameboyAddress(addr.bank, addr.offset)
            if a == offset and b == bank:
                label = l
                banke = addr.bank
                offsete = addr.offset
                beginFindAddrEnd = True
        return GameboyAddress(banke, offsete + self.find("label", f"_sizeof_{label}")) if beginFindAddrEnd else None