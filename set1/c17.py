#!/usr/bin/env python
import random
from shared import pkcs7_pad, pkcs7_unpad, random_aes_key, cbc_encrypt, cbc_decrypt


def get_rand_string():
    strings = [
        b"MDAwMDAwTm93IHRoYXQgdGhlIHBhcnR5IGlzIGp1bXBpbmc=",
        b"MDAwMDAxV2l0aCB0aGUgYmFzcyBraWNrZWQgaW4gYW5kIHRoZSBWZWdhJ3MgYXJlIHB1bXBpbic=",
        b"MDAwMDAyUXVpY2sgdG8gdGhlIHBvaW50LCB0byB0aGUgcG9pbnQsIG5vIGZha2luZw==",
        b"MDAwMDAzQ29va2luZyBNQydzIGxpa2UgYSBwb3VuZCBvZiBiYWNvbg==",
        b"MDAwMDA0QnVybmluZyAnZW0sIGlmIHlvdSBhaW4ndCBxdWljayBhbmQgbmltYmxl",
        b"MDAwMDA1SSBnbyBjcmF6eSB3aGVuIEkgaGVhciBhIGN5bWJhbA==",
        b"MDAwMDA2QW5kIGEgaGlnaCBoYXQgd2l0aCBhIHNvdXBlZCB1cCB0ZW1wbw==",
        b"MDAwMDA3SSdtIG9uIGEgcm9sbCwgaXQncyB0aW1lIHRvIGdvIHNvbG8=",
        b"MDAwMDA4b2xsaW4nIGluIG15IGZpdmUgcG9pbnQgb2g=",
        b"MDAwMDA5aXRoIG15IHJhZy10b3AgZG93biBzbyBteSBoYWlyIGNhbiBibG93",
    ]
    random_i = random.randrange(len(strings))
    return strings[random_i]


def mykey():
    """Static Key"""
    if not hasattr(mykey, "key"):
        mykey.key = random_aes_key()
    return mykey.key


def f1():
    """ Select random string -> Pad it -> Return CBC encrypted version and IV """
    s = get_rand_string()
    s = pkcs7_pad(s, 16)
    iv = random_aes_key()
    ct = cbc_encrypt(s, mykey(), iv)
    return ct, iv


def f2(ct, iv):
    """Consume the ciphertext produced by the first function, decrypt it,
    check its padding, and return true or false depending on whether the
    padding is valid."""
    pt = cbc_decrypt(ct, mykey(), iv)
    try:
        pt = pkcs7_unpad(pt, 16)
    except Exception:
        return False
    return True


def main():
    print("c17")
    ct, iv = f1()
    print(ct)
    print(iv)
    pt = f2(ct, iv)
    print(pt)


if __name__ == "__main__":
    main()
