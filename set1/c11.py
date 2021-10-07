#!/usr/bin/env python
"""
An ECB/CBC detection oracle

Now that you have ECB and CBC working:

Write a function to generate a random AES key; that's just 16 random bytes.

Write a function that encrypts data under an unknown key --- that is, a
function that generates a random key and encrypts under it.

The function should look like:

encryption_oracle(your-input) => [MEANINGLESS JIBBER JABBER]

Under the hood, have the function append 5-10 bytes (count chosen randomly)
before the plaintext and 5-10 bytes after the plaintext.

Now, have the function choose to encrypt under ECB 1/2 the time, and under CBC
the other half (just use random IVs each time for CBC). Use rand(2) to decide
which to use.

Detect the block cipher mode the function is using each time. You should end up
with a piece of code that, pointed at a block box that might be encrypting ECB
or CBC, tells you which one is happening.

"""

from collections import defaultdict
from random import randint
from shared import (
    ecb_encrypt,
    cbc_encrypt,
)


def random_aes_key():
    """Generate 16 random bytes"""
    return random_bytes(16)


def random_bytes(num):
    key = b""
    for i in range(num):
        num = randint(0, 255)
        key += num.to_bytes(1, "big")
    return key


def encryption_oracle(bytes_in):
    """Encrypts data under an unknown key"""
    # Append 5-10 bytes before plaintext
    pad_before = random_bytes(randint(5, 10))
    # Append 5-10 bytes after plaintext
    pad_after = random_bytes(randint(5, 10))
    source_bytes = pad_before + bytes_in + pad_after

    key = random_aes_key()

    # 50%/50% split between ECB and CBC
    if randint(1, 2) == 1:
        # ECB
        print("[Oracle: ECB] Shhhhh, don't tell anyone, but I decided to use ECB.")
        return ecb_encrypt(source_bytes, key)
    else:
        # CBC
        print("[Oracle: CBC] Shhhhh, don't tell anyone, but I decided to use CBC.")
        iv = random_aes_key()
        return cbc_encrypt(source_bytes, key, iv)


def chunks(lst, n):
    """Yield successive n-sized chunks from lst."""
    for i in range(0, len(lst), n):
        yield lst[i : i + n]


def repeated_blocks(source_bytes):
    seen = defaultdict(int)
    for block in chunks(source_bytes, 16):
        seen[block] += 1
    repeats = sum(x - 1 for x in seen.values())
    return repeats


def main():
    source_bytes = b"Hello, this is a test sentence. How am I supposed to detect the encryption mode? Wait, I am allowed to choose the input to the oracle, so I will create a repeated string and look for repeated blocks ...................................................................................."
    cypher_bytes = encryption_oracle(source_bytes)
    print(cypher_bytes)
    repeats = repeated_blocks(cypher_bytes)
    if repeats > 0:
        print(f"Found {repeats} repeated blocks, this is probably ECB...")
    else:
        print("Found no repeated blocks, this is probably CBC...")


if __name__ == "__main__":
    main()
