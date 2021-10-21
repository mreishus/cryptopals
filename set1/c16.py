#!/usr/bin/env python
from shared import pkcs7_pad, pkcs7_unpad, random_aes_key, cbc_encrypt, cbc_decrypt

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
    return b";admin=true;" in full_bytes

def mykey():
    """Static Key"""
    if not hasattr(mykey, "key"):
        mykey.key = random_aes_key()
    return mykey.key

def main():
    print("c16")
    ct = enc(b"myinputdata=here=test1234;here==")
    print("Cipher Text:")
    print(ct)
    print("Is admin? (Purpose of the exercise is to make this true)")
    print(is_admin(ct))

if __name__ == "__main__":
    main()
