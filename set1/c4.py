#!/usr/bin/env python
"""
https://cryptopals.com/sets/4

Detect single-character XOR

One of the 60-character strings in this file has been encrypted by single-character XOR.
Find it.

(Your code from #3 should help.)
"""
from shared import hex_bytes_xor
from eng_freq import frequency_score

def get_data(filename):
    lines = []
    with open(filename) as file:
        lines = file.readlines()
        lines = [line.rstrip() for line in lines]
    return lines

def main():
    lines = get_data("./4.txt")
    candidates = []
    for line_num, source_str in enumerate(lines):
        source_bytes = bytes.fromhex(source_str)
        for i in range(0xff):
            key = bytes([i]) * len(source_str)
            decode_bytes = hex_bytes_xor(source_bytes, key)
            decode_string = str("".join([chr(byte) for byte in decode_bytes])) #decode_bytes.decode("cp1252")
            candidates.append({
                'line_num': line_num,
                'source_str': source_str,
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
