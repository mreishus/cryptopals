#!/usr/bin/env python
"""
Run "pytest" to execute
"""
from unittest import TestCase, main

from shared import hex_string_to_b64_string, hex_bytes_to_b64_bytes, b64_bytes_to_b64_string

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
