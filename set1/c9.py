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
from shared import pkcs7_pad


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
