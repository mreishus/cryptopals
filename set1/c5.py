#!/usr/bin/env python
"""
https://cryptopals.com/sets/1/challenges/5

Implement repeating-key XOR

Here is the opening stanza of an important work of the English language:

Burning 'em, if you ain't quick and nimble
I go crazy when I hear a cymbal

Encrypt it, under the key "ICE", using repeating-key XOR.

In repeating-key XOR, you'll sequentially apply each byte of the key; the first
byte of plaintext will be XOR'd against I, the next C, the next E, then I again
for the 4th byte, and so on.
It should come out to:

0b3637272a2b2e63622c2e69692a23693a2a3c6324202d623d63343c2a26226324272765272
a282b2f20430a652e2c652a3124333a653e2b2027630c692b20283165286326302e27282f

Encrypt a bunch of stuff using your repeating-key XOR function. Encrypt your
mail. Encrypt your password file. Your .sig file. Get a feel for it. I promise,
we aren't wasting your time with this.
"""

from shared import hex_bytes_xor

def main():
    source_str = "Burning 'em, if you ain't quick and nimble\nI go crazy when I hear a cymbal"
    source_bytes = source_str.encode("ascii")
    source_hexstr = source_bytes.hex()

    key_str = "ICE"
    key_bytes = key_str.encode("ASCII")
    encrypted_bytes = hex_bytes_xor(source_bytes, key_bytes)
    encrypted_hexstr = encrypted_bytes.hex()

    expected = "0b3637272a2b2e63622c2e69692a23693a2a3c6324202d623d63343c2a26226324272765272" + "a282b2f20430a652e2c652a3124333a653e2b2027630c692b20283165286326302e27282f"

    print(f"Source String      : {source_str}")
    print(f"Source HexString   : {source_hexstr}")
    print(f"Key String         : {key_str}")
    print(f"Key HexString      : {key_bytes.hex()}")
    print(f"Expanded Key       : {key_str * (len(source_str) // len(key_str))}")
    print(f"Expanded Key HexStr: {(key_str * (1 + len(source_str) // len(key_str))).encode('ASCII').hex()}")
    print(f"Encrypted HexString: {encrypted_hexstr}")
    print(f"Matches expected? {expected == encrypted_hexstr}")

    # print(source_str)
    # print(source_bytes)
    # print(source_hexstr)

if __name__ == "__main__":
    main()
