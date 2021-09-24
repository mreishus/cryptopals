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
import math
from collections import Counter
from shared import hex_string_xor, hex_bytes_xor

# Estimated value of letter frequency in English
eng_freq = {
    "a": .084966,
    "b": .020720,
    "c": .045388,
    "d": .033844,
    "e": .111607,
    "f": .018121,
    "g": .024705,
    "h": .030034,
    "i": .075448,
    "j": .001965,
    "k": .011016,
    "l": .054893,
    "m": .030129,
    "n": .066544,
    "o": .071635,
    "p": .031671,
    "q": .001962,
    "r": .075809,
    "s": .057351,
    "t": .069509,
    "u": .036308,
    "v": .010074,
    "w": .012899,
    "x": .002902,
    "y": .017779,
    "z": .002722,
}


def compute_eng_freq_with_spaces(eng_freq):
    """
    Given an english character frequency list without space, add a space
    character and scale down the rest of the frequencies accordingly, so the
    sum is still 100%.
    """
    space_freq_estimate = 0.15
    output = {
        ' ': space_freq_estimate,
    }
    for letter, letter_freq in eng_freq.items():
        output[letter] = letter_freq  * (1.0 - space_freq_estimate)
    return output

eng_freq_with_spaces = compute_eng_freq_with_spaces(eng_freq)


def frequency_score(str_in):
    str_in = str_in.lower()
    counts = Counter(str_in)

    if len(str_in) == 0:
        return 0

    total_diff = 0.0
    for letter, ideal_freq in eng_freq_with_spaces.items():
        actual_freq = counts[letter] / len(str_in)
        this_diff = ideal_freq - actual_freq
        total_diff += this_diff * this_diff
        # print(f"let={letter} idea={ideal_freq} act={actual_freq} diff={this_diff} total={total_diff}")

    return math.sqrt(total_diff)

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
