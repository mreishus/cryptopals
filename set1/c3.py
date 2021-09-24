#!/usr/bin/env python
"""
https://cryptopals.com/sets/1/challenges/3

Single-byte XOR cipher

The hex encoded string:
1b37373331363f78151b7f2b783431333d78397828372d363c78373e783a393b3736

... has been XOR'd against a single character. Find the key, decrypt the message.
You can do this by hand. But don't: write code to do it for you.

How? Devise some method for "scoring" a piece of English plaintext. Character
frequency is a good metric. Evaluate each output and choose the one with the
best score.
"""

import re
from shared import hex_bytes_xor
from eng_freq import frequency_score

def main():
    print("Set 1 / Challenge 3")
    print("Single-byte XOR cipher")
    print("")

    source_str = "1b37373331363f78151b7f2b783431333d78397828372d363c78373e783a393b3736"
    source_bytes = bytes.fromhex(source_str)

    candidates = []
    for i in range(0xff):
        key = bytes([i]) * len(source_str)
        decode_bytes = hex_bytes_xor(source_bytes, key)
        decode_string = str("".join([chr(byte) for byte in decode_bytes])) #decode_bytes.decode("cp1252")
        # print(decode_string)
        # print(f"{i} {decode_bytes} {frequency_score(decode_string)}")
        candidates.append({
            'key_single': i,
            'key': key,
            'decode_bytes': decode_bytes,
            'decode_string': decode_string,
            'score': frequency_score(decode_string)
        })
    winner = min(candidates, key=lambda x: x['score'])
    print("Decoded with this best-fit key:")
    print(winner)

if __name__ == "__main__":
    main()
