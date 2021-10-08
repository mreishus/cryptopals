#!/usr/bin/env python
"""
Byte-at-a-time ECB decryption (Simple)

Copy your oracle function to a new function that encrypts buffers under ECB
mode using a consistent but unknown key (for instance, assign a single random
key, once, to a global variable).

Now take that same function and have it append to the plaintext, BEFORE
ENCRYPTING, the following string:
"""

import base64
from random import randint
from shared import (
    cbc_encrypt,
    detect_encryption_mode,
    ecb_encrypt,
    random_aes_key,
    random_bytes,
    repeated_blocks,
)


def encryption_oracle_12(bytes_in):
    """
    Encrypts data under an unknown static key (stays constant through runtime).
    Also appends an unknown string to the provided string.
    Produces: AES-128-ECB(your-string || unknown-string, random-key)
    """
    if not hasattr(encryption_oracle_12, "key"):
        encryption_oracle_12.key = random_aes_key()

    ## Append special string from exercise
    special_string = b"Um9sbGluJyBpbiBteSA1LjAKV2l0aCBteSByYWctdG9wIGRvd24gc28gbXkgaGFpciBjYW4gYmxvdwpUaGUgZ2lybGllcyBvbiBzdGFuZGJ5IHdhdmluZyBqdXN0IHRvIHNheSBoaQpEaWQgeW91IHN0b3A/IE5vLCBJIGp1c3QgZHJvdmUgYnkK"
    special_bytes = base64.b64decode(special_string)

    source_bytes = bytes_in + special_bytes

    # Always use ECB
    key = encryption_oracle_12.key
    return ecb_encrypt(source_bytes, key)


def last_byte_ecb_attack(blackbox, bs):
    # arg1: blackbox: Bytes -> Bytes function
    # arg2: bs: Int (blocksize)

    # Knowing block size, craft input block that is one byte short
    #   - What does the function put in the last byte position?

    # Step 0: Send 15 bytes [ Return block includes 1 unknown byte ]
    #         Check against 15 bytes + Brute force 1 byte
    # Step 1: Send 14 bytes [ Return block includes 2 unknown bytes ]
    #         Check against 14 bytes + 1 Decoded byte  + Brute force 1 byte
    # Step 2: Send 13 bytes [ Return block includes 3 unknown bytes ]
    #         Check against 13 bytes + 2 Decoded bytes + Brute force 1 byte

    ## After I have one block: I have 16 bytes decoded.
    ## Step 16:
    ## If I send 15 bytes, I get back two+ blocks.
    ##    The first block is my 15 bytes sent + 1 decoded byte.
    ##    The second block is the next 15 decoded bytes + 1 unknown byte.
    ##    So I send: 15 bytes. Check the 2nd block returned, not the first.
    ##    And I check against: (15 bytes + 16 decoded bytes)[Indexed to partial second block] + Brute Force 1 unknown byte.
    ## Step 17:
    ##    Send 14 bytes. Check the 2nd block returned, not the first.
    ##    Check against: (14 bytes + 17 decoded bytes)[Indexed to partial second block] + Brute Force 1 unknown

    decoded = b""

    for block_num in range(999):
        for step in range(bs):
            partial_block = b"Z" * (bs - (1 + step))
            target_cipher_bytes = blackbox(partial_block)
            offset = block_num * bs

            ## Try every possible next byte
            found = False
            for i in range(256):
                byte = i.to_bytes(1, "big")
                plain = partial_block + decoded + byte
                cipher = blackbox(plain)
                # print(i)
                # print(f"target[{target_cipher_bytes[0:bs]}]")
                # print(f"cipher[{cipher}]")
                # print(f"plain[{plain}]")
                if (
                    cipher[0 + offset : bs + offset]
                    == target_cipher_bytes[0 + offset : bs + offset]
                ):
                    found = True
                    decoded += byte
                    break
            if not found:
                # Could not find next byte
                return decoded

    return decoded


def main():
    print("c12")

    # Detect that ECB is being used
    mode = detect_encryption_mode(encryption_oracle_12)
    print("---> Encryption mode")
    print(f"Detected encryption mode: {mode}")
    print("")

    # Determine Block Size
    print("---> Block size")
    bs = None
    for i in range(100):
        pads = b"A" * i
        cipher_bytes = encryption_oracle_12(pads)
        repeats = repeated_blocks(cipher_bytes)
        if repeats > 0:
            print(
                f"We found the first set of repeats when sending {i} A characters in a row."
            )
            print(f"Therefore, the block size is half of that, or {i // 2} bytes.")
            print("")
            bs = i // 2
            break

    # AAAqwertyuiop
    # ----++++====
    # AAqwertyuiop
    # ----++++====
    # Aqwertyuiop
    # ----++++====
    # qwertyuiop
    # ----++++====
    # KNOWN: qwer
    # Now I need to get "t" in an unknown position. So
    # I go back to:
    # AAAqwertyuiop
    # ----++++====
    # KNOWN: qwert
    # AAqwertyuiop
    # ----++++====

    print(f"---> Last byte analysis [blocksize: {bs}]")
    decoded = last_byte_ecb_attack(encryption_oracle_12, bs)
    print(decoded)


if __name__ == "__main__":
    main()
