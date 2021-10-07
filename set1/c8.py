#!/usr/bin/env python
from collections import defaultdict

"""
Detect AES in ECB mode
In this file are a bunch of hex-encoded ciphertexts.

One of them has been encrypted with ECB.

Detect it.

Remember that the problem with ECB is that it is stateless and deterministic;
the same 16 byte plaintext block will always produce the same 16 byte
ciphertext.
"""


def get_data(filename):
    lines = []
    with open(filename) as file:
        lines = file.readlines()
        lines = [line.rstrip() for line in lines]
    return lines


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
    candidates = get_data("8.txt")
    for i, source_hex in enumerate(candidates):
        source_bytes = bytes.fromhex(source_hex)
        repeat_count = repeated_blocks(source_bytes)
        if repeat_count == 0:
            continue
        print(f"Candidate {i}: {repeat_count} Repeated blocks")
        print(sorted(list(chunks(source_hex, 16))))


if __name__ == "__main__":
    main()
