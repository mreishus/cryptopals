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
    return b"AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA"
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
    print(f"      ---> shh: decrypted to [{pt}]")
    try:
        pt = pkcs7_unpad(pt, 16)
    except Exception:
        return False
    return True


def main():
    print("c17")
    ct, iv = f1()
    print("Server gave me this cipher text:")
    print(ct)
    print("Server gave me this IV:")
    print(iv)

    print("")
    print("[Original] Is the padding valid?")
    pt = f2(ct, iv)
    print(pt)

    mod_ct = bytearray(ct)
    # 5 blocks: ct 0-79. To edit last char, change [63] or [-17] or [79 - 16]
    # 4 blocks: ct 0-63. To edit last char, change [47] or [-17] or [63 - 16]
    # 3 blocks: ct 0-47. To edit last char, change [31] or [-17] or [47 - 16]
    guess = ord('=')
    print(guess)
    # mod_ct[-17] = 0
    print(mod_ct[-17])
    for i in range(len(mod_ct)):
        print(f"{i} {mod_ct[i]}")
    print(f"Len = {len(mod_ct)}")

    answer = bytearray(len(mod_ct))
    guess_index = len(mod_ct) - 1
    modify_index = guess_index - 16
    for guess in range(256):
        if guess == 1:
            continue
        mod_ct = bytearray(ct)
        mod_ct[modify_index] ^= guess ^ 1
        valid_padding = f2(mod_ct, iv)
        print(f"{guess} {valid_padding}")
        if valid_padding:
            print(f"Guess is: {guess}")
            answer[guess_index] = guess
            break


    print("")
    print("[Modified] Is the padding valid?")
    ct = bytes(mod_ct)
    print(pt)


if __name__ == "__main__":
    main()
