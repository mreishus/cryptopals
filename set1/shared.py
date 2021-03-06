#!/usr/bin/env python
from Crypto.Cipher import AES
from Crypto.Util.Padding import unpad
from random import randint
from collections import defaultdict
from itertools import islice
import sys

##########
# Chall 18
##########

def ctr_crypt(plaintext_bytes, key_bytes, nonce_bytes=b"\x00" * 8):
    """ Works for both encryption and decryption. """
    bs = 16
    counter = 0

    encrypted = bytearray()
    cipher = AES.new(key_bytes, AES.MODE_ECB)
    for block in chunks(plaintext_bytes, bs):
        # Generate Nonce+Counter
        counter_bytes = counter.to_bytes(length=8, byteorder='little')
        nonce_counter_bytes = nonce_bytes + counter_bytes

        # Encrypt the Nonce+Coutner to make keystream
        xor_key = cipher.encrypt(nonce_counter_bytes)

        # num_key = [int(z) for z in xor_key]
        # print(num_key)

        # Shorten keystream if too long
        if len(xor_key) > len(block):
            xor_key = xor_key[:len(block)]

        # XOR This block with the keystream
        ct = hex_bytes_xor(block, xor_key)
        encrypted.extend(ct)

        # Inc counter
        counter += 1

    return bytes(encrypted)

def ctr_crypt2(plaintext_bytes, key_bytes, nonce_bytes=b"\x00" * 8):
    """ 
    Alternate implementation of ctr_crypt using a ctr_keystream generator 
    Behavior is exactly the same.
    """
    keystream_bytes = list(islice(ctr_keystream(key_bytes, nonce_bytes), 0, len(plaintext_bytes)))
    return hex_bytes_xor(plaintext_bytes, keystream_bytes)

def ctr_keystream(key_bytes, nonce_bytes=b"\x00" * 8):
    cipher = AES.new(key_bytes, AES.MODE_ECB)

    bs = 16
    counter = 0

    while True:
        # Generate Nonce+Counter
        counter_bytes = counter.to_bytes(length=8, byteorder='little')
        nonce_counter_bytes = nonce_bytes + counter_bytes

        # Encrypt the Nonce+Coutner to make keystream
        key_part = cipher.encrypt(nonce_counter_bytes)

        for byte in key_part:
            yield byte

        # Inc counter
        counter += 1


def pkcs7_unpad(bytes_in, block_size):
    """"""
    exception_msg = "Invalid padding"
    if block_size >= 256:
        raise ValueError("pkcs7_pad: Block size must be below 256")
    if (len(bytes_in) % block_size) > 1:
        raise Exception(exception_msg)
    last_byte = bytes_in[-1]
    if last_byte == 0:
        raise Exception(exception_msg)
    if last_byte > block_size:
        raise Exception(exception_msg)
    if last_byte <= block_size:
        # if last_byte=4, check -1 -2 -3 -4
        for i in range(-1, -1 - last_byte, -1):
            if bytes_in[i] != last_byte:
                raise Exception(exception_msg)
    # Strip padding
    return bytes_in[: 0 - last_byte]


##########
# Chall 11
##########


def detect_encryption_mode(black_box):
    """Given a black_box bytes -> bytes function, detect if it
    uses ECB or CBC"""
    bytes_in = b"aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa"
    bytes_out = black_box(bytes_in)
    repeats = repeated_blocks(bytes_out)
    if repeats > 0:
        return "ecb"
    return "cbc"


def repeated_blocks(source_bytes):
    """Bytes -> Int"""
    seen = defaultdict(int)
    for block in chunks(source_bytes, 16):
        seen[block] += 1
    repeats = sum(x - 1 for x in seen.values())
    return repeats


def random_aes_key():
    """Generate 16 random bytes"""
    return random_bytes(16)


def random_bytes(num):
    key = b""
    for i in range(num):
        num = randint(0, 255)
        key += num.to_bytes(1, "big")
    return key


##########
# Chall 10
##########


def cbc_decrypt(source_bytes, key_bytes, iv=b"\x00" * 16):
    bs = 16  # block_size
    prev = iv
    decrypted = bytearray()
    for block in chunks(source_bytes, bs):
        block = pkcs7_pad(block, bs)
        output1 = ecb_decrypt(block, key_bytes)
        output2 = hex_bytes_xor(output1, prev)
        # print("--")
        # print(f"block           {block}")
        # print(f"decrypted       {output1}")
        # print(f"decrypted+xored {output2}")
        decrypted.extend(output2)
        prev = block
    return bytes(decrypted)


def cbc_encrypt(plaintext_bytes, key_bytes, iv=b"\x00" * 16):
    bs = 16
    encrypted = bytearray()
    prev = iv
    for block in chunks(plaintext_bytes, bs):
        ## unpad??
        out1 = hex_bytes_xor(block, prev)
        out2 = ecb_encrypt(out1, key_bytes)
        encrypted.extend(out2)
        prev = out2
    return bytes(encrypted)


def chunks(lst, n):
    """Yield successive n-sized chunks from lst."""
    for i in range(0, len(lst), n):
        yield lst[i : i + n]


##########
# Chall 9
##########


