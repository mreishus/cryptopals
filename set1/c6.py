#!/usr/bin/env python
"""
Break repeating-key XOR It is officially on, now.

This challenge isn't conceptually hard, but it involves actual error-prone
coding. The other challenges in this set are there to bring you up to speed.
This one is there to qualify you. If you can do this one, you're probably just
fine up to Set 6.

There's a file here. It's been base64'd after being encrypted with repeating-key XOR.
Decrypt it.

Here's how:

    Let KEYSIZE be the guessed length of the key; try values from 2 to (say) 40.
    Write a function to compute the edit distance/Hamming distance between two strings. The Hamming distance is just the number of differing bits. The distance between:

    this is a test

    and

    wokka wokka!!!

    is 37. Make sure your code agrees before you proceed. 
"""
import base64
import heapq
import itertools
from shared import hamming_distance, hex_bytes_xor
from eng_freq import frequency_score

def get_data(filename):
    lines = []
    with open(filename) as file:
        lines = file.readlines()
        lines = [line.rstrip() for line in lines]
    return lines

def chunks(lst, n):
    """Yield successive n-sized chunks from lst."""
    for i in range(0, len(lst), n):
        yield lst[i:i + n]

def crack(source_bytes, keysize):
    print(f"Trying to crack with keysize {keysize}")
    blocks = list(chunks(source_bytes, keysize))
    # print("All blocks:")
    # print(blocks)
    fullkey = bytearray(b"")
    for i in range(keysize):
        # print(f"All {i} characters:")
        all_is = [b[i % len(b)] for b in blocks]
        this_key = solve_single_char_xor(all_is)
        # print(this_key)
        fullkey.append(this_key)
        # print(all_is)
    print(f"Possible key: {fullkey}")
    return fullkey

def solve_single_char_xor(source_bytes):
    candidates = []
    for key in range(0xff):
        decode_bytes = hex_bytes_xor(source_bytes, bytes([key]))
        decode_string = str("".join([chr(byte) for byte in decode_bytes])) #decode_bytes.decode("cp1252")
        # print(decode_string)
        # print(f"{i} {decode_bytes} {frequency_score(decode_string)}")
        candidates.append({
            'key': key,
            'decode_bytes': decode_bytes,
            'decode_string': decode_string,
            'score': frequency_score(decode_string)
        })
    winner = min(candidates, key=lambda x: x['score'])
    # print(winner)
    return winner['key']


def main():
    data = get_data("./6.txt")
    source_b64 = "".join(data)
    source_bytes = base64.b64decode(source_b64)

    keysize_candidates = []
    for keysize in range(2, 41):
        block1 = source_bytes[0:keysize]
        block2 = source_bytes[keysize:keysize*2]
        block3 = source_bytes[keysize*2:keysize*3]
        block4 = source_bytes[keysize*3:keysize*4]
        block5 = source_bytes[keysize*4:keysize*5]

        distances = []
        block_combos = itertools.combinations([block1, block2, block3, block4, block5], 2)
        for block_a, block_b in block_combos:
            this_distance = (hamming_distance(block_a, block_b) * 1.0) / keysize
            distances.append(this_distance)

        distance = sum(distances) / 5.0
        keysize_candidates.append({'keysize': keysize, 'distance': distance})

    # Get the 3 keysizes with the smallest block distances
    keysize_candidates = list(map(lambda c: c['keysize'], heapq.nsmallest(3, keysize_candidates, key=lambda x: x['distance'])))
    for keysize in keysize_candidates:
        key = crack(source_bytes, keysize)
        decode_bytes = hex_bytes_xor(source_bytes, key)
        print(decode_bytes)

if __name__ == "__main__":
    main()
