#!/usr/bin/env python
"""
https://cryptopals.com/sets/1/challenges/2

Fixed XOR
Write a function that takes two equal-length buffers and produces their XOR combination.
If your function works properly, then when you feed it the string:
1c0111001f010100061a024b53535009181c

... after hex decoding, and when XOR'd against:
686974207468652062756c6c277320657965

... should produce:
746865206b696420646f6e277420706c6179
"""

from shared import hex_string_xor


def main():
    print("Set 1 / Challenge 2")
    print("Fixed XOR")
    print("")

    x1 = "1c0111001f010100061a024b53535009181c"
    x2 = "686974207468652062756c6c277320657965"
    print(f"Input x1: {x1}")
    print(f"Input x2: {x2}")

    y = hex_string_xor(x1, x2)
    expected = "746865206b696420646f6e277420706c6179"
    print(f"Output y: {y}")
    print(f"Matches expected? {str(y == expected)}")

if __name__ == "__main__":
    main()