def pkcs7_pad(bytes_in, block_size):
    """
    Pad input bytes [bytes_in] to match a multiple of block_size

    https://en.wikipedia.org/wiki/Padding_(cryptography)#PKCS#5_and_PKCS#7
    https://datatracker.ietf.org/doc/html/rfc5652#section-6.3

    Padding by adding whole bytes.
    The value of each byte added is the number of bytes added.
    If we have to add 4 bytes, then we add "04 04 04 04".
    If we have to add 5 bytes, we add "05 05 05 05 05".
    etc.
    If we have to add more than 255 bytes (ff), then we crash.
    """
    if block_size >= 256:
        raise ValueError("pkcs7_pad: Block size must be below 256")
    count_to_add = (block_size - len(bytes_in)) % block_size
    pad_bytes = count_to_add.to_bytes(1, "big")
    pad_bytes *= count_to_add
    return bytes_in + pad_bytes


##########
# Chall 7
##########


def ecb_decrypt(source_bytes, key_bytes):
    """
    Easy mode AES ECB using a library.
    See more about it in c7.py.
    """
    cipher = AES.new(key_bytes, AES.MODE_ECB)
    return cipher.decrypt(source_bytes)
    return unpad(cipher.decrypt(source_bytes), AES.block_size)


def ecb_encrypt(plaintext_bytes, key_bytes):
    """
    Easy mode AES ECB using a library.
    See more about it in c7.py.
    """
    cipher = AES.new(key_bytes, AES.MODE_ECB)
    plaintext_bytes = pkcs7_pad(plaintext_bytes, 16)
    return cipher.encrypt(plaintext_bytes)


##########
# Chall 6
##########
def hamming_distance(bs1, bs2):
    """
    Number of differing bits in two equal length byte arrays
    Input1: bytes
    Input2: bytes
    Output: int
    """
    if len(bs1) != len(bs2):
        raise ValueError()
    total = 0
    for i, byte1 in enumerate(bs1):
        byte2 = bs2[i]

        for j in range(8):
            bit1 = byte1 & (1 << j)
            bit2 = byte2 & (1 << j)
            if bit1 != bit2:
                total += 1
    return total


##########
# Chall 2
##########


def hex_string_xor(hs1, hs2):
    """
    XOR
    Input:  2 hex strings
    Output: hex string
    """
    hb1 = bytes.fromhex(hs1)
    hb2 = bytes.fromhex(hs2)
    output = hex_bytes_xor(hb1, hb2)
    return output.hex()


def hex_bytes_xor(hb1, hb2):
    """
    XOR
    Input:  2 byte arrays
    Output: Byte array
    """
    if len(hb1) < len(hb2):
        return hex_bytes_xor(hb2, hb1)
    output = bytearray(b"")
    for i, b1 in enumerate(hb1):
        b2 = hb2[i % len(hb2)]
        b3 = b1 ^ b2
        output.append(b3)
    return output


##########
# Chall 1
##########

b64_table = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/"


def hex_string_to_b64_string(hex_string):
    """
    Input:  Hex String like "4d616e" (Ascii: "Man")
    Output: B64 String like "TWFu"

    INPUT
    M          a         n
    77         97        110
    0x4d       0x61      0x6e
    01001101   01100001  01101110  [Groups of 8]
    ------------------------------
    010011  010110  000101 101110  [Same bits, Groups of 6]
    0x54    0x57    0x46   0x75
    84      87      70     117
    T       W       F      u
    OUTPUT
    """
    hex_bytes = bytes.fromhex(hex_string)
    b64_bytes = hex_bytes_to_b64_bytes(hex_bytes)
    return b64_bytes_to_b64_string(b64_bytes)


def hex_bytes_to_b64_bytes(hex_bytes):
    """
    Input:  Hex bytes like bytes.fromhex("4d616e")
    Output: B64 bytes like bytes([19, 22, 5, 46])
    (See example above)
    """
    b64_bytes = bytearray(b"")
    next_b64_byte = 0
    bits_taken = 0

    # Find the individual 1s and 0s in hex_bytes, starting from the left
    for byte in hex_bytes:
        # In this byte, examine the 8 bits from left to right
        for i in range(7, -1, -1):
            mask = 1 << i
            bit = 1 if byte & mask > 0 else 0

            next_b64_byte <<= 1
            next_b64_byte += bit
            bits_taken += 1
            # print(f"bit[{bit}] next_b64_byte[{next_b64_byte}] bits_taken[{bits_taken}]")
            if bits_taken == 6:
                b64_bytes.append(next_b64_byte)
                next_b64_byte = 0
                bits_taken = 0

    # Converting octects (8 bits) to sextets (6 bits) doesn't always line up
    # Sometimes we need to add 0s to fill out the last character
    if bits_taken > 0:
        # We need (6 - bits_taken) more bits: Add 0s
        next_b64_byte <<= 6 - bits_taken
        b64_bytes.append(next_b64_byte)

    return bytes(b64_bytes)


def b64_bytes_to_b64_string(b64_bytes):
    """
    Input:  B64 bytes like bytes([19, 22, 5, 46])
    Output: B64 string like "TWfu"
    """
    output = ""
    parity = 0
    for byte in b64_bytes:
        output += b64_table[byte]
        parity = (parity + 1) % 4

    ## Add padding if needed; we're expected to output in groups of 4 characters
    if parity > 0:
        for _ in range(4 - parity):
            output += "="
    return output
