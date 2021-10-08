#!/usr/bin/env python
"""
Byte-at-a-time ECB decryption (Harder)

 Take your oracle function from #12. Now generate a random count of random
 bytes and prepend this string to every plaintext. You are now doing:

AES-128-ECB(random-prefix || attacker-controlled || target-bytes, random-key)

Same goal: decrypt the target-bytes.
Stop and think for a second.

What's harder than challenge #12 about doing this? How would you overcome that
obstacle? The hint is: you're using all the tools you already have; no crazy
math is required.

Think "STIMULUS" and "RESPONSE".
"""

import base64
from random import randint
from collections import defaultdict
from shared import (
    cbc_encrypt,
    chunks,
    detect_encryption_mode,
    ecb_encrypt,
    random_aes_key,
    random_bytes,
    repeated_blocks,
)


def random_prefix():
    if not hasattr(random_prefix, "key"):
        c = randint(0, 100)
        # TEMP: Make the random prefix always 16 bytes long, then try to solve that
        c = 16
        print(
            f"ssh, it's a secret. Our prefix is this many bytes long: {c}. Mod 16, that's: {c % 16}"
        )
        random_prefix.key = random_bytes(c)
    return random_prefix.key


def encryption_oracle_14(bytes_in):
    """
    Encrypts data under an unknown static key (stays constant through runtime).
    Also appends an unknown string to the provided string.
    Produces: AES-128-ECB(your-string || unknown-string, random-key)
    """
    if not hasattr(encryption_oracle_14, "key"):
        encryption_oracle_14.key = random_aes_key()

    ## Append special string from exercise
    prefix_bytes = random_prefix()
    special_string = b"Um9sbGluJyBpbiBteSA1LjAKV2l0aCBteSByYWctdG9wIGRvd24gc28gbXkgaGFpciBjYW4gYmxvdwpUaGUgZ2lybGllcyBvbiBzdGFuZGJ5IHdhdmluZyBqdXN0IHRvIHNheSBoaQpEaWQgeW91IHN0b3A/IE5vLCBJIGp1c3QgZHJvdmUgYnkK"
    special_bytes = base64.b64decode(special_string)

    source_bytes = prefix_bytes + bytes_in + special_bytes

    # Always use ECB
    key = encryption_oracle_14.key
    return ecb_encrypt(source_bytes, key)


def last_byte_ecb_attack(blackbox, bs, goff, start_looking):
    # arg1: blackbox: Bytes -> Bytes function
    # arg2: bs: Int (blocksize)
    # arg3: goff: Int (Global offset)
    # arg4: start_looking: Int (Another.. offset.. thingie..)

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
                    cipher[0 + offset + start_looking : bs + offset + start_looking]
                    == target_cipher_bytes[
                        0 + offset + start_looking : bs + offset + start_looking
                    ]
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
    mode = detect_encryption_mode(encryption_oracle_14)
    print("---> Encryption mode")
    print(f"Detected encryption mode: {mode}")
    print("")

    # Determine Block Size
    print("---> Block size")
    bs = None  # Block Size
    offset = None  # Offset
    start_looking = None  # This is.. another.. offset like variable but.. different?
    # ^ I have 3 different "offset" type variables, 2 here, and
    # 1 more in my last_byte_ecb_attack() function. Hopefully there is
    # some vocabulary I don't know yet to describe these concepts I'm using.
    for i in range(100):
        pads = b"A" * i
        cipher_bytes = encryption_oracle_14(pads)
        repeats = repeated_blocks(cipher_bytes)
        if repeats > 0:
            print(
                f"We found the first set of repeats when sending {i} A characters in a row."
            )
            print(f"Therefore, the block size is half of that, or {i // 2} bytes.")
            print("Or at least, it would be, if the oracle inserted 0 prefix bytes.")
            print(
                "Let's try some other strings like AABBBBBBBB to resolve our alignment problems and potentially narrow down the block size."
            )
            print("")
            # bs = i // 2
            for j in range(i - 1):
                if (i - j) % 2 == 1:
                    continue
                pads = (b"A" * j) + (b"B" * (i - j))
                cipher_bytes = encryption_oracle_14(pads)
                repeats = repeated_blocks(cipher_bytes)
                print(f"PrePad={j} 2Block={i-j} Total={i-j+j} repeats={repeats}")
                if repeats > 0:
                    bs = (i - j) // 2
                    offset = j
                else:
                    break

            # print(f"We have block_size={bs} offset={offset} But what is start_looking?")
            pads = (b"A" * offset) + (b"B" * (bs * 2))
            cipher_bytes = encryption_oracle_14(pads)

            # Find the contents of the repeated block
            seen = defaultdict(int)
            repeated_block = None
            for block in chunks(cipher_bytes, 16):
                seen[block] += 1
                if seen[block] > 1:
                    repeated_block = block
                    break
            # How far do we go down the cipher text to see the repeated block?
            start_looking = cipher_bytes.find(repeated_block)
            break
    print(
        f"Done! We found block_size={bs}, offset={offset} and start_looking={start_looking}"
    )

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

    print(f"---> Last byte analysis [blocksize: {bs}] [offset: {offset}]")
    decoded = last_byte_ecb_attack(encryption_oracle_14, bs, offset, start_looking)
    print(decoded)


if __name__ == "__main__":
    main()
