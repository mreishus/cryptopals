#!/usr/bin/env python
from pure_python_crypto import sha1_compress, SHA1, md_pad_64, big_endian_bytes
from shared import random_aes_key
import random

""" Implement a SHA-1 keyed MAC """


def mykey():
    """Static Key"""
    if not hasattr(mykey, "key"):
        mykey.key = random.choice(list(open("/usr/share/dict/words"))).strip()
        ## Convert to bytes
        mykey.key = mykey.key.encode("utf-8")
    return mykey.key


def generate_mac(message):
    """a secret-prefix MAC: SHA1(key || message)"""
    key = mykey()
    return bytes(SHA1(key + message))


def verify(message, mac):
    want_mac = generate_mac(message)
    return want_mac == mac


def main():
    print("c28")
    s = b"This is only a test"
    mac = generate_mac(s)
    print(s)
    print(mac.hex())
    print("Matches? ")
    print(verify(s, mac))


if __name__ == "__main__":
    main()
