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


def main():
    print("c12")
    # print(encryption_oracle_12(b"A"))
    # print(encryption_oracle_12(b"AA"))
    # print(encryption_oracle_12(b"AAA"))
    # print(encryption_oracle_12(b"AAAA"))

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

    print(f"---> Last byte analysis [blocksize: {bs}]")
    print(f"Sending {bs} As.. ")
    cipher_bytes = encryption_oracle_12(b"A" * bs)
    print(cipher_bytes)
    print("")
    print(f"Sending {bs - 1} As.. ")
    cipher_bytes = encryption_oracle_12(b"A" * (bs - 1))
    print(cipher_bytes)
    # Knowing block size, craft input block that is one byte short
    #   - What does the function put in the last byte position?


if __name__ == "__main__":
    main()
