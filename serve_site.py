import http.server
import socketserver
import os
import json

PORT = 9000
Handler = http.server.SimpleHTTPRequestHandler

from backend.patching.sym import sym
from typing import Any

def make_bugfix_file(file):
    print(f"Creating bugfixes text file for {DIR_START}/{file}...")
    bugfixes = ""
    for f in os.listdir(f"{DIR_START}/{file}/bugfixes"):
        bugfixes += f + "\n"
    open(f"{DIR_START}/{file}/ages.txt", "w").write(bugfixes)
    print("Bugfixes file successfully created!")

DIR_START = "romhack_builds"
for file in os.listdir(DIR_START):
    if os.path.exists(f"{DIR_START}/{file}/bugfixes"):
        if not os.path.exists(f"{DIR_START}/{file}/ages.txt"):
            make_bugfix_file(file)
        contents = open(f"{DIR_START}/{file}/ages.txt").read().splitlines()
        dirlist = os.listdir(f"{DIR_START}/{file}/bugfixes")
        if len(contents) != len(dirlist):
            make_bugfix_file(file)
        for i in range(len(dirlist)):
            if contents[i] != dirlist[i]:
                make_bugfix_file(file)
                break
    parsed_sym = sym(f"{DIR_START}/{file}/ages.sym")
    def make_eobs():
        maxes = {}
        mins = {}
        total_banks = max([val.bank for _, val in parsed_sym.get_labels().items()])
        bank_caves = []
        def find(find_max) -> Any:
            offsets = []
            labels = []
            maxLabels = []
            for label, val in parsed_sym.get_labels(False).items():
                if val.bank == len(maxes if find_max else mins):
                    offsets.append(val.offset)
                    labels.append(label)
            if len(offsets) > 0:
                maxOffset = max(offsets) if find_max else min(offsets)
                for i in range(len(offsets)):
                    if offsets[i] == maxOffset:
                        maxLabels.append(labels[i])
                return maxOffset, maxLabels[len(maxLabels) - 1]
            return None
        
        def loop(find_max):
            update_array = maxes if find_max else mins
            max, label = find(find_max)
            print(f"Found {"last" if find_max else "first"} address to work with at bank {hex(len(update_array))}. Should be {hex(max)}")
            update_array[label] = max
            if len(update_array) <= total_banks:
                loop(find_max)

        EOB_PATH = f"{DIR_START}/{file}/ages.json"
        if os.path.exists(EOB_PATH):
            bank_caves = json.loads(open(EOB_PATH).read())
        else:
            print(f"Getting end of banks for v{file}. This may take a few minutes.")
            loop(True)
            bankCount = 0
            for label, _ in maxes.items():
                label = label.split("@")[0]
                addr = parsed_sym.find("label", label).offset
                size = parsed_sym.find("label", "_sizeof_" + label)
                if size is not None:
                    addr += size
                num_hex = hex(0x4000 if addr >= 0x4000 else addr)
                bank_caves.append(num_hex)
                print(f"Ending address for bank {hex(bankCount)} is {num_hex}")
                bankCount += 1
            open(EOB_PATH, "w").write(json.dumps(bank_caves, indent=4))
            print(f"Saved the end of banks to {EOB_PATH} for later use.")
    make_eobs()

with socketserver.TCPServer(("", PORT), Handler) as httpd:
    print(f"Serving at port {PORT}")
    httpd.serve_forever()
