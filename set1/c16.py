#!/usr/bin/env python
from shared import pkcs7_pad, random_aes_key, cbc_encrypt, cbc_decrypt

def enc(input_bytes):
    prepend = b"comment1=cooking%20MCs;userdata="
    input_bytes = input_bytes.replace(b";", b"")
    input_bytes = input_bytes.replace(b"=", b"")
    append  = b";comment2=%20like%20a%20pound%20of%20bacon"

    full_bytes = prepend + input_bytes + append
    key = mykey()
    full_bytes = pkcs7_pad(full_bytes, 16)

    return cbc_encrypt(full_bytes, key, b"\x00" * 16)

def is_admin(encrypted_bytes):
    full_bytes = cbc_decrypt(encrypted_bytes, mykey(), b"\x00" * 16)
    print("    (The system has decoded the cipher text: )", full_bytes)
    return b";admin=true;" in full_bytes

def mykey():
    """Static Key"""
    if not hasattr(mykey, "key"):
        mykey.key = random_aes_key()
    return mykey.key

def main():
    print("c16")
    print("I am sending this plaintext to the function:")
    bytes_in = b"aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa"
    print(bytes_in)
    ct = enc(bytes_in)
    print("")
    print("I got this encrypted text back: ")
    print(ct)
    ct2 = bytearray(ct)
    ct2[16] ^= (ord(';') ^ ord('a'))
    ct2[17] ^= (ord('a') ^ ord('a'))
    ct2[18] ^= (ord('d') ^ ord('a'))
    ct2[19] ^= (ord('m') ^ ord('a'))
    ct2[20] ^= (ord('i') ^ ord('a'))
    ct2[21] ^= (ord('n') ^ ord('a'))
    ct2[22] ^= (ord('=') ^ ord('a'))
    ct2[23] ^= (ord('t') ^ ord('a'))
    ct2[24] ^= (ord('r') ^ ord('a'))
    ct2[25] ^= (ord('u') ^ ord('a'))
    ct2[26] ^= (ord('e') ^ ord('a'))
    ct2[27] ^= (ord(';') ^ ord('a'))
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
