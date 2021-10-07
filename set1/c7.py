#!/usr/bin/env python
import base64

# requires pycryptodome:
# yay -Syu python-pycryptodome
# or https://github.com/Legrandin/pycryptodome

"""
AES in ECB mode
https://cryptopals.com/sets/1/challenges/7

The Base64-encoded content in this file has been encrypted via AES-128 in ECB
mode under the key

"YELLOW SUBMARINE".

(case-sensitive, without the quotes; exactly 16 characters; I like "YELLOW
SUBMARINE" because it's exactly 16 bytes long, and now you do too).

Decrypt it. You know the key, after all.

Easiest way: use OpenSSL::Cipher and give it AES-128-ECB as the cipher.
"""

from shared import ecb_decrypt, ecb_encrypt


def get_data(filename):
    lines = []
    with open(filename) as file:
        lines = file.readlines()
        lines = [line.rstrip() for line in lines]
    return lines


def main():
    data = get_data("./7.txt")
    source_b64 = "".join(data)
    source_bytes = base64.b64decode(source_b64)

    key_ascii = "YELLOW SUBMARINE"
    key_bytes = str.encode(key_ascii)

    plaintext_bytes = ecb_decrypt(source_bytes, key_bytes)
    ## ECB Decrypt: Easy Mode:
    print("EASY MODE (Using a library to handle AES in ECB mode):")
    print("The message was: ", plaintext_bytes)
    print("--")
    ## ECB Encrypt:
    print("Trying to reencrypt and see if we match the original source:")
    reencrypted = ecb_encrypt(plaintext_bytes, key_bytes)
    print("Does it match?")
    print(reencrypted == source_bytes)
    # how AES works:
    #   https://www.youtube.com/watch?v=DLjzI5dX8jc
    #     ^ What is an SP Network
    #   https://www.youtube.com/watch?v=VYech-c5Dic
    #     ^ What is AES Rijndael
    #   https://www.youtube.com/watch?v=O4xNJsjtN6E
    #     ^ AES Rijndael Mechanics
    #   https://csrc.nist.gov/csrc/media/projects/cryptographic-standards-and-guidelines/documents/aes-development/rijndael-ammended.pdf
    #   https://github.com/Legrandin/pycryptodome/blob/016252bde04456614b68d4e4e8798bc124d91e7a/src/AES.c#L854
    #
    # SP Network (Substitution + Permutation network)
    # Split 128 bit block into 4v4 grid: (Each Square = 8 bit = 1 byte)
    # 0 4 8 12
    # 1 5 9 13
    # 2 6 10 14
    # 3 7 11 15
    #                    S                    P             P
    # XOR w/ k0 -> ( Substitute bytes -> Shift Rows -> Mix Columns -> Add Round Key (k1, k2, k3..) )
    #                ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^ 1 round
    # Last round does not have mix columns.
    # 128 bit key = 10 rounds
    # 192 bit key = 12 rounds
    # 256 bit key = 14 rounds
    # "Key Schedule" expands new keys for each round (k1, k2, k3..)
    #
    # Sub Bytes = Each byte in a 256 -> 256 lookup table, none of them are fixed, none of them are "reversible pairs"
    # Shift Rows: Row1-13 rotates one left, Row2-14 rotates two left, Row3-15 rotates three left,
    # Mix columns: Col 0-3 matrix multiply [ [ 2 3 1 1 ] [1 2 3 1] [1 1 2 3] [3 1 1 2] ] * [ [c0] [c1] [c2] [c3] ]
    #     Get their own matricies: Col 4-7, Col 8-11, Col 12-15
    #
    # AES is in CPU hardware: There are instructions to do one round
    # We're in a field with + and * reprenting operations that do not leave that field.
    #
    # Hard mode: Implement my own AES ECB (Not doing this)
    # I don't think the exercise wants me to do this, either.


if __name__ == "__main__":
    main()
