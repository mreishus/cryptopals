#!/usr/bin/env python
"""
Run "pytest" to execute
"""
from unittest import TestCase, main

from shared import hex_string_to_b64_string, hex_bytes_to_b64_bytes, b64_bytes_to_b64_string
from shared import hex_string_xor, hex_bytes_xor
from shared import hamming_distance

class Chal6TestCase(TestCase):
    def test_hamming_distance(self):
        str1 = "this is a test"
        str2 = "wokka wokka!!!"
        str1b = str1.encode("ascii")
        str2b = str2.encode("ascii")
        got = hamming_distance(str1b, str2b)
        want = 37
        self.assertEqual(got, want)

class Chal2TestCase(TestCase):
    def test_string_xor(self):
        x1 = "1c0111001f010100061a024b53535009181c"
        x2 = "686974207468652062756c6c277320657965"

        got  = hex_string_xor(x1, x2)
        want = "746865206b696420646f6e277420706c6179"
        self.assertEqual(got, want)

    def test_bytes_xor(self):
        b1 = bytes([1,   1, 16, 16, 16])
        b2 = bytes([1, 255, 31, 32, 33])
        got = hex_bytes_xor(b1, b2)
        want = bytes([0, 254, 15, 48, 49])
        self.assertEqual(got, want)

class Chal1TestCase(TestCase):
    def test_hex_string_to_b64_string(self):
        got = hex_string_to_b64_string("4d616e")
        want = "TWFu"
        self.assertEqual(got, want)

        got = hex_string_to_b64_string("4d61")
        want = "TWE="
        self.assertEqual(got, want)

        got = hex_string_to_b64_string("4d")
        want = "TQ=="
        self.assertEqual(got, want)

        got = hex_string_to_b64_string("49276d206b696c6c696e6720796f757220627261696e206c696b65206120706f69736f6e6f7573206d757368726f6f6d")
        want = "SSdtIGtpbGxpbmcgeW91ciBicmFpbiBsaWtlIGEgcG9pc29ub3VzIG11c2hyb29t"
        self.assertEqual(got, want)

    def test_hex_bytes_to_b64_bytes(self):
        got = hex_bytes_to_b64_bytes(bytes.fromhex("4d616e"))
        want = bytes([19, 22, 5, 46])
        self.assertEqual(want, got)

    def test_b64_bytes_to_b64_string(self):
        got = b64_bytes_to_b64_string(bytes([19, 22, 5, 46]))
        want = "TWFu"
        self.assertEqual(want, got)

if __name__ == "__main__":
    main()
