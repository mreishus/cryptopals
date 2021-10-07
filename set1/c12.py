#!/usr/bin/env python
"""
Byte-at-a-time ECB decryption (Simple)

Copy your oracle function to a new function that encrypts buffers under ECB
mode using a consistent but unknown key (for instance, assign a single random
key, once, to a global variable).

Now take that same function and have it append to the plaintext, BEFORE
ENCRYPTING, the following string:
"""

import base64


def main():
    print("c12")
    special_string = b"Um9sbGluJyBpbiBteSA1LjAKV2l0aCBteSByYWctdG9wIGRvd24gc28gbXkgaGFpciBjYW4gYmxvdwpUaGUgZ2lybGllcyBvbiBzdGFuZGJ5IHdhdmluZyBqdXN0IHRvIHNheSBoaQpEaWQgeW91IHN0b3A/IE5vLCBJIGp1c3QgZHJvdmUgYnkK"
    special_bytes = base64.b64decode(special_string)

    ## I'm not supposed to spoil myself by looking at special bytes, so let's use a diff
    ## one while I'm debugging
    special_string = "SSB3YW50IHdpbmQgdG8gYmxvdw=="
    special_bytes = base64.b64decode(special_string)
    print(special_bytes)


if __name__ == "__main__":
    main()
