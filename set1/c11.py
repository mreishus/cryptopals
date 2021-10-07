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

from random import randint


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

    # 50%/50% split between ECB and CBC
    if randint(1, 2) == 1:
        # ECB
        print("ECB")
    else:
        # CBC
        print("CBC")
    return source_bytes


def main():
    print("hi")
    key = random_aes_key()
    print(key)
    source_bytes = b"Hello"
    print(encryption_oracle(source_bytes))


if __name__ == "__main__":
    main()
