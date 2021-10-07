#!/usr/bin/env python
"""
Implement PKCS#7 padding

A block cipher transforms a fixed-sized block (usually 8 or 16 bytes) of
plaintext into ciphertext. But we almost never want to transform a single
block; we encrypt irregularly-sized messages.

One way we account for irregularly-sized messages is by padding, creating a
plaintext that is an even multiple of the blocksize. The most popular padding
scheme is called PKCS#7.

So: pad any block to a specific block length, by appending the number of bytes
of padding to the end of the block. For instance,

"YELLOW SUBMARINE"

... padded to 20 bytes would be:

"YELLOW SUBMARINE\x04\x04\x04\x04"
"""


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


def main():
    source_str = "YELLOW SUBMARINE"
    source_bytes = str.encode(source_str)
    print("Input bytes:")
    print(source_bytes)
    print("")
    for bs in range(16, 22):
        out_bytes = pkcs7_pad(source_bytes, bs)
        print(f"Padded with pkcs7_pad to blocksize {bs}:")
        print(out_bytes)
        print("")


if __name__ == "__main__":
    main()
