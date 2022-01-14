#!/usr/bin/env python
from mt_rng import MTRNG
from shared import chunks, hex_bytes_xor
import random
import time
import os


def rng_crypt(plaintext_bytes, key_num):
    # key = 16 bit unsigned int = 0 - 65535
    bs = 4  # Each pull from the RNG gets us 4 bytes of random info
    r = MTRNG()
    r.seed_mt(key_num)
    encrypted = bytearray()
    for block in chunks(plaintext_bytes, bs):
        rng_num = r.extract_number()
        xor_key = rng_num.to_bytes(4, "big")

        # Shorten keystream if too long
        if len(xor_key) > len(block):
            xor_key = xor_key[: len(block)]

        ct = hex_bytes_xor(block, xor_key)
        encrypted.extend(ct)
    return encrypted


def rng_decrypt(source_bytes, key_num):
    # key = 16 bit unsigned int = 0 - 65535
    return rng_crypt(source_bytes, key_num)


def generate_plaintext():
    # Make a random plaintext
    word_file = "/usr/share/dict/words"
    words = open(word_file).read().splitlines()
    text = ""
    for i in range(10):
        word = random.choice(words)
        text += word + " "
    text += "AAAAAAAAAAAAAA"
    return text.encode("utf-8")


def is_current_time_token(test_token):
    key = int(time.time())
    r = MTRNG()
    r.seed_mt(key)
    token = bytearray()
    for _ in range(16):
        token_part = r.extract_number().to_bytes(4, "big")
        token.extend(token_part)
    return test_token == token


def main():
    # You can create a trivial stream cipher out of any PRNG; use it to generate a
    # sequence of 8 bit outputs and call those outputs a keystream. XOR each byte
    # of plaintext with each successive byte of keystream.

    # plaintext = b"This is a test plaintext. AAAAAAAAAAAAAA"
    plaintext = generate_plaintext()

    # Write the function that does this for MT19937 using a 16-bit seed. Verify that
    # you can encrypt and decrypt properly. This code should look similar to your
    # CTR code.
    key_num = random.randint(0, 65535)
    ct = rng_crypt(plaintext, key_num)
    print("Verifying encrypt with known key: ")
    print(f"{plaintext} -> {ct}")
    plaintext = rng_decrypt(ct, key_num)
    print("Verifying decrypt with known key: ")
    print(f"{ct} -> {plaintext}")

    # Use your function to encrypt a known plaintext (say, 14 consecutive 'A'
    # characters) prefixed by a random number of random characters. From the
    # ciphertext, recover the "key" (the 16 bit seed).
    print("")
    print("Recovering key from ciphertext by brute forcing the PRNG key...")
    print("")
    for x in range(65535):
        if x % 2500 == 0:
            print(x)
        plaintext_bytes = rng_decrypt(ct, x)
        # plaintext = plaintext_bytes.decode("utf-8")
        # if "AAAAAAAAAAAAAA" in plaintext:
        if b"AAAAAAAAAAAAAA" in plaintext_bytes:
            print(f"Found a match! Our key guess is {x}.")
            break
    print(f"Did the code above find it? The real key was {key_num}.")

    print("")
    print("")

    # Use the same idea to generate a random "password reset token" using
    # MT19937 seeded from the current time. Write a function to check if any
    # given password token is actually the product of an MT19937 PRNG seeded
    # with the current time.
    key = int(time.time())
    r = MTRNG()
    r.seed_mt(key)
    token = bytearray()
    for _ in range(16):
        token_part = r.extract_number().to_bytes(4, "big")
        token.extend(token_part)
    print("Generating a password reset token..")
    print(token)
    print(f"Was this a token generated this second? {is_current_time_token(token)}")
    rand_token = os.urandom(16)
    print(
        f"Verifying that a random token is not dectected as generated this second: {is_current_time_token(rand_token)} should be false"
    )


if __name__ == "__main__":
    main()
