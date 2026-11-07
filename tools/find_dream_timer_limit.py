from backend.ap.patching.z80asm.Util import value_to_byte_array

if __name__ == "__main__":
    n = 60 # 60 frames = 1 second in a gbc game.
    print("Getting limit for the dream timer...")
    try:
        while len(value_to_byte_array(n, 2)) == 2:
            n += 60
    finally:
        print(n, "Dream timer limit (in seconds):", round((n - 60) / 60))
else:
    print("This tool must be ran with the Python CLI.")