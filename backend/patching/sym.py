from ..ap.patching.z80asm.Assembler import *
from typing import Any

def str_hex_to_int(h) -> int:
    return int("0x" + h, 0)

class sym():
    bank_limit = 0x0b
    def __init__(self, sym_path):
        with open(sym_path, "rt") as f:
            self.array = []
            array = f.readlines()
            for line in array:
                self.array.append(strip_line(line))

    def browse_sym(self, property) -> List[str]:
        found_property = False
        info = []
        for stuff in self.array:
            if stuff == "":
                continue
            if stuff.startswith("[") and "]" in stuff:
                if found_property:
                    break
                if not found_property and stuff == f"[{property}]":
                    found_property = True
            elif found_property:
                info.append(stuff)
        return info
    
    def get_labels(self, change_gbAddress_offset = True, as_gbAddress = True, as_defines = False) -> Dict[str, List[GameboyAddress]]:
        info = {}
        for stuff in self.browse_sym("labels"):
            address, label = stuff.split(" ")
            bank, addr = address.split(":")
            if (as_defines and label in info) or (str_hex_to_int(addr[:1]) > self.bank_limit and (as_gbAddress and not as_defines)):
                continue
            if label not in info:
                info[label] = []
            info[label].append(GameboyAddress(str_hex_to_int(bank), str_hex_to_int(addr), change_gbAddress_offset) if as_gbAddress and not as_defines else address if not as_defines else f"${addr}")
            if as_defines:
                info[label] = info[label][0]
        return info

    def get_defs(self) -> Dict[str, List[int]]:
        info = {}
        for stuff in self.browse_sym("definitions"):
            address, label = stuff.split(" ")
            if label not in info:
                info[label] = []
            info[label].append(str_hex_to_int(address))
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

    def find(self, type: str, label: str) -> None | Dict[str, Any] | List[GameboyAddress] | str | List[int]:
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

    def filter(self, type: str, label: str) -> List[Dict[str, Any] | List[GameboyAddress] | str | List[int]]:
        arr = []
        if type == "section":
            for section in self.get_sections():
                for p, _ in section.items():
                    if section[p] == label:
                        arr.append(section)
        elif type.startswith("label"):
            labels = self.get_labels("_noChangeToGbAddressOffset" not in type)
            defs = self.get_defs()
            if "_findFromBankAndAddr" in type:
                for lbl, l in labels.items():
                    if l.__str__() == label:
                        arr.append(lbl)
            else:
                for j in [labels, defs]:
                    for l in j.keys():
                        if l == label:
                            print(l, labels[l])
                            arr.append(labels[l])
        return arr

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