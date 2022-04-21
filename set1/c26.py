#!/usr/bin/env python
from shared import pkcs7_pad, random_aes_key, ctr_crypt

def enc(input_bytes):
    prepend = b"comment1=cooking%20MCs;userdata="
    input_bytes = input_bytes.replace(b";", b"")
    input_bytes = input_bytes.replace(b"=", b"")
    append  = b";comment2=%20like%20a%20pound%20of%20bacon"

    full_bytes = prepend + input_bytes + append
    key = mykey()
    full_bytes = pkcs7_pad(full_bytes, 16)

    return ctr_crypt(full_bytes, key, b"\x00" * 8)

def is_admin(encrypted_bytes):
    full_bytes = ctr_crypt(encrypted_bytes, mykey(), b"\x00" * 8)
    print("    (The system has decoded the cipher text: )", full_bytes)
    return b";admin=true;" in full_bytes

def mykey():
    """Static Key"""
    if not hasattr(mykey, "key"):
        mykey.key = random_aes_key()
    return mykey.key

def main():
    print("c26")
    print("I am sending this plaintext to the function:")
    bytes_in = b"aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa"
    print(bytes_in)
    ct = enc(bytes_in)
    print("")
    print("I got this encrypted text back: ")
    print(ct)
    ct2 = bytearray(ct)
    # We want to modify what's at byte 32, so change those bytes directly.
    # Unlike CBC, which requires you to change the previous block, CTR bitflipping
    # directly modifies the changed bit.
    i = 32
    ct2[i + 0] ^= (ord(';') ^ ord('a'))
    ct2[i + 1] ^= (ord('a') ^ ord('a'))
    ct2[i + 2] ^= (ord('d') ^ ord('a'))
    ct2[i + 3] ^= (ord('m') ^ ord('a'))
    ct2[i + 4] ^= (ord('i') ^ ord('a'))
    ct2[i + 5] ^= (ord('n') ^ ord('a'))
    ct2[i + 6] ^= (ord('=') ^ ord('a'))
    ct2[i + 7] ^= (ord('t') ^ ord('a'))
    ct2[i + 8] ^= (ord('r') ^ ord('a'))
    ct2[i + 9] ^= (ord('u') ^ ord('a'))
    ct2[i + 10] ^= (ord('e') ^ ord('a'))
    ct2[i + 11] ^= (ord(';') ^ ord('a'))
    print("")
    print("I will make bit flipping attacks to change the cyphertext without knowing the key: ")
    print("Modified cyphertext: ")
    print(bytes(ct2))
    print("")
    print("Checking to see if the system thinks the original ciphertext belongs to an admin:")
    print(is_admin(ct))
    print("")
    print("Checking to see if the system thinks the modified ciphertext belongs to an admin:")
    print(is_admin(ct2))

if __name__ == "__main__":
    main()

